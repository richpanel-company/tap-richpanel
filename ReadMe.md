# tap-richpanel

A [Singer](https://singer.io) tap for extracting data from a Richpanel account.

## Installation

Clone this repository, and then:

```bash
› cd richpanel-tap
› python3 -m venv ~/.virtualenvs/richpanel-tap
› source ~/.virtualenvs/richpanel-tap/bin/activate
› pip install -e .
```

## Run

#### Run the application

```bash

richpanel-tap -c sample_config.json --discover

```

## Authentication

Please generate API Keys to use Richpanel Graph API. 

It can be generated from **Settings => Advanced Settings => API Settings**

**config.json**
```json
{
  "api_key": "THISISARICHPANELKEY",
  "start_date": "2020-01-01T00:00:00Z"
}
```

## Schema

Check in Repository
