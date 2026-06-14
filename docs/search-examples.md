# Search Examples

These examples assume demo data has been loaded:

```sh
python scripts/load_demo_data.py --clear
python server/server.py
```

Open the UI at:

```text
http://localhost:5000
```

## Demo Records

The sample dataset includes safe fake records such as:

- `192.168.1.10` with title `Example Nginx Server` and domain `demo.local`
- `192.168.1.20` with title `Intranet Portal` and domain `intranet.local`
- `10.0.0.15` with title `Staging API Console` and domain `staging.internal`
- `127.0.0.1` with title `Local Flask Demo` and domain `localhost`

Header keys include:

- `Server`
- `Content-Security-Policy`
- `X-Frame-Options`

## Search From the UI

Use the Search card:

1. Select a search type.
2. Enter a demo search term.
3. Submit the form.

Useful demo terms:

- Title: `nginx`
- Domain: `demo.local`
- Port: `443`
- Header key: `Content-Security-Policy`
- Header response: `gunicorn`, `nginx`, or `demo`

## Search With Curl

Title search:

```sh
curl "http://localhost:5000/bytitle?bytitle=nginx"
```

Domain search:

```sh
curl "http://localhost:5000/bydomain?bydomain=demo.local"
```

Port search:

```sh
curl "http://localhost:5000/byport?byport=443"
```

Header key search:

```sh
curl "http://localhost:5000/byhkeyresponse?hkeyresponse=Content-Security-Policy"
```

Header response search:

```sh
curl "http://localhost:5000/byhresponse?byhresponse=gunicorn"
```

## Pagination

Several search endpoints support `from` and `to` query parameters:

```sh
curl "http://localhost:5000/bytitle?bytitle=nginx&from=0&to=10"
```

These values slice the matching result list before the JSON response is returned.
