"""Tests for Reddit JSON profile generation.

Validates all OASIS-required fields are present with correct names and defaults.
"""
import json
from app.services.oasis_profile_generator import OasisAgentProfile


class TestSaveRedditJson:

    def _read_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_required_fields_present(self, generator, sample_profiles, tmp_path):
        path = str(tmp_path / "reddit.json")
        generator._save_reddit_json(sample_profiles, path)
        data = self._read_json(path)
        required = {
            "user_id", "username", "realname", "bio", "persona",
            "karma", "created_at", "age", "gender", "mbti", "country",
        }
        for entry in data:
            missing = required - set(entry.keys())
            assert not missing, f"Missing fields: {missing}"

    def test_username_not_user_name(self, generator, sample_profiles, tmp_path):
        path = str(tmp_path / "reddit.json")
        generator._save_reddit_json(sample_profiles, path)
        data = self._read_json(path)
        for entry in data:
            assert "username" in entry
            assert "user_name" not in entry

    def test_gender_normalized(self, generator, tmp_path):
        profile = OasisAgentProfile(
            user_id=0, user_name="g_test", name="G Test",
            bio="Test", persona="Test persona", gender="Woman",
        )
        path = str(tmp_path / "reddit.json")
        generator._save_reddit_json([profile], path)
        data = self._read_json(path)
        assert data[0]["gender"] == "female"

    def test_defaults_for_missing_optional_fields(self, generator, tmp_path):
        profile = OasisAgentProfile(
            user_id=0, user_name="minimal", name="Minimal",
            bio="Minimal bio", persona="Minimal persona",
        )
        path = str(tmp_path / "reddit.json")
        generator._save_reddit_json([profile], path)
        data = self._read_json(path)
        entry = data[0]
        assert isinstance(entry["age"], int)
        assert entry["gender"] in ("male", "female", "other")
        assert isinstance(entry["mbti"], str) and len(entry["mbti"]) == 4
        assert isinstance(entry["country"], str) and len(entry["country"]) > 0

    def test_entry_count_matches_profiles(self, generator, sample_profiles, tmp_path):
        path = str(tmp_path / "reddit.json")
        generator._save_reddit_json(sample_profiles, path)
        data = self._read_json(path)
        assert len(data) == len(sample_profiles)
