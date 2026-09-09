import unittest

from book_startup_program_data.capture import normalize
from book_startup_program_data.cli import resource, validate


class SourceTests(unittest.TestCase):
    def raw(self):
        return (
            "<h1>United States</h1>"
            "<p>A ten-week accelerator program for high potential technology startups based in the United States.</p>"
            "<p>United States - Hybrid. Seed to Series A.</p>"
            "<p>Equity-free support and product credits.</p>"
            "<p>Commitment from CTO and/or technical roles is required.</p>"
        ).encode("utf-8")

    def test_google_source_fixture(self):
        source = resource("source.json")
        data = normalize(self.raw(), source, "2026-09-07T00:00:00Z")
        item = data["items"][0]
        item["provenance"].update(
            raw_object_key="landing/test",
            bronze_manifest_key="control/manifests/test",
        )
        self.assertEqual(item["title"], "Google for Startups Accelerator: United States")
        self.assertEqual(item["status"], "unknown")
        self.assertEqual(item["deadline"], {"kind": "unknown", "at": None})
        self.assertEqual(item["value"], {"kind": "in_kind", "amount": None, "currency": None, "guaranteed": False})
        self.assertFalse(item["terms"]["equity_required"])
        self.assertIsNone(item["terms"]["incorporation_required"])
        self.assertEqual(validate(data)["schema_version"], source["schema_version"])

    def test_source_drift_rejected(self):
        with self.assertRaises(ValueError):
            normalize(b"<h1>unrelated page</h1>", resource("source.json"), "2026-09-07T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
