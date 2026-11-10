
**all labelled** (n = 1867)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.772 [0.725, 0.817] | 0.911 [0.862, 0.948] | 0.837 |
| Plain embedding (MiniLM, raw text) | 0.721 [0.676, 0.768] | 0.885 [0.829, 0.930] | 0.797 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.722 [0.674, 0.775] | 0.885 [0.835, 0.930] | 0.796 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.721 [0.676, 0.768] | 0.885 [0.829, 0.930] | 0.797 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.729 [0.681, 0.775] | 0.883 [0.829, 0.928] | 0.801 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.721 [0.677, 0.768] | 0.886 [0.832, 0.932] | 0.796 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.721 [0.677, 0.767] | 0.886 [0.832, 0.932] | 0.796 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.781 [0.736, 0.825] | 0.925 [0.897, 0.950] | 0.845 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.680 [0.634, 0.722] | 0.846 [0.792, 0.890] | 0.756 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.837 [0.789, 0.878] | 0.949 [0.909, 0.977] | 0.889 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.848 [0.820, 0.877] | 0.965 [0.948, 0.980] | 0.902 |
| AgentDup (lexical) | 0.903 [0.875, 0.925] | 0.984 [0.974, 0.993] | 0.938 |
| AgentDup (+ local embedding) | 0.890 [0.839, 0.929] | 0.980 [0.968, 0.990] | 0.927 |
| ablation: no template stripping | 0.890 [0.839, 0.928] | 0.970 [0.948, 0.987] | 0.926 |
| ablation: no code overlap | 0.872 [0.825, 0.910] | 0.983 [0.968, 0.994] | 0.920 |
| ablation: no issue/reference links | 0.872 [0.822, 0.913] | 0.973 [0.949, 0.989] | 0.914 |
| ablation: no author/agent context | 0.892 [0.842, 0.931] | 0.980 [0.968, 0.989] | 0.928 |
| ablation: no time features | 0.836 [0.784, 0.876] | 0.951 [0.907, 0.981] | 0.889 |

**self-replacement (same author)** (n = 1525)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.776 [0.717, 0.828] | 0.909 [0.850, 0.956] | 0.838 |
| Plain embedding (MiniLM, raw text) | 0.721 [0.659, 0.771] | 0.880 [0.813, 0.933] | 0.795 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.725 [0.664, 0.779] | 0.890 [0.834, 0.938] | 0.799 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.721 [0.659, 0.771] | 0.880 [0.813, 0.933] | 0.795 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.730 [0.671, 0.779] | 0.881 [0.814, 0.936] | 0.800 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.723 [0.664, 0.775] | 0.884 [0.818, 0.937] | 0.796 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.723 [0.664, 0.775] | 0.884 [0.818, 0.937] | 0.796 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.782 [0.724, 0.834] | 0.927 [0.891, 0.957] | 0.846 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.683 [0.629, 0.736] | 0.843 [0.777, 0.894] | 0.757 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.839 [0.784, 0.887] | 0.949 [0.899, 0.983] | 0.890 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.857 [0.824, 0.891] | 0.968 [0.948, 0.984] | 0.908 |
| AgentDup (lexical) | 0.906 [0.874, 0.932] | 0.988 [0.976, 0.995] | 0.941 |
| AgentDup (+ local embedding) | 0.887 [0.827, 0.933] | 0.982 [0.968, 0.992] | 0.925 |
| ablation: no template stripping | 0.885 [0.827, 0.930] | 0.972 [0.946, 0.992] | 0.923 |
| ablation: no code overlap | 0.869 [0.813, 0.914] | 0.986 [0.969, 0.997] | 0.919 |
| ablation: no issue/reference links | 0.870 [0.808, 0.920] | 0.976 [0.948, 0.995] | 0.913 |
| ablation: no author/agent context | 0.889 [0.829, 0.936] | 0.982 [0.967, 0.993] | 0.927 |
| ablation: no time features | 0.836 [0.777, 0.886] | 0.950 [0.896, 0.985] | 0.889 |

