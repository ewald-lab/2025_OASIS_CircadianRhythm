"""Remove Image and correlated features, and save as a single Parquet file."""

from pathlib import Path
import pandas as pd
from pycytominer.feature_select import feature_select

def main() -> None:
    input_file = Path("../2_outputs/proc_data/normalized.parquet")
    output_file = Path("../2_outputs/proc_data/normalized_filtered.parquet")

    df_combined = pd.read_parquet(input_file)

    # Remove Image features
    df_filtered = df_combined.loc[:, ~df_combined.columns.str.startswith("Image")]

    # Filter out correlated and low-variance features
    selected_features = feature_select(
        profiles=df_filtered,
        features='infer',
        image_features=False,
        samples='all',
        operation=[
            'variance_threshold',
            'correlation_threshold',
            'drop_na_columns'
        ],
        na_cutoff=0.05,
        corr_threshold=0.9,
        corr_method='pearson',
        output_file=None,
    )

    # Drop missing columns
    missing_cols = selected_features.columns[selected_features.isnull().any()]
    selected_features = selected_features.drop(columns=[i for i in missing_cols if "Metadata" not in i])

    selected_features.to_parquet(output_file, index=False)


if __name__ == "__main__":
    main()
