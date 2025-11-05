#!/bin/bash
# Add BigQuery permissions to the service account

SERVICE_ACCOUNT="nudge-hackathob@affable-album-354309.iam.gserviceaccount.com"
PROJECT_ID="affable-album-354309"

echo "================================================"
echo "Adding BigQuery permissions to service account"
echo "================================================"
echo ""
echo "Service Account: $SERVICE_ACCOUNT"
echo "Project: $PROJECT_ID"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ ERROR: gcloud CLI is not installed"
    echo ""
    echo "Please install gcloud CLI or use Google Cloud Console to add permissions manually:"
    echo "  https://console.cloud.google.com/iam-admin/iam?project=$PROJECT_ID"
    echo ""
    echo "Required roles:"
    echo "  - roles/bigquery.jobUser"
    echo "  - roles/bigquery.dataViewer"
    exit 1
fi

echo "1. Adding BigQuery Job User role..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/bigquery.jobUser"

echo ""
echo "2. Adding BigQuery Data Viewer role..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/bigquery.dataViewer"

echo ""
echo "================================================"
echo "✅ Permissions added successfully!"
echo "================================================"
echo ""
echo "Wait 1-2 minutes for the changes to propagate, then test:"
echo "  python3 download_and_load_bigquery.py"
echo ""
