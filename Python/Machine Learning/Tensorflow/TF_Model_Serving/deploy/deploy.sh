gcloud \
  beta functions \
  deploy auto_deploy \
  --runtime python37 \
  --project disco-abacus-265000 \
  --region asia-northeast1 \
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=disco-abacus-265000-8cfc5503d74e.json \
  --memory 2048 \
  --timeout 540 \
  --trigger-http