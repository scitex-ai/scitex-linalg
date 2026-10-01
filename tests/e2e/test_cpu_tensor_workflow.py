"""Own real optional CPU tensor statistics and tabular distance workflows."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import torch

import scitex_linalg as sxl

pytestmark = pytest.mark.e2e


@pytest.mark.parametrize("dtype", [torch.float32, torch.float64])
@pytest.mark.parametrize(
    "operation,global_expected,row_expected",
    [
        ("nanvar", 1.25, [1.0, 1.0]),
        ("nanstd", np.sqrt(1.25), [1.0, 1.0]),
        ("nanprod", 24.0, [3.0, 8.0]),
        ("nanargmin", 0, [0, 0]),
        ("nanargmax", 5, [2, 2]),
    ],
)
def test_cpu_nan_statistics_preserve_values_and_shapes(dtype, operation, global_expected, row_expected):
    # Arrange: two synthetic observations, with missing values in each row.
    observations = torch.tensor([[1.0, float("nan"), 3.0], [2.0, float("nan"), 4.0]], dtype=dtype)
    reduction = getattr(sxl, operation)
    # Act: compare global and per-observation public reductions on real CPU tensors.
    global_result = reduction(observations)
    rows = reduction(observations, dim=1, keepdim=True)
    # Assert: hand-calculated population statistics, index locations, and dimensions.
    assert (
        float(global_result),
        rows.flatten().tolist(),
        tuple(rows.shape),
        rows.device.type,
        rows.dtype == (torch.int64 if operation.startswith("nanarg") else dtype),
    ) == (pytest.approx(global_expected), pytest.approx(row_expected), (2, 1), "cpu", True)


@pytest.mark.parametrize(
    "operation,one_expected,rows_expected",
    [
        ("nancumsum", [1.0, 1.0, 4.0], [[1.0, 1.0, 4.0], [2.0, 2.0, 6.0]]),
        ("nancumprod", [1.0, 1.0, 3.0], [[1.0, 1.0, 3.0], [2.0, 2.0, 8.0]]),
    ],
)
def test_cpu_cumulative_statistics_support_default_and_explicit_dimensions(operation, one_expected, rows_expected):
    # Arrange: real CPU sequences containing missing samples.
    one = torch.tensor([1.0, float("nan"), 3.0], dtype=torch.float64)
    rows = torch.tensor([[1.0, float("nan"), 3.0], [2.0, float("nan"), 4.0]], dtype=torch.float64)
    cumulative = getattr(sxl, operation)
    # Act: run the documented default dimension and an explicit row dimension.
    one_result = cumulative(one)
    rows_result = cumulative(rows, dim=1)
    # Assert: missing samples contribute the identity and preserve CPU dtype/shape.
    assert (one_result.tolist(), rows_result.tolist(), rows_result.device.type, rows_result.dtype) == (
        one_expected, rows_expected, "cpu", torch.float64
    )


@pytest.mark.parametrize("container", ["numpy", "list", "torch", "frame"])
def test_pairwise_distances_round_trip_supported_input_containers(container):
    # Arrange: two points forming a hand-calculated 3-4-5 triangle.
    points = [[0.0, 3.0], [0.0, 4.0]]
    inputs = {
        "numpy": np.asarray(points),
        "list": points,
        "torch": torch.tensor(points, dtype=torch.float64),
        "frame": pd.DataFrame(points),
    }
    expected_types = {"numpy": np.ndarray, "list": list, "torch": torch.Tensor, "frame": pd.DataFrame}
    # Act: preserve the native input container through the public distance helper.
    result = sxl.euclidean_distance(inputs[container], inputs[container], axis=0)
    values = result.to_numpy() if isinstance(result, pd.DataFrame) else np.asarray(result)
    # Assert: the requested container carries the actual pairwise numeric result.
    assert (isinstance(result, expected_types[container]), values.tolist()) == (True, [[0.0, 5.0], [5.0, 0.0]])


def test_series_distance_matches_known_reference_points():
    # Arrange: a tabular point and the origin/3-4 reference columns.
    point = pd.Series([0.0, 0.0])
    references = np.asarray([[0.0, 3.0], [0.0, 4.0]])
    # Act: use the same public distance path for a Series input.
    result = sxl.euclidean_distance(point, references, axis=0)
    # Assert: tabular output preserves the Series contract and real distances.
    assert (isinstance(result, pd.Series), result.tolist()) == (True, [0.0, 5.0])


@pytest.mark.parametrize("container", ["frame", "series"])
def test_geometric_median_round_trips_pandas_measurements(container):
    # Arrange: symmetric synthetic observations with known middle values.
    inputs = {"frame": pd.DataFrame([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]), "series": pd.Series([1.0, 2.0, 3.0])}
    expected = {"frame": [2.0, 5.0], "series": [2.0]}
    expected_types = {"frame": pd.DataFrame, "series": pd.Series}
    # Act: the optional real CPU tensor backend reduces the selected sample axis.
    result = sxl.geometric_median(inputs[container], dim=-1)
    # Assert: the public median result retains the tabular type and numeric values.
    assert (isinstance(result, expected_types[container]), result.to_numpy().flatten().tolist()) == (
        True, pytest.approx(expected[container])
    )
