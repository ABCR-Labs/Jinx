# Truncated raw patch text (for PRSense / vector-triage re-implementations) for PRs in the benchmark.
import pyarrow.parquet as pq, pickle, sys, collections
need = pickle.load(open(sys.argv[2], "rb"))["need"]
pf = pq.ParquetFile(sys.argv[1]); out = collections.defaultdict(list); size = collections.Counter()
for g in range(pf.num_row_groups):
    tb = pf.read_row_group(g, columns=["pr_id", "filename", "patch"]).to_pydict()
    for pid, fn, patch in zip(tb["pr_id"], tb["filename"], tb["patch"]):
        if pid in need and patch and size[pid] < 4000:
            chunk = f"diff --git a/{fn} b/{fn}\n{patch[:2000]}\n"; out[pid].append(chunk); size[pid] += len(chunk)
    print(g, len(out), flush=True)
pickle.dump({k: "".join(v)[:4000] for k, v in out.items()}, open(sys.argv[3], "wb")); print("done")
