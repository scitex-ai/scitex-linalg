"""Runtime cross-package import gate.

This test imports every cross-package module that 'scitex-linalg'
references in its source tree. Three outcomes:

- Module installed AND import succeeds → test PASSES.
- Module installed BUT import fails (e.g. internal rename like
  `scitex_io._load_cache` → `scitex_io._loading._load_cache`) →
  test FAILS loudly.
- Module NOT installed (peer standalone absent in the CI env) →
  test is SKIPPED via `pytest.importorskip`. The umbrella's CI
  (which installs every peer) catches cross-package renames.
"""
import importlib

import pytest

# ===== AUTO-GENERATED: cross-package imports =====
CROSS_PACKAGE_IMPORTS = [
    'scitex_dev',
]
# ===== END AUTO-GENERATED =====


@pytest.mark.parametrize("module_name", CROSS_PACKAGE_IMPORTS)
def test_cross_package_import_module_loads_successfully(module_name):
    """Importing scitex-linalg's declared cross-package dependency must succeed."""
    # Arrange
    pytest.importorskip(module_name.split('.')[0])
    # Act
    mod = importlib.import_module(module_name)
    # Assert
    assert mod is not None
