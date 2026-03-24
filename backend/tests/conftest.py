import pytest
from app.services.oasis_profile_generator import OasisProfileGenerator, OasisAgentProfile


@pytest.fixture
def sample_profile():
    """A single fully-populated OasisAgentProfile."""
    return OasisAgentProfile(
        user_id=0,
        user_name="test_user_123",
        name="Test User",
        bio="A test user for validation",
        persona="Test User is an enthusiastic participant in social discussions.",
        karma=1500,
        friend_count=100,
        follower_count=200,
        statuses_count=500,
        age=25,
        gender="male",
        mbti="INTJ",
        country="China",
        profession="Student",
        interested_topics=["Technology", "Education"],
        source_entity_uuid="test-uuid-123",
        source_entity_type="Student",
    )


@pytest.fixture
def sample_profiles(sample_profile):
    """List of two profiles: one individual, one organization (missing optional fields)."""
    org = OasisAgentProfile(
        user_id=1,
        user_name="org_official",
        name="Official Org",
        bio="Official account",
        persona="This is an official institutional account.",
        karma=5000,
        friend_count=50,
        follower_count=10000,
        statuses_count=200,
        source_entity_uuid="test-uuid-456",
        source_entity_type="University",
    )
    return [sample_profile, org]


@pytest.fixture
def generator():
    """OasisProfileGenerator instance without calling __init__ (no external services needed)."""
    return OasisProfileGenerator.__new__(OasisProfileGenerator)