**cross-author** (n = 342)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.757 [0.702, 0.811] | 0.921 [0.881, 0.956] | 0.832 |
| Plain embedding (MiniLM, raw text) | 0.725 [0.664, 0.791] | 0.906 [0.847, 0.949] | 0.807 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.711 [0.609, 0.811] | 0.865 [0.794, 0.936] | 0.784 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.725 [0.664, 0.791] | 0.906 [0.847, 0.949] | 0.807 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.725 [0.661, 0.797] | 0.892 [0.838, 0.936] | 0.804 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.713 [0.649, 0.782] | 0.895 [0.850, 0.933] | 0.799 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.713 [0.649, 0.782] | 0.895 [0.850, 0.933] | 0.799 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.778 [0.716, 0.839] | 0.918 [0.875, 0.957] | 0.843 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.664 [0.603, 0.726] | 0.863 [0.807, 0.913] | 0.754 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.827 [0.776, 0.880] | 0.947 [0.915, 0.973] | 0.882 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.810 [0.765, 0.853] | 0.953 [0.923, 0.979] | 0.873 |
| AgentDup (lexical) | 0.889 [0.845, 0.928] | 0.971 [0.951, 0.990] | 0.925 |
| AgentDup (+ local embedding) | 0.901 [0.865, 0.930] | 0.971 [0.951, 0.992] | 0.932 |
| ablation: no template stripping | 0.912 [0.877, 0.942] | 0.962 [0.939, 0.983] | 0.938 |
| ablation: no code overlap | 0.886 [0.848, 0.924] | 0.971 [0.949, 0.993] | 0.926 |
| ablation: no issue/reference links | 0.883 [0.849, 0.920] | 0.959 [0.936, 0.985] | 0.919 |
| ablation: no author/agent context | 0.904 [0.867, 0.936] | 0.971 [0.951, 0.990] | 0.934 |
| ablation: no time features | 0.833 [0.783, 0.884] | 0.956 [0.911, 0.986] | 0.889 |

**cross-author, same agent** (n = 228)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.776 [0.725, 0.832] | 0.930 [0.890, 0.961] | 0.844 |
| Plain embedding (MiniLM, raw text) | 0.737 [0.681, 0.800] | 0.917 [0.868, 0.951] | 0.816 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.732 [0.662, 0.805] | 0.899 [0.856, 0.939] | 0.809 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.737 [0.681, 0.800] | 0.917 [0.868, 0.951] | 0.816 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.750 [0.694, 0.806] | 0.899 [0.853, 0.936] | 0.823 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.737 [0.678, 0.794] | 0.908 [0.872, 0.940] | 0.816 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.737 [0.678, 0.794] | 0.908 [0.872, 0.940] | 0.816 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.811 [0.750, 0.859] | 0.925 [0.883, 0.956] | 0.861 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.671 [0.585, 0.741] | 0.860 [0.804, 0.906] | 0.755 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.846 [0.797, 0.897] | 0.952 [0.929, 0.976] | 0.895 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.825 [0.775, 0.874] | 0.961 [0.940, 0.982] | 0.883 |
| AgentDup (lexical) | 0.882 [0.828, 0.925] | 0.965 [0.939, 0.990] | 0.919 |
| AgentDup (+ local embedding) | 0.899 [0.851, 0.939] | 0.965 [0.937, 0.990] | 0.929 |
| ablation: no template stripping | 0.904 [0.854, 0.945] | 0.961 [0.934, 0.986] | 0.931 |
| ablation: no code overlap | 0.886 [0.843, 0.925] | 0.969 [0.944, 0.994] | 0.924 |
| ablation: no issue/reference links | 0.890 [0.840, 0.934] | 0.956 [0.928, 0.983] | 0.923 |
| ablation: no author/agent context | 0.904 [0.857, 0.942] | 0.969 [0.945, 0.991] | 0.933 |
| ablation: no time features | 0.846 [0.796, 0.896] | 0.961 [0.929, 0.985] | 0.897 |

