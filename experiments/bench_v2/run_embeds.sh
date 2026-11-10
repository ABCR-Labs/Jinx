#!/bin/bash
cd /home/ubuntu/research/prdupecheck/bench2
python3 embed_model.py BAAI/bge-small-en-v1.5 raw bge_raw 256
python3 embed_model.py BAAI/bge-small-en-v1.5 diff bge_diff 256
python3 embed_model.py microsoft/unixcoder-base diff unix_diff 256
python3 embed_model.py BAAI/bge-small-en-v1.5 stripped bge_stripped 256
echo ALLDONE
