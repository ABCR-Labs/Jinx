"""contrib-guard duplicate matchers.
phoenix-assistant/contrib-guard: exact Python port of src/utils/tfidf.ts + duplicate-detector.ts (title+body TF-IDF, IDF over the scanned items).
balyakin/contrib-guard: imports the tool's own Python module (processing/duplicate_detection.py)."""
import math, re, sys, importlib.util
from collections import Counter

_P = "/home/ubuntu/research/prdupecheck/bots/balyakin_contrib-guard/contrib-guard-main/src/contrib_guard/processing/duplicate_detection.py"
_spec = importlib.util.spec_from_file_location("cg_balyakin", _P); cg_balyakin = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(cg_balyakin)
NONALNUM = re.compile(r"[^a-z0-9\s]")

def phoenix_tokenize(text):
    return [t for t in re.split(r"\s+", NONALNUM.sub(" ", text.lower())) if len(t) > 2]

def phoenix_scores(new_text, cand_texts):
    docs = [phoenix_tokenize(t) for t in [new_text] + cand_texts]
    n = len(docs); df = Counter(t for d in docs for t in set(d))
    idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
    vecs = []
    for d in docs:
        tf = Counter(d); L = len(d) or 1
        vecs.append({t: v / L * idf.get(t, 1) for t, v in tf.items()})
    q = vecs[0]; qn = math.sqrt(sum(v * v for v in q.values()))
    out = []
    for v in vecs[1:]:
        vn = math.sqrt(sum(x * x for x in v.values()))
        out.append(0.0 if not qn or not vn else sum(x * v.get(k, 0.0) for k, x in q.items()) / (qn * vn))
    return out

def balyakin_scores(new_title, new_files, cands):
    """title Jaccard from the tool; plus the tool's 'touches same files as similar PR' flag (title sim >= 0.7 and shared file)."""
    out = []
    for title, files in cands:
        s = cg_balyakin.title_similarity(new_title, title)
        out.append((s, float(s >= 0.7 and bool(set(new_files) & set(files)))))
    return out
