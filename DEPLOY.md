This repository includes simple deployment manifests for Heroku, Render, and Koyeb.

Files added:
- `Procfile` - Heroku classic web process: `web: python -m file_xor`
- `heroku.yml` - Heroku container / build manifest (uses `Dockerfile`)
- `render.yaml` - Render service definition (docker environment)
- `koyeb.yaml` - Koyeb app manifest (build from repository)

Notes / Next steps:
- Set environment variables (API_ID, API_HASH, BOT_TOKEN, DATABASE_URL, etc.) in your platform's dashboard or in `config.env` for local testing.
- The start command used is `python -m file_xor` (the package entrypoint). 
- The repository already contains a `Dockerfile` at the project root — the manifests assume you will build that image.
