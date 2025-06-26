#!/usr/bin/env python3
"""Create combined event display with heatmaps and waveforms."""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import uproot

from utils.channel_map import buildDRSBoards

DT_NS = 1.0  # ADC sampling interval in ns


def load_waveforms(root_file, event_number, tree_name="EventTree", run_number=624):
    """Return scintillator and Cherenkov waveforms for a single event."""
    boards = buildDRSBoards(run=run_number)
    scint, cer = {}, {}
    with uproot.open(root_file) as f:
        tree = f[tree_name]
        for board in boards.values():
            for ch in board.GetListOfChannels():
                name = ch.GetChannelName()
                arr = tree[name].array(entry_start=event_number,
                                        entry_stop=event_number + 1,
                                        library="np")[0]
                info = {"waveform": arr, "x": ch.iTowerX, "y": ch.iTowerY}
                if ch.isCer:
                    cer[name] = info
                else:
                    scint[name] = info
    return scint, cer


def plot_event(event_number, root_file, heatmap_dir="plots/Run624/event_display",
               out_dir="combined_events", run_number=624):
    """Create and save combined figure for a single event."""
    os.makedirs(out_dir, exist_ok=True)

    scint_wfs, cer_wfs = load_waveforms(root_file, event_number,
                                        run_number=run_number)

    sci_img = mpimg.imread(os.path.join(
        heatmap_dir, f"event_display_Evt{event_number}_Sci.png"))
    cer_img = mpimg.imread(os.path.join(
        heatmap_dir, f"event_display_Evt{event_number}_Cer.png"))

    time_axis = np.arange(len(next(iter(scint_wfs.values()))["waveform"])) * DT_NS

    def max_channel(wfs):
        best_name, best_peak, best_info = "", -np.inf, None
        for name, info in wfs.items():
            peak = info["waveform"].max()
            if peak > best_peak:
                best_name, best_peak, best_info = name, peak, info
        return best_name, best_peak, best_info

    sci_name, sci_peak, sci_info = max_channel(scint_wfs)
    cer_name, cer_peak, cer_info = max_channel(cer_wfs)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    axes[0, 0].imshow(sci_img)
    axes[0, 0].set_title(f"Scintillator Heatmap, evt {event_number}")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(cer_img)
    axes[0, 1].set_title(f"Cherenkov Heatmap, evt {event_number}")
    axes[0, 1].axis("off")

    axes[1, 0].plot(time_axis, sci_info["waveform"])
    axes[1, 0].set_xlabel("Time (ns)")
    axes[1, 0].set_ylabel("ADC counts")
    axes[1, 0].set_title(f"Scintillator {sci_name}")

    axes[1, 1].plot(time_axis, cer_info["waveform"], color="C1")
    axes[1, 1].set_xlabel("Time (ns)")
    axes[1, 1].set_title(f"Cherenkov {cer_name}")

    def add_inset(ax, info, name, peak):
        width = 2
        height = 2
        x = info["x"]
        y = info["y"]
        inset_ax = inset_axes(ax, width=width, height=height,
                              bbox_to_anchor=(x - width/2, y - height/2, width, height),
                              bbox_transform=ax.transData, loc="lower left")
        inset_ax.plot(time_axis, info["waveform"], color="C3")
        inset_ax.set_xticks([])
        inset_ax.set_yticks([])
        inset_ax.set_title(f"{name}\n{peak:.1f}", fontsize=8)

    add_inset(axes[0, 0], sci_info, sci_name, sci_peak)
    add_inset(axes[0, 1], cer_info, cer_name, cer_peak)

    plt.tight_layout()
    out_png = os.path.join(out_dir, f"combined_event{event_number:03d}.png")
    fig.savefig(out_png)
    plt.close(fig)
    print(f"Saved {out_png}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plot combined event display")
    parser.add_argument("root_file", help="Input ROOT file")
    parser.add_argument("event_number", type=int, help="Event index")
    parser.add_argument("--heatmap-dir", default="plots/Run624/event_display",
                        dest="heatmap_dir", help="Directory with heatmap PNGs")
    parser.add_argument("--out-dir", default="combined_events",
                        dest="out_dir", help="Output directory")
    parser.add_argument("--run", dest="run", default=624, type=int,
                        help="Run number for channel map")

    args = parser.parse_args()

    plot_event(args.event_number, args.root_file,
               heatmap_dir=args.heatmap_dir,
               out_dir=args.out_dir, run_number=args.run)
