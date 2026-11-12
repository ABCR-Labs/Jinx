"""Build the captioned demo video (no voice-over) from real screenshots and CLI output.

Inputs: docs/assets/*.png, the live-run screenshots in paper/tooldemo/video/shots/, and the CLI fixture output.
Output: paper/tooldemo/video/jinx_demo.mp4 (1920x1080, about 3 minutes)."""

import os
import pathlib
import subprocess
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
W, H = 1920, 1080
F = "/usr/share/fonts/truetype/dejavu/"
SANS, BOLD, MONO = (ImageFont.truetype(F + n, s) for n, s in
                    [("DejaVuSans.ttf", 40), ("DejaVuSans-Bold.ttf", 64), ("DejaVuSansMono.ttf", 30)])
CAP = ImageFont.truetype(F + "DejaVuSans.ttf", 36)
INDIGO, TEAL, INK = (79, 70, 229), (13, 148, 136), (30, 27, 75)


def canvas(title):
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 130], fill=INDIGO)
    d.text((70, 30), title, font=BOLD, fill="white")
    return im, d


def caption(im, text):
    d = ImageDraw.Draw(im)
    lines = textwrap.wrap(text, 88)
    top = H - 60 - 48 * len(lines)
    d.rectangle([0, top - 30, W, H], fill=(17, 24, 39))
    for i, ln in enumerate(lines):
        d.text((70, top + 48 * i), ln, font=CAP, fill="white")
    return im


def paste(im, path, box):
    x0, y0, x1, y1 = box
    p = Image.open(path).convert("RGB")
    p.thumbnail((x1 - x0, y1 - y0), Image.LANCZOS)
    im.paste(p, (x0 + (x1 - x0 - p.width) // 2, y0 + (y1 - y0 - p.height) // 2))
    return im


def text_slide(title, body, font=SANS, top=200, step=58):
    im, d = canvas(title)
    for i, ln in enumerate(body):
        d.text((90, top + step * i), ln, font=font, fill=INK)
    return im


def banner():
    svg = os.path.join(ROOT, "docs/assets/banner.svg")
    out = os.path.join(HERE, "shots/banner.png")
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--window-size=1280,320", f"--screenshot={out}", f"file://{svg}"], check=False, capture_output=True)
    im = Image.new("RGB", (W, H), (49, 46, 129))
    return paste(im, out, (0, 280, W, 760))


S = os.path.join(HERE, "shots")
cli = pathlib.Path(S, "cli_dup.txt").read_text().splitlines()
yaml = pathlib.Path(ROOT, ".github/workflows/jinx.yml").read_text().splitlines()
slides = [
    (banner(), 12, "Jinx: explainable duplicate warnings for pull requests from coding agents."),
    (paste(canvas("Agents open many PRs, some redo open work")[0], os.path.join(S, "pulls.png"), (60, 150, W - 60, 860)), 22,
     ("Coding agents open many pull requests. Some redo work that is already open, and a maintainer may review both "
     "before noticing. Here are four demo PRs on the Jinx repository: three for the same issue and one unrelated.")),
    (text_slide("Add one workflow file", yaml, font=MONO, top=170, step=40), 25,
     ("Jinx is a GitHub Action. It uses the workflow's own token, needs no API key, reads PR metadata and diffs through "
     "the API, and never runs the PR's code.")),
    (paste(canvas("A new PR opens: Jinx comments")[0], os.path.join(ROOT, "docs/assets/action_comment.png"), (60, 170, W - 60, 820)), 35,
     ("PR #15 redoes open PR #12. Jinx compares it with every open PR: same linked issue, shared files, overlapping "
     "lines, identical added lines, similar text after removing agent boilerplate. It explains the match and never "
     "closes anything.")),
    (text_slide("And when to stay quiet", [
        "#13  docs: explain how to choose the threshold   ->  no comment (unrelated)",
        "#14  same issue, different wording and code       ->  score 0.30, no comment",
        "",
        "The default threshold (0.5) keeps false alarms near 2 in 100 clean PRs.",
        "Lower it to catch duplicates like #14, at the cost of more alerts.",
    ], font=MONO, top=230, step=64), 25,
     ("An unrelated docs PR got no comment. A PR for the same issue written very differently scored 0.30, below the "
     "default threshold, so it was missed. The threshold is the knob that trades misses against false alarms.")),
    (text_slide("The same check runs locally", ["$ pip install git+https://github.com/ABCR-Labs/Jinx",
                                                 "$ jinx check examples/new_pr.json --open-queue examples/open_prs.jsonl --top 2",
                                                 ""] + cli, font=ImageFont.truetype(F + "DejaVuSansMono.ttf", 25), top=170, step=40), 25,
     ("This is a real agent PR from huggingface/transformers, from the AIDev dataset. Jinx finds its twin among 19 "
     "open PRs in about 10 ms on a CPU.")),
    (paste(canvas("How it compares (313 cross-author duplicates)")[0], os.path.join(ROOT, "docs/assets/fig_far.png"), (60, 160, W - 60, 820)), 30,
     ("On real AIDev queues, Jinx ranks the right PR first 93% of the time, tied with a link rule and a classic research "
     "detector. Its false alarms are 1.8 per 100 clean PRs, about a third of the best existing bot's.")),
    (text_slide("Limitations", [
        "- Misses duplicates that change different files (Recall@1 0.72 on those).",
        "- Labels come from PR comments; a human check of 100 pairs is under way.",
        "- Evaluated on historical data plus this demo run, not a maintainer deployment.",
        "- An optional Claude Haiku check halves false alarms, but costs API money",
        "  and is not part of Jinx yet.",
    ], top=230, step=70), 22, "Jinx is not more accurate than the best baselines; it packages them with explanations."),
    (text_slide("Try it", ["github.com/ABCR-Labs/Jinx", "", "pip install git+https://github.com/ABCR-Labs/Jinx",
                           "uses: ABCR-Labs/Jinx@main", "", "MIT licence  ·  CPU only  ·  no API key"], top=300, step=70), 12,
     "Jinx is open source. Thanks for watching."),
]
os.makedirs(os.path.join(HERE, "frames"), exist_ok=True)
lst = []
for i, (im, sec, cap) in enumerate(slides):
    f = os.path.join(HERE, "frames", f"{i:02d}.png")
    caption(im, cap).save(f)
    lst += [f"file '{f}'", f"duration {sec}"]
lst.append(f"file '{f}'")
pathlib.Path(HERE, "frames", "list.txt").write_text("\n".join(lst) + "\n")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(HERE, "frames", "list.txt"),
                "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "20", os.path.join(HERE, "jinx_demo.mp4")], check=True)
print(sum(s for _, s, _ in slides), "seconds")
