import json
import unittest
from pathlib import Path

from book_startup_program_data.capture import normalize, source_config
from book_startup_program_data.cli import resource, validate


class SourceTests(unittest.TestCase):
    def raw(self):
        return (
            b"<h1>United States</h1>"
            b"<p>A ten-week accelerator program for high potential technology startups based in the United States.</p>"
            b"<p>United States - Hybrid. Seed to Series A.</p>"
            b"<p>Equity-free support and product credits.</p>"
            b"<p>Commitment from CTO and/or technical roles is required.</p>"
        )

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

    def test_generic_program_sources_normalize(self):
        catalog = json.loads((Path(__file__).resolve().parents[1] / "sources.json").read_text(encoding="utf-8"))
        generic = [source_config(source_id) for source_id in catalog["enabled_sources"]]
        generic = [source for source in generic if source.get("generic_html")]
        self.assertEqual(len(generic), 4)
        for source in generic:
            with self.subTest(source=source["id"]):
                markers = source.get("required_markers") or [source["title"]]
                raw = ("<script>ignored</script><p>" + " ".join(markers) + "</p>").encode("utf-8")
                data = normalize(raw, source, "2026-09-08T00:00:00Z")
                item = data["items"][0]
                item["provenance"].update(raw_object_key="landing/test", bronze_manifest_key="control/manifests/test")
                self.assertEqual(item["category"], source["category"])
                self.assertEqual(item["status"], source.get("status", "unknown"))
                self.assertEqual(validate(data)["schema_version"], "startup_program.v1")
                hidden_only = ("<script>" + " ".join(markers) + "</script>").encode("utf-8")
                with self.assertRaises(ValueError):
                    normalize(hidden_only, source, "2026-09-08T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
