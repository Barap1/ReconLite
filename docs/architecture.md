# Architecture

ReconLite is a local/authorized network reconnaissance dashboard. The pipeline is:

```text
Input scope -> Masscan discovery -> SSL certificate enrichment -> async HTTP probing -> MongoDB storage -> Flask search dashboard
```

## Scanner Flow

1. Operators add an approved private/local scope through the dashboard.
2. The server stores that scope in `ips.txt`.
3. The scanner runs Masscan against the approved scope list.
4. The scanner reads Masscan output from `masscanResults.txt`.
5. For discovered hosts, it fetches TLS certificates on port `443` and extracts the certificate common name.
6. It probes HTTP/HTTPS targets by IP and, when appropriate, by certificate domain name.
7. It parses response titles, headers, redirect targets, and response snippets.
8. It posts batches to the Flask `/insert` endpoint.

## Server Flow

`server/server.py` provides the local dashboard and JSON API. It handles:

- Scope submission through `/add_ip`.
- Scanner startup through `/scan`.
- Scanner stop requests through `/scanstop`.
- Status polling through `/scanstatus` and `/scanchunks`.
- Search routes backed by MongoDB.
- Destructive collection deletion through `/delete` and `/perform_delete`.
- Basic health metadata through `/health`.

## Database Flow

MongoDB stores scanner result documents in the configured database and collection:

- `MONGO_URI`, default `mongodb://localhost:27017/`
- `DATABASE_NAME`, default `scannerdb`
- `COLLECTION_NAME`, default `sslchecker`

Records include top-level `ip` and `ports` fields plus nested response documents such as:

- `http_responseForIP`
- `https_responseForIP`
- `http_responseForDomainName`
- `https_responseForDomainName`

## Frontend Flow

The dashboard in `server/templates/index.html` uses Bootstrap and browser JavaScript. It:

- Submits scan configuration.
- Adds approved scopes.
- Polls scan status and processed chunks.
- Links to delete confirmation.
- Builds search URLs for title, domain, IP, port, header value, and header key searches.

## Status Tracking

The server writes lightweight local status files:

- `status.json`: scanner running state and start time.
- `chunks_processed.json`: count of inserted result batches.

These files are intentionally ignored by git.

## Why Demo Mode Exists

Demo mode lets reviewers evaluate the dashboard and API without running Masscan or scanning any network. It uses safe sample data under `sample_data/` and is the recommended default for portfolio review.