**cross-author, cross-agent** (n = 114)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.719 [0.622, 0.852] | 0.904 [0.807, 0.988] | 0.808 |
| Plain embedding (MiniLM, raw text) | 0.702 [0.582, 0.820] | 0.886 [0.778, 0.955] | 0.787 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.667 [0.500, 0.875] | 0.798 [0.669, 0.947] | 0.734 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.702 [0.582, 0.820] | 0.886 [0.778, 0.955] | 0.787 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.675 [0.556, 0.829] | 0.877 [0.771, 0.951] | 0.766 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.667 [0.547, 0.817] | 0.868 [0.764, 0.940] | 0.764 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.667 [0.547, 0.817] | 0.868 [0.764, 0.940] | 0.764 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.711 [0.618, 0.842] | 0.904 [0.800, 1.000] | 0.806 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.649 [0.541, 0.784] | 0.868 [0.771, 0.961] | 0.752 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.789 [0.711, 0.878] | 0.939 [0.852, 0.990] | 0.856 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.781 [0.697, 0.871] | 0.939 [0.852, 0.990] | 0.853 |
| AgentDup (lexical) | 0.904 [0.846, 0.968] | 0.982 [0.958, 1.000] | 0.937 |
| AgentDup (+ local embedding) | 0.904 [0.863, 0.958] | 0.982 [0.958, 1.000] | 0.939 |
| ablation: no template stripping | 0.930 [0.898, 0.973] | 0.965 [0.933, 1.000] | 0.952 |
| ablation: no code overlap | 0.886 [0.815, 0.963] | 0.974 [0.936, 1.000] | 0.928 |
| ablation: no issue/reference links | 0.868 [0.808, 0.974] | 0.965 [0.932, 1.000] | 0.912 |
| ablation: no author/agent context | 0.904 [0.852, 0.974] | 0.974 [0.945, 1.000] | 0.938 |
| ablation: no time features | 0.807 [0.721, 0.909] | 0.947 [0.862, 1.000] | 0.872 |

**cross-author, no explicit #ref to gold** (n = 199)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.683 [0.602, 0.770] | 0.879 [0.819, 0.942] | 0.772 |
| Plain embedding (MiniLM, raw text) | 0.709 [0.627, 0.785] | 0.879 [0.790, 0.943] | 0.783 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.693 [0.617, 0.788] | 0.854 [0.783, 0.934] | 0.769 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.709 [0.627, 0.785] | 0.879 [0.790, 0.943] | 0.783 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.709 [0.632, 0.783] | 0.859 [0.783, 0.925] | 0.782 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.704 [0.626, 0.776] | 0.859 [0.783, 0.922] | 0.781 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.704 [0.626, 0.776] | 0.859 [0.783, 0.922] | 0.781 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.714 [0.645, 0.797] | 0.874 [0.800, 0.936] | 0.788 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.628 [0.528, 0.705] | 0.819 [0.740, 0.889] | 0.715 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.744 [0.661, 0.831] | 0.910 [0.857, 0.954] | 0.818 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.714 [0.632, 0.788] | 0.920 [0.872, 0.963] | 0.803 |
| AgentDup (lexical) | 0.834 [0.779, 0.884] | 0.960 [0.937, 0.987] | 0.888 |
| AgentDup (+ local embedding) | 0.854 [0.808, 0.897] | 0.960 [0.935, 0.992] | 0.901 |
| ablation: no template stripping | 0.869 [0.811, 0.914] | 0.945 [0.917, 0.974] | 0.908 |
| ablation: no code overlap | 0.829 [0.774, 0.879] | 0.960 [0.935, 0.994] | 0.890 |
| ablation: no issue/reference links | 0.849 [0.800, 0.897] | 0.945 [0.916, 0.986] | 0.893 |
| ablation: no author/agent context | 0.859 [0.814, 0.904] | 0.960 [0.939, 0.986] | 0.904 |
| ablation: no time features | 0.759 [0.676, 0.843] | 0.925 [0.852, 0.978] | 0.831 |

**self-replacement, no explicit #ref to gold** (n = 1077)

