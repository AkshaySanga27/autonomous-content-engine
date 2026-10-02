from pydantic import BaseModel, Field, field_validator
from typing import List

class CampaignRequest(BaseModel):
    product: str = Field(min_length=2, max_length=120)
    audience: str = Field(min_length=2, max_length=120)
    campaign_goal: str = Field(min_length=2, max_length=200)
    channels: List[str] = Field(min_length=1, max_length=5)
    @field_validator('channels')
    @classmethod
    def normalize_channels(cls, v):
        allowed={'email','linkedin','twitter','instagram'}
        out=[x.lower().strip() for x in v]
        bad=set(out)-allowed
        if bad: raise ValueError(f'Unsupported channels: {sorted(bad)}')
        return list(dict.fromkeys(out))

class EmailItem(BaseModel):
    subject: str = Field(max_length=80)
    body: str = Field(max_length=3000)

class SocialItem(BaseModel):
    headline: str = Field(max_length=100)
    body: str = Field(max_length=1500)
    call_to_action: str = Field(max_length=120)

class CampaignOutput(BaseModel):
    campaign_summary: str = Field(max_length=500)
    emails: List[EmailItem] = Field(default_factory=list, max_length=5)
    social_posts: List[SocialItem] = Field(default_factory=list, max_length=5)

class CampaignResponse(BaseModel):
    request: CampaignRequest
    campaign: CampaignOutput
    validation_passed: bool
    revision_count: int
    retrieved_context: str
