#!/usr/bin/env bash
declare -a BUCKET="asia-southeast1-airflow-dev-c77b25f3-bucket"
declare -a FOLDERS=(dags plugins)

# Begin the sync
echo "Sync to gs://$BUCKET"

for FOLDER in "${FOLDERS[@]}"; do  
  COMMAND="gsutil -m rsync -d -r $FOLDER gs://$BUCKET/$FOLDER"
  echo "-----Syncing folder '$FOLDER'"
  eval $COMMAND
done

echo "-----Done syncing on $(date -u)"