# tap-zendesk
Tap for Richpanel

## Installation

1. Create and activate a virtualenv
1. `pip install -e '.[dev]'`

---

## Authentication

Please generate API Keys to use Richpanel Graph API. 

It can be generated from **Settings => Advanced Settings => API Settings**

**config.json**
```json
{
  "api_key": "THISISARICHPANELKEY",
  "start_date": "2000-01-01T00:00:00Z"
}
```

Copyright &copy; 2018 Stitch