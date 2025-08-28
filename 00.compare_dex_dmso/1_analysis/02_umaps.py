"""Make UMAP scatterplots of the normalized data."""

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import umap
from sklearn.preprocessing import StandardScaler

def main() -> None:

    input_file = Path("../2_outputs/proc_data/normalized_filtered.parquet")
    output_dir = Path("../2_outputs/figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(input_file)

    # Separate features and metadata
    feature_cols = [col for col in df.columns if not col.startswith("Metadata")]
    metadata_cols = [col for col in df.columns if col.startswith("Metadata")]

    features = df[feature_cols]
    metadata = df[metadata_cols]

    # Standardize the features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Compute UMAP
    reducer = umap.UMAP(random_state=42)
    embedding = reducer.fit_transform(features_scaled)

    # Create a DataFrame for the UMAP results
    umap_df = pd.DataFrame(embedding, columns=["UMAP1", "UMAP2"])
    umap_df = pd.concat([umap_df, metadata.reset_index(drop=True)], axis=1)

    # Plot UMAP colored by a metadata column (e.g., Metadata_Media)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x="UMAP1",
        y="UMAP2",
        hue="Metadata_Media",
        data=umap_df,
        palette="tab10",
        alpha=0.7,
        s=50,
        edgecolor=None
    )
    plt.title("UMAP of Normalized Filtered Features")
    plt.legend(title="Media", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_dir / "umap_by_media.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x="UMAP1",
        y="UMAP2",
        hue="Metadata_Batch",
        data=umap_df,
        palette="tab10",
        alpha=0.7,
        s=50,
        edgecolor=None
    )
    plt.title("UMAP of Normalized Filtered Features")
    plt.legend(title="Batch", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_dir / "umap_by_batch.png", dpi=300)
    plt.close()

    # Plot UMAP colored by continuous Metadata_Count_Cells
    plt.figure(figsize=(10, 8))
    scatter = sns.scatterplot(
        x="UMAP1",
        y="UMAP2",
        hue="Metadata_Count_Cells",
        data=umap_df,
        palette="viridis",
        alpha=0.7,
        s=50,
        edgecolor=None,
        legend=False
    )
    cbar = plt.colorbar(scatter.collections[0], ax=plt.gca(), label="Count Cells")
    plt.title("UMAP colored by Metadata_Count_Cells")
    plt.tight_layout()
    plt.savefig(output_dir / "umap_by_count_cells.png", dpi=300)
    plt.close()

    # --- UMAP of DMSO only ---
    dmso_df = df.loc[df["Metadata_control_type"] == "negcon", :]
    features = dmso_df[feature_cols]
    metadata = dmso_df[metadata_cols]

    # Standardize the features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Compute UMAP
    reducer = umap.UMAP(random_state=42)
    embedding = reducer.fit_transform(features_scaled)

    # Create a DataFrame for the UMAP results
    umap_df = pd.DataFrame(embedding, columns=["UMAP1", "UMAP2"])
    umap_df = pd.concat([umap_df, metadata.reset_index(drop=True)], axis=1)

    # Plot UMAP colored by a metadata column (e.g., Metadata_Media)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x="UMAP1",
        y="UMAP2",
        hue="Metadata_Media",
        data=umap_df,
        palette="tab10",
        alpha=0.7,
        s=50,
        edgecolor=None
    )
    plt.title("UMAP of Solvent Controls")
    plt.legend(title="Media", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_dir / "umap_by_media_solvent_ctrls.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x="UMAP1",
        y="UMAP2",
        hue="Metadata_Plate",
        data=umap_df,
        palette="tab10",
        alpha=0.7,
        s=50,
        edgecolor=None
    )
    plt.title("UMAP of Solvent Controls")
    plt.legend(title="Plate", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_dir / "umap_by_plate_solvent_ctrls.png", dpi=300)
    plt.close()

    # --- UMAP per Metadata_Media, colored by Metadata_Count_Cells ---
    for treatment, split_df in df.groupby("Metadata_Media"):
        features_split = split_df[feature_cols]
        metadata_split = split_df[metadata_cols]
        # Standardize features for this split
        scaler_split = StandardScaler()
        features_scaled_split = scaler_split.fit_transform(features_split)
        # Compute UMAP for this split
        reducer_split = umap.UMAP(random_state=42)
        embedding_split = reducer_split.fit_transform(features_scaled_split)
        # Create DataFrame for UMAP results
        umap_split_df = pd.DataFrame(embedding_split, columns=["UMAP1", "UMAP2"])
        umap_split_df = pd.concat([umap_split_df, metadata_split.reset_index(drop=True)], axis=1)

        # Plot cell count
        plt.figure(figsize=(10, 8))
        scatter = sns.scatterplot(
            x="UMAP1",
            y="UMAP2",
            hue="Metadata_Count_Cells",
            data=umap_split_df,
            palette="viridis",
            alpha=0.7,
            s=50,
            edgecolor=None,
            legend=False
        )
        plt.colorbar(scatter.collections[0], ax=plt.gca(), label="Count Cells")
        plt.title(f"UMAP for {treatment} colored by Metadata_Count_Cells")
        plt.tight_layout()
        fname = f"umap_by_count_cells_{treatment}.png".replace("/", "-")
        plt.savefig(output_dir / fname, dpi=300)
        plt.close()

        # Plot compound
        plt.figure(figsize=(10, 8))
        scatter = sns.scatterplot(
            x="UMAP1",
            y="UMAP2",
            hue="Metadata_Compound",
            data=umap_split_df,
            palette="tab10",
            alpha=0.7,
            s=50,
            edgecolor=None,
            legend=False
        )
        plt.title(f"UMAP for {treatment} colored by Metadata_Compound")
        plt.tight_layout()
        fname = f"umap_by_compound_{treatment}.png".replace("/", "-")
        plt.savefig(output_dir / fname, dpi=300)
        plt.close()

if __name__ == "__main__":
    main()