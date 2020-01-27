gcloud \
  sql instances \
  create myinstance \
  --database-version=POSTGRES_11 \
  --cpu=2 \
  --memory=7680MiB \
  --region="asia-northeast1"