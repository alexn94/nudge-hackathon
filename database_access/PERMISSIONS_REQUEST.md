# BigQuery Jogosultság Kérelem

## Service Account
**Email**: `nudge-hackathob@affable-album-354309.iam.gserviceaccount.com`

## Kért szerepkörök

Kérem, add hozzá a következő szerepköröket a fenti service account-hoz a `affable-album-354309` projektben:

### 1. BigQuery Job User
- **Szerepkör ID**: `roles/bigquery.jobUser`
- **Miért szükséges**: Query-k futtatásához (SELECT, INSERT, stb.)
- **Jogosultságok**: 
  - `bigquery.jobs.create` - Query job létrehozása
  - `bigquery.jobs.get` - Job állapot lekérdezése

### 2. BigQuery Data Viewer
- **Szerepkör ID**: `roles/bigquery.dataViewer`
- **Miért szükséges**: Táblák és adatok olvasásához
- **Jogosultságok**:
  - `bigquery.datasets.get` - Dataset metaadatok olvasása
  - `bigquery.tables.get` - Tábla metaadatok olvasása  
  - `bigquery.tables.getData` - Tábla adatok olvasása
  - `bigquery.tables.list` - Táblák listázása

## Hogyan add hozzá (Google Cloud Console)

1. Menj a [IAM & Admin oldalra](https://console.cloud.google.com/iam-admin/iam?project=affable-album-354309)
2. Keresd meg a service account-ot: `nudge-hackathob@affable-album-354309.iam.gserviceaccount.com`
3. Kattints a **pencil icon** (szerkesztés) gombra
4. Kattints **"ADD ANOTHER ROLE"**
5. Válaszd ki: **"BigQuery Job User"**
6. Kattints újra **"ADD ANOTHER ROLE"**
7. Válaszd ki: **"BigQuery Data Viewer"**
8. Kattints **"SAVE"**

## Hogyan add hozzá (gcloud CLI)

```bash
# BigQuery Job User
gcloud projects add-iam-policy-binding affable-album-354309 \
    --member="serviceAccount:nudge-hackathob@affable-album-354309.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

# BigQuery Data Viewer
gcloud projects add-iam-policy-binding affable-album-354309 \
    --member="serviceAccount:nudge-hackathob@affable-album-354309.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

## Ellenőrzés

A változtatások propagálása után (1-2 perc) tesztelhető:

```bash
python3 download_and_load_bigquery.py
```

## Jelenleg használt workaround

Addig amíg ezek a jogosultságok nincsenek meg, a `download_bigquery_direct.py` script működik, mert az közvetlenül olvassa a táblát query job létrehozása nélkül:

```bash
python3 download_bigquery_direct.py  # Ez működik jogosultság nélkül is
```

## Kapcsolat

Ha kérdésed van, írj nekem!
