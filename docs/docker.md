# Docker Compose Demo Environment

Docker Compose starts Flask and MongoDB for ReconLite dashboard and demo use.

```sh
docker compose up --build
```

Then load safe demo records:

```sh
docker compose exec web python scripts/load_demo_data.py --clear
```

Open:

```text
http://localhost:5000
```

## What Docker Runs

- `mongo`: official MongoDB image with a local named volume.
- `web`: ReconLite Flask app built from this repository.

The web container sets:

- `MONGO_URI=mongodb://mongo:27017/`
- `DATABASE_NAME=scannerdb`
- `COLLECTION_NAME=sslchecker`
- `DEMO_MODE=true`
- `ALLOW_PUBLIC_SCAN=false`

## Masscan in Docker

Real scanning with Masscan is not enabled by default in Docker. Masscan often needs elevated privileges and careful network configuration, and it can generate high traffic.

This Docker path is intentionally for dashboard and demo mode so reviewers can evaluate ReconLite without scanning real networks.
