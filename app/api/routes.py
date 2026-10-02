from fastapi import APIRouter, HTTPException
from app.models.schemas import CampaignRequest, CampaignResponse
from app.graph.workflow import build_graph
router=APIRouter(prefix='/api')
@router.post('/campaign', response_model=CampaignResponse)
def campaign(req: CampaignRequest):
    try:
        result=build_graph().invoke({'request':req})
        return CampaignResponse(request=req,campaign=result['final'],validation_passed=not result.get('validation_errors'),revision_count=result.get('revision_count',0),retrieved_context=result['context'])
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))
