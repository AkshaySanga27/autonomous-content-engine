from typing import TypedDict, Any
from app.models.schemas import CampaignRequest, CampaignOutput
class State(TypedDict, total=False):
    request: CampaignRequest
    context: str
    draft: CampaignOutput
    validation_errors: list[str]
    revision_count: int
    final: CampaignOutput
