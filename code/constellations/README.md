# Constellations of consecutive gaps: code

CPython with numpy (the engine is the inclusion-exclusion engine 4.5 of `code/engine_45/`, with all points of the
constellation forced). Data: `data/constellations/`.

| file | role |
|---|---|
| `cell_A_engine.py` | notebook cell: writes `konst_worker.py` (the engine) |
| `cell_N_pairs_triples_47.py` | notebook cell: pairs and triples at 47# |
| `cell_N2_stages.py` | notebook cell: pairs and triples at 5#, ..., 43# (full enumeration up to 13#), with checks |
| `cell_N3_quadruples.py` | notebook cell: quadruples at 5#, ..., 47#, with checks |
| `check_all.py` | all checks on the data in the repository |
| `models_p0_47.py` | exact model coefficients from p0 = 47, with checks |
| `missing_table.py` | missing constellations and their causes |
| `sieve_104.py`, `survival_104.py` | survival test up to span 104 (needs `sito_1e9.npz` from `code/survival/sito.py`) |

The notebook cells must run in the folder that will hold the results; on Windows the worker functions live in
`konst_worker.py`, which the processes import. The scripts find the data relative to their own location.
