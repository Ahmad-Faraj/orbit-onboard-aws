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
        # 5 edges -> at most 6 distinct module nodes referenced
        self.assertLessEqual(out.count("-->"), 5)


class ModuleSurface(unittest.TestCase):
    def test_exposes_core_functions(self):
        for name in ("count_definitions_by", "top_files", "composition",
                     "module_map", "module_dependencies", "core_definitions",
                     "recent_authors", "resolve_project_id", "render", "main"):
            self.assertTrue(hasattr(onb, name), name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
