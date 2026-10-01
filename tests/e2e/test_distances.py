"""E2E: real distance/norm computations against known values (PS-212).

Drives the real ``scitex_linalg`` numpy paths with hand-checked expectations.
No network, loopback-only by construction (pure in-memory).
"""

from __future__ import annotations

import numpy as np
import pytest

pytestmark = pytest.mark.e2e

import scitex_linalg as sxl


def test_euclidean_3_4_5() -> None:
    # Arrange
    uu = np.array([0.0, 0.0])
    vv = np.array([3.0, 4.0])
    # Act
    result = sxl.euclidean_distance(uu, vv, axis=0)
    # Assert
    assert float(result) == 5.0


def test_nannorm_propagates_nan() -> None:
    # Arrange — documented semantics (src/scitex_linalg/_misc.py + unit
    # tests test_nannorm_single_nan_input_returns_nan /
    # test_nannorm_all_nan_input_returns_nan): any NaN -> NaN.
    vv = np.array([3.0, np.nan, 4.0])
    # Act
    result = sxl.nannorm(vv)
    # Assert
    assert np.isnan(float(result))


def test_cosine_orthogonal_is_zero() -> None:
    # Arrange
    v1 = np.array([1.0, 0.0])
    v2 = np.array([0.0, 1.0])
    # Act
    result = sxl.cosine(v1, v2)
    # Assert
    assert abs(float(result)) < 1e-12
