"""Tests for Zep API naming convention converters.

These catch the bug class where LLM-generated entity/edge names
(snake_case, camelCase, spaces, etc.) must be normalized before
hitting the Zep API.
"""
import pytest
from app.services.graph_builder import to_pascal_case, to_screaming_snake_case


class TestToPascalCase:

    @pytest.mark.parametrize("input_name,expected", [
        ("music_festival", "MusicFestival"),
        ("social_media_user", "SocialMediaUser"),
        ("news_article", "NewsArticle"),
        # Already PascalCase — idempotent
        ("MusicFestival", "MusicFestival"),
        ("SocialMediaUser", "SocialMediaUser"),
        # camelCase
        ("musicFestival", "MusicFestival"),
        ("socialMediaUser", "SocialMediaUser"),
        # kebab-case
        ("music-festival", "MusicFestival"),
        # Space-separated (LLMs sometimes return this)
        ("music festival", "MusicFestival"),
        # SCREAMING_SNAKE_CASE
        ("MUSIC_FESTIVAL", "MusicFestival"),
        # Single word
        ("user", "User"),
        # Mixed delimiters
        ("social_media-user post", "SocialMediaUserPost"),
        # Empty string
        ("", ""),
    ])
    def test_to_pascal_case(self, input_name, expected):
        assert to_pascal_case(input_name) == expected


class TestToScreamingSnakeCase:

    @pytest.mark.parametrize("input_name,expected", [
        ("works_at", "WORKS_AT"),
        ("is_friend_of", "IS_FRIEND_OF"),
        # camelCase
        ("worksAt", "WORKS_AT"),
        ("isFriendOf", "IS_FRIEND_OF"),
        # PascalCase
        ("WorksAt", "WORKS_AT"),
        # kebab-case
        ("works-at", "WORKS_AT"),
        # Space-separated
        ("works at", "WORKS_AT"),
        # Already SCREAMING_SNAKE — idempotent
        ("WORKS_AT", "WORKS_AT"),
        # Single word
        ("knows", "KNOWS"),
        # Mixed delimiters
        ("has_friend-of type", "HAS_FRIEND_OF_TYPE"),
        # Empty string
        ("", ""),
    ])
    def test_to_screaming_snake_case(self, input_name, expected):
        assert to_screaming_snake_case(input_name) == expected
