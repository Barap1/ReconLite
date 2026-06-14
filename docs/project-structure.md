# Project Structure

```text
.
├── .env.example
├── .github/
│   └── workflows/
├── .tours/
│   └── server.tour
├── Dockerfile
├── docker-compose.yml
├── docs/
├── info
├── README.md
├── reconlite_utils.py
├── requirements.txt
├── requirements-dev.txt
├── sample_data/
│   └── demo_results.json
├── scanner.py
├── scripts/
│   └── load_demo_data.py
├── server/
│   ├── server.py
│   └── templates/
│       ├── 404.html
│       ├── delete_confirmation.html
│       └── index.html
└── tests/
```

## Major Files

- `README.md`: Portfolio-facing overview, setup, safety notice, and links to deeper docs.
- `info`: Embedded image rendered near the top of the README.
- `scanner.py`: Masscan, certificate extraction, async HTTP probing, parsing, and result submission.
- `server/server.py`: Flask dashboard, API routes, MongoDB connection, scan control, and status tracking.
- `reconlite_utils.py`: Pure validation helpers for ports, integers, scan scopes, and scanner command construction.
- `sample_data/demo_results.json`: Safe sample records for dashboard and API demos.
- `scripts/load_demo_data.py`: MongoDB loader for sample data.
- `Dockerfile` and `docker-compose.yml`: Demo/dashboard environment with Flask and MongoDB.
- `requirements.txt`: Runtime Python dependencies.
- `requirements-dev.txt`: Test/development dependencies.
- `docs/`: Architecture, API, safety, Docker, demo, search, audit, and final-summary docs.
- `tests/`: Lightweight CI-safe tests.

## Generated Runtime Files

The app may create local runtime files that are ignored by git:

- `ips.txt`
- `masscanResults.txt`
- `status.json`
- `chunks_processed.json`
- `outputs/`
- `tmp/`
- `temp/`
