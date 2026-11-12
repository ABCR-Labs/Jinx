# Claude Haiku on open-only queues

`experiments/bench_v2/haiku_open.py 1600 8.5` asked Claude Haiku 4.5 about Jinx's top five open-only candidates for
every cross-author query and for 1,600 of the 2,513 no-duplicate queries (random, seed 7; `llm_haiku45_open_negsample.parquet`).
Verdicts for identical (query, candidate) pairs from the earlier run were reused; new spend is in `llm_haiku45_open_cost.json`.

This folder is `eval2.py` run with `NEG_SUBSET=llm_haiku45_open_negsample.parquet`: models and rankings are the same as
in `results/`, but false alarms and operating curves use only the sampled no-duplicate queries, so every method,
Haiku included, is scored on the same queries. Haiku's false-alarm numbers in `results/false_alarms.csv` are not valid
(unsampled queries keep Jinx's raw score) and the papers take them from here.
