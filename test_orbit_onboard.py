#!/usr/bin/env python3
"""Smoke tests for orbit-onboard (no network).

The substance of orbit-onboard is its Orbit queries, which are exercised live.
These tests confirm the module loads cleanly and exposes its expected surface,
so a broken edit fails CI before it ships.

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


class ModuleSurface(unittest.TestCase):
    def test_exposes_core_functions(self):
        for name in ("count_definitions_by", "top_files", "composition",
                     "core_definitions", "recent_authors", "resolve_project_id",
                     "section", "main"):
            self.assertTrue(hasattr(onb, name), name)

    def test_top_files_and_composition_are_callables(self):
        self.assertTrue(callable(onb.top_files))
        self.assertTrue(callable(onb.composition))


if __name__ == "__main__":
    unittest.main(verbosity=2)
