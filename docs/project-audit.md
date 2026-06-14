# Project Audit and Improvement Plan

## Current files and structure

- `README.md`: Short setup and usage notes for the original Shodan-style recon engine. It embeds the top project image with centered HTML:
  - `<h1 align="center">Shodan Style Recon Engine</h1>`
  - `<div align="center"><img src="info" alt="Information about my project"></div>`
- `info`: Embedded README image file. This file must remain in the repository so the README image continues to render.
- `info1` and `old-info`: Additional image/reference assets.
- `scanner.py`: Python scanner pipeline using Masscan, OpenSSL certificate extraction, asynchronous HTTP probing, BeautifulSoup parsing, and POST insertion back into the Flask server.
- `server/server.py`: Flask dashboard and JSON API backed by MongoDB.
- `server/templates/index.html`: Bootstrap-based dashboard for scan controls, adding scopes, searching, and status polling.
- `server/templates/delete_confirmation.html`: Confirmation page that calls the delete API.
- `server/templates/404.html`: Simple not-found page.
- `.tours/server.tour`: CodeTour walkthrough describing the original scan/server flow.
- `.vscode/settings.json`: Editor settings.
- `.gitignore`: Existing ignore file.
- `LICENSE`: MIT license.

## What `scanner.py` does

`scanner.py` defines `SSLChecker`, which:

1. Creates `ips.txt` and `masscanResults.txt` if they are missing.
2. Runs Masscan against the configured input file, currently targeting SSL port `443`.
3. Reads Masscan output and extracts IP addresses with a regular expression.
4. Fetches TLS certificates from discovered IPs and extracts the certificate common name with `pyOpenSSL`.
5. Uses `aiohttp` to probe HTTP and HTTPS by IP and, when a certificate common name looks like a valid domain, by domain.
6. Parses HTML, XML, plain text, and JSON responses for titles, headers, redirects, and response snippets.
7. Posts collected result batches to the Flask server `/insert` endpoint for MongoDB storage.

## What `server/server.py` does

`server/server.py` starts a Flask app with:

- A home route rendering the Bootstrap dashboard.
- `/insert` for receiving scanner batches and inserting them into MongoDB.
- `/add_ip` for appending user-submitted scopes to `../ips.txt`.
- Search routes for title, domain, IP, port, header values, and header keys.
- Delete routes for removing all records from the MongoDB collection.
- Scan control routes for launching the scanner subprocess, stopping it, reporting status, and reporting processed chunks.

The server also writes local status files:

- `status.json`: Tracks whether a scanner process is running and when it started.
- `chunks_processed.json`: Tracks how many scanner result batches were inserted.

## What the templates do

- `index.html` provides the scan form, add-scope form, status display, stop/delete controls, search selector, and client-side JavaScript for calling Flask endpoints.
- `delete_confirmation.html` confirms destructive collection deletion and calls `DELETE /perform_delete`.
- `404.html` gives a simple return-to-home action for unmatched paths.

## How MongoDB is used

The server creates a `MongoClient` with the hardcoded URI `mongodb://localhost:27017/`, then uses database `scannerdb` and collection `sslchecker`. Scanner result batches are inserted with `insert_many`. Search endpoints query the same collection and return JSON with:

- `total_entries`
- `entries`

## How Masscan is invoked

`scanner.py` currently builds a string command:

```text
sudo masscan -p443 --rate <rate> --wait 0 -iL <ips_file> -oH <results_file>
```

It then runs that command with `subprocess.run(..., shell=True, check=True)`.

The Flask server currently builds another string command to launch `scanner.py` and runs it with `subprocess.Popen(..., shell=True, ...)`. This is a rough edge because form inputs are included in a shell command string.

## How the README image is embedded

The README embeds the `info` file near the top using centered HTML:

```html
<h1 align="center">Shodan Style Recon Engine</h1>

<div align="center">
<img src="info" alt="Information about my project">
</div>
```

The improved README should preserve this centered image pattern and keep `info` in the repository.

## Current risks and rough edges

- The project is framed broadly as vulnerability analysis and penetration testing without enough safety-first scope language.
- The roadmap includes "Test with bug bounties", which should be replaced with safer authorization/scope-management language.
- Public scan safety defaults are not enforced.
- `/add_ip` accepts arbitrary input and appends it directly to `ips.txt`.
- `/scan` accepts scanner parameters directly from a form and uses them in a shell command string.
- The scanner server launch uses `shell=True`.
- The scanner Masscan invocation also uses `shell=True`.
- MongoDB URI, database, and collection names are hardcoded.
- No demo mode or safe sample data exists for reviewers.
- No Docker Compose path exists for running the dashboard with MongoDB.
- No lightweight tests exist around safe parsing or demo data.
- API, architecture, safety, and project structure docs are missing.
- UI language does not clearly state that scanning must be limited to systems and networks the operator owns or has explicit permission to test.

## Approved improvement plan

1. Rebrand the project as ReconLite: Shodan-Style Local Recon Engine.
2. Add safety-first language throughout README, docs, and dashboard UI.
3. Add demo data and a loader so reviewers can try search flows without scanning.
4. Add Docker Compose for Flask and MongoDB in dashboard/demo mode.
5. Add environment-driven configuration for MongoDB and safety flags.
6. Add helper utilities for port parsing, numeric input validation, private/local scope validation, and list-based scanner command construction.
7. Replace the server-side scanner launch command with list-based subprocess arguments and no `shell=True`.
8. Add scope validation before writing submitted scopes to `ips.txt`.
9. Add lightweight tests for utility helpers and sample data shape.
10. Rewrite the README while preserving the centered `info` image.
11. Add architecture, API, safety, Docker, demo, search examples, and project structure docs.
12. Improve the Bootstrap UI messaging without rebuilding the frontend or introducing React.
13. Avoid running Masscan, public scans, or CI jobs that require MongoDB or Masscan.
