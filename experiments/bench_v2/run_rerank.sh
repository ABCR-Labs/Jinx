#!/bin/bash
cd /home/ubuntu/research/prdupecheck/bench2
python3 rerank_ce.py
THREADS=4 python3 llm_judge.py Qwen/Qwen2.5-1.5B-Instruct qwen15 5 300
echo RERANK_ALLDONE
