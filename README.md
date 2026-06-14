<h1 align="center">ReconLite: Shodan-Style Local Recon Engine</h1>

<div align="center">
<img src="info" alt="ReconLite architecture diagram">
</div>

## Overview

ReconLite is a safe, demoable Shodan-style reconnaissance dashboard for local and authorized network environments.

It keeps the original project concept: Masscan discovers hosts with open SSL services, Python enriches those hosts with certificate and HTTP metadata, MongoDB stores the results, and a Flask dashboard makes the data searchable.

Pipeline:

```text
Approved scope -> Masscan discovery -> SSL certificate CN extraction -> async HTTP/HTTPS probing -> MongoDB storage -> Flask dashboard search
```

Current stack:

- Python
- Flask
- MongoDB
- Masscan
- aiohttp
- pyOpenSSL
- BeautifulSoup
- Bootstrap, HTML, CSS, and JavaScript

## Safety Notice

Only scan systems and networks you own or have explicit permission to test.

ReconLite is intended for local labs, private networks, approved internal testing, and portfolio demonstrations. Public scanning is disabled by default with `ALLOW_PUBLIC_SCAN=false`.

## Features

- Local Flask dashboard for scan controls and search.
- MongoDB-backed result storage.
- Masscan-based discovery for authorized scopes.
- TLS certificate common name extraction.
- Async HTTP/HTTPS probing by IP and domain name.
- Title, domain, IP, port, response-header-value, and response-header-key search.
- Demo mode with safe sample data.
- Docker Compose demo environment with Flask and MongoDB.
- Lightweight tests for safe helper utilities and demo data shape.
- Safety-first scope validation for private/local defaults.

## Architecture

ReconLite has two main runtime pieces:

- `scanner.py`: runs Masscan, extracts certificate metadata, probes HTTP/HTTPS, parses responses, and posts result batches to Flask.
- `server/server.py`: serves the dashboard, validates scan inputs, launches the scanner, stores results in MongoDB, and exposes search APIs.

See [docs/architecture.md](docs/architecture.md) for the full flow.

## Demo Mode

Demo mode lets reviewers use the dashboard without scanning real networks.

```sh
docker compose up --build
docker compose exec web python scripts/load_demo_data.py --clear
```

Open:

```text
http://localhost:5000
```

Try searches such as:

- `nginx`
- `demo.local`
- `443`
- `Content-Security-Policy`

See [docs/demo-mode.md](docs/demo-mode.md).

## Quick Start with Docker

Docker Compose starts Flask and MongoDB for dashboard/demo use:

```sh
docker compose up --build
docker compose exec web python scripts/load_demo_data.py --clear
```

Open:

```text
http://localhost:5000
```

Real Masscan scanning is not enabled by default in Docker. This is intentional for safety and portability. See [docs/docker.md](docs/docker.md).

## Manual Local Setup

```sh
git clone https://github.com/Barap1/Shodan-Style-Recon-Engine.git
cd Shodan-Style-Recon-Engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start MongoDB, then load demo data:

```sh
python scripts/load_demo_data.py --clear
python server/server.py
```

Open:

```text
http://localhost:5000
```

Environment variables can be copied from `.env.example`:

```text
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=scannerdb
COLLECTION_NAME=sslchecker
DEMO_MODE=false
ALLOW_PUBLIC_SCAN=false
```

## Running Authorized Scans

Only scan systems and networks you own or have explicit permission to test.

1. Install Masscan on the host where `scanner.py` will run.
2. Start MongoDB.
3. Start the Flask server:

   ```sh
   python server/server.py
   ```

4. Open `http://localhost:5000`.
5. Add an approved private/local scope, such as `localhost`, `127.0.0.1`, or `192.168.1.0/24`.
6. Run the scanner with conservative rate, timeout, chunk size, and port settings.

Public scopes are rejected by default. Set `ALLOW_PUBLIC_SCAN=true` only for explicitly authorized scopes.

## Search API

ReconLite exposes JSON search endpoints:

- `GET /bytitle?bytitle=nginx`
- `GET /bydomain?bydomain=demo.local`
- `GET /byip?byip=192.168.1.10`
- `GET /byport?byport=443`
- `GET /byhresponse?byhresponse=nginx`
- `GET /byhkeyresponse?hkeyresponse=Content-Security-Policy`
- `GET /health`

See [docs/api.md](docs/api.md) and [docs/search-examples.md](docs/search-examples.md).

## Project Structure

Key files:

- `scanner.py`: Masscan and enrichment pipeline.
- `server/server.py`: Flask dashboard and API.
- `reconlite_utils.py`: Validation helpers.
- `sample_data/demo_results.json`: Safe demo records.
- `scripts/load_demo_data.py`: Demo data loader.
- `docs/`: Architecture, API, safety, Docker, demo, and structure docs.
- `tests/`: Lightweight CI-safe tests.

See [docs/project-structure.md](docs/project-structure.md).

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Safety](docs/safety.md)
- [Demo Mode](docs/demo-mode.md)
- [Docker](docs/docker.md)
- [Project Structure](docs/project-structure.md)
- [Project Audit](docs/project-audit.md)

## Limitations

- ReconLite is not a replacement for Shodan.
- ReconLite is not a vulnerability scanner by itself.
- Masscan requires care, permissions, and appropriate rate limits.
- Docker demo mode does not run real Masscan by default.
- The search schema is prototype-level and optimized for a portfolio/demo flow.
- The dashboard does not include a full authentication or authorization system.

## Future Improvements

- Richer service fingerprinting.
- Authentication for the dashboard.
- Role-based access to destructive actions.
- Import Nmap or Masscan result files.
- CSV and JSON export.
- Better scan job queue and history.
- Improved frontend results view.
- Authorization/scope management for approved test environments.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
