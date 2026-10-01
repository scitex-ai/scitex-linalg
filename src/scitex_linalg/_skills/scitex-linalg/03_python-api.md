---
description: |
  [TOPIC] Python API
  [DETAILS] All public callables — distances, similarity, geometric median, vector rebasing, triangle-side coordinate solver.
tags: [scitex-linalg-python-api]
---

# Python API

```python
import scitex_linalg as sla
```

## Distances

| Callable | Purpose |
|---|---|
| `euclidean_distance(a, b)` | Scalar L2 distance between two vectors |
| `edist(a, b)` | Short-name alias |
| `cdist(A, B)` | Pairwise distance matrix (numpy-friendly wrapper around `scipy.spatial.distance.cdist`) |

## Similarity

| Callable | Purpose |
|---|---|
| `cosine(a, b)` | Cosine similarity |
| `nannorm(v, axis=-1)` | Vector norm; any NaN propagates to the result |

## Geometry

| Callable | Purpose |
|---|---|
| `geometric_median(xx, dim=-1)` | Robust median across the selected sample axis using the optional Torch backend |
| `rebase_a_vec(v, basis)` | Express `v` in a new orthonormal basis |
| `three_line_lengths_to_coords(a, b, c)` | Solve triangle side-lengths to 2-D coordinates |

## Notes

- Install `scitex-linalg[torch]` or `[all]` for `geometric_median` and the
  Torch numerical helpers. Without that extra, `geometric_median` is `None`
  and each Torch numerical helper raises an actionable `ImportError` on use.
- `geometric_median` takes `xx` and `dim`; it has no `backend` argument.
  NumPy, list and pandas inputs pass through tensor conversion and retain
  their container type. The converter selects CUDA when Torch reports it
  available, so that path requires hardware supported by the installed Torch
  build. Tensor inputs retain their dtype and device. Release controls exercise
  the CPU path; GPU execution has not been validated for this release.
- `euclidean_distance` accepts NumPy, list, pandas and CPU tensor inputs.
  Array results retain the input container type; vector-to-vector scalar
  results are NumPy scalars.

## Torch numerical helpers

`nanmax`, `nanmin`, `nanvar`, `nanstd`, `nanprod`, `nancumsum`, `nancumprod`,
`nanargmax`, `nanargmin`, and `apply_to` operate on real Torch tensors.
Variance and standard deviation use population normalization; missing values
are ignored. Cumulative sum/product use zero/one for missing samples.
Global reductions use `dim=None`; specify `dim` and `keepdim` for row-wise
reductions. Cumulative operations default to dimension zero.

## See also

- `scipy.spatial.distance` — heavyweight alternative for huge `cdist` cases
- `scitex-stats` — for statistical tests on the distances
