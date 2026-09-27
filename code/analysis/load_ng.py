"""Loader for population matrices n_{g,j}(p#) stored in Holt-style CSV files
(rows "Gap Sum = g", columns "Length = j")."""
import csv
import re


def load_ng(path):
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    head = rows[0]
    cols = {i: int(re.search(r"(\d+)", h).group(1))
            for i, h in enumerate(head) if h.strip().startswith("Length")}
    for r in rows[1:]:
        if not r or not r[0].startswith("Gap Sum"):
            continue
        g = int(re.search(r"(\d+)", r[0]).group(1))
        out[g] = {j: int(r[i]) for i, j in cols.items() if i < len(r) and r[i].strip()}
    return out
