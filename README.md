# TikTokSMI Disparagement Humor

This repository contains the code and instructions necessary for replication. 

## Installation

```batch
git clone https://github.com/daisukenm/TikTokSMI_Disparagement_Humor.git
cd TikTokSMI_Disparagement_Humor
```

## Repository Structure
```
.
├── data_analysis/
│   ├── data_analysis.Rmd            # R script for data analysis
│   └── data_analysis.html           # Knitted result of data analysis
├── data_collection/
│   ├── tiktok_api/                  # External package (see below)
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── io.py
│   │   ├── LICENSE                  # Original license of the external package
│   │   └── NOTICE.md
│   └── TikTok_fetch.py              # Python script to fetch TikTok data
├── data_processing/
│   ├── sentiment_analysis.py        # Python script to conduct sentiment analysis
│   ├── video_coding_reliability.Rmd # R script used for reliability check of video coding
│   └── sentiment_validation.Rmd     # R script used for sentiment analysis validation
├── (.env)                           # not in repo, but should be placed here
├── .gitattributes
├── .gitignore
├── LICENSE
└── README.md         
```

## Procedure

1. Run `data_collection/TikTok_fetch.py` to fetch TikTok data
2. Code TikTok Content (manually, see codebook in the main paper)
3. Run `data_processing/sentiment_analysis.py` to label sentiment to each comment
4. Run `data_analysis/data_analysis.Rmd` to analyze data

## TikTok Data Collection
### Dependencies

`TikTok_fetch.py` runs on a Python package adapted from an external open-source project:

Tolochko, P. (2025). *TikTok API Client: A Python package for fetching TikTok video and comment metadata* (Version 0.1.0) [Computer software]. https://doi.org/10.5281/zenodo.16566437

#### License Compliance
The original MIT license is preserved in: 
```bash
data_collection/tiktok_api/LICENSE
```
Attribution details are documented in:
```bash
data_collection/tiktok_api/NOTICE.md
```
All rights to the original code remain with the original author.

#### Modifications to the package

After cloning the external package repository as instructed, following modifications are made to the original scripts:

In `client.py`, functions `fetch_videos_data` and `fetch_comments_data`'s argument `output_dir: str = "TikTok_Data/video_data"` and `output_dir: str = "TikTok_Data/comments_data"`, respectively, have been both changed to `output_dir: str` to accomodate non-default data storage directory to ensure data security. 

Similarly, `io.py`'s functions `video_data_to_csv` and `comments_data_to_csv`'s argument `output_file="TikTok_Data/video_data.csv"` and `output_file="TikTok_Data/comments_data.csv"`, respectively, have been both changed to `output_file` for the same reason.

### Prerequisites

Additionally, make sure you have the following: 

- Access to the TikTok Research API
- `key` and `secret` from TikTok API, as well as secure data storage directory, both stored in `.env` file

```bash

export TIKTOK_KEY="your_key"
export TIKTOK_SECRET="your_secret"

export DATA_STORAGE="path\to\your\secure\storage"
```
