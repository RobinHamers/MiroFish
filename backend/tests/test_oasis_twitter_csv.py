"""Tests for Twitter CSV profile generation.

Catches the exact bugs that broke OASIS ingestion:
- 'user_name' header instead of 'username'
- Missing 'user_char' column
"""
import csv
from app.services.oasis_profile_generator import OasisAgentProfile


class TestSaveTwitterCsv:

    def _read_csv(self, path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _read_headers(self, path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return next(reader)

    def test_header_has_username_not_user_name(self, generator, sample_profiles, tmp_path):
        path = str(tmp_path / "twitter.csv")
        generator._save_twitter_csv(sample_profiles, path)
        headers = self._read_headers(path)
        assert "username" in headers, f"Expected 'username' in headers, got: {headers}"
        assert "user_name" not in headers, f"'user_name' should not be in headers, got: {headers}"

    def test_header_has_user_char(self, generator, sample_profiles, tmp_path):
        path = str(tmp_path / "twitter.csv")
        generator._save_twitter_csv(sample_profiles, path)
        headers = self._read_headers(path)
        assert "user_char" in headers, f"Expected 'user_char' in headers, got: {headers}"

    def test_exact_header_order(self, generator, sample_profiles, tmp_path):
        path = str(tmp_path / "twitter.csv")
        generator._save_twitter_csv(sample_profiles, path)
        headers = self._read_headers(path)
        expected = [
            "user_id", "username", "name", "bio", "user_char",
            "friend_count", "follower_count", "statuses_count", "created_at",
        ]
        assert headers == expected

    def test_row_count_matches_profiles(self, generator, sample_profiles, tmp_path):
        path = str(tmp_path / "twitter.csv")
        generator._save_twitter_csv(sample_profiles, path)
        rows = self._read_csv(path)
        assert len(rows) == len(sample_profiles)

    def test_user_char_populated_from_persona(self, generator, sample_profiles, tmp_path):
        path = str(tmp_path / "twitter.csv")
        generator._save_twitter_csv(sample_profiles, path)
        rows = self._read_csv(path)
        for row in rows:
            assert row["user_char"].strip(), "user_char must not be empty"

    def test_newlines_stripped_from_bio_and_user_char(self, generator, tmp_path):
        profile = OasisAgentProfile(
            user_id=0,
            user_name="newline_test",
            name="Newline Test",
            bio="Line one\nLine two\rLine three",
            persona="Persona line one\nPersona line two",
        )
        path = str(tmp_path / "twitter.csv")
        generator._save_twitter_csv([profile], path)
        rows = self._read_csv(path)
        row = rows[0]
        assert "\n" not in row["bio"]
        assert "\r" not in row["bio"]
        assert "\n" not in row["user_char"]
