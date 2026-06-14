# API Documentation

All examples assume the Flask app is running at `http://localhost:5000`.

## `GET /`

Purpose: Render the ReconLite dashboard.

```sh
curl http://localhost:5000/
```

## `POST /add_ip`

Purpose: Add an authorized scan scope to `ips.txt`.

Form field:

- `ip_address`: private/local IP, CIDR, or `localhost` by default.

```sh
curl -X POST http://localhost:5000/add_ip \
  -d "ip_address=192.168.1.0/24"
```

Sample response:

```json
{"message": "Scan scope added successfully"}
```

## `POST /scan`

Purpose: Start the scanner subprocess with validated numeric options and ports.

Form fields:

- `masscan_rate`
- `timeout`
- `chunkSize`
- `ports`

```sh
curl -X POST http://localhost:5000/scan \
  -d "masscan_rate=1000" \
  -d "timeout=3" \
  -d "chunkSize=50" \
  -d "ports=80,443"
```

Sample response:

```json
{"message": "Scanner started successfully"}
```

## `GET /scanstatus`

Purpose: Return scanner state and elapsed time.

```sh
curl http://localhost:5000/scanstatus
```

Sample response:

```json
{"status": "running", "elapsed_time": 12}
```

## `GET /scanchunks`

Purpose: Return the number of inserted scanner chunks while a scan is running.

```sh
curl http://localhost:5000/scanchunks
```

Sample response:

```json
{"chunks_processed": 2}
```

## `POST /scanstop`

Purpose: Stop the current scanner process when one is running.

```sh
curl -X POST http://localhost:5000/scanstop
```

Sample response:

```json
{"message": "Scanner stopped successfully"}
```

## `GET /health`

Purpose: Return basic service and safety-mode metadata.

```sh
curl http://localhost:5000/health
```

Sample response:

```json
{
  "status": "ok",
  "demo_mode": true,
  "allow_public_scan": false
}
```

## `GET /bytitle?bytitle=nginx`

Purpose: Search nested response titles.

Query param:

- `bytitle`

```sh
curl "http://localhost:5000/bytitle?bytitle=nginx"
```

Sample response shape:

```json
{
  "total_entries": 1,
  "entries": [
    {
      "ip": "192.168.1.10",
      "ports": [{"port": 80}, {"port": 443}]
    }
  ]
}
```

## `GET /bydomain?bydomain=demo.local`

Purpose: Search nested response domain values.

Query param:

- `bydomain`

```sh
curl "http://localhost:5000/bydomain?bydomain=demo.local"
```

Sample response shape:

```json
{"total_entries": 1, "entries": [{"ip": "192.168.1.10"}]}
```

## `GET /byip?byip=192.168.1.10`

Purpose: Search by top-level IP.

Query param:

- `byip`

```sh
curl "http://localhost:5000/byip?byip=192.168.1.10"
```

Sample response shape:

```json
{"total_entries": 1, "entries": [{"ip": "192.168.1.10"}]}
```

## `GET /byport?byport=443`

Purpose: Search by discovered port.

Query param:

- `byport`

```sh
curl "http://localhost:5000/byport?byport=443"
```

Sample response shape:

```json
{"total_entries": 1, "entries": [{"ports": [{"port": 443}]}]}
```

## `GET /byhresponse?byhresponse=nginx`

Purpose: Search response header values.

Query param:

- `byhresponse`

```sh
curl "http://localhost:5000/byhresponse?byhresponse=nginx"
```

Sample response shape:

```json
{"total_entries": 1, "entries": [{"ip": "192.168.1.10"}]}
```

## `GET /byhkeyresponse?hkeyresponse=Content-Security-Policy`

Purpose: Search response header keys.

Query param:

- `hkeyresponse`

```sh
curl "http://localhost:5000/byhkeyresponse?hkeyresponse=Content-Security-Policy"
```

Sample response shape:

```json
{"total_entries": 1, "entries": [{"ip": "192.168.1.10"}]}
```

## `GET /delete`

Purpose: Render delete confirmation UI.

```sh
curl http://localhost:5000/delete
```

## `DELETE /perform_delete`

Purpose: Delete all documents from the configured MongoDB collection.

```sh
curl -X DELETE http://localhost:5000/perform_delete
```

Sample response:

```json
{"message": "Deleted 6 documents"}
```

## Pagination

Search routes accept optional `from` and `to` query params where implemented:

```sh
curl "http://localhost:5000/bytitle?bytitle=nginx&from=0&to=10"
```
