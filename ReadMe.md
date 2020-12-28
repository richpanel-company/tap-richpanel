# tap-richpanel

A [Singer](https://singer.io) tap for extracting data from a Richpanel account.

## Installation

Clone this repository, and then:

```bash
› python setup.py install
```

## Run

#### Run the application

```bash

python tap_richpanel.py -c config.json

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

**Conversation**
```json
{
  "properties":   {
      "type": "object",
      "additionalProperties": True,
      "properties": {
          "publicId": {
              "type": "string"
          },
          "subject": {
              "type": "string"
          },
          "from": {
              "type": "string"
          },
          "to": {
              "type": "string"
          },
          "status": {
              "type": "string"
          },
          "type": {
              "type": "string"
          },
          "email": {
              "type": "string"
          },
          "assignee": {
              "type": "string"
          },
          "rating": {
              "type": "string"
          },
          "ratingFor": {
              "type": "string"
          },
          "tags": {
              "type": "list"
          },
          "isArchived": {
              "type": "boolean"
          },
          "reOpenStatus": {
              "type": "boolean"
          },
          "firstClosedAt": {
              "type": "integer"
          },
          "firstResponseTime": {
              "type": "integer"
          },
          "archivedAt": {
              "type": "integer"
          },
          "createdAt": {
              "type": "integer"
          },
          "updatedAt": {
              "type": "integer"
          }
      }
  },
}
```

**Customer**
```json
{
  "properties":   {
      "type": "object",
      "additionalProperties": True,
      "properties": {
          "id": {
              "type": "string"
          },
          "firstName": {
              "type": "string"
          },
          "lastName": {
              "type": "string"
          }, "email": {
              "type": "string"
          },
          "createdAt": {
              "type": "integer"
          },
          "updatedAt": {
              "type": "integer"
          }
      }
  },
}
```
