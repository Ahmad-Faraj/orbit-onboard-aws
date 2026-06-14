#!/usr/bin/env python3
"""Tests for orbit-onboard's pure logic (no network).

Run: python3 test_orbit_onboard.py
"""

import importlib.machinery
import importlib.util
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_loader = importlib.machinery.SourceFileLoader(
    "orbit_onboard", os.path.join(HERE, "orbit-onboard"))
_spec = importlib.util.spec_from_loader("orbit_onboard", _loader)
onb = importlib.util.module_from_spec(_spec)
_loader.exec_module(onb)


class ModuleOf(unittest.TestCase):
    def test_two_segment_module(self):
        self.assertEqual(onb.module_of("crates/query-engine/compiler/src/x.rs"),
                         "crates/query-engine")

    def test_single_segment(self):
        self.assertEqual(onb.module_of("Makefile"), "Makefile")

    def test_empty(self):
        self.assertEqual(onb.module_of(""), "?")


class ShortModule(unittest.TestCase):
    def test_trims_known_prefixes(self):
        self.assertEqual(onb.short_module("crates/query-engine"), "query-engine")
        self.assertEqual(onb.short_module("clients/gkgpb"), "gkgpb")

    def test_leaves_unknown(self):
        self.assertEqual(onb.short_module("apps/web"), "apps/web")


class RollupModules(unittest.TestCase):
    def test_rolls_files_to_modules(self):
        rows = [
            {"file": "crates/a/src/x.rs", "n": 10},
            {"file": "crates/a/src/y.rs", "n": 5},
            {"file": "crates/b/src/z.rs", "n": 7},
        ]
        mods = onb.rollup_modules(rows)
        self.assertEqual(mods["crates/a"], 15)
        self.assertEqual(mods["crates/b"], 7)

    def test_handles_missing_counts(self):
        mods = onb.rollup_modules([{"file": "a/b/c", "n": None}])
        self.assertEqual(mods["a/b"], 0)


class ProjectSummary(unittest.TestCase):
    def test_full_summary(self):
        out = onb.project_summary(1200, 9, [{"kind": "Field"}, {"kind": "Method"}])
        self.assertIn("~1200 definitions", out)
        self.assertIn("9 modules", out)
        self.assertIn("mostly fields and methods", out)

    def test_empty(self):
        self.assertIsNone(onb.project_summary(0, 0, []))


class MermaidModules(unittest.TestCase):
    def test_none_when_empty(self):
        self.assertIsNone(onb.mermaid_modules([]))

    def test_renders_graph_with_counts(self):
        out = onb.mermaid_modules([(("crates/a", "crates/b"), 12)])
        self.assertTrue(out.startswith("```mermaid"))
        self.assertIn("graph LR", out)
        self.assertIn("|12|", out)
        self.assertIn('"a"', out)
        self.assertIn('"b"', out)

    def test_caps_edges(self):
        edges = [((f"crates/a{i}", "crates/b"), 1) for i in range(20)]
        out = onb.mermaid_modules(edges, limit=5)
        self.assertLessEqual(out.count("-->"), 5)

    def test_label_is_sanitized(self):
        # a module name with risky characters must not break the label syntax
        out = onb.mermaid_modules([(('crates/we"ird', "crates/b"), 3)])
        self.assertNotIn('we"ird', out)


class ModuleSurface(unittest.TestCase):
    def test_exposes_core_functions(self):
        for name in ("definitions_by_file", "composition", "module_dependencies",
                     "core_definitions", "recent_authors", "resolve_project_id",
                     "render", "main"):
            self.assertTrue(hasattr(onb, name), name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
