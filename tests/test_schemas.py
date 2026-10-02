from app.models.schemas import CampaignRequest

def test_request():
    r=CampaignRequest(product='Test', audience='SMBs', campaign_goal='Signups', channels=['email'])
    assert r.channels==['email']
