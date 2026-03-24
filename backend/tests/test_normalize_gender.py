"""Tests for gender normalization to OASIS format (male/female/other)."""
import pytest


class TestNormalizeGender:

    @pytest.mark.parametrize("input_val,expected", [
        ("male", "male"),
        ("female", "female"),
        ("Male", "male"),
        ("FEMALE", "female"),
        ("man", "male"),
        ("woman", "female"),
        ("Woman", "female"),
        ("boy", "male"),
        ("girl", "female"),
        ("organization", "other"),
        ("Organization", "other"),
        ("other", "other"),
        ("nonbinary", "other"),
        ("", "other"),
        (None, "other"),
        ("  male  ", "male"),
    ])
    def test_normalize_gender(self, generator, input_val, expected):
        assert generator._normalize_gender(input_val) == expected
