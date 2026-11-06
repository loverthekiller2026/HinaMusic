# 🎵 HinaMusic

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy?repo=https://github.com/loverthekiller2026/HinaMusic)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Railway deployment

1. Click the **Deploy on Railway** button above, or create a new Railway project and choose **Deploy from GitHub repo**.
2. Select `loverthekiller2026/HinaMusic`. Railway will build the included `Dockerfile`.
3. Add the environment variables below in the Railway service's **Variables** tab.
4. Deploy and inspect the deployment logs.

### Required environment variables

| Variable | Description |
| --- | --- |
| `API_ID` | Telegram API ID |
| `API_HASH` | Telegram API hash |
| `BOT_TOKEN` | Bot token from BotFather |
| `OWNER_ID` | Telegram numeric owner ID |
| `LOGGER_ID` | Numeric ID of the log group/channel |
| `MONGO_DB_URI` | MongoDB connection URI |
| `STRING_SESSION` | Assistant/user account Pyrogram session |

Optional assistant sessions can be supplied as `STRING_SESSION2` through `STRING_SESSION5`.

**Important:** The bot requires at least one assistant session. Add the assistant account to the target voice-chat group and make sure the configured log group/channel has an active voice chat, as required by the current startup code. Keep all tokens, session strings, and database credentials private; enter them only as Railway variables, never commit them to Git.

### Runtime

Railway uses the repository's Dockerfile (Python 3.11, FFmpeg and required system libraries). The bot runs with:

```bash
python -m AloneMusic
```

The Railway config restarts the service after an unexpected failure. This does not guarantee uninterrupted playback if Telegram, the host, or external media providers are unavailable.

## Project

HinaMusic is based on the AloneMusic Telegram voice-chat music bot codebase. See the source tree and license for details.
