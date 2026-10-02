import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from app.graph.state import State
from app.models.schemas import CampaignOutput
from app.rag.retriever import retrieve
from app.services.llm import get_llm


def planner(state: State):
    q=f"{state['request'].product} {state['request'].audience} {state['request'].campaign_goal}"
    return {'context': retrieve(q), 'revision_count': 0}

def generate(state: State):
    llm=get_llm().with_structured_output(CampaignOutput)
    r=state['request']
    prompt=f"""Create a marketing campaign. Product: {r.product}. Audience: {r.audience}. Goal: {r.campaign_goal}. Channels: {r.channels}.
Brand/product context:
{state['context']}
Create concise, factual copy. Only create email items when email is requested and social posts for non-email channels."""
    return {'draft': llm.invoke([HumanMessage(content=prompt)])}

def validate(state: State):
    errors=[]; d=state['draft']; channels=state['request'].channels
    if 'email' in channels and not d.emails: errors.append('Email channel requested but no emails generated')
    if any(c!='email' for c in channels) and not d.social_posts: errors.append('Social channel requested but no social posts generated')
    for e in d.emails:
        if len(e.subject)>80 or len(e.body)>3000: errors.append('Email length exceeded')
    for s in d.social_posts:
        if len(s.headline)>100 or len(s.body)>1500 or len(s.call_to_action)>120: errors.append('Social content length exceeded')
    return {'validation_errors': errors}

def route(state: State):
    if not state.get('validation_errors'): return 'finish'
    if state.get('revision_count',0)>=2: return 'finish'
    return 'revise'

def revise(state: State):
    llm=get_llm().with_structured_output(CampaignOutput)
    r=state['request']; errors='; '.join(state.get('validation_errors',[]))
    prompt=f"""Revise this campaign to fix these validation errors: {errors}. Request: {r.model_dump_json()}. Context: {state['context']}. Draft: {state['draft'].model_dump_json()}. Return a corrected campaign."""
    return {'draft': llm.invoke([HumanMessage(content=prompt)]), 'revision_count': state.get('revision_count',0)+1}

def finish(state: State): return {'final': state['draft']}

def build_graph():
    g=StateGraph(State); g.add_node('plan',planner); g.add_node('generate',generate); g.add_node('validate',validate); g.add_node('revise',revise); g.add_node('finish',finish)
    g.set_entry_point('plan'); g.add_edge('plan','generate'); g.add_edge('generate','validate'); g.add_conditional_edges('validate',route,{'revise':'revise','finish':'finish'}); g.add_edge('revise','validate'); g.add_edge('finish',END); return g.compile()
