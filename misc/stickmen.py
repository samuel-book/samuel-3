"""Icon arrays: out of 100 people with a non-mild stroke, how many have a good outcome.

Absolute numbers come from: logit(p) = logit(BASELINE) + net benefit (log odds ratio),
with net-benefit values read by eye from the S-learner figure. BASELINE is the
assumed chance of a good outcome with no treatment - replace with your own figure.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

BASELINE = 0.25
# log odds ratio read from the curves at 2, 4 and 6 hours onset-to-thrombectomy
LOR = {"none": {2: 1.43, 4: 0.81, 6: 0.43},
       "ivt":  {2: 1.66, 4: 1.13, 6: 0.85}}

GOOD, BAD = "#1e8a3c", "#d2423f"
INK, MUTED, SURF = "#0b0b0b", "#52514e", "#fcfcfb"


def n_good(lor):
    lo = np.log(BASELINE / (1 - BASELINE)) + lor
    return int(round(100 / (1 + np.exp(-lo))))


def stickman(ax, x, y, good, s=1.0):
    c = GOOD if good else BAD
    lw = 1.6
    ax.add_patch(Circle((x, y + 0.30 * s), 0.11 * s, color=c, lw=0))
    ax.plot([x, x], [y + 0.19 * s, y - 0.08 * s], color=c, lw=lw, solid_capstyle="round")
    if good:   # arms raised
        ax.plot([x - 0.17 * s, x, x + 0.17 * s], [y + 0.25 * s, y + 0.10 * s, y + 0.25 * s], color=c, lw=lw)
    else:      # arms hanging down
        ax.plot([x - 0.14 * s, x, x + 0.14 * s], [y - 0.06 * s, y + 0.12 * s, y - 0.06 * s], color=c, lw=lw)
    ax.plot([x - 0.12 * s, x, x + 0.12 * s], [y - 0.34 * s, y - 0.08 * s, y - 0.34 * s], color=c, lw=lw,
            solid_capstyle="round")


def panel(ax, k, title):
    ax.set_xlim(-0.6, 9.6); ax.set_ylim(-0.7, 9.9); ax.set_aspect("equal"); ax.axis("off")
    for i in range(100):
        row, col = divmod(i, 10)
        stickman(ax, col, 9 - row, i < k)   # good outcomes fill from the top-left
    ax.set_title(title, fontsize=12.5, color=INK, pad=4, loc="left")
    ax.text(-0.4, -1.3, f"{k} recover well", color=GOOD, fontsize=13, fontweight="bold", ha="left")
    ax.text(9.4, -1.3, f"{100 - k} do not", color=BAD, fontsize=13, fontweight="bold", ha="right")


fig = plt.figure(figsize=(15, 9.4), dpi=200, facecolor=SURF)
gs = fig.add_gridspec(2, 4, left=0.02, right=0.99, top=0.80, bottom=0.08, wspace=0.14, hspace=0.42)

# No-treatment reference panel, centred vertically in the first column
ax0 = fig.add_subplot(gs[0, 0]); ax0.set_facecolor(SURF)
panel(ax0, n_good(0.0), "No treatment")

times = [2, 4, 6]
for r, key in enumerate(["none", "ivt"]):
    for c, t in enumerate(times):
        ax = fig.add_subplot(gs[r, c + 1]); ax.set_facecolor(SURF)
        panel(ax, n_good(LOR[key][t]), f"Clot removal at {t} hours")
        if c == 0:
            p = ax.get_position()
            lab = ["Clot removal only", "Clot-busting medicine within 2 hours, then clot removal"][r]
            fig.text(p.x0, p.y1 + 0.045, lab, fontsize=14.5, fontweight="bold", color=INK)
            fig.add_artist(plt.Line2D([p.x0, 0.99], [p.y1 + 0.037] * 2, color="#c9c8c3", lw=1))


fig.text(0.02, 0.965, "Out of 100 people with a serious stroke, how many recover well?",
         fontsize=19, fontweight="bold", color=INK)
fig.text(0.02, 0.925,
         "Faster clot removal means more people recover well. Clot-busting medicine first adds a few more - "
         "but delay to clot removal costs about the same either way.",
         fontsize=12.5, color=MUTED)
# Key
kx, ky = 0.04, 0.20
axk = fig.add_axes([kx, ky, 0.14, 0.16]); axk.set_xlim(0, 4); axk.set_ylim(0, 3); axk.axis("off")
stickman(axk, 0.4, 2.2, True, 1.4); axk.text(0.9, 2.2, "Recovers\nwell", va="center", fontsize=11, color=INK)
stickman(axk, 0.4, 0.7, False, 1.4); axk.text(0.9, 0.7, "Does not\nrecover well", va="center", fontsize=11, color=INK)
fig.text(0.02, 0.03, f"Illustrative figures, based on S-Learner predictions.",
         fontsize=10, color=MUTED)

fig.savefig("stickmen_scenarios.png", facecolor=SURF)
#fig.savefig("stickmen_scenarios.svg", facecolor=SURF)
for key in LOR:
    print(key, {t: n_good(v) for t, v in LOR[key].items()})
print("none", n_good(0))
