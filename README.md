# File_Xor
- Streams files directly from Telegram without saving them locally, avoiding download/seek delays and allowing immediate streaming playback.

[![Stars](https://img.shields.io/github/stars/Dot-ser/file_xor?style=social)](https://github.com/Dot-ser/File-Xor/stargazers)
[![Forks](https://img.shields.io/github/forks/Dot-ser/file_xor?style=social)](https://github.com/Dot-ser/File-Xor/network/members)

![alt text](https://files.catbox.moe/f11xqf.jpg)

If you find file_xor helpful, please consider giving it a [⭐ star](https://github.com/Dot-ser/File-Xor/stargazers) and [forking](https://github.com/Dot-ser/File-Xor/fork) the repository — it really helps the project grow!

Fast Telegram-based file streaming and download bot + web server that streams files directly from Telegram without pre-downloading them to local disk, reducing download delays and enabling immediate playback.

## Why file_xor

- Fast downloading and streaming: built for efficient chunked streaming of large files.
- Uses a Telegram channel as a file database, so files are stored/retrieved from Telegram media messages.
- Web frontend for playback and secure per-file links with secret codes.
- Lightweight Quart + Uvicorn web service and an integrated Telegram bot.

## Features

- Stream files with byte-range support (seek / resume).
- Secure download links using secret codes stored in message captions.
- Support for large files via chunked streaming and configurable chunk sizes.
- Simple deploy options: Heroku, Render, Koyeb (manifests included).
## Quick Start (local)

1. Create a virtual environment and install dependencies:

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `config.env.example` to `config.env` and fill the values:

```powershell
cp config.env.example config.env
# edit config.env with your favorite editor
```

3. Run the app:
```
py -m file_xor
```

The web server will use `PORT` from environment (default 8000 in code). The bot will also run within the same process.



## 🚀 Deploy File-XOR Bot on Servers

Easily deploy using your preferred platform:

[![Deploy to Heroku](https://img.shields.io/badge/⚡_Deploy_to_Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/deploy?template=https://github.com/Dot-ser/file-xor)
[![Deploy to Render](https://img.shields.io/badge/☁️_Deploy_to_Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/deploy?repo=https://github.com/Dot-ser/file-xor)
[![Deploy to Koyeb](https://img.shields.io/badge/🚀_Deploy_to_Koyeb-121212?style=for-the-badge&logo=koyeb&logoColor=white)](https://app.koyeb.com/deploy?from=https://github.com/Dot-ser/file-xor)




Container / Docker

- This repository already contains a `Dockerfile`. Build and run locally as usual:

```powershell
docker build -t file_xor:latest .
docker run -e BOT_TOKEN=... -e API_ID=... -e API_HASH=... -e FILEDB_CHANNEL=... -p 8000:8000 file_xor:latest
```

## Configuration (`config.env`)

Copy this into `config.env` and replace values.

```env
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
API_ID=your_api_id
FILEDB_CHANNEL=your_filedb_id
DOMAIN_URL=_your_domin_url
LANG=js
SUDO=your_uid
DATABASE_URL=your_postgresqldb_url
MODE=private
OWNER_ID=owner_uid
PORT=5000
BOT_NAME=your_bot_name
BOT_LOGO=your_logo_wrking_url
MAX_FILE_SIZE=4096 
GEN_SECRET_KEY_LENGTH=16
```

Notes:
- `DATABASE_URL` is optional for local file streaming with the Telegram channel method, but recommended for production if you use a Postgres db.
- `FILEDB_CHANNEL` must be a channel or chat where the bot can read media messages used as the file database.

## Usage

- Upload files to your configured `FILEDB_CHANNEL` using your bot or other helpers (see `plugins/getlink_files.py`).
- The bot generates secret-coded links and captions which your web server uses to authorize downloads.
- Stream pages are available at `/stream/<file_id>?code=<secret>` and direct downloads at `/dl/<file_id>?code=<secret>`.

## Developer

- Author / Maintainer: Dot-ser

## Contributing

- Pull requests welcome. Please open issues for bugs or feature requests.

## License

See `LICENSE` in the repository root.