| Method | R@1 [95% CI] | R@5 [95% CI] | MRR |
|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.771 [0.699, 0.826] | 0.910 [0.832, 0.960] | 0.836 |
| Plain embedding (MiniLM, raw text) | 0.717 [0.647, 0.776] | 0.883 [0.806, 0.939] | 0.794 |
| PRSense v2.2 (re-impl, local MiniLM) | 0.722 [0.652, 0.783] | 0.893 [0.818, 0.945] | 0.799 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.717 [0.647, 0.776] | 0.883 [0.806, 0.939] | 0.794 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.722 [0.652, 0.781] | 0.885 [0.804, 0.939] | 0.797 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.721 [0.650, 0.782] | 0.887 [0.809, 0.941] | 0.795 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.721 [0.649, 0.781] | 0.887 [0.809, 0.941] | 0.794 |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.767 [0.694, 0.823] | 0.932 [0.908, 0.957] | 0.839 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.679 [0.609, 0.736] | 0.851 [0.766, 0.906] | 0.758 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.800 [0.721, 0.859] | 0.934 [0.858, 0.981] | 0.863 |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.827 [0.795, 0.862] | 0.961 [0.934, 0.984] | 0.889 |
| AgentDup (lexical) | 0.892 [0.864, 0.917] | 0.989 [0.982, 0.995] | 0.934 |
| AgentDup (+ local embedding) | 0.868 [0.784, 0.923] | 0.982 [0.972, 0.992] | 0.914 |
| ablation: no template stripping | 0.863 [0.781, 0.920] | 0.975 [0.950, 0.992] | 0.910 |
| ablation: no code overlap | 0.853 [0.781, 0.905] | 0.991 [0.984, 0.997] | 0.911 |
| ablation: no issue/reference links | 0.868 [0.785, 0.922] | 0.984 [0.971, 0.994] | 0.914 |
| ablation: no author/agent context | 0.868 [0.783, 0.924] | 0.982 [0.970, 0.993] | 0.914 |
| ablation: no time features | 0.798 [0.717, 0.858] | 0.937 [0.856, 0.985] | 0.863 |

**False alarms on 2,965 PRs with no duplicate**

