"""Score the returned sheets: precision of the comment labels, A-B agreement, and agreement with the Haiku audit."""

import json
import os
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.loads(pathlib.Path(HERE, "label_map.json").read_text())
key = pd.read_csv(os.path.join(HERE, "key_do_not_open.csv"))
a, b = (pd.read_excel(p, sheet_name="Pairs").set_index("id").label.map(M) for p in sys.argv[1:3])


def kappa(x, y):
    m = x.notna() & y.notna()
    x, y = x[m], y[m]
    po = (x == y).mean()
    pe = sum((x == c).mean() * (y == c).mean() for c in set(x) | set(y))
    return (po - pe) / (1 - pe), int(m.sum())


def prec(x, ok, nb=2000):
    v = x.dropna().isin(ok).to_numpy(float)
    bs = np.random.default_rng(0).choice(v, (nb, len(v))).mean(1)
    return round(v.mean(), 3), [round(q, 3) for q in np.quantile(bs, [0.025, 0.975])]


strict, loose = ["duplicate", "replacement"], ["duplicate", "replacement", "subsumed"]
hk = key.set_index("id").haiku
out = {
    "n": int(a.notna().sum()),
    "kappa_A_B": kappa(a, b),
    "kappa_A_haiku": kappa(a, hk),
    "kappa_B_haiku": kappa(b, hk),
    "precision_strict_A": prec(a, strict), "precision_strict_B": prec(b, strict),
    "precision_loose_A": prec(a, loose), "precision_loose_B": prec(b, loose),
    "haiku_strict_same_rows": prec(hk, strict),
}
print(json.dumps(out, indent=1))
pathlib.Path(HERE, "agreement.json").write_text(json.dumps(out, indent=1))
