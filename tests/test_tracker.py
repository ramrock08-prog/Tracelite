"""Tests for TraceLite.

A test is a tiny program that checks your code gives the right answer.
Run them all with:

    python -m unittest discover -s tests -v
"""

import os
import sys
import sqlite3
import tempfile
import unittest

# Make `import tracelite` work when running this file directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tracelite as tl  # noqa: E402
from tracelite.tracker import _percentile  # noqa: E402


class TestEstimateCost(unittest.TestCase):
    """The money math must be correct -- this is the heart of the tool."""

    def test_known_model_one_million_tokens(self):
        # gpt-4o-mini is priced (0.15 in, 0.60 out) per 1M tokens.
        self.assertAlmostEqual(
            tl.estimate_cost("gpt-4o-mini", 1_000_000, 1_000_000), 0.75
        )

    def test_unknown_model_is_free(self):
        self.assertEqual(
            tl.estimate_cost("a-model-we-do-not-know", 1_000_000, 1_000_000), 0.0
        )

    def test_zero_tokens_cost_nothing(self):
        self.assertEqual(tl.estimate_cost("gpt-4o-mini", 0, 0), 0.0)


class TestPercentile(unittest.TestCase):
    """The p50 / p95 numbers in the report must be right."""

    def test_empty_list(self):
        self.assertEqual(_percentile([], 50), 0.0)

    def test_single_value(self):
        self.assertEqual(_percentile([10], 95), 10)

    def test_middle_of_two(self):
        self.assertEqual(_percentile([0, 10], 50), 5.0)  # halfway between 0 and 10

    def test_middle_of_four(self):
        self.assertEqual(_percentile([1, 2, 3, 4], 50), 2.5)  # between 2 and 3


class TestTrack(unittest.TestCase):
    """One AI call should produce exactly one saved row."""

    def test_records_a_successful_call(self):
        with tempfile.TemporaryDirectory() as folder:
            db = os.path.join(folder, "test.db")
            tl.init(db)
            with tl.track("gpt-4o-mini", provider="test", prompt="hi") as span:
                span.set_response("hello", prompt_tokens=1_000_000, completion_tokens=0)

            rows = sqlite3.connect(db).execute(
                "SELECT model, cost_usd, status FROM traces"
            ).fetchall()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][0], "gpt-4o-mini")
            self.assertAlmostEqual(rows[0][1], 0.15)
            self.assertEqual(rows[0][2], "ok")

    def test_records_a_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            db = os.path.join(folder, "test.db")
            tl.init(db)
            with self.assertRaises(ValueError):
                with tl.track("gpt-4o-mini", provider="test", prompt="boom"):
                    raise ValueError("model returned 500")

            rows = sqlite3.connect(db).execute(
                "SELECT status, error FROM traces"
            ).fetchall()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][0], "error")
            self.assertIn("ValueError", rows[0][1])


if __name__ == "__main__":
    unittest.main()
