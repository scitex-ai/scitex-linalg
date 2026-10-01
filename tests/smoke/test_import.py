"""Smoke: installed package imports and computes a distance (PS-211).

Subprocess-driven (``sys.executable -c ...``) so this proves the installed
distribution resolves — an in-process import would not. Hermetic: no
network, no credentials, no writes outside tmp dirs.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

pytestmark = pytest.mark.smoke


def test_import_and_cosine_subprocess() -> None:
    # Arrange
    argv = [
        sys.executable,
        "-c",
        "import numpy as np, scitex_linalg as sxl; "
        "print(round(float(sxl.cosine(np.array([1, 0]), np.array([1, 1]))), 4))",
    ]
    # Act
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    # Assert
    assert (completed.returncode, completed.stdout.strip()) == (0, "0.7071")
