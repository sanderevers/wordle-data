# Wordle-data

Extract score data from a Slack channel with Wordle results.

## Install

Assuming you have a `python3` environment available on your system.

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Configure

Create a `.env` file with `SLACK_BOT_TOKEN=....` in it. Fill in your bot token.
Optionally, include `CHANNEL_NAME`, `FROM_DATE`, `TO_DATE` (ISO8601 format).

## Run

    python main.py

This will search the Slack workspace for a `#wordle` channel, fetch all messages,
and extract user id, game type (Wordle/Woordle/Woordle6), game number, timestamp and score.
It dumps this data into a `results.json` and a `users.json` file.

## Deactivate virtual env

    deactivate