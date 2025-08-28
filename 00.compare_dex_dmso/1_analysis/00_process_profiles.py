"""Combine Cell Painting CSVs across batches, add metadata, and save as a single Parquet file."""

from pathlib import Path
import pandas as pd


def main() -> None:
    """Load, annotate, and combine Cell Painting profiles from batch folders."""
    input_root = Path("../0_inputs/profiles")
    input_meta = Path("../0_inputs/OASIS_BRDID_MAP.csv")
    output_file = Path("../2_outputs/proc_data/normalized.parquet")
    dfs = []

    for batch_dir in input_root.iterdir():
        if not batch_dir.is_dir():
            continue

        batch_name = batch_dir.name
        plate_files = sorted(batch_dir.glob("*.csv.gz"))

        plate_ids = [f.stem.split("_")[0] for f in plate_files]
        plate_nums = [int(pid.replace("BR", "")) for pid in plate_ids]

        # Assign treatments: smaller plate number → DMSO, larger → DMSO_DEX
        treatments = {min(plate_nums): "DMSO", max(plate_nums): "DEX"}

        for file, pid, num in zip(plate_files, plate_ids, plate_nums):
            df = pd.read_csv(file)
            df = df.assign(
                Metadata_Batch=batch_name,
                Metadata_Plate=pid,
                Metadata_Media=treatments[num],
            )
            dfs.append(df)

    df_combined = pd.concat(dfs, ignore_index=True)

    oasis_id = pd.read_csv(input_meta)[["OASIS_ID", "BROAD_ID", "PREFERRED_NAME"]].rename(
        columns={
            "OASIS_ID": "Metadata_OASIS_ID",
            "BROAD_ID": "Metadata_batch_id",
            "PREFERRED_NAME": "Metadata_PREFERRED_NAME"
        }
    )

    # Left join on Metadata_batch_id
    df_combined = df_combined.merge(
        oasis_id,
        on="Metadata_batch_id",
        how="left"
    )

    # Create compound label
    df_combined["Metadata_Compound"] = df_combined["Metadata_PREFERRED_NAME"]
    df_combined.loc[df_combined["Metadata_control_type"] == "negcon", "Metadata_Compound"] = "NegCon"
    df_combined["Metadata_Compound"] = df_combined["Metadata_Compound"].fillna(df_combined["Metadata_OASIS_ID"])
    df_combined["Metadata_Compound"] = df_combined["Metadata_Compound"].fillna(df_combined["Metadata_batch_id"])
    df_combined["Metadata_Treatment"] = (
        df_combined["Metadata_Compound"].astype(str) + "_" + df_combined["Metadata_Media"].astype(str)
    )

    # Move Metadata_ columns to the front
    metadata_cols = [c for c in df_combined.columns if c.startswith("Metadata_")]
    other_cols = [c for c in df_combined.columns if not c.startswith("Metadata_")]
    df_combined = df_combined[metadata_cols + other_cols]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_combined.to_parquet(output_file, index=False)


if __name__ == "__main__":
    main()
