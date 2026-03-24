
import os
import sys
import csv
import json
import tempfile
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Add project path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from app.services.oasis_profile_generator import OasisProfileGenerator, OasisAgentProfile

def test_fixes():
    print("Testing fixes...")

    # 1. Test NameError fix (indirectly by ensuring it doesn't crash)
    # We can't easily trigger the Zep search without a real API key and graph_id,
    # but we can check if the code is syntactically correct and references 's' correctly now.

    # 2. Test description field in Twitter CSV
    test_profiles = [
        OasisAgentProfile(
            user_id=0,
            user_name="testuser",
            name="Test User",
            bio="This is a bio",
            persona="This is a persona",
        )
    ]

    generator = OasisProfileGenerator.__new__(OasisProfileGenerator)

    with tempfile.TemporaryDirectory() as temp_dir:
        twitter_path = os.path.join(temp_dir, "twitter.csv")
        generator._save_twitter_csv(test_profiles, twitter_path)

        with open(twitter_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)

        print(f"Twitter headers: {headers}")
        assert "description" in headers
        assert rows[0]["description"] == "This is a bio"
        assert rows[0]["bio"] == "This is a bio"

        # 3. Test description field in Reddit JSON
        reddit_path = os.path.join(temp_dir, "reddit.json")
        generator._save_reddit_json(test_profiles, reddit_path)

        with open(reddit_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"Reddit fields: {list(data[0].keys())}")
        assert "description" in data[0]
        assert data[0]["description"] == "This is a bio"
        assert data[0]["bio"] == "This is a bio"

        # 4. Test to_twitter_format and to_reddit_format
        twitter_dict = test_profiles[0].to_twitter_format()
        assert twitter_dict["description"] == "This is a bio"

        reddit_dict = test_profiles[0].to_reddit_format()
        assert reddit_dict["description"] == "This is a bio"

    print("All tests passed!")

if __name__ == "__main__":
    try:
        test_fixes()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
