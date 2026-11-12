const J = window.JINX;
const byName = Object.fromEntries(J.methods.map((m) => [m.name, m]));
const fills = {
  n_cross: J.n_cross,
  after_1h: J.cost.after_1h + "%",
  after_1d: J.cost.after_1d + "%",
  reviewed_before: J.cost.reviewed_before + "%",
  jinx_far: byName["Jinx"].far,
  cg_far: byName["contrib-guard"].far,
  latency: Math.round(J.latency_ms) + " ms",
  haiku_jinx: J.haiku.jinx_far_same_sample,
  haiku_far: J.haiku.far,
  haiku_cost: J.haiku.cents_per_pr,
};
document.querySelectorAll("[data-k]").forEach((el) => { el.textContent = fills[el.dataset.k]; });

const maxFar = Math.max(...J.methods.map((m) => m.far));
const tbody = document.querySelector("#cmp tbody");
for (const m of J.methods) {
  const tr = document.createElement("tr");
  if (m.ours) tr.className = "ours";
  tr.innerHTML =
    `<td><b>${m.name}</b><span class="desc">${m.desc}</span></td>` +
    `<td><div class="cell"><span class="val">${Math.round(m.top1)}</span><span class="bar good" style="width:${(m.top1 - 50) * 3}px"></span>` +
    `<span class="ci">${Math.round(m.top1_lo)}–${Math.round(m.top1_hi)}</span></div></td>` +
    `<td><div class="cell"><span class="val">${m.far.toFixed(1)}</span><span class="bar bad" style="width:${(m.far / maxFar) * 160}px"></span>` +
    `<span class="ci">${m.far_lo.toFixed(1)}–${m.far_hi.toFixed(1)}</span></div></td>`;
  tbody.appendChild(tr);
}

const levels = ["0.01", "0.02", "0.05", "0.1", "0.2"];
const slider = document.getElementById("far");
const bars = document.getElementById("bars");
for (const m of J.methods) {
  const row = document.createElement("div");
  row.className = "brow" + (m.ours ? " ours" : "");
  row.innerHTML = `<span class="lbl">${m.name}</span><div class="track"><div class="fill"></div></div><span class="pct"></span>`;
  bars.appendChild(row);
  m.row = row;
}
function draw() {
  const t = levels[slider.value];
  document.getElementById("farlabel").textContent = Math.round(parseFloat(t) * 100);
  for (const m of J.methods) {
    const v = m.curve[t];
    m.row.querySelector(".fill").style.width = v + "%";
    m.row.querySelector(".pct").textContent = v + "%";
  }
}
slider.addEventListener("input", draw);
draw();

document.querySelectorAll(".copy").forEach((b) => b.addEventListener("click", () => {
  navigator.clipboard.writeText(document.getElementById(b.dataset.target).textContent);
  b.textContent = "Copied";
  setTimeout(() => { b.textContent = "Copy"; }, 1500);
}));
