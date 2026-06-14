import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO_DATA_FILE = PROJECT_ROOT / "sample_data" / "demo_results.json"


def iter_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from iter_strings(item)


class DemoDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DEMO_DATA_FILE.open("r", encoding="utf-8") as demo_file:
            cls.records = json.load(demo_file)

    def test_demo_data_is_list_with_at_least_five_records(self):
        self.assertIsInstance(self.records, list)
        self.assertGreaterEqual(len(self.records), 5)

    def test_records_have_required_top_level_fields(self):
        for record in self.records:
            with self.subTest(ip=record.get("ip")):
                self.assertIn("ip", record)
                self.assertIn("ports", record)
                self.assertIsInstance(record["ports"], list)
                self.assertGreaterEqual(len(record["ports"]), 1)

    def test_records_have_searchable_title_domain_and_headers(self):
        combined = " ".join(iter_strings(self.records))
        self.assertIn("Example Nginx Server", combined)
        self.assertIn("demo.local", combined)
        self.assertIn("intranet.local", combined)
        self.assertIn("staging.internal", combined)
        self.assertIn("Content-Security-Policy", combined)
        self.assertIn("X-Frame-Options", combined)
        self.assertIn("response", combined.lower())


if __name__ == "__main__":
    unittest.main()
