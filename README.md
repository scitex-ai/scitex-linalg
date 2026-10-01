# scitex-linalg

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>Small linear-algebra helpers — distances, NaN-aware norms, geometric median, vector projections.</b></p>

<p align="center">
  <a href="https://scitex-linalg.readthedocs.io/">Full Documentation</a> · <code>uv pip install scitex-linalg[all]</code>
</p>

<!-- scitex-badges:start -->
<p align="center">
  <a href="https://pypi.org/project/scitex-linalg/"><img src="https://img.shields.io/pypi/v/scitex-linalg?label=pypi" alt="pypi"></a>
  <a href="https://pypi.org/project/scitex-linalg/"><img src="https://img.shields.io/pypi/pyversions/scitex-linalg?label=python" alt="python"></a>
  <a href="https://scitex-linalg.readthedocs.io/en/latest/"><img src="https://img.shields.io/readthedocs/scitex-linalg?label=docs" alt="docs"></a>
</p>
<p align="center">
  <a href="https://github.com/ywatanabe1989/scitex-linalg/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/ywatanabe1989/scitex-linalg/ci.yml?branch=develop&label=tests" alt="tests"></a>
  <a href="https://codecov.io/gh/ywatanabe1989/scitex-linalg"><img src="https://img.shields.io/codecov/c/github/ywatanabe1989/scitex-linalg/develop?label=cov" alt="cov"></a>
</p>
<!-- scitex-badges:end -->

---

## Quick Start

```python
import scitex_linalg as sxl

sxl.cdist(u, v)                # pairwise distances
sxl.cosine(v1, v2)             # cosine similarity (NaN-safe)
sxl.nannorm(v, axis=-1)        # norm; propagates NaN
sxl.rebase_a_vec(v, v_base)    # project v onto v_base basis
```

## Demo

```mermaid
flowchart LR
    A["u, v (np.ndarray)"] --> B["scitex_linalg.cdist"]
    B --> C["pairwise distance matrix"]
    A2["v with NaNs"] --> D["scitex_linalg.nannorm"]
    D --> E["vector norm; NaN propagates"]
    A3["v, v_base"] --> F["scitex_linalg.rebase_a_vec"]
    F --> G["projected coords"]
    A4["xx (torch.Tensor)"] --> H["scitex_linalg.geometric_median"]
    H --> I["robust median point"]
```

<p align="center"><sub><b>Figure 1.</b> Demo. Distances, NaN-propagating norms, projections, and the torch geometric median.</sub></p>

```python
>>> import numpy as np, scitex_linalg as sxl
>>> sxl.cosine(np.array([1, 0]), np.array([1, 1]))
0.7071...
>>> sxl.nannorm(np.array([3.0, np.nan, 4.0]))
nan
>>> sxl.nannorm(np.array([3.0, 4.0]))
5.0
```

## Installation

```bash
uv pip install "scitex-linalg[all]"
```

<details>
<summary><strong>Extras</strong></summary>

| Extra | Enables |
|-------|---------|
| `all` | Everything below (`torch`) |
| `torch` | Geometric median (`torch`, `geom-median`) |
| `dev` | Test/lint tools (`pytest`, `ruff`, `scitex-dev`) |
| `docs` | Sphinx build (`sphinx`, theme/parser extensions) |

</details>

## Architecture

```mermaid
flowchart LR
    UV["u, v"] --> DIST[euclidean_distance / cdist / edist]
    V["vectors"] --> MISC[cosine / nannorm / rebase_a_vec]
    XX["xx (torch.Tensor)"] --> GM[geometric_median]
    DEC[vendor decorators] --> NP[numpy_fn]
    DEC --> TF[torch_fn]
```

<p align="center"><sub><b>Figure 2.</b> Architecture. Pure numpy/scipy core plus the torch geometric-median path and vendored decorators.</sub></p>

Tiny single-purpose helpers. Core dependencies cover numpy/scipy/sympy/pandas.
Install `scitex-linalg[torch]` for the geometric median and Torch numerical helpers;
the package imports without that optional extra.

## 1 Interfaces

<details open>
<summary><strong>Python API</strong></summary>

<br>

```python
import scitex_linalg as sxl

sxl.euclidean_distance(u, v, axis=0)      # element-wise Euclidean distance
sxl.cdist(u, v)                           # pairwise distances
sxl.edist(u, v)                           # alias for euclidean_distance
sxl.cosine(v1, v2)                        # cosine similarity (NaN-safe)
sxl.nannorm(v, axis=-1)                   # NaN-aware vector norm
sxl.rebase_a_vec(v, v_base)               # project v onto v_base basis
sxl.three_line_lengths_to_coords(a, b, c) # triangle side lengths -> 2-D coords
sxl.geometric_median(xx, dim=-1)          # torch geometric median (requires [torch] extra)
```

</details>

## Status

Standalone fork of `scitex.linalg` — intended to remain importable as
`scitex.linalg` via the SciTeX umbrella package's bridge module. Decorators
(`numpy_fn`, `torch_fn`, `wrap`) are vendored under `_vendor_decorators/`
to keep the package free of `scitex.*` runtime deps; when `scitex-decorators`
is split out, those will be replaced with a direct dependency.

## Part of SciTeX

`scitex-linalg` is part of [**SciTeX**](https://scitex.ai). Install via
the umbrella with `pip install scitex[linalg]` to use as
`scitex.linalg` (Python).

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because we believe research infrastructure deserves the same freedoms as the software it runs on.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>