| Method | FAR, threshold set for 50% cross-author detection | correct top-1 alerts (cross-author) | FAR at tool default | correct alerts at default |
|---|---|---|---|---|
| Li et al. 2017 (TF-IDF title+description) | 0.094 | 0.424 | - | - |
| Plain embedding (MiniLM, raw text) | 0.121 | 0.427 | - | - |
| PRSense v2.2 (re-impl, local MiniLM) | 0.127 | 0.371 | 0.036 | 0.190 |
| PRism (re-impl: embedding stage, local MiniLM) | 0.121 | 0.427 | 0.046 | 0.243 |
| Simili-bot (re-impl: vector stage, local MiniLM) | 0.111 | 0.436 | 0.377 | 0.620 |
| vector-triage (re-impl: vector top-5 + FTS5 RRF, local MiniLM) | 0.126 | 0.412 | 0.019 | 0.108 |
| vector-triage, no 0.75 filter (re-impl, local MiniLM) | 0.126 | 0.412 | - | - |
| contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code) | 0.117 | 0.418 | 0.282 | 0.594 |
| contrib-guard/balyakin (tool's own code: title Jaccard + same files) | 0.146 | 0.430 | 0.020 | 0.170 |
| Ren et al. 2019 (INTRUDE clues, LR) | 0.041 | 0.433 | - | - |
| Wang et al. 2019 (INTRUDE + time, LR) | 0.046 | 0.442 | - | - |
| AgentDup (lexical) | 0.032 | 0.468 | - | - |
| AgentDup (+ local embedding) | 0.025 | 0.471 | - | - |
| ablation: no template stripping | 0.023 | 0.480 | - | - |
| ablation: no code overlap | 0.035 | 0.477 | - | - |
| ablation: no issue/reference links | 0.038 | 0.462 | - | - |
| ablation: no author/agent context | 0.026 | 0.468 | - | - |
| ablation: no time features | 0.034 | 0.444 | - | - |

```json
{
 "paired": {
  "AgentDup (lexical)": {
   "vs": "Wang et al. 2019 (INTRUDE + time, LR)",
   "dR@5": 0.017543859649122806,
   "dR@5 CI": [
    -0.008646786117027941,
    0.05166210713831274
   ],
   "dMRR": 0.05212384479668038,
   "dMRR CI": [
    0.018830297294851937,
    0.09030876102746148
   ],
   "dR@1": 0.07894736842105263,
   "dR@1 CI": [
    0.034612068965517245,
    0.125
   ],
   "cross-author, no explicit #ref to gold": {
    "vs": "Wang et al. 2019 (INTRUDE + time, LR)",
    "n": 199,
    "dR@1": 0.12060301507537688,
    "dR@1 CI": [
     0.06015037593984962,
     0.20408430387861948
    ],
    "dR@5": 0.04020100502512563,
    "dR@5 CI": [
     0.004715879033680127,
     0.1
    ],
    "dMRR": 0.08548512615904458,
    "dMRR CI": [
     0.03956940520390491,
     0.15420364907448023
    ]
   },
   "vs best existing bot, cross-author": {
    "vs": "contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code)",
    "n": 342,
    "dR@1": 0.1111111111111111,
    "dR@1 CI": [
     0.05019270422496229,
     0.1662148880950559
    ],
    "dR@5": 0.05263157894736842,
    "dR@5 CI": [
     0.011764705882352941,
     0.10103695843898136
    ],
    "dMRR": 0.08225283590134462,
    "dMRR CI": [
     0.038656167696400595,
     0.13044142509043385
    ]
   },
   "vs best existing bot, cross-author, no explicit #ref to gold": {
    "vs": "contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code)",
    "n": 199,
    "dR@1": 0.12060301507537688,
    "dR@1 CI": [
     0.04477136609943911,
     0.20320855614973263
    ],
    "dR@5": 0.08542713567839195,
    "dR@5 CI": [
     0.030293317793317797,
     0.17033068783068783
    ],
    "dMRR": 0.10016840304674467,
    "dMRR CI": [
     0.04143856855765917,
     0.1796356900230107
    ]
   },
   "FAR": {
    "vs lowest-FAR baseline": "Ren et al. 2019 (INTRUDE clues, LR)",
    "dFAR": -0.008768971332209106,
    "dFAR CI": [
     -0.015050069423718256,
     -0.0026167735538805826
    ]
   }
  },
  "AgentDup (+ local embedding)": {
   "vs": "Wang et al. 2019 (INTRUDE + time, LR)",
   "dR@5": 0.017543859649122806,
   "dR@5 CI": [
    -0.010309278350515464,
    0.052277097902097835
   ],
   "dMRR": 0.05947169750388936,
   "dMRR CI": [
    0.0269568305384083,
    0.09359460032431409
   ],
   "dR@1": 0.09064327485380116,
   "dR@1 CI": [
    0.04782091097308489,
    0.12941176470588237
   ],
   "cross-author, no explicit #ref to gold": {
    "vs": "Wang et al. 2019 (INTRUDE + time, LR)",
    "n": 199,
    "dR@1": 0.1407035175879397,
    "dR@1 CI": [
     0.07791064569233584,
     0.21154411764705874
    ],
    "dR@5": 0.04020100502512563,
    "dR@5 CI": [
     0.0,
     0.10294340463458107
    ],
    "dMRR": 0.09794168751330334,
    "dMRR CI": [
     0.05115848012571512,
     0.15755100468118763
    ]
   },
   "vs best existing bot, cross-author": {
    "vs": "contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code)",
    "n": 342,
    "dR@1": 0.12280701754385964,
    "dR@1 CI": [
     0.06427999491611591,
     0.1725067385444744
    ],
    "dR@5": 0.05263157894736842,
    "dR@5 CI": [
     0.012721035848874287,
     0.10000759878419442
    ],
    "dMRR": 0.08960068860855361,
    "dMRR CI": [
     0.04525194809906505,
     0.13403629290655616
    ]
   },
   "vs best existing bot, cross-author, no explicit #ref to gold": {
    "vs": "contrib-guard/phoenix v1.0 (port, TF-IDF title+body; verified = npm code)",
    "n": 199,
    "dR@1": 0.1407035175879397,
    "dR@1 CI": [
     0.06040268456375839,
     0.21154891304347812
    ],
    "dR@5": 0.08542713567839195,
    "dR@5 CI": [
     0.028774399834970734,
     0.17059625668449185
    ],
    "dMRR": 0.1126249644010034,
    "dMRR CI": [
     0.05131024061238302,
     0.1843081159270325
    ]
   },
   "FAR": {
    "vs lowest-FAR baseline": "Ren et al. 2019 (INTRUDE clues, LR)",
    "dFAR": -0.01551433389544688,
    "dFAR CI": [
     -0.02218327616998823,
     -0.009593980872514252
    ]
   }
  }
 },
 "best_baseline_cross_author_R@5": "Wang et al. 2019 (INTRUDE + time, LR)",
 "lexical_feature_ms_per_query": {
  "median": 22.004112499416806,
  "p90": 228.52856449753813,
  "max": 7344.2877659981605
 },
 "queue_size": {
  "median": 40.0,
  "p90": 314.0
 }
}
```