# Reddit Music Data Scraper

This project provides tools to scrape and process music-related discussions from Reddit. It consists of two main scripts that work together to collect and format data from music subreddits.

## Overview

The project allows you to:
- Download posts from music-related subreddits using the Reddit API
- Convert the downloaded JSON data into CSV format for easier analysis
- Configure various parameters like post sorting and rate limiting

## Scripts

### get-data.py

This script handles the Reddit API interaction and data collection. It uses PRAW (Python Reddit API Wrapper) to fetch posts from specified subreddits.

Key features:
- Configurable number of posts to download
- Multiple sorting options (new, top, hot)
- Rate limiting to respect Reddit's API guidelines
- Comprehensive error handling and logging
- Saves data in JSON format

### convert_to_csv.py

This utility script converts the JSON data collected by `get-data.py` into CSV format.

Features:
- Preserves all relevant post data
- Handles UTF-8 encoding
- Creates output directories if they don't exist
- Maintains data structure consistency

## Setup

1. Install required dependencies:
```bash
pip install praw
```

2. Configure your Reddit API credentials in `get-data.py`:
- Replace `YOUR_CLIENT_ID` with your Reddit API client ID
- Replace `YOUR_CLIENT_SECRET` with your Reddit API client secret
- Update `USERNAME` with your Reddit username

## Usage

1. Run the data collection script:
```bash
python get-data.py
```

2. Convert the collected data to CSV:
```bash
python convert_to_csv.py
```

## Output

The scripts will create:
- A `reddit_data` directory (or custom directory specified in `get-data.py`)
- JSON files containing the raw post data
- CSV files with the converted data
- A log file (`reddit_download.log`) tracking the download process

## Notes

- The default configuration downloads 100 posts from r/LetsTalkMusic
- Rate limiting is set to 2 seconds between requests to avoid API restrictions
