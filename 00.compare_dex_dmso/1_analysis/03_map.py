"""Calculate phenotypic activity of compounds for each media type."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from copairs import map
from copairs.matching import assign_reference_index

def main() -> None:

    input_file = Path("../2_outputs/proc_data/normalized_filtered.parquet")
    output_fig_dir = Path("../2_outputs/figures")
    output_table_dir = Path("../2_outputs/tables")
    output_fig_dir.mkdir(parents=True, exist_ok=True)
    output_table_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(input_file)
    df["Metadata_Concentration_uM"] = df["Metadata_Concentration_uM"].fillna(0)

    df_dmso = df.query("Metadata_Media == 'DMSO'").copy()
    df_dex = df.query("Metadata_Media == 'DEX'").copy()

    reference_col = "Metadata_reference_index"

    # pairs are defined the same way for both datasets
    pos_sameby = ["Metadata_Treatment", reference_col]
    pos_diffby = []

    neg_sameby = []
    neg_diffby = ["Metadata_Treatment", reference_col]

    # --- mAP of DMSO only ---
    df_dmso_activity = assign_reference_index(
        df_dmso,
        "Metadata_Treatment == 'NegCon_DMSO'",  # condition to get reference profiles (neg controls)
        reference_col=reference_col,
        default_value=-1,
    )

    # Calculate AP
    metadata = df_dmso_activity.filter(regex="^Metadata")
    profiles = df_dmso_activity.filter(regex="^(?!Metadata)").values

    activity_ap = map.average_precision(
        metadata, profiles, pos_sameby, pos_diffby, neg_sameby, neg_diffby
    )
    activity_ap = activity_ap.query("Metadata_Treatment != 'NegCon_DMSO'")  # remove DMSO
    activity_ap.to_csv(output_table_dir / "activity_ap_dmso.csv", index=False)

    # Calculate MAP
    activity_map = map.mean_average_precision(
        activity_ap, pos_sameby, null_size=1000000, threshold=0.05, seed=0
    )
    activity_map["-log10(p-value)"] = -activity_map["corrected_p_value"].apply(np.log10)
    activity_map.to_csv(output_table_dir / "activity_map_dmso.csv", index=False)

    # Plot results
    active_ratio = activity_map.below_corrected_p.mean()

    plt.figure(figsize=(5, 4))
    plt.scatter(
        data=activity_map,
        x="mean_average_precision",
        y="-log10(p-value)",
        c="below_corrected_p",
        cmap="tab10",
        s=10,
    )
    plt.title("Phenotypic activity assesement")
    plt.xlabel("mAP")
    plt.ylabel("-log10(p-value)")
    plt.axhline(-np.log10(0.05), color="black", linestyle="--")
    plt.text(
        0.65,
        1.5,
        f"Phenotypically active = {100 * active_ratio:.2f}%",
        va="center",
        ha="left",
    )
    plt.savefig(output_fig_dir / "phenotypic_activity_DMSO.png", dpi=300)
    plt.close()


    # --- mAP of DEX co-treatment ---
    df_dex_activity = assign_reference_index(
        df_dex,
        "Metadata_Treatment == 'NegCon_DEX'",  # condition to get reference profiles (neg controls)
        reference_col=reference_col,
        default_value=-1,
    )

    # Calculate AP
    metadata = df_dex_activity.filter(regex="^Metadata")
    profiles = df_dex_activity.filter(regex="^(?!Metadata)").values

    activity_ap = map.average_precision(
        metadata, profiles, pos_sameby, pos_diffby, neg_sameby, neg_diffby
    )
    activity_ap = activity_ap.query("Metadata_Treatment != 'NegCon_DEX'")  # remove DMSO
    activity_ap.to_csv(output_table_dir / "activity_ap_dex.csv", index=False)

    # Calculate MAP
    activity_map = map.mean_average_precision(
        activity_ap, pos_sameby, null_size=1000000, threshold=0.05, seed=0
    )
    activity_map["-log10(p-value)"] = -activity_map["corrected_p_value"].apply(np.log10)
    activity_map.to_csv(output_table_dir / "activity_map_dex.csv", index=False)

    # Plot results
    active_ratio = activity_map.below_corrected_p.mean()

    plt.figure(figsize=(5, 4))
    plt.scatter(
        data=activity_map,
        x="mean_average_precision",
        y="-log10(p-value)",
        c="below_corrected_p",
        cmap="tab10",
        s=10,
    )
    plt.title("Phenotypic activity assesement")
    plt.xlabel("mAP")
    plt.ylabel("-log10(p-value)")
    plt.axhline(-np.log10(0.05), color="black", linestyle="--")
    plt.text(
        0.65,
        1.5,
        f"Phenotypically active = {100 * active_ratio:.2f}%",
        va="center",
        ha="left",
    )
    plt.savefig(output_fig_dir / "phenotypic_activity_DEX.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    main()