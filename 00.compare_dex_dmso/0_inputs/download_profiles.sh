#!/usr/bin/env bash

BASE_URL="https://cellpainting-gallery.s3.amazonaws.com/cpg0037-oasis/broad/workspace/profiles"

# Define the batches and plate IDs
BATCHES=(
  "2025_04_14_OASIS_U2OS_Industry_Batch1"
  "2025_04_14_OASIS_U2OS_Industry_Batch3"
  "2025_04_14_OASIS_U2OS_Industry_Batch4"
)

PLATES_BATCH1=("BR00147142" "BR00147143")
PLATES_BATCH3=("BR00147152" "BR00147153")
PLATES_BATCH4=("BR00147157" "BR00147158")

OUTPUT_DIR="./profiles"

for BATCH in "${BATCHES[@]}"; do
  BATCH_DIR="${OUTPUT_DIR}/${BATCH}"
  mkdir -p "$BATCH_DIR"

  case $BATCH in
    "2025_04_14_OASIS_U2OS_Industry_Batch1") PLATES=("${PLATES_BATCH1[@]}");;
    "2025_04_14_OASIS_U2OS_Industry_Batch3") PLATES=("${PLATES_BATCH3[@]}");;
    "2025_04_14_OASIS_U2OS_Industry_Batch4") PLATES=("${PLATES_BATCH4[@]}");;
  esac

  for PLATE in "${PLATES[@]}"; do
    FILE_URL="${BASE_URL}/${BATCH}/${PLATE}/${PLATE}_normalized_feature_select_negcon_batch.csv.gz"
    DEST_FILE="${BATCH_DIR}/${PLATE}_normalized_feature_select_negcon_batch.csv.gz"

    if [ -f "$DEST_FILE" ]; then
      echo "Skipping $DEST_FILE (already exists)"
    else
      echo "Downloading ${FILE_URL} ..."
      curl -L -o "$DEST_FILE" "$FILE_URL"
    fi
  done

done
