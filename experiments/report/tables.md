**cross-author** (n = 342)

| Family | Strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |
|---|---|---|---|---|
| 7 supervised | All signals, LR | 0.906 [0.87, 0.94] | 0.974 [0.96, 0.99] | 0.935 [0.91, 0.96] |
| 7 supervised | Jinx + MiniLM, LR (current tool) | 0.901 [0.87, 0.93] | 0.971 [0.95, 0.99] | 0.932 [0.91, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.901 [0.86, 0.93] | 0.974 [0.96, 0.99] | 0.931 [0.90, 0.96] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | 0.898 [0.86, 0.94] | 0.971 [0.95, 0.99] | 0.932 [0.91, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 0.898 [0.86, 0.93] | 0.971 [0.95, 0.99] | 0.930 [0.90, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 0.895 [0.86, 0.93] | 0.971 [0.95, 0.99] | 0.929 [0.90, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 0.895 [0.86, 0.93] | 0.971 [0.95, 0.99] | 0.928 [0.90, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 0.892 [0.86, 0.93] | 0.971 [0.95, 0.99] | 0.927 [0.90, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 0.889 [0.86, 0.92] | 0.971 [0.95, 0.99] | 0.925 [0.90, 0.95] |
| 7 supervised | Jinx lexical, LR | 0.889 [0.85, 0.93] | 0.971 [0.95, 0.99] | 0.925 [0.90, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 0.886 [0.85, 0.92] | 0.971 [0.95, 0.99] | 0.925 [0.90, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker-base (stacked LR) | 0.883 [0.84, 0.92] | 0.974 [0.96, 0.99] | 0.923 [0.89, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 0.880 [0.85, 0.92] | 0.971 [0.95, 0.99] | 0.922 [0.90, 0.95] |
| 7 supervised | All signals, gradient boosting | 0.877 [0.84, 0.92] | 0.959 [0.94, 0.98] | 0.915 [0.89, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 0.874 [0.84, 0.92] | 0.971 [0.95, 0.99] | 0.919 [0.90, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 0.874 [0.84, 0.91] | 0.971 [0.95, 0.99] | 0.918 [0.89, 0.95] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 0.871 [0.83, 0.91] | 0.971 [0.95, 0.99] | 0.918 [0.89, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 0.871 [0.84, 0.92] | 0.971 [0.95, 0.99] | 0.917 [0.89, 0.95] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 0.871 [0.84, 0.92] | 0.971 [0.95, 0.99] | 0.916 [0.89, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 0.868 [0.83, 0.92] | 0.971 [0.95, 0.99] | 0.916 [0.89, 0.95] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 0.868 [0.82, 0.92] | 0.965 [0.94, 0.99] | 0.912 [0.88, 0.95] |
| 7 supervised | Jinx features, gradient boosting | 0.865 [0.83, 0.91] | 0.956 [0.93, 0.98] | 0.908 [0.88, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 0.854 [0.82, 0.90] | 0.971 [0.95, 0.99] | 0.906 [0.88, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 0.851 [0.82, 0.90] | 0.968 [0.95, 0.99] | 0.904 [0.88, 0.94] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 re-rank top-5 | 0.842 [0.80, 0.90] | 0.971 [0.95, 0.99] | 0.902 [0.88, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-5 | 0.839 [0.80, 0.88] | 0.971 [0.95, 0.99] | 0.899 [0.87, 0.93] |
| 3 links | Links only (same issue / #ref) | 0.839 [0.78, 0.90] | 0.924 [0.88, 0.97] | 0.882 [0.84, 0.93] |
| 10 stacked cascade (ours) | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.816 [0.76, 0.87] | 0.953 [0.93, 0.98] | 0.876 [0.84, 0.91] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-5 | 0.810 [0.76, 0.86] | 0.971 [0.95, 0.99] | 0.877 [0.84, 0.91] |
| 7 supervised | INTRUDE + time (Wang et al. 2019), LR | 0.810 [0.77, 0.86] | 0.953 [0.92, 0.98] | 0.873 [0.84, 0.91] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-10 | 0.804 [0.75, 0.86] | 0.965 [0.94, 0.99] | 0.877 [0.84, 0.91] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-10 | 0.792 [0.74, 0.84] | 0.942 [0.91, 0.97] | 0.858 [0.82, 0.89] |
| 5 existing bot | contrib-guard/phoenix (bot, exact port) | 0.778 [0.73, 0.84] | 0.918 [0.87, 0.96] | 0.843 [0.80, 0.89] |
| 4 embedding | BGE-small template-stripped | 0.763 [0.70, 0.82] | 0.915 [0.86, 0.96] | 0.830 [0.78, 0.88] |
| 1 lexical | TF-IDF template-stripped | 0.760 [0.71, 0.82] | 0.930 [0.89, 0.97] | 0.835 [0.79, 0.88] |
| 4 embedding | BGE-base template-stripped | 0.760 [0.70, 0.82] | 0.909 [0.85, 0.95] | 0.828 [0.78, 0.88] |
| 1 lexical | TF-IDF raw text (Li et al. 2017) | 0.757 [0.70, 0.82] | 0.921 [0.88, 0.96] | 0.832 [0.79, 0.88] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding + code | 0.757 [0.69, 0.83] | 0.921 [0.88, 0.97] | 0.831 [0.78, 0.88] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-5 | 0.751 [0.70, 0.80] | 0.971 [0.95, 0.99] | 0.840 [0.80, 0.87] |
| 4 embedding | BGE-small raw text | 0.751 [0.69, 0.82] | 0.921 [0.87, 0.96] | 0.823 [0.77, 0.87] |
| 4 embedding | MiniLM template-stripped | 0.751 [0.70, 0.82] | 0.898 [0.85, 0.94] | 0.820 [0.77, 0.87] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 0.749 [0.69, 0.80] | 0.953 [0.93, 0.98] | 0.841 [0.81, 0.88] |
| 1 lexical | BM25 template-stripped | 0.737 [0.68, 0.80] | 0.909 [0.87, 0.96] | 0.814 [0.77, 0.86] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding | 0.734 [0.68, 0.80] | 0.909 [0.86, 0.96] | 0.816 [0.77, 0.87] |
| 4 embedding | MiniLM raw text | 0.725 [0.67, 0.79] | 0.906 [0.85, 0.95] | 0.807 [0.76, 0.86] |
| 5 existing bot | Simili-bot (bot, re-impl) | 0.725 [0.67, 0.79] | 0.892 [0.84, 0.93] | 0.804 [0.76, 0.86] |
| 6 unsupervised hybrid | RRF hybrid: text + code + links + recency | 0.713 [0.61, 0.80] | 0.918 [0.88, 0.96] | 0.802 [0.74, 0.87] |
| 1 lexical | BM25 raw text | 0.711 [0.65, 0.77] | 0.898 [0.85, 0.95] | 0.796 [0.75, 0.85] |
| 5 existing bot | PRSense (bot, re-impl) | 0.711 [0.61, 0.81] | 0.865 [0.79, 0.93] | 0.784 [0.70, 0.87] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM re-rank top-10 | 0.708 [0.64, 0.77] | 0.939 [0.91, 0.97] | 0.810 [0.77, 0.85] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-10 | 0.708 [0.66, 0.76] | 0.906 [0.87, 0.94] | 0.798 [0.76, 0.83] |
| 4 embedding | UniXcoder template-stripped text | 0.637 [0.56, 0.73] | 0.816 [0.75, 0.90] | 0.719 [0.65, 0.80] |
| 2 code | BM25 on diff | 0.585 [0.50, 0.69] | 0.781 [0.68, 0.88] | 0.678 [0.59, 0.77] |
| 2 code | Code overlap sum (files+hunks+lines) | 0.576 [0.50, 0.66] | 0.795 [0.70, 0.88] | 0.673 [0.59, 0.75] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-5 | 0.567 [0.50, 0.64] | 0.971 [0.95, 0.99] | 0.732 [0.69, 0.78] |
| 4 embedding | Jina code embeddings v2 on diff | 0.520 [0.43, 0.64] | 0.696 [0.60, 0.81] | 0.609 [0.52, 0.72] |
| 4 embedding | BGE-small on diff | 0.515 [0.43, 0.63] | 0.696 [0.60, 0.82] | 0.600 [0.51, 0.72] |
| 2 code | Changed-files Jaccard | 0.512 [0.44, 0.59] | 0.734 [0.64, 0.82] | 0.617 [0.54, 0.69] |
| 2 code | Hunk overlap | 0.512 [0.43, 0.61] | 0.760 [0.68, 0.85] | 0.616 [0.54, 0.70] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base re-rank top-10 | 0.503 [0.42, 0.59] | 0.874 [0.83, 0.91] | 0.652 [0.60, 0.72] |
| 2 code | Identical changed lines | 0.480 [0.41, 0.57] | 0.708 [0.63, 0.81] | 0.577 [0.51, 0.67] |
| 4 embedding | MiniLM on diff | 0.477 [0.40, 0.58] | 0.664 [0.56, 0.80] | 0.565 [0.48, 0.68] |
| 4 embedding | UniXcoder (code model) on diff | 0.477 [0.38, 0.60] | 0.640 [0.53, 0.78] | 0.558 [0.46, 0.68] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-10 | 0.442 [0.38, 0.52] | 0.868 [0.83, 0.91] | 0.624 [0.58, 0.68] |
| 4 embedding | CodeBERT (mean-pooled) on diff | 0.380 [0.30, 0.50] | 0.512 [0.40, 0.67] | 0.448 [0.35, 0.58] |
| 0 trivial | Recency only (newest open PR first) | 0.193 [0.13, 0.28] | 0.450 [0.32, 0.61] | 0.316 [0.23, 0.43] |


**all labelled** (n = 1867)

| Family | Strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |
|---|---|---|---|---|
| 7 supervised | Jinx lexical, LR | 0.903 [0.88, 0.93] | 0.984 [0.98, 0.99] | 0.938 [0.92, 0.95] |
| 7 supervised | All signals, LR | 0.894 [0.85, 0.93] | 0.975 [0.96, 0.99] | 0.930 [0.89, 0.96] |
| 7 supervised | Jinx + MiniLM, LR (current tool) | 0.890 [0.84, 0.93] | 0.980 [0.97, 0.99] | 0.927 [0.89, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 0.882 [0.83, 0.92] | 0.980 [0.97, 0.99] | 0.923 [0.88, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.880 [0.83, 0.92] | 0.981 [0.97, 0.99] | 0.922 [0.88, 0.95] |
| 7 supervised | All signals, gradient boosting | 0.879 [0.85, 0.91] | 0.976 [0.96, 0.99] | 0.922 [0.90, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 0.878 [0.83, 0.92] | 0.981 [0.97, 0.99] | 0.921 [0.88, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 0.878 [0.83, 0.92] | 0.982 [0.97, 0.99] | 0.920 [0.88, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 0.876 [0.82, 0.92] | 0.980 [0.97, 0.99] | 0.920 [0.88, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 0.876 [0.82, 0.92] | 0.980 [0.97, 0.99] | 0.920 [0.88, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 0.875 [0.83, 0.91] | 0.981 [0.97, 0.99] | 0.920 [0.88, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 0.875 [0.82, 0.92] | 0.982 [0.97, 0.99] | 0.920 [0.88, 0.95] |
| 7 supervised | Jinx features, gradient boosting | 0.874 [0.84, 0.91] | 0.975 [0.96, 0.99] | 0.919 [0.90, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 0.874 [0.82, 0.91] | 0.980 [0.97, 0.99] | 0.919 [0.88, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 0.874 [0.82, 0.91] | 0.980 [0.97, 0.99] | 0.918 [0.88, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 0.873 [0.82, 0.91] | 0.980 [0.97, 0.99] | 0.918 [0.88, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 0.871 [0.82, 0.91] | 0.982 [0.97, 0.99] | 0.916 [0.88, 0.94] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 0.866 [0.82, 0.91] | 0.981 [0.97, 0.99] | 0.915 [0.88, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker-base (stacked LR) | 0.862 [0.81, 0.90] | 0.981 [0.97, 0.99] | 0.911 [0.87, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 0.861 [0.81, 0.90] | 0.980 [0.97, 0.99] | 0.911 [0.87, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 0.858 [0.81, 0.90] | 0.978 [0.97, 0.99] | 0.909 [0.87, 0.94] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 0.852 [0.80, 0.90] | 0.979 [0.97, 0.99] | 0.906 [0.87, 0.94] |
| 7 supervised | INTRUDE + time (Wang et al. 2019), LR | 0.848 [0.82, 0.88] | 0.965 [0.95, 0.98] | 0.902 [0.88, 0.92] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 0.846 [0.79, 0.89] | 0.980 [0.97, 0.99] | 0.902 [0.86, 0.93] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-5 | 0.835 [0.79, 0.87] | 0.980 [0.97, 0.99] | 0.896 [0.86, 0.92] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-10 | 0.813 [0.76, 0.85] | 0.978 [0.97, 0.99] | 0.880 [0.84, 0.91] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-5 | 0.806 [0.76, 0.85] | 0.980 [0.97, 0.99] | 0.875 [0.84, 0.90] |
| 3 links | Links only (same issue / #ref) | 0.804 [0.76, 0.84] | 0.940 [0.91, 0.96] | 0.866 [0.83, 0.89] |
| 10 stacked cascade (ours) | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.798 [0.75, 0.84] | 0.967 [0.96, 0.98] | 0.869 [0.83, 0.90] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-10 | 0.791 [0.75, 0.83] | 0.952 [0.94, 0.96] | 0.856 [0.82, 0.88] |
| 5 existing bot | contrib-guard/phoenix (bot, exact port) | 0.781 [0.73, 0.82] | 0.925 [0.90, 0.95] | 0.845 [0.81, 0.88] |
| 1 lexical | TF-IDF template-stripped | 0.777 [0.73, 0.82] | 0.916 [0.86, 0.95] | 0.842 [0.80, 0.88] |
| 6 unsupervised hybrid | RRF hybrid: text + code + links + recency | 0.775 [0.74, 0.81] | 0.940 [0.90, 0.97] | 0.850 [0.81, 0.88] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding + code | 0.774 [0.72, 0.82] | 0.928 [0.88, 0.96] | 0.842 [0.79, 0.88] |
| 1 lexical | TF-IDF raw text (Li et al. 2017) | 0.772 [0.72, 0.82] | 0.911 [0.86, 0.95] | 0.837 [0.79, 0.88] |
| 4 embedding | BGE-base template-stripped | 0.769 [0.72, 0.81] | 0.898 [0.85, 0.94] | 0.831 [0.78, 0.87] |
| 4 embedding | BGE-small raw text | 0.765 [0.71, 0.81] | 0.901 [0.84, 0.95] | 0.828 [0.78, 0.87] |
| 4 embedding | BGE-small template-stripped | 0.763 [0.71, 0.81] | 0.900 [0.84, 0.94] | 0.827 [0.78, 0.87] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 0.756 [0.71, 0.80] | 0.965 [0.95, 0.98] | 0.844 [0.81, 0.88] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding | 0.755 [0.71, 0.80] | 0.910 [0.86, 0.95] | 0.827 [0.78, 0.87] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-5 | 0.748 [0.70, 0.79] | 0.980 [0.97, 0.99] | 0.835 [0.80, 0.86] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM re-rank top-10 | 0.747 [0.70, 0.79] | 0.961 [0.95, 0.97] | 0.836 [0.80, 0.87] |
| 1 lexical | BM25 template-stripped | 0.744 [0.70, 0.79] | 0.904 [0.86, 0.94] | 0.817 [0.77, 0.86] |
| 1 lexical | BM25 raw text | 0.735 [0.69, 0.78] | 0.901 [0.86, 0.94] | 0.810 [0.77, 0.85] |
| 4 embedding | MiniLM template-stripped | 0.730 [0.68, 0.78] | 0.883 [0.83, 0.93] | 0.802 [0.75, 0.84] |
| 5 existing bot | Simili-bot (bot, re-impl) | 0.729 [0.68, 0.77] | 0.883 [0.83, 0.93] | 0.801 [0.75, 0.84] |
| 5 existing bot | PRSense (bot, re-impl) | 0.722 [0.67, 0.77] | 0.885 [0.84, 0.93] | 0.796 [0.75, 0.84] |
| 4 embedding | MiniLM raw text | 0.721 [0.67, 0.77] | 0.885 [0.83, 0.93] | 0.797 [0.75, 0.84] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-10 | 0.716 [0.67, 0.75] | 0.911 [0.89, 0.93] | 0.799 [0.76, 0.83] |
| 4 embedding | UniXcoder template-stripped text | 0.656 [0.61, 0.70] | 0.819 [0.77, 0.86] | 0.731 [0.69, 0.77] |
| 2 code | Code overlap sum (files+hunks+lines) | 0.640 [0.59, 0.69] | 0.827 [0.77, 0.88] | 0.729 [0.68, 0.77] |
| 2 code | BM25 on diff | 0.631 [0.58, 0.68] | 0.806 [0.75, 0.86] | 0.712 [0.67, 0.76] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-5 | 0.599 [0.56, 0.64] | 0.980 [0.97, 0.99] | 0.747 [0.72, 0.78] |
| 2 code | Identical changed lines | 0.587 [0.54, 0.63] | 0.770 [0.72, 0.82] | 0.674 [0.63, 0.72] |
| 4 embedding | Jina code embeddings v2 on diff | 0.567 [0.52, 0.62] | 0.755 [0.71, 0.81] | 0.656 [0.61, 0.70] |
| 2 code | Changed-files Jaccard | 0.561 [0.51, 0.61] | 0.786 [0.74, 0.83] | 0.665 [0.62, 0.71] |
| 2 code | Hunk overlap | 0.557 [0.51, 0.61] | 0.797 [0.74, 0.85] | 0.666 [0.62, 0.71] |
| 4 embedding | BGE-small on diff | 0.556 [0.51, 0.60] | 0.751 [0.70, 0.80] | 0.646 [0.60, 0.69] |
| 4 embedding | UniXcoder (code model) on diff | 0.547 [0.50, 0.60] | 0.721 [0.67, 0.78] | 0.630 [0.58, 0.68] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base re-rank top-10 | 0.523 [0.48, 0.57] | 0.911 [0.90, 0.92] | 0.680 [0.65, 0.71] |
| 4 embedding | MiniLM on diff | 0.518 [0.47, 0.57] | 0.711 [0.66, 0.77] | 0.610 [0.57, 0.66] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-10 | 0.506 [0.47, 0.55] | 0.892 [0.88, 0.91] | 0.664 [0.64, 0.69] |
| 4 embedding | CodeBERT (mean-pooled) on diff | 0.441 [0.40, 0.49] | 0.626 [0.58, 0.69] | 0.530 [0.49, 0.58] |
| 0 trivial | Recency only (newest open PR first) | 0.358 [0.31, 0.42] | 0.640 [0.57, 0.72] | 0.484 [0.43, 0.55] |


**self-replacement** (n = 1525)

| Family | Strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |
|---|---|---|---|---|
| 7 supervised | Jinx lexical, LR | 0.906 [0.87, 0.93] | 0.988 [0.98, 1.00] | 0.941 [0.92, 0.96] |
| 7 supervised | All signals, LR | 0.892 [0.84, 0.93] | 0.976 [0.95, 0.99] | 0.929 [0.89, 0.96] |
| 7 supervised | Jinx + MiniLM, LR (current tool) | 0.887 [0.83, 0.93] | 0.982 [0.97, 0.99] | 0.925 [0.88, 0.96] |
| 7 supervised | All signals, gradient boosting | 0.879 [0.85, 0.91] | 0.980 [0.97, 0.99] | 0.924 [0.90, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 0.879 [0.82, 0.93] | 0.982 [0.97, 0.99] | 0.922 [0.88, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 0.876 [0.82, 0.92] | 0.982 [0.97, 0.99] | 0.920 [0.88, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 0.876 [0.82, 0.92] | 0.985 [0.97, 1.00] | 0.919 [0.88, 0.95] |
| 7 supervised | Jinx features, gradient boosting | 0.875 [0.84, 0.91] | 0.979 [0.96, 0.99] | 0.921 [0.90, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 0.875 [0.82, 0.92] | 0.983 [0.97, 0.99] | 0.920 [0.88, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.875 [0.82, 0.92] | 0.983 [0.97, 0.99] | 0.920 [0.88, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 0.875 [0.82, 0.92] | 0.982 [0.97, 0.99] | 0.919 [0.88, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 0.874 [0.82, 0.92] | 0.982 [0.97, 0.99] | 0.919 [0.87, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 0.872 [0.81, 0.92] | 0.982 [0.97, 0.99] | 0.918 [0.87, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 0.871 [0.81, 0.92] | 0.982 [0.97, 0.99] | 0.918 [0.87, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 0.870 [0.81, 0.92] | 0.984 [0.97, 1.00] | 0.917 [0.88, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 0.870 [0.82, 0.92] | 0.985 [0.97, 1.00] | 0.916 [0.87, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 0.870 [0.82, 0.92] | 0.984 [0.97, 0.99] | 0.917 [0.88, 0.95] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 0.865 [0.81, 0.91] | 0.984 [0.97, 0.99] | 0.915 [0.87, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 0.862 [0.81, 0.91] | 0.982 [0.97, 0.99] | 0.912 [0.87, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 0.860 [0.80, 0.91] | 0.980 [0.97, 0.99] | 0.911 [0.87, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker-base (stacked LR) | 0.858 [0.80, 0.91] | 0.982 [0.97, 0.99] | 0.909 [0.86, 0.94] |
| 7 supervised | INTRUDE + time (Wang et al. 2019), LR | 0.857 [0.82, 0.89] | 0.968 [0.95, 0.99] | 0.908 [0.88, 0.93] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 0.849 [0.79, 0.90] | 0.982 [0.97, 0.99] | 0.905 [0.86, 0.94] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 0.840 [0.78, 0.89] | 0.982 [0.97, 0.99] | 0.899 [0.85, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-5 | 0.834 [0.78, 0.88] | 0.982 [0.97, 0.99] | 0.895 [0.85, 0.93] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-10 | 0.814 [0.76, 0.86] | 0.980 [0.97, 0.99] | 0.880 [0.84, 0.92] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-5 | 0.805 [0.75, 0.85] | 0.982 [0.97, 0.99] | 0.874 [0.83, 0.91] |
| 3 links | Links only (same issue / #ref) | 0.797 [0.74, 0.84] | 0.944 [0.91, 0.97] | 0.863 [0.82, 0.90] |
| 10 stacked cascade (ours) | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.794 [0.74, 0.84] | 0.970 [0.96, 0.98] | 0.867 [0.83, 0.90] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-10 | 0.790 [0.74, 0.84] | 0.954 [0.94, 0.97] | 0.856 [0.82, 0.89] |
| 6 unsupervised hybrid | RRF hybrid: text + code + links + recency | 0.789 [0.75, 0.83] | 0.945 [0.90, 0.98] | 0.860 [0.82, 0.90] |
| 5 existing bot | contrib-guard/phoenix (bot, exact port) | 0.782 [0.72, 0.83] | 0.927 [0.89, 0.96] | 0.846 [0.80, 0.89] |
| 1 lexical | TF-IDF template-stripped | 0.780 [0.72, 0.83] | 0.913 [0.86, 0.96] | 0.843 [0.79, 0.89] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding + code | 0.778 [0.72, 0.84] | 0.929 [0.88, 0.97] | 0.845 [0.79, 0.89] |
| 1 lexical | TF-IDF raw text (Li et al. 2017) | 0.776 [0.72, 0.83] | 0.909 [0.85, 0.96] | 0.838 [0.79, 0.88] |
| 4 embedding | BGE-base template-stripped | 0.770 [0.71, 0.83] | 0.896 [0.84, 0.95] | 0.832 [0.78, 0.88] |
| 4 embedding | BGE-small raw text | 0.769 [0.71, 0.82] | 0.897 [0.83, 0.95] | 0.830 [0.78, 0.88] |
| 4 embedding | BGE-small template-stripped | 0.763 [0.70, 0.82] | 0.896 [0.84, 0.95] | 0.826 [0.77, 0.88] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding | 0.760 [0.71, 0.81] | 0.910 [0.85, 0.96] | 0.829 [0.78, 0.88] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 0.758 [0.70, 0.81] | 0.967 [0.95, 0.98] | 0.844 [0.80, 0.88] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM re-rank top-10 | 0.756 [0.70, 0.81] | 0.967 [0.95, 0.98] | 0.841 [0.80, 0.88] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-5 | 0.748 [0.69, 0.80] | 0.982 [0.97, 0.99] | 0.834 [0.79, 0.87] |
| 1 lexical | BM25 template-stripped | 0.746 [0.69, 0.80] | 0.903 [0.85, 0.95] | 0.817 [0.77, 0.86] |
| 1 lexical | BM25 raw text | 0.740 [0.68, 0.79] | 0.902 [0.85, 0.95] | 0.813 [0.76, 0.86] |
| 5 existing bot | Simili-bot (bot, re-impl) | 0.730 [0.67, 0.78] | 0.881 [0.82, 0.94] | 0.800 [0.75, 0.85] |
| 4 embedding | MiniLM template-stripped | 0.725 [0.67, 0.78] | 0.879 [0.82, 0.93] | 0.798 [0.75, 0.85] |
| 5 existing bot | PRSense (bot, re-impl) | 0.725 [0.67, 0.78] | 0.890 [0.83, 0.94] | 0.799 [0.75, 0.85] |
| 4 embedding | MiniLM raw text | 0.721 [0.66, 0.77] | 0.880 [0.82, 0.93] | 0.795 [0.74, 0.85] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-10 | 0.718 [0.67, 0.76] | 0.912 [0.89, 0.93] | 0.799 [0.76, 0.83] |
| 4 embedding | UniXcoder template-stripped text | 0.660 [0.61, 0.71] | 0.820 [0.77, 0.87] | 0.734 [0.69, 0.78] |
| 2 code | Code overlap sum (files+hunks+lines) | 0.654 [0.60, 0.71] | 0.834 [0.77, 0.89] | 0.742 [0.69, 0.79] |
| 2 code | BM25 on diff | 0.641 [0.59, 0.69] | 0.812 [0.76, 0.87] | 0.720 [0.67, 0.77] |
| 2 code | Identical changed lines | 0.610 [0.56, 0.66] | 0.784 [0.73, 0.84] | 0.696 [0.65, 0.74] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-5 | 0.607 [0.56, 0.65] | 0.982 [0.97, 0.99] | 0.751 [0.72, 0.78] |
| 4 embedding | Jina code embeddings v2 on diff | 0.577 [0.53, 0.63] | 0.769 [0.72, 0.82] | 0.666 [0.62, 0.71] |
| 2 code | Changed-files Jaccard | 0.572 [0.52, 0.63] | 0.797 [0.75, 0.85] | 0.676 [0.63, 0.73] |
| 2 code | Hunk overlap | 0.567 [0.52, 0.62] | 0.805 [0.75, 0.86] | 0.678 [0.63, 0.73] |
| 4 embedding | BGE-small on diff | 0.565 [0.52, 0.61] | 0.764 [0.72, 0.81] | 0.656 [0.61, 0.70] |
| 4 embedding | UniXcoder (code model) on diff | 0.563 [0.51, 0.62] | 0.740 [0.69, 0.80] | 0.646 [0.60, 0.70] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base re-rank top-10 | 0.527 [0.48, 0.57] | 0.919 [0.90, 0.93] | 0.686 [0.65, 0.72] |
| 4 embedding | MiniLM on diff | 0.527 [0.48, 0.58] | 0.722 [0.68, 0.77] | 0.620 [0.58, 0.67] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-10 | 0.521 [0.48, 0.57] | 0.897 [0.88, 0.91] | 0.673 [0.64, 0.71] |
| 4 embedding | CodeBERT (mean-pooled) on diff | 0.454 [0.41, 0.50] | 0.652 [0.61, 0.70] | 0.549 [0.51, 0.59] |
| 0 trivial | Recency only (newest open PR first) | 0.395 [0.34, 0.45] | 0.682 [0.62, 0.75] | 0.522 [0.47, 0.58] |


**cross-author, same agent** (n = 228)

| Family | Strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |
|---|---|---|---|---|
| 7 supervised | All signals, LR | 0.908 [0.86, 0.95] | 0.965 [0.94, 0.99] | 0.933 [0.90, 0.96] |
| 7 supervised | Jinx + MiniLM, LR (current tool) | 0.899 [0.85, 0.94] | 0.965 [0.94, 0.99] | 0.929 [0.90, 0.96] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 0.899 [0.85, 0.94] | 0.965 [0.94, 0.99] | 0.927 [0.89, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 0.899 [0.85, 0.94] | 0.965 [0.94, 0.99] | 0.927 [0.89, 0.96] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 0.895 [0.86, 0.93] | 0.974 [0.95, 0.99] | 0.930 [0.90, 0.96] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | 0.895 [0.85, 0.94] | 0.965 [0.94, 0.99] | 0.927 [0.89, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 0.895 [0.85, 0.93] | 0.965 [0.94, 0.99] | 0.927 [0.90, 0.95] |
| 7 supervised | All signals, gradient boosting | 0.895 [0.85, 0.94] | 0.965 [0.94, 0.99] | 0.926 [0.89, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 0.895 [0.85, 0.93] | 0.965 [0.94, 0.99] | 0.925 [0.89, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 0.895 [0.85, 0.94] | 0.965 [0.94, 0.99] | 0.925 [0.89, 0.96] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 0.890 [0.85, 0.94] | 0.965 [0.94, 0.99] | 0.925 [0.89, 0.96] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.890 [0.84, 0.93] | 0.969 [0.94, 0.99] | 0.923 [0.89, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 0.886 [0.84, 0.93] | 0.965 [0.94, 0.99] | 0.922 [0.89, 0.95] |
| 7 supervised | Jinx lexical, LR | 0.882 [0.83, 0.93] | 0.965 [0.94, 0.99] | 0.919 [0.89, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 0.877 [0.83, 0.92] | 0.969 [0.95, 0.99] | 0.918 [0.89, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 0.877 [0.83, 0.92] | 0.965 [0.94, 0.99] | 0.917 [0.89, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 0.877 [0.84, 0.92] | 0.965 [0.94, 0.99] | 0.917 [0.89, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 0.877 [0.84, 0.92] | 0.965 [0.94, 0.99] | 0.917 [0.89, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 0.877 [0.83, 0.93] | 0.965 [0.94, 0.99] | 0.916 [0.89, 0.95] |
| 7 supervised | Jinx features, gradient boosting | 0.873 [0.83, 0.92] | 0.961 [0.94, 0.99] | 0.915 [0.88, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 0.873 [0.83, 0.92] | 0.965 [0.94, 0.99] | 0.915 [0.89, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 0.873 [0.83, 0.92] | 0.965 [0.94, 0.99] | 0.914 [0.88, 0.95] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker-base (stacked LR) | 0.868 [0.82, 0.91] | 0.969 [0.94, 0.99] | 0.913 [0.88, 0.94] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 0.864 [0.82, 0.91] | 0.969 [0.94, 0.99] | 0.912 [0.88, 0.94] |
| 3 links | Links only (same issue / #ref) | 0.851 [0.80, 0.90] | 0.934 [0.89, 0.97] | 0.892 [0.85, 0.93] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 re-rank top-5 | 0.838 [0.79, 0.90] | 0.965 [0.94, 0.99] | 0.897 [0.86, 0.94] |
| 7 supervised | INTRUDE + time (Wang et al. 2019), LR | 0.825 [0.77, 0.88] | 0.961 [0.94, 0.98] | 0.883 [0.85, 0.92] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-5 | 0.816 [0.76, 0.87] | 0.965 [0.94, 0.99] | 0.882 [0.84, 0.92] |
| 5 existing bot | contrib-guard/phoenix (bot, exact port) | 0.811 [0.76, 0.87] | 0.925 [0.88, 0.96] | 0.861 [0.82, 0.90] |
| 10 stacked cascade (ours) | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.803 [0.74, 0.86] | 0.943 [0.91, 0.97] | 0.868 [0.82, 0.91] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-5 | 0.798 [0.73, 0.86] | 0.965 [0.94, 0.99] | 0.866 [0.82, 0.91] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding + code | 0.798 [0.75, 0.85] | 0.930 [0.90, 0.96] | 0.858 [0.82, 0.90] |
| 1 lexical | BM25 template-stripped | 0.785 [0.72, 0.84] | 0.934 [0.90, 0.96] | 0.852 [0.80, 0.89] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-10 | 0.781 [0.72, 0.83] | 0.956 [0.92, 0.99] | 0.861 [0.82, 0.90] |
| 1 lexical | BM25 raw text | 0.781 [0.72, 0.84] | 0.925 [0.89, 0.96] | 0.848 [0.80, 0.89] |
| 1 lexical | TF-IDF template-stripped | 0.781 [0.73, 0.84] | 0.934 [0.90, 0.97] | 0.847 [0.81, 0.89] |
| 4 embedding | BGE-base template-stripped | 0.781 [0.71, 0.84] | 0.917 [0.88, 0.95] | 0.844 [0.79, 0.89] |
| 4 embedding | MiniLM template-stripped | 0.781 [0.72, 0.84] | 0.912 [0.88, 0.94] | 0.843 [0.80, 0.89] |
| 4 embedding | BGE-small template-stripped | 0.781 [0.71, 0.84] | 0.921 [0.88, 0.96] | 0.842 [0.79, 0.89] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding | 0.776 [0.71, 0.83] | 0.939 [0.90, 0.97] | 0.849 [0.80, 0.89] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-10 | 0.776 [0.71, 0.84] | 0.934 [0.90, 0.97] | 0.845 [0.80, 0.89] |
| 1 lexical | TF-IDF raw text (Li et al. 2017) | 0.776 [0.72, 0.83] | 0.930 [0.89, 0.96] | 0.844 [0.80, 0.88] |
| 4 embedding | BGE-small raw text | 0.772 [0.70, 0.83] | 0.930 [0.89, 0.96] | 0.838 [0.78, 0.88] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 0.763 [0.70, 0.83] | 0.947 [0.92, 0.98] | 0.845 [0.80, 0.89] |
| 6 unsupervised hybrid | RRF hybrid: text + code + links + recency | 0.754 [0.68, 0.82] | 0.939 [0.91, 0.97] | 0.837 [0.79, 0.88] |
| 5 existing bot | Simili-bot (bot, re-impl) | 0.750 [0.70, 0.81] | 0.899 [0.86, 0.94] | 0.823 [0.78, 0.87] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-5 | 0.737 [0.67, 0.79] | 0.965 [0.94, 0.99] | 0.827 [0.78, 0.87] |
| 4 embedding | MiniLM raw text | 0.737 [0.68, 0.80] | 0.917 [0.87, 0.95] | 0.816 [0.77, 0.86] |
| 5 existing bot | PRSense (bot, re-impl) | 0.732 [0.66, 0.81] | 0.899 [0.86, 0.94] | 0.809 [0.75, 0.87] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM re-rank top-10 | 0.724 [0.67, 0.77] | 0.947 [0.91, 0.97] | 0.819 [0.78, 0.85] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-10 | 0.693 [0.63, 0.75] | 0.886 [0.84, 0.93] | 0.784 [0.74, 0.83] |
| 4 embedding | UniXcoder template-stripped text | 0.675 [0.60, 0.75] | 0.860 [0.81, 0.91] | 0.759 [0.70, 0.82] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-5 | 0.596 [0.53, 0.68] | 0.965 [0.94, 0.99] | 0.750 [0.71, 0.81] |
| 2 code | BM25 on diff | 0.592 [0.52, 0.66] | 0.811 [0.75, 0.87] | 0.695 [0.64, 0.75] |
| 2 code | Code overlap sum (files+hunks+lines) | 0.570 [0.50, 0.65] | 0.816 [0.76, 0.88] | 0.674 [0.62, 0.74] |
| 4 embedding | BGE-small on diff | 0.531 [0.46, 0.61] | 0.750 [0.68, 0.83] | 0.633 [0.57, 0.70] |
| 4 embedding | Jina code embeddings v2 on diff | 0.518 [0.44, 0.60] | 0.724 [0.65, 0.80] | 0.618 [0.55, 0.69] |
| 2 code | Hunk overlap | 0.509 [0.44, 0.59] | 0.763 [0.70, 0.85] | 0.618 [0.56, 0.69] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base re-rank top-10 | 0.496 [0.43, 0.57] | 0.882 [0.83, 0.93] | 0.650 [0.60, 0.71] |
| 2 code | Changed-files Jaccard | 0.496 [0.43, 0.57] | 0.750 [0.69, 0.83] | 0.616 [0.56, 0.68] |
| 2 code | Identical changed lines | 0.487 [0.41, 0.58] | 0.724 [0.66, 0.81] | 0.587 [0.53, 0.67] |
| 4 embedding | MiniLM on diff | 0.482 [0.42, 0.56] | 0.711 [0.64, 0.80] | 0.586 [0.53, 0.66] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-10 | 0.478 [0.41, 0.57] | 0.868 [0.82, 0.91] | 0.649 [0.60, 0.71] |
| 4 embedding | UniXcoder (code model) on diff | 0.474 [0.40, 0.57] | 0.671 [0.59, 0.77] | 0.573 [0.50, 0.66] |
| 4 embedding | CodeBERT (mean-pooled) on diff | 0.399 [0.31, 0.50] | 0.548 [0.45, 0.67] | 0.472 [0.38, 0.58] |
| 0 trivial | Recency only (newest open PR first) | 0.193 [0.14, 0.27] | 0.496 [0.37, 0.65] | 0.330 [0.25, 0.43] |


**cross-author, cross-agent** (n = 114)

| Family | Strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |
|---|---|---|---|---|
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.921 [0.87, 0.97] | 0.982 [0.96, 1.00] | 0.948 [0.92, 0.98] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker-base (stacked LR) | 0.912 [0.86, 0.96] | 0.982 [0.96, 1.00] | 0.942 [0.91, 0.98] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | 0.904 [0.86, 0.97] | 0.982 [0.96, 1.00] | 0.942 [0.91, 0.98] |
| 7 supervised | Jinx + MiniLM, LR (current tool) | 0.904 [0.87, 0.96] | 0.982 [0.96, 1.00] | 0.939 [0.91, 0.98] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 0.904 [0.84, 0.97] | 0.982 [0.96, 1.00] | 0.939 [0.90, 0.98] |
| 7 supervised | All signals, LR | 0.904 [0.85, 0.97] | 0.991 [0.98, 1.00] | 0.938 [0.91, 0.98] |
| 7 supervised | Jinx lexical, LR | 0.904 [0.85, 0.97] | 0.982 [0.96, 1.00] | 0.937 [0.90, 0.98] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 0.895 [0.83, 0.97] | 0.982 [0.96, 1.00] | 0.935 [0.90, 0.98] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-5 | 0.886 [0.84, 0.96] | 0.982 [0.96, 1.00] | 0.935 [0.91, 0.98] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 0.886 [0.83, 0.95] | 0.982 [0.96, 1.00] | 0.933 [0.91, 0.97] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 0.886 [0.83, 0.95] | 0.982 [0.96, 1.00] | 0.932 [0.91, 0.97] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 0.886 [0.84, 0.95] | 0.982 [0.96, 1.00] | 0.930 [0.90, 0.97] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 0.886 [0.83, 0.95] | 0.974 [0.95, 1.00] | 0.928 [0.89, 0.97] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 0.877 [0.83, 0.95] | 0.982 [0.96, 1.00] | 0.926 [0.90, 0.97] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 0.877 [0.83, 0.95] | 0.982 [0.96, 1.00] | 0.926 [0.90, 0.97] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 0.877 [0.82, 0.95] | 0.982 [0.96, 1.00] | 0.925 [0.90, 0.97] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 0.868 [0.80, 0.95] | 0.982 [0.96, 1.00] | 0.922 [0.89, 0.97] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 0.860 [0.79, 0.95] | 0.982 [0.96, 1.00] | 0.917 [0.88, 0.97] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 0.860 [0.79, 0.95] | 0.982 [0.96, 1.00] | 0.917 [0.88, 0.97] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 re-rank top-5 | 0.851 [0.78, 0.97] | 0.982 [0.96, 1.00] | 0.913 [0.87, 0.98] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-10 | 0.851 [0.75, 0.96] | 0.982 [0.96, 1.00] | 0.910 [0.85, 0.97] |
| 7 supervised | Jinx features, gradient boosting | 0.851 [0.76, 0.96] | 0.947 [0.87, 1.00] | 0.893 [0.82, 0.98] |
| 7 supervised | All signals, gradient boosting | 0.842 [0.75, 0.95] | 0.947 [0.91, 1.00] | 0.894 [0.83, 0.97] |
| 10 stacked cascade (ours) | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.842 [0.73, 0.96] | 0.974 [0.95, 1.00] | 0.892 [0.81, 0.97] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-5 | 0.833 [0.77, 0.93] | 0.982 [0.96, 1.00] | 0.898 [0.86, 0.96] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 0.833 [0.77, 0.93] | 0.982 [0.96, 1.00] | 0.898 [0.86, 0.96] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-10 | 0.825 [0.76, 0.92] | 0.956 [0.92, 0.99] | 0.884 [0.84, 0.94] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 0.816 [0.70, 0.95] | 0.947 [0.90, 1.00] | 0.876 [0.79, 0.97] |
| 3 links | Links only (same issue / #ref) | 0.816 [0.71, 0.95] | 0.904 [0.81, 1.00] | 0.861 [0.76, 0.97] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 0.807 [0.74, 0.92] | 0.982 [0.96, 1.00] | 0.883 [0.84, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 0.798 [0.73, 0.91] | 0.965 [0.94, 1.00] | 0.878 [0.84, 0.95] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-5 | 0.781 [0.71, 0.89] | 0.982 [0.96, 1.00] | 0.865 [0.82, 0.93] |
| 7 supervised | INTRUDE + time (Wang et al. 2019), LR | 0.781 [0.69, 0.87] | 0.939 [0.85, 0.99] | 0.853 [0.78, 0.92] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-10 | 0.737 [0.65, 0.86] | 0.947 [0.91, 0.99] | 0.826 [0.76, 0.91] |
| 4 embedding | BGE-small template-stripped | 0.728 [0.63, 0.88] | 0.904 [0.80, 0.98] | 0.806 [0.72, 0.91] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 0.719 [0.61, 0.82] | 0.965 [0.93, 1.00] | 0.834 [0.78, 0.89] |
| 1 lexical | TF-IDF template-stripped | 0.719 [0.62, 0.85] | 0.921 [0.82, 1.00] | 0.811 [0.72, 0.91] |
| 1 lexical | TF-IDF raw text (Li et al. 2017) | 0.719 [0.62, 0.85] | 0.904 [0.81, 0.99] | 0.808 [0.72, 0.91] |
| 4 embedding | BGE-base template-stripped | 0.719 [0.62, 0.86] | 0.895 [0.79, 0.97] | 0.798 [0.71, 0.90] |
| 5 existing bot | contrib-guard/phoenix (bot, exact port) | 0.711 [0.61, 0.85] | 0.904 [0.80, 1.00] | 0.806 [0.71, 0.92] |
| 4 embedding | BGE-small raw text | 0.711 [0.61, 0.88] | 0.904 [0.80, 0.98] | 0.794 [0.71, 0.91] |
| 4 embedding | MiniLM raw text | 0.702 [0.59, 0.82] | 0.886 [0.78, 0.96] | 0.787 [0.69, 0.88] |
| 4 embedding | MiniLM template-stripped | 0.693 [0.60, 0.83] | 0.868 [0.77, 0.95] | 0.774 [0.69, 0.88] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM re-rank top-10 | 0.675 [0.55, 0.83] | 0.921 [0.86, 0.99] | 0.790 [0.71, 0.90] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding + code | 0.675 [0.55, 0.84] | 0.904 [0.82, 1.00] | 0.775 [0.68, 0.90] |
| 5 existing bot | Simili-bot (bot, re-impl) | 0.675 [0.57, 0.82] | 0.877 [0.78, 0.95] | 0.766 [0.68, 0.87] |
| 5 existing bot | PRSense (bot, re-impl) | 0.667 [0.51, 0.86] | 0.798 [0.67, 0.95] | 0.734 [0.60, 0.90] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding | 0.649 [0.56, 0.79] | 0.851 [0.75, 0.97] | 0.751 [0.66, 0.87] |
| 1 lexical | BM25 template-stripped | 0.640 [0.54, 0.77] | 0.860 [0.75, 0.99] | 0.739 [0.64, 0.86] |
| 6 unsupervised hybrid | RRF hybrid: text + code + links + recency | 0.632 [0.45, 0.82] | 0.877 [0.79, 1.00] | 0.732 [0.61, 0.88] |
| 2 code | Code overlap sum (files+hunks+lines) | 0.588 [0.43, 0.78] | 0.754 [0.55, 0.92] | 0.672 [0.51, 0.84] |
| 1 lexical | BM25 raw text | 0.570 [0.47, 0.68] | 0.842 [0.73, 0.98] | 0.693 [0.60, 0.81] |
| 2 code | BM25 on diff | 0.570 [0.40, 0.81] | 0.719 [0.54, 0.93] | 0.643 [0.47, 0.88] |
| 4 embedding | UniXcoder template-stripped text | 0.561 [0.43, 0.76] | 0.728 [0.57, 0.91] | 0.641 [0.50, 0.82] |
| 2 code | Changed-files Jaccard | 0.544 [0.39, 0.72] | 0.702 [0.53, 0.87] | 0.620 [0.47, 0.79] |
| 4 embedding | Jina code embeddings v2 on diff | 0.526 [0.37, 0.80] | 0.640 [0.49, 0.89] | 0.590 [0.44, 0.85] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base re-rank top-10 | 0.518 [0.36, 0.67] | 0.860 [0.78, 0.93] | 0.655 [0.54, 0.77] |
| 2 code | Hunk overlap | 0.518 [0.37, 0.70] | 0.754 [0.57, 0.90] | 0.614 [0.47, 0.77] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-5 | 0.509 [0.40, 0.62] | 0.982 [0.96, 1.00] | 0.698 [0.64, 0.77] |
| 4 embedding | BGE-small on diff | 0.482 [0.33, 0.75] | 0.588 [0.43, 0.83] | 0.534 [0.38, 0.79] |
| 4 embedding | UniXcoder (code model) on diff | 0.482 [0.33, 0.75] | 0.579 [0.41, 0.87] | 0.528 [0.37, 0.80] |
| 2 code | Identical changed lines | 0.465 [0.35, 0.66] | 0.675 [0.53, 0.89] | 0.558 [0.45, 0.75] |
| 4 embedding | MiniLM on diff | 0.465 [0.32, 0.71] | 0.570 [0.42, 0.85] | 0.523 [0.38, 0.76] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-10 | 0.368 [0.24, 0.48] | 0.868 [0.81, 0.94] | 0.573 [0.49, 0.65] |
| 4 embedding | CodeBERT (mean-pooled) on diff | 0.342 [0.23, 0.55] | 0.439 [0.29, 0.71] | 0.398 [0.27, 0.63] |
| 0 trivial | Recency only (newest open PR first) | 0.193 [0.10, 0.35] | 0.360 [0.23, 0.57] | 0.288 [0.18, 0.46] |


**cross-author, no #ref in text** (n = 199)

| Family | Strategy | Recall@1 [95% CI] | Recall@5 [95% CI] | MRR [95% CI] |
|---|---|---|---|---|
| 7 supervised | All signals, LR | 0.864 [0.81, 0.91] | 0.965 [0.94, 0.99] | 0.905 [0.87, 0.94] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 0.864 [0.82, 0.91] | 0.960 [0.94, 0.99] | 0.904 [0.87, 0.94] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.864 [0.81, 0.91] | 0.965 [0.94, 0.99] | 0.904 [0.87, 0.93] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | 0.859 [0.81, 0.91] | 0.960 [0.94, 0.99] | 0.905 [0.87, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 0.859 [0.82, 0.91] | 0.960 [0.94, 0.99] | 0.901 [0.87, 0.94] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 0.854 [0.81, 0.90] | 0.970 [0.95, 0.99] | 0.903 [0.87, 0.94] |
| 7 supervised | Jinx + MiniLM, LR (current tool) | 0.854 [0.81, 0.90] | 0.960 [0.94, 0.99] | 0.901 [0.87, 0.93] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 0.854 [0.81, 0.90] | 0.960 [0.94, 0.99] | 0.899 [0.87, 0.93] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 0.849 [0.80, 0.90] | 0.960 [0.94, 0.99] | 0.898 [0.87, 0.93] |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker-base (stacked LR) | 0.849 [0.79, 0.89] | 0.965 [0.94, 0.99] | 0.898 [0.86, 0.93] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 0.849 [0.81, 0.90] | 0.960 [0.94, 0.99] | 0.897 [0.87, 0.93] |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 0.844 [0.80, 0.89] | 0.960 [0.94, 0.99] | 0.896 [0.87, 0.93] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 0.844 [0.80, 0.90] | 0.960 [0.94, 0.99] | 0.896 [0.87, 0.93] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 0.844 [0.80, 0.90] | 0.960 [0.94, 0.99] | 0.895 [0.87, 0.94] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 0.839 [0.80, 0.89] | 0.960 [0.94, 0.99] | 0.892 [0.86, 0.93] |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 0.839 [0.80, 0.89] | 0.960 [0.94, 0.99] | 0.892 [0.86, 0.93] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 0.834 [0.78, 0.88] | 0.960 [0.94, 0.99] | 0.892 [0.86, 0.93] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 0.834 [0.79, 0.89] | 0.960 [0.94, 0.99] | 0.890 [0.86, 0.93] |
| 7 supervised | Jinx lexical, LR | 0.834 [0.78, 0.88] | 0.960 [0.94, 0.99] | 0.888 [0.86, 0.92] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 0.834 [0.78, 0.89] | 0.960 [0.94, 0.99] | 0.888 [0.85, 0.93] |
| 7 supervised | All signals, gradient boosting | 0.829 [0.77, 0.90] | 0.945 [0.92, 0.98] | 0.881 [0.84, 0.93] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 0.824 [0.77, 0.88] | 0.960 [0.94, 0.99] | 0.884 [0.85, 0.92] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 0.819 [0.77, 0.88] | 0.965 [0.94, 0.99] | 0.882 [0.85, 0.92] |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 re-rank top-5 | 0.809 [0.75, 0.88] | 0.960 [0.94, 0.99] | 0.879 [0.84, 0.93] |
| 7 supervised | Jinx features, gradient boosting | 0.804 [0.75, 0.87] | 0.935 [0.89, 0.98] | 0.864 [0.82, 0.92] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-5 | 0.794 [0.74, 0.85] | 0.960 [0.94, 0.99] | 0.867 [0.83, 0.91] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-5 | 0.769 [0.71, 0.83] | 0.960 [0.94, 0.99] | 0.843 [0.80, 0.89] |
| 10 stacked cascade (ours) | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.759 [0.69, 0.83] | 0.930 [0.90, 0.97] | 0.830 [0.78, 0.88] |
| 4 embedding | BGE-base template-stripped | 0.754 [0.66, 0.83] | 0.884 [0.78, 0.95] | 0.814 [0.72, 0.88] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-10 | 0.744 [0.65, 0.81] | 0.950 [0.92, 0.98] | 0.834 [0.78, 0.88] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-10 | 0.744 [0.69, 0.80] | 0.915 [0.87, 0.95] | 0.816 [0.77, 0.86] |
| 4 embedding | BGE-small template-stripped | 0.734 [0.64, 0.81] | 0.884 [0.79, 0.95] | 0.802 [0.71, 0.87] |
| 4 embedding | BGE-small raw text | 0.729 [0.64, 0.81] | 0.894 [0.80, 0.96] | 0.797 [0.71, 0.87] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding + code | 0.724 [0.64, 0.81] | 0.899 [0.82, 0.97] | 0.803 [0.73, 0.87] |
| 3 links | Links only (same issue / #ref) | 0.724 [0.65, 0.81] | 0.869 [0.79, 0.94] | 0.797 [0.73, 0.87] |
| 7 supervised | INTRUDE + time (Wang et al. 2019), LR | 0.714 [0.63, 0.79] | 0.920 [0.87, 0.96] | 0.803 [0.74, 0.86] |
| 5 existing bot | contrib-guard/phoenix (bot, exact port) | 0.714 [0.63, 0.80] | 0.874 [0.80, 0.94] | 0.788 [0.71, 0.86] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 0.709 [0.62, 0.78] | 0.945 [0.92, 0.98] | 0.817 [0.77, 0.86] |
| 4 embedding | MiniLM template-stripped | 0.709 [0.63, 0.79] | 0.869 [0.78, 0.93] | 0.783 [0.70, 0.85] |
| 4 embedding | MiniLM raw text | 0.709 [0.62, 0.78] | 0.879 [0.79, 0.94] | 0.783 [0.70, 0.85] |
| 5 existing bot | Simili-bot (bot, re-impl) | 0.709 [0.62, 0.78] | 0.859 [0.77, 0.92] | 0.782 [0.70, 0.84] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-5 | 0.704 [0.63, 0.77] | 0.960 [0.94, 0.99] | 0.802 [0.75, 0.85] |
| 6 unsupervised hybrid | RRF hybrid: text + code + links + recency | 0.704 [0.62, 0.78] | 0.894 [0.84, 0.96] | 0.789 [0.72, 0.86] |
| 1 lexical | BM25 template-stripped | 0.698 [0.62, 0.78] | 0.864 [0.80, 0.94] | 0.771 [0.70, 0.85] |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM re-rank top-10 | 0.693 [0.62, 0.77] | 0.940 [0.91, 0.97] | 0.803 [0.76, 0.85] |
| 5 existing bot | PRSense (bot, re-impl) | 0.693 [0.62, 0.79] | 0.854 [0.77, 0.93] | 0.769 [0.69, 0.85] |
| 1 lexical | TF-IDF template-stripped | 0.688 [0.61, 0.78] | 0.894 [0.84, 0.95] | 0.776 [0.70, 0.85] |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding | 0.688 [0.61, 0.77] | 0.859 [0.78, 0.94] | 0.771 [0.70, 0.85] |
| 1 lexical | TF-IDF raw text (Li et al. 2017) | 0.683 [0.60, 0.77] | 0.879 [0.81, 0.94] | 0.772 [0.70, 0.84] |
| 1 lexical | BM25 raw text | 0.658 [0.58, 0.74] | 0.844 [0.78, 0.92] | 0.744 [0.68, 0.81] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-10 | 0.643 [0.57, 0.72] | 0.869 [0.81, 0.92] | 0.745 [0.69, 0.80] |
| 4 embedding | UniXcoder template-stripped text | 0.608 [0.52, 0.72] | 0.774 [0.69, 0.89] | 0.686 [0.61, 0.79] |
| 2 code | BM25 on diff | 0.533 [0.46, 0.63] | 0.779 [0.70, 0.86] | 0.650 [0.58, 0.73] |
| 2 code | Code overlap sum (files+hunks+lines) | 0.533 [0.46, 0.62] | 0.789 [0.74, 0.85] | 0.644 [0.59, 0.71] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-5 | 0.518 [0.44, 0.63] | 0.960 [0.94, 0.99] | 0.707 [0.66, 0.78] |
| 2 code | Changed-files Jaccard | 0.482 [0.41, 0.58] | 0.729 [0.67, 0.80] | 0.600 [0.54, 0.68] |
| 2 code | Hunk overlap | 0.482 [0.41, 0.58] | 0.749 [0.69, 0.84] | 0.593 [0.54, 0.67] |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base re-rank top-10 | 0.467 [0.40, 0.54] | 0.839 [0.79, 0.88] | 0.614 [0.56, 0.67] |
| 4 embedding | Jina code embeddings v2 on diff | 0.467 [0.38, 0.60] | 0.673 [0.60, 0.78] | 0.571 [0.49, 0.69] |
| 4 embedding | BGE-small on diff | 0.457 [0.38, 0.58] | 0.683 [0.60, 0.80] | 0.564 [0.49, 0.68] |
| 4 embedding | UniXcoder (code model) on diff | 0.432 [0.34, 0.56] | 0.623 [0.52, 0.77] | 0.525 [0.43, 0.65] |
| 4 embedding | MiniLM on diff | 0.412 [0.34, 0.51] | 0.628 [0.54, 0.76] | 0.515 [0.45, 0.62] |
| 2 code | Identical changed lines | 0.397 [0.32, 0.51] | 0.653 [0.57, 0.78] | 0.505 [0.44, 0.61] |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-10 | 0.352 [0.28, 0.45] | 0.869 [0.82, 0.92] | 0.573 [0.52, 0.65] |
| 4 embedding | CodeBERT (mean-pooled) on diff | 0.286 [0.21, 0.40] | 0.427 [0.31, 0.59] | 0.358 [0.26, 0.49] |
| 0 trivial | Recency only (newest open PR first) | 0.231 [0.14, 0.37] | 0.477 [0.32, 0.66] | 0.352 [0.24, 0.50] |


**Best Recall@1 of each strategy family, per duplicate class**

| Duplicate class | n | trivial | lexical | stacked cascade (ours) | code | links | embedding | existing bot | unsupervised hybrid | supervised | re-ranker on top-k | LLM judge on top-k | best overall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| same issue, different code (classes C/D, shares linked issue) | 35 | 0.31 | 0.86 | 0.91 | 0.29 | 0.94 | 0.86 | 0.83 | 0.74 | 0.91 | 0.94 | 0.91 | Links only (same issue / #ref) (0.94) |
| same code, different description (code twin, text TF-IDF < 0.3) | 287 | 0.39 | 0.47 | 0.80 | 0.72 | 0.57 | 0.56 | 0.59 | 0.59 | 0.86 | 0.74 | 0.79 | Jinx lexical, LR (0.86) |
| cross-author, same code, different description | 34 | 0.26 | 0.62 | 0.97 | 0.91 | 0.76 | 0.74 | 0.82 | 0.76 | 0.94 | 0.94 | 0.97 | LLM judge Qwen2.5-14B + Jinx (avg) top-5 (0.97) |
| class A. code twin (>=50% identical changed lines) | 994 | 0.41 | 0.79 | 0.91 | 0.81 | 0.82 | 0.77 | 0.80 | 0.84 | 0.95 | 0.88 | 0.91 | Jinx lexical, LR (0.95) |
| cross-author, class A. code twin (>=50% identical changed lines) | 139 | 0.21 | 0.86 | 0.97 | 0.78 | 0.92 | 0.84 | 0.89 | 0.89 | 0.98 | 0.93 | 0.98 | LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 (0.98) |
| class B. partial code overlap | 701 | 0.29 | 0.76 | 0.87 | 0.58 | 0.80 | 0.78 | 0.77 | 0.76 | 0.88 | 0.86 | 0.86 | All signals, LR (0.88) |
| cross-author, class B. partial code overlap | 164 | 0.20 | 0.70 | 0.89 | 0.52 | 0.80 | 0.76 | 0.72 | 0.76 | 0.91 | 0.87 | 0.88 | All signals, LR (0.91) |
| class C. same files, different code | 44 | 0.45 | 0.73 | 0.86 | 0.43 | 0.68 | 0.68 | 0.68 | 0.70 | 0.89 | 0.86 | 0.86 | Jinx lexical, LR (0.89) |
| cross-author, class C. same files, different code | 10 | 0.10 | 0.60 | 0.80 | 0.30 | 0.60 | 0.50 | 0.50 | 0.60 | 0.70 | 0.80 | 0.80 | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 (0.80) |
| class D. no shared files (intent-level) | 128 | 0.30 | 0.81 | 0.81 | 0.31 | 0.75 | 0.73 | 0.77 | 0.69 | 0.76 | 0.79 | 0.81 | TF-IDF template-stripped (0.81) |
| cross-author, class D. no shared files (intent-level) | 29 | 0.10 | 0.69 | 0.76 | 0.28 | 0.76 | 0.66 | 0.66 | 0.66 | 0.69 | 0.66 | 0.72 | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 (0.76) |


**Paired difference vs `Jinx + MiniLM, LR (current tool)`, cross-author (points; CI excludes 0 = significant)**

| Strategy | ΔRecall@1 | ΔRecall@5 | ΔMRR |
|---|---|---|---|
| All signals, LR | +0.6 [-1.2, +2.5] | +0.3 [-0.8, +1.1] | +0.2 [-0.9, +1.4] |
| Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | +0.0 [-2.2, +1.8] | +0.3 [+0.0, +1.0] | -0.1 [-1.3, +0.9] |
| LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | -0.3 [-2.3, +2.4] | +0.0 [+0.0, +0.0] | -0.0 [-1.1, +1.4] |
| Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | -0.3 [-2.4, +2.1] | +0.0 [+0.0, +0.0] | -0.2 [-1.3, +1.0] |
| Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | -0.6 [-2.3, +1.3] | +0.0 [+0.0, +0.0] | -0.4 [-1.3, +0.5] |
| Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | -0.6 [-3.0, +2.2] | +0.0 [+0.0, +0.0] | -0.3 [-1.5, +1.1] |
| LLM judge Qwen2.5-7B + Jinx (avg) top-5 | -0.9 [-2.5, +1.2] | +0.0 [+0.0, +0.0] | -0.6 [-1.4, +0.5] |
| LLM judge Qwen2.5-7B + Jinx (avg) top-10 | -1.2 [-2.9, +0.8] | +0.0 [+0.0, +0.0] | -0.7 [-1.6, +0.3] |
| Jinx lexical, LR | -1.2 [-3.2, +1.0] | +0.0 [-0.8, +0.9] | -0.7 [-1.9, +0.5] |
| Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | -1.5 [-3.4, +0.9] | +0.0 [+0.0, +0.0] | -0.7 [-1.7, +0.5] |
| Cascade: Jinx + BGE-reranker-base (stacked LR) | -1.8 [-4.3, +0.4] | +0.3 [+0.0, +1.0] | -1.0 [-2.3, +0.2] |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | -2.0 [-3.9, +0.5] | +0.0 [+0.0, +0.0] | -1.0 [-2.0, +0.3] |
| All signals, gradient boosting | -2.3 [-5.5, +1.2] | -1.2 [-2.6, +0.4] | -1.7 [-4.0, +0.6] |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | -2.6 [-4.9, +0.0] | +0.0 [+0.0, +0.0] | -1.5 [-2.7, -0.0] |
| Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | -2.6 [-5.3, +0.4] | +0.0 [+0.0, +0.0] | -1.4 [-2.7, +0.2] |
| LLM judge Qwen2.5-14B + Jinx (avg) top-5 | -2.9 [-5.6, +0.4] | +0.0 [+0.0, +0.0] | -1.5 [-2.9, +0.2] |
| Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | -2.9 [-5.5, -0.3] | +0.0 [-0.8, +0.9] | -1.5 [-2.8, -0.0] |
| Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | -2.9 [-5.5, +0.7] | +0.0 [+0.0, +0.0] | -1.7 [-3.2, +0.4] |
| Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | -3.2 [-8.4, +1.4] | -0.6 [-3.1, +1.4] | -2.0 [-5.7, +0.9] |
| LLM judge Qwen2.5-14B + Jinx (avg) top-10 | -3.2 [-6.0, +0.4] | +0.0 [+0.0, +0.0] | -1.7 [-3.1, +0.2] |
| Jinx features, gradient boosting | -3.5 [-6.8, +0.0] | -1.5 [-4.3, +0.4] | -2.5 [-5.0, +0.2] |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | -4.7 [-7.2, -1.1] | +0.0 [+0.0, +0.0] | -2.7 [-4.2, -0.6] |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | -5.0 [-7.6, -1.3] | -0.3 [-1.5, +0.9] | -2.8 [-4.4, -0.7] |
| LLM judge Claude Haiku 4.5 re-rank top-5 | -5.8 [-9.0, -1.2] | +0.0 [+0.0, +0.0] | -3.0 [-4.8, -0.4] |
| Links only (same issue / #ref) | -6.1 [-10.9, -0.4] | -4.7 [-9.0, -0.7] | -5.0 [-9.2, -0.5] |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | -6.1 [-8.8, -3.1] | +0.0 [+0.0, +0.0] | -3.3 [-4.8, -1.6] |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | -8.5 [-13.7, -3.7] | -1.8 [-3.5, -0.4] | -5.6 [-8.9, -2.6] |
| INTRUDE + time (Wang et al. 2019), LR | -9.1 [-13.1, -5.0] | -1.8 [-5.2, +0.9] | -5.9 [-9.3, -2.7] |
| LLM judge Qwen2.5-7B re-rank top-5 | -9.1 [-13.1, -4.9] | +0.0 [+0.0, +0.0] | -5.6 [-8.1, -3.2] |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | -9.6 [-14.8, -5.2] | -0.6 [-1.8, +0.5] | -5.5 [-8.4, -2.9] |
| LLM judge Qwen2.5-7B re-rank top-10 | -10.8 [-14.7, -6.7] | -2.9 [-5.9, -1.0] | -7.4 [-10.3, -4.9] |
| contrib-guard/phoenix (bot, exact port) | -12.3 [-17.0, -6.8] | -5.3 [-9.7, -1.2] | -9.0 [-13.4, -4.8] |
| BGE-small template-stripped | -13.7 [-19.0, -8.3] | -5.6 [-11.2, -1.2] | -10.2 [-14.9, -6.0] |
| BGE-base template-stripped | -14.0 [-19.7, -8.4] | -6.1 [-12.2, -1.5] | -10.4 [-15.5, -6.0] |
| TF-IDF template-stripped | -14.0 [-19.0, -8.2] | -4.1 [-7.7, -0.7] | -9.8 [-14.0, -5.4] |
| TF-IDF raw text (Li et al. 2017) | -14.3 [-19.2, -8.5] | -5.0 [-8.8, -1.3] | -10.0 [-14.3, -5.7] |
| RRF hybrid: BM25 + embedding + code | -14.3 [-20.7, -7.8] | -5.0 [-9.8, -0.9] | -10.2 [-15.5, -5.2] |
| BGE-small raw text | -14.9 [-20.2, -9.0] | -5.0 [-10.5, -0.7] | -10.9 [-15.3, -6.5] |
| LLM judge Qwen2.5-14B re-rank top-5 | -14.9 [-18.7, -11.1] | +0.0 [+0.0, +0.0] | -9.3 [-11.8, -7.0] |
| MiniLM template-stripped | -14.9 [-20.5, -8.5] | -7.3 [-12.7, -3.2] | -11.2 [-16.0, -6.7] |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | -15.2 [-19.9, -10.5] | -1.8 [-3.4, -0.3] | -9.1 [-11.8, -6.3] |
| BM25 template-stripped | -16.4 [-21.6, -11.2] | -6.1 [-10.6, -1.7] | -11.8 [-16.3, -7.3] |
| RRF hybrid: BM25 + embedding | -16.7 [-21.4, -11.2] | -6.1 [-10.9, -1.4] | -11.6 [-15.8, -7.0] |
| Simili-bot (bot, re-impl) | -17.5 [-23.2, -11.2] | -7.9 [-13.4, -3.6] | -12.8 [-17.9, -8.2] |
| MiniLM raw text | -17.5 [-22.9, -11.6] | -6.4 [-12.2, -2.1] | -12.6 [-17.5, -8.2] |
| RRF hybrid: text + code + links + recency | -18.7 [-28.2, -9.7] | -5.3 [-8.8, -1.3] | -13.1 [-19.9, -6.4] |
| PRSense (bot, re-impl) | -19.0 [-27.8, -10.1] | -10.5 [-17.9, -3.9] | -14.8 [-22.8, -7.4] |
| BM25 raw text | -19.0 [-24.5, -13.6] | -7.3 [-12.0, -2.5] | -13.6 [-17.9, -9.1] |
| LLM judge Qwen2.5-14B re-rank top-10 | -19.3 [-23.6, -14.8] | -6.4 [-10.5, -3.4] | -13.4 [-16.6, -10.4] |
| Cross-encoder ms-marco MiniLM re-rank top-10 | -19.3 [-25.9, -12.5] | -3.2 [-6.9, -0.3] | -12.3 [-16.9, -7.8] |
| UniXcoder template-stripped text | -26.3 [-33.5, -17.7] | -15.5 [-22.1, -7.8] | -21.3 [-27.7, -13.7] |
| BM25 on diff | -31.6 [-40.2, -22.3] | -19.0 [-29.5, -9.6] | -25.5 [-34.6, -16.5] |
| Code overlap sum (files+hunks+lines) | -32.5 [-39.9, -24.3] | -17.5 [-26.6, -9.9] | -25.9 [-33.4, -18.9] |
| LLM judge Qwen2.5-1.5B re-rank top-5 | -33.3 [-39.4, -26.6] | +0.0 [+0.0, +0.0] | -20.0 [-23.2, -16.0] |
| Jina code embeddings v2 on diff | -38.0 [-47.2, -25.9] | -27.5 [-37.2, -16.6] | -32.4 [-41.4, -21.2] |
| BGE-small on diff | -38.6 [-47.6, -27.2] | -27.5 [-37.5, -15.8] | -33.2 [-42.1, -22.3] |
| Changed-files Jaccard | -38.9 [-45.8, -30.9] | -23.7 [-32.3, -15.4] | -31.5 [-38.6, -24.1] |
| Hunk overlap | -38.9 [-46.9, -29.6] | -21.1 [-28.9, -13.1] | -31.6 [-39.3, -23.6] |
| Cross-encoder BGE-reranker-base re-rank top-10 | -39.8 [-47.5, -31.7] | -9.6 [-13.8, -6.5] | -28.1 [-33.4, -22.5] |
| Identical changed lines | -42.1 [-48.6, -33.8] | -26.3 [-33.4, -16.9] | -35.5 [-41.5, -27.5] |
| MiniLM on diff | -42.4 [-50.7, -31.9] | -30.7 [-41.2, -17.4] | -36.7 [-45.4, -25.9] |
| UniXcoder (code model) on diff | -42.4 [-51.4, -30.6] | -33.0 [-43.8, -19.4] | -37.4 [-47.0, -25.1] |
| LLM judge Qwen2.5-1.5B re-rank top-10 | -45.9 [-52.1, -38.8] | -10.2 [-13.5, -6.7] | -30.9 [-34.7, -26.4] |
| CodeBERT (mean-pooled) on diff | -52.0 [-60.9, -41.0] | -45.9 [-57.1, -32.0] | -48.5 [-58.2, -36.5] |
| Recency only (newest open PR first) | -70.8 [-77.3, -61.9] | -52.0 [-63.9, -36.8] | -61.7 [-69.9, -51.1] |


**Paired difference vs `INTRUDE + time (Wang et al. 2019), LR`, cross-author (points; CI excludes 0 = significant)**

| Strategy | ΔRecall@1 | ΔRecall@5 | ΔMRR |
|---|---|---|---|
| All signals, LR | +9.6 [+5.6, +13.4] | +2.0 [-0.8, +5.3] | +6.2 [+2.9, +9.1] |
| Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | +9.1 [+4.3, +13.1] | +2.0 [-0.6, +5.4] | +5.8 [+2.3, +9.1] |
| Jinx + MiniLM, LR (current tool) | +9.1 [+5.0, +13.1] | +1.8 [-0.9, +5.2] | +5.9 [+2.7, +9.3] |
| Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | +8.8 [+4.8, +12.8] | +1.8 [-0.9, +5.2] | +5.7 [+2.6, +8.8] |
| LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | +8.8 [+5.2, +13.2] | +1.8 [-0.9, +5.2] | +5.9 [+3.0, +9.5] |
| Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | +8.5 [+4.3, +12.8] | +1.8 [-0.9, +5.2] | +5.7 [+2.6, +8.9] |
| Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | +8.5 [+4.3, +12.6] | +1.8 [-0.9, +5.2] | +5.5 [+2.2, +8.8] |
| LLM judge Qwen2.5-7B + Jinx (avg) top-5 | +8.2 [+4.2, +12.4] | +1.8 [-0.9, +5.2] | +5.4 [+2.2, +8.8] |
| Jinx lexical, LR | +7.9 [+3.7, +12.7] | +1.8 [-0.8, +5.0] | +5.2 [+1.9, +9.1] |
| LLM judge Qwen2.5-7B + Jinx (avg) top-10 | +7.9 [+3.8, +12.0] | +1.8 [-0.9, +5.2] | +5.2 [+2.0, +8.6] |
| Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | +7.6 [+4.1, +11.2] | +1.8 [-0.9, +5.2] | +5.2 [+2.3, +8.3] |
| Cascade: Jinx + BGE-reranker-base (stacked LR) | +7.3 [+2.3, +11.4] | +2.0 [-0.6, +5.4] | +5.0 [+1.5, +8.1] |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | +7.0 [+3.6, +10.7] | +1.8 [-0.9, +5.2] | +4.9 [+2.0, +8.1] |
| All signals, gradient boosting | +6.7 [+3.2, +10.8] | +0.6 [-1.6, +3.2] | +4.2 [+1.6, +7.0] |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | +6.4 [+3.0, +9.9] | +1.8 [-0.9, +5.2] | +4.5 [+1.7, +7.3] |
| Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | +6.4 [+2.2, +11.2] | +1.8 [-0.9, +5.2] | +4.6 [+1.3, +8.2] |
| LLM judge Qwen2.5-14B + Jinx (avg) top-5 | +6.1 [+1.9, +11.0] | +1.8 [-0.9, +5.2] | +4.4 [+1.1, +8.2] |
| Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | +6.1 [+1.6, +10.5] | +1.8 [-0.7, +4.9] | +4.5 [+1.2, +7.7] |
| Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | +6.1 [+2.3, +10.7] | +1.8 [-0.9, +5.2] | +4.3 [+1.2, +7.8] |
| LLM judge Qwen2.5-14B + Jinx (avg) top-10 | +5.8 [+1.7, +10.8] | +1.8 [-0.9, +5.2] | +4.3 [+1.0, +8.1] |
| Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | +5.8 [+0.0, +11.2] | +1.2 [-2.5, +5.3] | +3.9 [-0.8, +8.2] |
| Jinx features, gradient boosting | +5.6 [+1.9, +9.6] | +0.3 [-1.6, +2.5] | +3.5 [+1.0, +6.2] |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | +4.4 [+0.6, +9.0] | +1.8 [-0.9, +5.2] | +3.3 [+0.3, +6.8] |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | +4.1 [+0.5, +8.2] | +1.5 [-1.6, +5.1] | +3.2 [+0.2, +6.5] |
| LLM judge Claude Haiku 4.5 re-rank top-5 | +3.2 [-0.4, +8.3] | +1.8 [-0.9, +5.2] | +3.0 [+0.1, +6.7] |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | +2.9 [-0.9, +7.0] | +1.8 [-0.9, +5.2] | +2.6 [-0.4, +6.0] |
| Links only (same issue / #ref) | +2.9 [-1.1, +7.8] | -2.9 [-5.8, +0.7] | +0.9 [-1.9, +4.2] |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | +0.6 [-4.1, +4.8] | +0.0 [-3.2, +3.6] | +0.3 [-2.9, +2.9] |
| LLM judge Qwen2.5-7B re-rank top-5 | +0.0 [-4.9, +5.0] | +1.8 [-0.9, +5.2] | +0.4 [-3.3, +4.1] |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | -0.6 [-4.8, +2.9] | +1.2 [-1.6, +4.4] | +0.5 [-2.0, +2.6] |
| LLM judge Qwen2.5-7B re-rank top-10 | -1.8 [-6.1, +2.4] | -1.2 [-4.4, +2.0] | -1.5 [-5.0, +1.4] |
| contrib-guard/phoenix (bot, exact port) | -3.2 [-7.0, +1.1] | -3.5 [-6.5, -0.5] | -3.0 [-5.9, +0.0] |
| BGE-small template-stripped | -4.7 [-9.5, +0.4] | -3.8 [-7.2, -0.8] | -4.3 [-8.2, -0.6] |
| BGE-base template-stripped | -5.0 [-9.8, +0.0] | -4.4 [-8.0, -1.3] | -4.4 [-8.2, -0.8] |
| TF-IDF template-stripped | -5.0 [-8.6, -1.0] | -2.3 [-4.5, +0.0] | -3.8 [-6.5, -1.0] |
| TF-IDF raw text (Li et al. 2017) | -5.3 [-8.9, -1.3] | -3.2 [-5.8, -0.6] | -4.1 [-6.8, -1.3] |
| RRF hybrid: BM25 + embedding + code | -5.3 [-11.4, +0.6] | -3.2 [-6.2, +0.3] | -4.2 [-9.0, +0.1] |
| BGE-small raw text | -5.8 [-10.6, -0.5] | -3.2 [-6.9, +0.0] | -5.0 [-8.7, -1.2] |
| LLM judge Qwen2.5-14B re-rank top-5 | -5.8 [-10.6, -1.1] | +1.8 [-0.9, +5.2] | -3.3 [-7.0, +0.4] |
| MiniLM template-stripped | -5.8 [-10.0, -0.6] | -5.6 [-8.7, -3.0] | -5.3 [-8.7, -1.8] |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | -6.1 [-10.9, -1.8] | +0.0 [-3.0, +3.8] | -3.1 [-6.6, -0.0] |
| BM25 template-stripped | -7.3 [-11.9, -2.6] | -4.4 [-7.7, -0.3] | -5.8 [-9.3, -2.1] |
| RRF hybrid: BM25 + embedding | -7.6 [-11.9, -2.8] | -4.4 [-7.6, -0.5] | -5.7 [-8.9, -2.1] |
| Simili-bot (bot, re-impl) | -8.5 [-13.2, -3.1] | -6.1 [-9.3, -3.4] | -6.9 [-10.6, -3.3] |
| MiniLM raw text | -8.5 [-12.5, -4.0] | -4.7 [-8.4, -1.8] | -6.6 [-10.0, -3.5] |
| RRF hybrid: text + code + links + recency | -9.6 [-18.6, -1.6] | -3.5 [-6.6, +0.4] | -7.1 [-13.7, -1.3] |
| PRSense (bot, re-impl) | -9.9 [-18.2, -2.0] | -8.8 [-15.3, -3.3] | -8.9 [-16.6, -2.5] |
| BM25 raw text | -9.9 [-14.8, -5.1] | -5.6 [-9.4, -1.1] | -7.6 [-11.2, -3.8] |
| LLM judge Qwen2.5-14B re-rank top-10 | -10.2 [-14.2, -6.8] | -4.7 [-8.6, -0.6] | -7.5 [-10.8, -4.8] |
| Cross-encoder ms-marco MiniLM re-rank top-10 | -10.2 [-16.9, -3.9] | -1.5 [-6.0, +2.8] | -6.3 [-11.6, -1.5] |
| UniXcoder template-stripped text | -17.3 [-23.8, -9.5] | -13.7 [-20.0, -6.6] | -15.3 [-21.2, -8.4] |
| BM25 on diff | -22.5 [-31.0, -13.6] | -17.3 [-27.5, -8.5] | -19.5 [-28.3, -11.2] |
| Code overlap sum (files+hunks+lines) | -23.4 [-30.9, -16.3] | -15.8 [-25.1, -7.7] | -20.0 [-27.8, -13.5] |
| LLM judge Qwen2.5-1.5B re-rank top-5 | -24.3 [-31.2, -16.8] | +1.8 [-0.9, +5.2] | -14.0 [-18.3, -9.0] |
| Jina code embeddings v2 on diff | -28.9 [-38.1, -17.9] | -25.7 [-35.5, -15.3] | -26.4 [-35.6, -16.3] |
| BGE-small on diff | -29.5 [-38.5, -19.1] | -25.7 [-36.1, -14.1] | -27.2 [-36.3, -17.2] |
| Changed-files Jaccard | -29.8 [-36.5, -22.8] | -21.9 [-31.1, -13.9] | -25.6 [-32.7, -19.0] |
| Hunk overlap | -29.8 [-37.9, -21.4] | -19.3 [-27.5, -10.8] | -25.7 [-33.4, -18.0] |
| Cross-encoder BGE-reranker-base re-rank top-10 | -30.7 [-39.4, -22.6] | -7.9 [-12.9, -3.4] | -22.1 [-28.4, -16.4] |
| Identical changed lines | -33.0 [-38.8, -25.8] | -24.6 [-32.2, -15.1] | -29.5 [-35.2, -22.2] |
| MiniLM on diff | -33.3 [-41.4, -24.1] | -28.9 [-39.7, -16.1] | -30.8 [-39.2, -21.0] |
| UniXcoder (code model) on diff | -33.3 [-42.4, -22.3] | -31.3 [-42.6, -17.7] | -31.5 [-41.1, -19.9] |
| LLM judge Qwen2.5-1.5B re-rank top-10 | -36.8 [-43.0, -30.6] | -8.5 [-12.4, -3.6] | -24.9 [-28.9, -20.7] |
| CodeBERT (mean-pooled) on diff | -43.0 [-51.6, -33.0] | -44.2 [-55.9, -30.0] | -42.5 [-52.3, -31.1] |
| Recency only (newest open PR first) | -61.7 [-68.7, -52.0] | -50.3 [-63.0, -34.0] | -55.7 [-64.5, -44.3] |


**Paired difference vs `contrib-guard/phoenix (bot, exact port)`, cross-author (points; CI excludes 0 = significant)**

| Strategy | ΔRecall@1 | ΔRecall@5 | ΔMRR |
|---|---|---|---|
| All signals, LR | +12.9 [+7.5, +17.3] | +5.6 [+1.2, +10.0] | +9.2 [+5.1, +13.1] |
| Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | +12.3 [+5.8, +17.6] | +5.6 [+1.5, +10.0] | +8.8 [+4.2, +13.3] |
| Jinx + MiniLM, LR (current tool) | +12.3 [+6.8, +17.0] | +5.3 [+1.2, +9.7] | +9.0 [+4.8, +13.4] |
| Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | +12.0 [+6.6, +17.0] | +5.3 [+1.2, +9.7] | +8.7 [+4.7, +13.0] |
| LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | +12.0 [+6.7, +17.3] | +5.3 [+1.2, +9.7] | +8.9 [+5.0, +13.7] |
| Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | +11.7 [+6.5, +16.7] | +5.3 [+1.2, +9.7] | +8.7 [+4.8, +13.0] |
| Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | +11.7 [+6.3, +16.5] | +5.3 [+1.2, +9.7] | +8.5 [+4.2, +13.1] |
| LLM judge Qwen2.5-7B + Jinx (avg) top-5 | +11.4 [+6.2, +16.2] | +5.3 [+1.2, +9.7] | +8.4 [+4.2, +13.0] |
| Jinx lexical, LR | +11.1 [+5.4, +16.7] | +5.3 [+1.2, +9.7] | +8.2 [+3.9, +13.2] |
| LLM judge Qwen2.5-7B + Jinx (avg) top-10 | +11.1 [+5.9, +15.9] | +5.3 [+1.2, +9.7] | +8.3 [+4.1, +12.7] |
| Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | +10.8 [+6.0, +15.2] | +5.3 [+1.2, +9.7] | +8.2 [+4.3, +12.5] |
| Cascade: Jinx + BGE-reranker-base (stacked LR) | +10.5 [+4.3, +15.8] | +5.6 [+1.5, +10.0] | +8.0 [+3.5, +12.2] |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | +10.2 [+5.5, +14.8] | +5.3 [+1.2, +9.7] | +7.9 [+4.1, +12.3] |
| All signals, gradient boosting | +9.9 [+6.0, +13.8] | +4.1 [+0.6, +8.0] | +7.3 [+4.2, +10.4] |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | +9.6 [+4.9, +13.9] | +5.3 [+1.2, +9.7] | +7.5 [+3.8, +11.5] |
| Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | +9.6 [+4.9, +14.8] | +5.3 [+1.2, +9.7] | +7.6 [+3.5, +12.5] |
| LLM judge Qwen2.5-14B + Jinx (avg) top-5 | +9.4 [+4.8, +14.5] | +5.3 [+1.2, +9.7] | +7.4 [+3.5, +12.4] |
| Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | +9.4 [+3.6, +14.8] | +5.3 [+1.2, +9.8] | +7.5 [+3.3, +11.8] |
| Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | +9.4 [+5.2, +13.8] | +5.3 [+1.2, +9.7] | +7.3 [+3.6, +11.9] |
| LLM judge Qwen2.5-14B + Jinx (avg) top-10 | +9.1 [+4.6, +14.2] | +5.3 [+1.2, +9.7] | +7.3 [+3.4, +12.3] |
| Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | +9.1 [+3.3, +14.5] | +4.7 [-0.3, +10.0] | +6.9 [+1.9, +12.1] |
| Jinx features, gradient boosting | +8.8 [+4.7, +12.6] | +3.8 [+0.8, +6.9] | +6.5 [+3.7, +9.5] |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | +7.6 [+3.3, +12.6] | +5.3 [+1.2, +9.7] | +6.3 [+2.6, +11.1] |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | +7.3 [+3.3, +11.8] | +5.0 [+0.6, +9.7] | +6.2 [+2.6, +10.6] |
| LLM judge Claude Haiku 4.5 re-rank top-5 | +6.4 [+1.6, +12.2] | +5.3 [+1.2, +9.7] | +6.0 [+2.3, +10.9] |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | +6.1 [+0.7, +11.1] | +5.3 [+1.2, +9.7] | +5.7 [+1.6, +10.1] |
| Links only (same issue / #ref) | +6.1 [+1.9, +11.3] | +0.6 [-0.7, +2.3] | +3.9 [+1.5, +6.8] |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | +3.8 [-1.9, +8.9] | +3.5 [-0.4, +8.0] | +3.3 [-0.2, +6.4] |
| INTRUDE + time (Wang et al. 2019), LR | +3.2 [-1.1, +7.0] | +3.5 [+0.5, +6.5] | +3.0 [-0.0, +5.9] |
| LLM judge Qwen2.5-7B re-rank top-5 | +3.2 [-3.3, +9.5] | +5.3 [+1.2, +9.7] | +3.4 [-1.5, +8.6] |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | +2.6 [-2.3, +6.7] | +4.7 [+0.4, +9.4] | +3.5 [+0.0, +6.5] |
| LLM judge Qwen2.5-7B re-rank top-10 | +1.5 [-4.5, +6.7] | +2.3 [-2.7, +7.2] | +1.5 [-3.2, +6.0] |
| BGE-small template-stripped | -1.5 [-5.6, +2.1] | -0.3 [-3.8, +2.9] | -1.3 [-4.6, +1.6] |
| BGE-base template-stripped | -1.8 [-5.9, +1.6] | -0.9 [-4.9, +2.7] | -1.4 [-4.3, +1.1] |
| TF-IDF template-stripped | -1.8 [-5.1, +1.8] | +1.2 [-0.3, +3.1] | -0.8 [-2.8, +1.2] |
| TF-IDF raw text (Li et al. 2017) | -2.0 [-5.6, +1.5] | +0.3 [-1.1, +1.7] | -1.1 [-3.1, +0.9] |
| RRF hybrid: BM25 + embedding + code | -2.0 [-7.6, +2.7] | +0.3 [-3.1, +3.8] | -1.2 [-5.5, +2.5] |
| BGE-small raw text | -2.6 [-6.5, +0.8] | +0.3 [-3.4, +3.6] | -1.9 [-4.7, +0.5] |
| LLM judge Qwen2.5-14B re-rank top-5 | -2.6 [-9.0, +3.0] | +5.3 [+1.2, +9.7] | -0.3 [-5.3, +4.7] |
| MiniLM template-stripped | -2.6 [-5.5, +0.6] | -2.0 [-5.5, +0.8] | -2.3 [-4.5, +0.0] |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | -2.9 [-8.7, +1.5] | +3.5 [-0.5, +8.4] | -0.1 [-4.4, +3.8] |
| BM25 template-stripped | -4.1 [-8.6, -0.5] | -0.9 [-3.1, +1.6] | -2.8 [-5.4, -0.4] |
| RRF hybrid: BM25 + embedding | -4.4 [-7.7, -1.5] | -0.9 [-2.8, +1.7] | -2.7 [-4.4, -0.8] |
| Simili-bot (bot, re-impl) | -5.3 [-8.7, -2.0] | -2.6 [-5.9, +0.3] | -3.9 [-6.5, -1.5] |
| MiniLM raw text | -5.3 [-8.3, -2.4] | -1.2 [-4.4, +1.6] | -3.6 [-5.9, -1.5] |
| RRF hybrid: text + code + links + recency | -6.4 [-15.1, +1.0] | +0.0 [-3.8, +4.5] | -4.1 [-10.6, +1.5] |
| PRSense (bot, re-impl) | -6.7 [-14.2, +0.4] | -5.3 [-12.7, +1.2] | -5.9 [-13.2, +0.4] |
| BM25 raw text | -6.7 [-12.2, -2.7] | -2.0 [-4.6, +0.7] | -4.6 [-7.8, -1.9] |
| LLM judge Qwen2.5-14B re-rank top-10 | -7.0 [-12.6, -2.5] | -1.2 [-6.6, +4.2] | -4.5 [-8.9, -0.7] |
| Cross-encoder ms-marco MiniLM re-rank top-10 | -7.0 [-13.1, -1.5] | +2.0 [-3.5, +7.4] | -3.3 [-8.6, +1.5] |
| UniXcoder template-stripped text | -14.0 [-19.1, -8.5] | -10.2 [-15.7, -4.1] | -12.3 [-17.1, -7.1] |
| BM25 on diff | -19.3 [-27.1, -11.1] | -13.7 [-24.7, -4.7] | -16.5 [-25.3, -8.5] |
| Code overlap sum (files+hunks+lines) | -20.2 [-27.5, -13.1] | -12.3 [-22.4, -2.9] | -17.0 [-25.1, -9.7] |
| LLM judge Qwen2.5-1.5B re-rank top-5 | -21.1 [-28.2, -13.1] | +5.3 [+1.2, +9.7] | -11.0 [-16.0, -4.9] |
| Jina code embeddings v2 on diff | -25.7 [-33.7, -16.0] | -22.2 [-32.2, -11.8] | -23.4 [-32.0, -13.6] |
| BGE-small on diff | -26.3 [-34.2, -17.0] | -22.2 [-33.1, -10.6] | -24.2 [-33.1, -14.5] |
| Changed-files Jaccard | -26.6 [-33.6, -19.9] | -18.4 [-28.1, -9.4] | -22.6 [-29.9, -15.7] |
| Hunk overlap | -26.6 [-34.5, -18.7] | -15.8 [-25.1, -6.3] | -22.6 [-30.7, -14.6] |
| Cross-encoder BGE-reranker-base re-rank top-10 | -27.5 [-37.9, -17.9] | -4.4 [-10.5, +1.2] | -19.1 [-26.4, -12.3] |
| Identical changed lines | -29.8 [-36.1, -22.2] | -21.1 [-29.1, -10.7] | -26.5 [-32.5, -18.6] |
| MiniLM on diff | -30.1 [-37.5, -21.3] | -25.4 [-36.3, -12.1] | -27.8 [-36.0, -18.0] |
| UniXcoder (code model) on diff | -30.1 [-38.1, -20.2] | -27.8 [-39.0, -14.2] | -28.5 [-37.5, -17.6] |
| LLM judge Qwen2.5-1.5B re-rank top-10 | -33.6 [-40.3, -26.4] | -5.0 [-10.4, +1.4] | -21.9 [-26.4, -16.9] |
| CodeBERT (mean-pooled) on diff | -39.8 [-47.7, -29.8] | -40.6 [-52.7, -26.4] | -39.5 [-48.9, -28.2] |
| Recency only (newest open PR first) | -58.5 [-65.5, -49.0] | -46.8 [-59.8, -29.5] | -52.7 [-61.3, -40.5] |


**False-alarm rate on 2,965 PRs with no duplicate** (threshold = median top-1 score of training-fold cross-author duplicates)

| Family | Strategy | False-alarm rate | Cross-author correct alerts |
|---|---|---|---|
| 7 supervised | Jinx features, gradient boosting | 1.3% | 46.2% |
| 7 supervised | All signals, LR | 1.6% | 48.8% |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | 1.8% | 48.5% |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 2.4% | 45.6% |
| 7 supervised | All signals, gradient boosting | 2.4% | 49.7% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 2.5% | 45.9% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 2.5% | 45.9% |
| 7 supervised | Jinx + MiniLM, LR (current tool) | 2.5% | 47.1% |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 2.5% | 46.2% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 2.8% | 45.3% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 2.8% | 45.3% |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 2.8% | 46.2% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 2.9% | 45.0% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 2.9% | 45.3% |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 3.1% | 46.2% |
| 7 supervised | Jinx lexical, LR | 3.2% | 46.8% |
| 10 stacked cascade (ours) | Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 3.7% | 44.2% |
| 3 links | Links only (same issue / #ref) | 3.8% | 46.2% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-5 | 4.0% | 43.3% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-7B re-rank top-10 | 4.0% | 43.0% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-5 | 4.2% | 42.7% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-5 | 4.2% | 44.2% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-14B re-rank top-10 | 4.2% | 42.4% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-Coder-7B re-rank top-10 | 4.3% | 43.0% |
| 10 stacked cascade (ours) | Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 4.3% | 41.5% |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 4.5% | 45.6% |
| 7 supervised | INTRUDE + time (Wang et al. 2019), LR | 4.6% | 44.2% |
| 10 stacked cascade (ours) | Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 4.7% | 45.0% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 5.0% | 44.2% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 5.0% | 44.2% |
| 9 LLM judge on top-k | LLM judge Claude Haiku 4.5 re-rank top-5 | 5.4% | 57.3% |
| 4 embedding | BGE-small template-stripped | 6.4% | 42.1% |
| 4 embedding | BGE-small raw text | 6.9% | 43.3% |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 6.9% | 44.7% |
| 10 stacked cascade (ours) | Cascade: Jinx + BGE-reranker-base (stacked LR) | 6.9% | 46.8% |
| 4 embedding | BGE-base template-stripped | 7.3% | 43.6% |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 8.8% | 45.9% |
| 1 lexical | TF-IDF template-stripped | 8.9% | 42.7% |
| 1 lexical | TF-IDF raw text (Li et al. 2017) | 9.4% | 42.4% |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 10.7% | 43.0% |
| 5 existing bot | Simili-bot (bot, re-impl) | 11.1% | 43.6% |
| 5 existing bot | contrib-guard/phoenix (bot, exact port) | 11.7% | 41.8% |
| 4 embedding | MiniLM template-stripped | 11.9% | 43.6% |
| 4 embedding | Jina code embeddings v2 on diff | 12.0% | 33.0% |
| 4 embedding | MiniLM raw text | 12.1% | 42.7% |
| 4 embedding | BGE-small on diff | 12.1% | 32.7% |
| 5 existing bot | PRSense (bot, re-impl) | 12.7% | 37.1% |
| 8 re-ranker on top-k | Cross-encoder ms-marco MiniLM re-rank top-10 | 13.4% | 40.9% |
| 4 embedding | MiniLM on diff | 15.2% | 30.1% |
| 4 embedding | CodeBERT (mean-pooled) on diff | 15.3% | 26.0% |
| 4 embedding | UniXcoder (code model) on diff | 16.1% | 29.2% |
| 2 code | BM25 on diff | 17.5% | 30.4% |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding + code | 18.0% | 49.4% |
| 1 lexical | BM25 template-stripped | 18.7% | 39.8% |
| 1 lexical | BM25 raw text | 21.0% | 38.6% |
| 2 code | Changed-files Jaccard | 24.4% | 33.9% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-5 | 24.4% | 32.5% |
| 4 embedding | UniXcoder template-stripped text | 24.8% | 36.8% |
| 2 code | Code overlap sum (files+hunks+lines) | 25.1% | 30.7% |
| 9 LLM judge on top-k | LLM judge Qwen2.5-1.5B re-rank top-10 | 25.7% | 25.7% |
| 2 code | Hunk overlap | 29.6% | 26.3% |
| 6 unsupervised hybrid | RRF hybrid: text + code + links + recency | 31.7% | 44.2% |
| 2 code | Identical changed lines | 32.0% | 24.3% |
| 6 unsupervised hybrid | RRF hybrid: BM25 + embedding | 37.3% | 62.9% |
| 0 trivial | Recency only (newest open PR first) | 44.1% | 5.6% |
| 8 re-ranker on top-k | Cross-encoder BGE-reranker-base re-rank top-10 | 45.1% | 26.3% |


**Operating curve: share of cross-author duplicates caught (correct top-1 above threshold) at a fixed false-alarm rate**

| Strategy | FAR 1% | FAR 2% | FAR 5% | FAR 10% | FAR 20% |
|---|---|---|---|---|---|
| LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | 31.3% | 49.7% | 71.3% | 82.7% | 86.5% |
| All signals, LR | 40.6% | 56.1% | 70.2% | 77.8% | 83.9% |
| All signals, gradient boosting | 23.4% | 44.7% | 69.0% | 76.9% | 83.0% |
| Jinx features, gradient boosting | 39.2% | 58.8% | 68.4% | 76.3% | 82.5% |
| Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 23.1% | 40.4% | 64.0% | 74.9% | 81.3% |
| Jinx + MiniLM, LR (current tool) | 30.1% | 43.6% | 63.2% | 74.9% | 81.0% |
| Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 23.7% | 33.0% | 62.6% | 73.4% | 83.0% |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 19.9% | 38.6% | 61.7% | 74.9% | 80.7% |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 19.9% | 38.6% | 61.7% | 74.9% | 81.0% |
| Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 19.0% | 42.1% | 59.9% | 69.6% | 81.0% |
| Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 22.2% | 43.6% | 59.9% | 73.7% | 80.7% |
| Jinx lexical, LR | 19.0% | 35.4% | 58.8% | 72.2% | 78.7% |
| LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 28.4% | 42.7% | 57.0% | 74.0% | 80.1% |
| LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 28.4% | 42.7% | 57.0% | 74.3% | 80.4% |
| LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 12.6% | 27.2% | 56.7% | 71.6% | 78.4% |
| LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 12.6% | 27.2% | 56.4% | 71.3% | 78.1% |
| Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 20.5% | 31.3% | 55.3% | 71.6% | 82.7% |
| Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 13.7% | 31.9% | 52.0% | 70.8% | 78.4% |
| Links only (same issue / #ref) | 22.8% | 33.3% | 50.9% | 58.2% | 68.4% |
| LLM judge Qwen2.5-7B re-rank top-5 | 14.6% | 24.9% | 50.9% | 62.9% | 72.5% |
| LLM judge Qwen2.5-7B re-rank top-10 | 14.6% | 24.3% | 49.4% | 62.3% | 71.1% |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 17.5% | 26.9% | 48.8% | 58.5% | 69.9% |
| Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 14.6% | 23.4% | 47.1% | 63.7% | 78.4% |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | 17.3% | 24.0% | 46.8% | 60.5% | 73.4% |
| INTRUDE + time (Wang et al. 2019), LR | 12.9% | 22.2% | 46.5% | 57.6% | 68.4% |
| LLM judge Qwen2.5-14B re-rank top-5 | 12.9% | 26.6% | 46.5% | 65.2% | 70.8% |
| LLM judge Qwen2.5-14B re-rank top-10 | 12.9% | 26.6% | 46.2% | 63.5% | 68.7% |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | 17.3% | 23.7% | 46.2% | 58.2% | 71.1% |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 9.6% | 19.9% | 45.3% | 64.9% | 77.2% |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 9.6% | 19.9% | 45.3% | 64.9% | 77.2% |
| BGE-small template-stripped | 6.1% | 14.0% | 37.1% | 52.0% | 61.1% |
| BGE-small raw text | 5.8% | 12.6% | 36.5% | 50.3% | 59.6% |
| Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 5.0% | 15.5% | 36.3% | 52.3% | 66.4% |
| Cascade: Jinx + BGE-reranker-base (stacked LR) | 5.8% | 14.0% | 33.3% | 58.8% | 78.7% |
| BGE-base template-stripped | 4.1% | 10.2% | 33.3% | 48.8% | 60.2% |
| TF-IDF template-stripped | 10.2% | 17.3% | 33.0% | 47.1% | 56.1% |
| TF-IDF raw text (Li et al. 2017) | 10.2% | 15.5% | 32.7% | 46.2% | 55.8% |
| Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 5.8% | 14.0% | 28.7% | 50.0% | 75.1% |
| Simili-bot (bot, re-impl) | 5.3% | 12.3% | 26.6% | 38.0% | 52.3% |
| MiniLM raw text | 5.0% | 12.3% | 25.7% | 37.1% | 53.8% |
| MiniLM template-stripped | 6.4% | 12.0% | 24.9% | 38.3% | 55.0% |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 6.7% | 13.7% | 24.0% | 39.5% | 53.5% |
| Jina code embeddings v2 on diff | 5.6% | 10.8% | 23.1% | 31.0% | 37.1% |
| PRSense (bot, re-impl) | 7.0% | 11.7% | 22.8% | 34.2% | 48.0% |
| Cross-encoder ms-marco MiniLM re-rank top-10 | 3.5% | 8.8% | 22.5% | 35.1% | 46.2% |
| BGE-small on diff | 2.6% | 9.1% | 22.2% | 29.8% | 36.8% |
| contrib-guard/phoenix (bot, exact port) | 5.0% | 9.6% | 20.8% | 36.8% | 56.1% |
| UniXcoder (code model) on diff | 4.1% | 10.8% | 20.5% | 25.4% | 32.7% |
| MiniLM on diff | 1.2% | 7.9% | 19.3% | 26.9% | 33.0% |
| CodeBERT (mean-pooled) on diff | 5.8% | 9.6% | 18.4% | 24.3% | 27.2% |
| Code overlap sum (files+hunks+lines) | 7.0% | 8.2% | 15.2% | 20.8% | 29.5% |
| LLM judge Qwen2.5-1.5B re-rank top-5 | 4.1% | 7.6% | 14.6% | 19.6% | 29.8% |
| BM25 on diff | 4.4% | 7.3% | 14.0% | 21.9% | 31.9% |
| BM25 template-stripped | 2.9% | 4.1% | 11.7% | 26.9% | 40.9% |
| UniXcoder template-stripped text | 3.5% | 7.9% | 11.4% | 18.1% | 32.5% |
| RRF hybrid: text + code + links + recency | 0.0% | 0.0% | 11.1% | 17.5% | 30.7% |
| BM25 raw text | 2.9% | 3.8% | 10.5% | 23.1% | 37.4% |
| LLM judge Qwen2.5-1.5B re-rank top-10 | 3.5% | 5.8% | 9.4% | 16.1% | 23.7% |
| LLM judge Claude Haiku 4.5 re-rank top-5 | 5.6% | 5.6% | 5.6% | 70.5% | 77.8% |
| Cross-encoder BGE-reranker-base re-rank top-10 | 1.2% | 1.2% | 2.3% | 4.7% | 13.2% |
| Changed-files Jaccard | 0.0% | 0.0% | 0.0% | 17.0% | 27.8% |
| Identical changed lines | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Hunk overlap | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| RRF hybrid: BM25 + embedding | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| RRF hybrid: BM25 + embedding + code | 0.0% | 0.0% | 0.0% | 0.0% | 45.6% |
| Recency only (newest open PR first) | 0.0% | 0.0% | 0.0% | 0.6% | 1.8% |


**Random-pair (classic) vs live-queue evaluation** (Kendall tau = 0.75)

| Strategy | Random-pair AUC | rank | Live-queue cross-author R@1 | rank |
|---|---|---|---|---|
| All signals, LR | 0.991 | 1 | 0.906 | 1 |
| All signals, gradient boosting | 0.989 | 2 | 0.877 | 14 |
| Jinx + MiniLM, LR (current tool) | 0.986 | 3 | 0.901 | 2 |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-10 | 0.984 | 4 | 0.874 | 15 |
| LLM judge Claude Haiku 4.5 + Jinx (avg) top-5 | 0.984 | 5 | 0.898 | 4 |
| LLM judge Qwen2.5-Coder-7B + Jinx (avg) top-5 | 0.984 | 6 | 0.880 | 13 |
| Cascade: Jinx + Qwen2.5-Coder-7B judge (stacked LR) | 0.984 | 7 | 0.886 | 11 |
| LLM judge Qwen2.5-7B + Jinx (avg) top-10 | 0.984 | 8 | 0.889 | 9 |
| LLM judge Qwen2.5-14B + Jinx (avg) top-10 | 0.983 | 9 | 0.868 | 20 |
| LLM judge Qwen2.5-7B + Jinx (avg) top-5 | 0.983 | 10 | 0.892 | 8 |
| Jinx lexical, LR | 0.983 | 11 | 0.889 | 9 |
| LLM judge Qwen2.5-14B + Jinx (avg) top-5 | 0.983 | 12 | 0.871 | 17 |
| Cascade: Jinx + Qwen2.5-14B judge (stacked LR) | 0.982 | 13 | 0.874 | 15 |
| LLM judge Claude Haiku 4.5 re-rank top-5 | 0.982 | 14 | 0.842 | 25 |
| Cascade: Jinx + Qwen2.5-7B judge (stacked LR) | 0.982 | 15 | 0.895 | 6 |
| Cross-encoder BGE-reranker-v2-m3 + Jinx (avg) top-10 | 0.982 | 16 | 0.871 | 17 |
| Jinx features, gradient boosting | 0.982 | 17 | 0.865 | 22 |
| LLM judge Qwen2.5-Coder-7B re-rank top-10 | 0.982 | 18 | 0.804 | 31 |
| Cascade: Jinx + BGE-reranker + Qwen2.5-7B (stacked LR) | 0.982 | 19 | 0.901 | 2 |
| Cascade: Jinx + fine-tuned reranker + Qwen2.5-7B (stacked LR) | 0.981 | 20 | 0.898 | 4 |
| Cascade: Jinx + fine-tuned BGE-reranker (stacked LR) | 0.981 | 21 | 0.895 | 6 |
| LLM judge Qwen2.5-Coder-7B re-rank top-5 | 0.981 | 22 | 0.839 | 26 |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-5 | 0.981 | 23 | 0.854 | 23 |
| LLM judge Qwen2.5-1.5B + Jinx (avg) top-10 | 0.981 | 24 | 0.851 | 24 |
| Cascade: Jinx + BGE-reranker-base (stacked LR) | 0.979 | 25 | 0.883 | 12 |
| Cross-encoder BGE-reranker-base + Jinx (avg) top-10 | 0.978 | 26 | 0.871 | 17 |
| Cross-encoder ms-marco MiniLM + Jinx (avg) top-10 | 0.978 | 27 | 0.868 | 20 |
| LLM judge Qwen2.5-7B re-rank top-5 | 0.975 | 28 | 0.810 | 29 |
| INTRUDE + time (Wang et al. 2019), LR | 0.974 | 29 | 0.810 | 29 |
| LLM judge Qwen2.5-7B re-rank top-10 | 0.972 | 30 | 0.792 | 32 |
| LLM judge Qwen2.5-14B re-rank top-5 | 0.972 | 31 | 0.751 | 39 |
| Fine-tuned BGE-reranker (repo-grouped folds) re-rank top-10 | 0.968 | 32 | 0.816 | 28 |
| Cross-encoder BGE-reranker-v2-m3 re-rank top-10 | 0.968 | 33 | 0.749 | 42 |
| LLM judge Qwen2.5-14B re-rank top-10 | 0.967 | 34 | 0.708 | 50 |
| Simili-bot (bot, re-impl) | 0.960 | 35 | 0.725 | 45 |
| Links only (same issue / #ref) | 0.959 | 36 | 0.839 | 26 |
| MiniLM raw text | 0.958 | 37 | 0.725 | 45 |
| BGE-small raw text | 0.958 | 38 | 0.751 | 39 |
| BGE-small template-stripped | 0.958 | 39 | 0.763 | 34 |
| MiniLM template-stripped | 0.958 | 40 | 0.751 | 39 |
| TF-IDF template-stripped | 0.957 | 41 | 0.760 | 35 |
| BGE-base template-stripped | 0.957 | 42 | 0.760 | 35 |
| TF-IDF raw text (Li et al. 2017) | 0.955 | 43 | 0.757 | 37 |
| PRSense (bot, re-impl) | 0.953 | 44 | 0.711 | 48 |
| contrib-guard/phoenix (bot, exact port) | 0.952 | 45 | 0.778 | 33 |
| Cross-encoder ms-marco MiniLM re-rank top-10 | 0.951 | 46 | 0.708 | 50 |
| LLM judge Qwen2.5-1.5B re-rank top-5 | 0.938 | 47 | 0.567 | 55 |
| RRF hybrid: BM25 + embedding | 0.937 | 48 | 0.734 | 44 |
| LLM judge Qwen2.5-1.5B re-rank top-10 | 0.923 | 49 | 0.442 | 64 |
| RRF hybrid: BM25 + embedding + code | 0.910 | 50 | 0.757 | 37 |
| Code overlap sum (files+hunks+lines) | 0.904 | 51 | 0.576 | 54 |
| Cross-encoder BGE-reranker-base re-rank top-10 | 0.893 | 52 | 0.503 | 60 |
| BM25 template-stripped | 0.891 | 53 | 0.737 | 43 |
| Hunk overlap | 0.886 | 54 | 0.512 | 58 |
| BM25 raw text | 0.885 | 55 | 0.711 | 48 |
| Changed-files Jaccard | 0.873 | 56 | 0.512 | 58 |
| BM25 on diff | 0.869 | 57 | 0.585 | 53 |
| RRF hybrid: text + code + links + recency | 0.850 | 58 | 0.713 | 47 |
| Jina code embeddings v2 on diff | 0.844 | 59 | 0.520 | 56 |
| BGE-small on diff | 0.842 | 60 | 0.515 | 57 |
| UniXcoder template-stripped text | 0.841 | 61 | 0.637 | 52 |
| Identical changed lines | 0.838 | 62 | 0.480 | 61 |
| MiniLM on diff | 0.805 | 63 | 0.477 | 62 |
| UniXcoder (code model) on diff | 0.781 | 64 | 0.477 | 62 |
| CodeBERT (mean-pooled) on diff | 0.653 | 65 | 0.380 | 65 |
| Recency only (newest open PR first) | 0.641 | 66 | 0.193 | 66 |


**Latency and cost**

| Component | Numbers |
|---|---|
| lexical features ms/query | {"median": 22.004112499416806, "p90": 228.5285644975381} |
| cpu_rerankers | {"cross-encoder/ms-marco-MiniLM-L6-v2": {"cpu_threads": 4, "pairs": 200, "ms_per_pair": 45.7, "ms_per_query_top10": 457.5}, "BAAI/bge-reranker-base": {"cpu_threads": 4, "pairs": 200, "ms_per_pair": 286.1, "ms_per_query_top10": 2861.4}} |
| gpu_bge_diff | {"tag": "bge_diff", "model": "BAAI/bge-small-en-v1.5", "variant": "diff", "maxlen": 512, "n": 76209, "dim": 384, "gpu": "L4", "seconds": 144.0, "ms_per_pr_gpu": 1.89} |
| gpu_bge_raw | {"tag": "bge_raw", "model": "BAAI/bge-small-en-v1.5", "variant": "raw", "maxlen": 512, "n": 76209, "dim": 384, "gpu": "L4", "seconds": 125.0, "ms_per_pr_gpu": 1.64} |
| gpu_bge_stripped | {"tag": "bge_stripped", "model": "BAAI/bge-small-en-v1.5", "variant": "stripped", "maxlen": 512, "n": 76209, "dim": 384, "gpu": "L4", "seconds": 120.7, "ms_per_pr_gpu": 1.583} |
| gpu_bgebase_stripped | {"tag": "bgebase_stripped", "model": "BAAI/bge-base-en-v1.5", "variant": "stripped", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 244.3, "ms_per_pr_gpu": 3.205} |
| gpu_ce_bgebase | {"tag": "ce_bgebase", "model": "BAAI/bge-reranker-base", "pairs": 43591, "gpu": "L4", "seconds": 137.5, "ms_per_pair_gpu": 3.154} |
| gpu_ce_bgem3 | {"tag": "ce_bgem3", "model": "BAAI/bge-reranker-v2-m3", "pairs": 43591, "gpu": "L4", "seconds": 445.7, "ms_per_pair_gpu": 10.224} |
| gpu_ce_msmarco | {"tag": "ce_msmarco", "model": "cross-encoder/ms-marco-MiniLM-L6-v2", "pairs": 43591, "gpu": "L4", "seconds": 41.6, "ms_per_pair_gpu": 0.954} |
| gpu_codebert_diff | {"tag": "codebert_diff", "model": "microsoft/codebert-base", "variant": "diff", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 262.1, "ms_per_pr_gpu": 3.44} |
| gpu_finetune_bgebase | {"gpu": "L4", "folds": [{"fold": 0, "base": "BAAI/bge-reranker-base", "train_pairs": 34896, "test_pairs": 8695, "train_s": 678.1, "predict_s": 121.0}, {"fold": 1, "base": "BAAI/bge-reranker-base", "train_pairs": 34892, "test_pairs": 8699, "train_s": 668.5, "predict_s": 120.4}, {"fold": 2, "base": "BAAI/bge-reranker-base", "train_pairs": 34821, "test_pairs": 8770, "train_s": 668.3, "predict_s": 121.9}, {"fold": 3, "base": "BAAI/bge-reranker-base", "train_pairs": 34868, "test_pairs": 8723, "train_s": 668.1, "predict_s": 118.9}, {"fold": 4, "base": "BAAI/bge-reranker-base", "train_pairs": 34887, "test_pairs": 8704, "train_s": 674.0, "predict_s": 121.1}], "train_s_total": 3357.0, "predict_ms_per_pair_gpu": 13.84} |
| gpu_jinacode_diff | {"tag": "jinacode_diff", "model": "jinaai/jina-embeddings-v2-base-code", "variant": "diff", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 620.2, "ms_per_pr_gpu": 8.138} |
| gpu_qwen14 | {"tag": "qwen14", "model": "Qwen/Qwen2.5-14B-Instruct", "pairs": 43591, "gpu": "L40S", "seconds": 5187.5, "ms_per_pair_gpu_batched": 119.003, "prompt_tokens_total": 49530439} |
| gpu_qwen15 | {"tag": "qwen15", "model": "Qwen/Qwen2.5-1.5B-Instruct", "pairs": 43591, "gpu": "L40S", "seconds": 687.2, "ms_per_pair_gpu_batched": 15.766, "prompt_tokens_total": 49530439} |
| gpu_qwen7 | {"tag": "qwen7", "model": "Qwen/Qwen2.5-7B-Instruct", "pairs": 43591, "gpu": "L40S", "seconds": 2567.3, "ms_per_pair_gpu_batched": 58.895, "prompt_tokens_total": 49530439} |
| gpu_qwencoder7 | {"tag": "qwencoder7", "model": "Qwen/Qwen2.5-Coder-7B-Instruct", "pairs": 43591, "gpu": "L40S", "seconds": 2478.3, "ms_per_pair_gpu_batched": 56.854, "prompt_tokens_total": 49530439} |
| gpu_unix_diff | {"tag": "unix_diff", "model": "microsoft/unixcoder-base", "variant": "diff", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 284.0, "ms_per_pr_gpu": 3.727} |
| gpu_unix_stripped | {"tag": "unix_stripped", "model": "microsoft/unixcoder-base", "variant": "stripped", "maxlen": 512, "n": 76209, "dim": 768, "gpu": "L4", "seconds": 247.7, "ms_per_pr_gpu": 3.251} |
| claude haiku45 API | {"pairs": 4587, "ms/pair median": 912.8988000011304, "ms/pair p90": 977.3896139959106, "model": "claude-haiku-4-5", "usd": 7.252751, "budget": 15.0} |
