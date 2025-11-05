#!/bin/bash
# Jogosultságok hozzáadása a BigQuery service account-hoz

echo "Jogosultságok hozzáadása..."
echo ""

# BigQuery Data Viewer
echo "1. BigQuery Data Viewer hozzáadása..."
gcloud projects add-iam-policy-binding affable-album-354309 \
    --member="serviceAccount:nudge-hackathob@affable-album-354309.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"

echo ""

# BigQuery Job User
echo "2. BigQuery Job User hozzáadása..."
gcloud projects add-iam-policy-binding affable-album-354309 \
    --member="serviceAccount:nudge-hackathob@affable-album-354309.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

echo ""
echo "✅ Kész! Várj 1-2 percet, majd teszteld:"
echo "   python lista_mindent.py"
