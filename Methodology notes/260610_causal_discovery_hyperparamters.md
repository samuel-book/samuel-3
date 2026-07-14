# Hyperparamters in causallearn.search.ConstraintBased.PC

Here is a full breakdown of all the hyperparameters available in `causallearn`'s `pc()` function: [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

```python
from causallearn.search.ConstraintBased.PC import pc

cg = pc(data, alpha, indep_test, stable, uc_rule, uc_priority,
        mvpc, correction_name, background_knowledge, verbose, show_progress)
```

## Core Parameters

- **`data`** — `numpy.ndarray` of shape `(n_samples, n_features)`. The only required argument.
- **`alpha`** — Significance level for conditional independence tests, float in `(0, 1)`. Default `0.05`. Tuning this is the single most impactful choice: higher α → denser graph (more edges), lower α → sparser graph. [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

## Independence Test (`indep_test`)

Default is `'fisherz'`. Options: [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

| Value | Test | Best suited for |
|---|---|---|
| `'fisherz'` | Fisher's Z | Continuous, linear Gaussian data |
| `'chisq'` | Chi-squared | Discrete data |
| `'gsq'` | G-squared | Discrete data |
| `'kci'` | Kernel-based CI (KCI) | Nonlinear/non-Gaussian data |
| `'mv_fisherz'` | Missing-value Fisher's Z | Data with missing values |

KCI is theoretically the most powerful for nonlinear relationships but has **O(n³)** complexity, so it's slow on large samples. [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

## Skeleton Discovery

- **`stable`** — Boolean, default `True`. Uses the *order-independent* (stabilized) version of PC, which avoids skeleton results depending on variable ordering. Almost always leave this as `True` unless replicating older results. [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

## Unshielded Collider Orientation (`uc_rule`)

Controls how X–Z–Y triples with no X–Y edge are oriented: [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

- `0` — **`uc_sepset`** (default): standard v-structure orientation using separation sets
- `1` — **`maxP`**: performs an additional CI test to confirm colliders, more conservative
- `2` — **`definiteMaxP`**: only orients *definite* colliders, preserving more uncertainty

## Collider Conflict Resolution (`uc_priority`)

When two rules conflict over the same collider: [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

- `-1` — Use the default of the chosen `uc_rule`
- `0` — Overwrite (last rule wins)
- `1` — Orient as bi-directed edge
- `2` — **Prioritize existing colliders** (default)
- `3` — Prioritize the stronger collider (by p-value)
- `4` — Prioritize stronger* colliders (stricter version)

## Missing Data

- **`mvpc`** — Boolean, default `False`. Activates testwise-deletion missing-value PC. Pair with `indep_test='mv_fisherz'`. [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)
- **`correction_name`** — Correction method for missing-value PC. Default: `'MV_Crtn_Fisher_Z'`. [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

## Prior Knowledge & Output

- **`background_knowledge`** — A `BackgroundKnowledge` object to inject known causal directions or forbidden edges as constraints. Default `None`. [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)
- **`verbose`** — Print detailed output. Default `False`. [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)
- **`show_progress`** — Show a progress bar. Default `True`. [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

## Advanced: Passing CI Test Parameters & Caching

You can pass keyword arguments directly through to the independence test. For example, to customise KCI: [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

```python
from causallearn.utils.cit import kci
cg = pc(data, 0.05, kci, kernelZ='Polynomial', approx=False, est_width='median')
```

For large graphs with slow tests (especially KCI), you can **cache p-values** to disk and resume or fine-tune other parameters without rerunning all CI tests: [causal-learn.readthedocs](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/PC.html)

```python
cg = pc(data, 0.05, kci, cache_path='/path/to/cache.json')
# Then tweak uc_rule without recomputing CI tests:
cg2 = pc(data, 0.05, kci, cache_path='/path/to/cache.json', uc_rule=1)
```

This is particularly useful in your healthcare datasets where KCI over many variables would otherwise be prohibitively slow.