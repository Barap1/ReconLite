# Demo Mode

Demo mode lets reviewers use the ReconLite dashboard without scanning real networks.

It is intended for portfolio review, local UI testing, and API exploration. It uses safe sample records from `sample_data/demo_results.json` and does not run Masscan.

## Load Demo Data

Start MongoDB, then run:

```sh
python scripts/load_demo_data.py --clear
python server/server.py
```

Open:

```text
http://localhost:5000
```

## Try Sample Searches

- Title: `nginx`
- Domain: `demo.local`
- Port: `443`
- Header key: `Content-Security-Policy`

## Safety

Demo mode is the recommended path for reviewers. It shows the dashboard and search behavior without running network discovery or generating scan traffic.
