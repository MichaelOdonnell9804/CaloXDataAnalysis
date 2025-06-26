#!/usr/bin/env python3
import os, glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import uproot

# ── CONFIG ───────────────────────────────────────────────────────
root_file      = "run0624_250611172809.root"
tree_name      = "EventTree"
branch_sci     = "DRS_Board0_Group0_Channel0"
branch_cer     = "DRS_Board0_Group0_Channel1"
dt_ns          = 1.0         # ADC sampling interval

pulse_dir      = "interesting_events"
heatmap_dir    = "html/event_display"
out_dir        = "combined_events"
os.makedirs(out_dir, exist_ok=True)

# ── LOAD ALL WAVEFORMS ────────────────────────────────────────────
with uproot.open(root_file) as f:
    tree     = f[tree_name]
    scint_wfs = np.vstack(tree[branch_sci].array(library="np"))
    cer_wfs   = np.vstack(tree[branch_cer].array(library="np"))

time_axis = np.arange(scint_wfs.shape[1]) * dt_ns

# ── BUILD COMBINED FIGURES ────────────────────────────────────────
for pulse_png in sorted(glob.glob(f"{pulse_dir}/event_*.png")):
    # extract event index from filename
    evt = int(os.path.basename(pulse_png).split("_")[1].split(".")[0])

    # load heatmaps (you may need to tweak these filenames)
    sci_hm = mpimg.imread(f"{heatmap_dir}/event_display_Evt{evt}_Sci.png")
    cer_hm = mpimg.imread(f"{heatmap_dir}/event_display_Evt{evt}_Cer.png")

    # make 2×2 figure
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), 
                             gridspec_kw={"height_ratios":[1,1]})

    # top row: heatmaps
    axes[0,0].imshow(sci_hm); axes[0,0].axis("off")
    axes[0,0].set_title(f"Scintillator Heatmap, evt {evt}")
    axes[0,1].imshow(cer_hm); axes[0,1].axis("off")
    axes[0,1].set_title(f"Cherenkov Heatmap, evt {evt}")

    # bottom row: pulses
    axes[1,0].plot(time_axis, scint_wfs[evt])
    axes[1,0].set_title("Scintillator Pulse")
    axes[1,0].set_xlabel("Time (ns)")
    axes[1,0].set_ylabel("ADC counts")

    axes[1,1].plot(time_axis, cer_wfs[evt])
    axes[1,1].set_title("Cherenkov Pulse")
    axes[1,1].set_xlabel("Time (ns)")

    plt.tight_layout()
    out_png = f"{out_dir}/combined_evt{evt:04d}.png"
    fig.savefig(out_png)
    plt.close(fig)
    print(f"→ saved {out_png}")

print("All done!")
