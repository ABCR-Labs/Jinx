window.JINX = {
 "n_cross": 313,
 "methods": [
  {
   "name": "Jinx",
   "desc": "This tool (GitHub Action default)",
   "ours": true,
   "top1": 91.7,
   "top1_lo": 88.0,
   "top1_hi": 95.1,
   "far": 1.9,
   "far_lo": 1.3,
   "far_hi": 2.7,
   "curve": {
    "0.01": 27,
    "0.02": 48,
    "0.05": 67,
    "0.1": 77,
    "0.2": 86
   }
  },
  {
   "name": "Jinx + MiniLM",
   "desc": "This tool with its optional local text model",
   "ours": true,
   "top1": 92.7,
   "top1_lo": 88.9,
   "top1_hi": 95.8,
   "far": 1.8,
   "far_lo": 1.2,
   "far_hi": 2.5,
   "curve": {
    "0.01": 32,
    "0.02": 52,
    "0.05": 68,
    "0.1": 79,
    "0.2": 87
   }
  },
  {
   "name": "Link rule",
   "desc": "Same issue or #mention; text similarity breaks ties",
   "ours": false,
   "top1": 93.6,
   "top1_lo": 90.4,
   "top1_hi": 97.0,
   "far": 1.2,
   "far_lo": 0.7,
   "far_hi": 1.7,
   "curve": {
    "0.01": 44,
    "0.02": 61,
    "0.05": 70,
    "0.1": 76,
    "0.2": 85
   }
  },
  {
   "name": "INTRUDE + time",
   "desc": "Classic research detector (Wang et al. 2019)",
   "ours": false,
   "top1": 91.4,
   "top1_lo": 87.8,
   "top1_hi": 94.8,
   "far": 2.0,
   "far_lo": 1.3,
   "far_hi": 3.0,
   "curve": {
    "0.01": 34,
    "0.02": 47,
    "0.05": 67,
    "0.1": 79,
    "0.2": 85
   }
  },
  {
   "name": "contrib-guard",
   "desc": "Best existing open-source duplicate-PR bot we tested",
   "ours": false,
   "top1": 91.4,
   "top1_lo": 88.5,
   "top1_hi": 94.7,
   "far": 5.5,
   "far_lo": 4.0,
   "far_hi": 7.0,
   "curve": {
    "0.01": 12,
    "0.02": 18,
    "0.05": 42,
    "0.1": 61,
    "0.2": 79
   }
  },
  {
   "name": "Simili-bot",
   "desc": "Existing duplicate-PR bot (re-implemented)",
   "ours": false,
   "top1": 87.9,
   "top1_lo": 84.5,
   "top1_hi": 91.9,
   "far": 4.5,
   "far_lo": 3.2,
   "far_hi": 6.2,
   "curve": {
    "0.01": 17,
    "0.02": 29,
    "0.05": 50,
    "0.1": 64,
    "0.2": 76
   }
  },
  {
   "name": "PRSense",
   "desc": "Existing duplicate-PR bot (re-implemented)",
   "ours": false,
   "top1": 82.7,
   "top1_lo": 74.5,
   "top1_hi": 90.9,
   "far": 4.7,
   "far_lo": 3.5,
   "far_hi": 6.0,
   "curve": {
    "0.01": 21,
    "0.02": 29,
    "0.05": 43,
    "0.1": 61,
    "0.2": 71
   }
  },
  {
   "name": "Text similarity",
   "desc": "Title and description word overlap (TF-IDF)",
   "ours": false,
   "top1": 91.1,
   "top1_lo": 88.1,
   "top1_hi": 94.3,
   "far": 3.5,
   "far_lo": 2.5,
   "far_hi": 4.8,
   "curve": {
    "0.01": 20,
    "0.02": 34,
    "0.05": 54,
    "0.1": 65,
    "0.2": 75
   }
  }
 ],
 "cost": {
  "after_1h": 44,
  "after_1d": 15,
  "after_7d": 5,
  "reviewed_before": 22
 },
 "latency_ms": 6.1,
 "haiku": {
  "far": 0.8,
  "jinx_far_same_sample": 1.7,
  "cents_per_pr": 0.8
 }
};
