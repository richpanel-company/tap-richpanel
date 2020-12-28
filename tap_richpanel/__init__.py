#!/usr/bin/env python3

import singer
import argparse
import json
from python_graphql_client import GraphqlClient

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://graph.richpanel.com/data-api")

REQUIRED_CONFIG_KEYS = ['api_key']
STATE = {}
CONFIG = {}

logger = singer.get_logger()

def write_schema_from_header(entity, header, keys):
    schema =    {
                    "type": "object",
                    "properties": {}
                }
    header_map = []
    for column in header:
        #for now everything is a string; ideas for later:
        #1. intelligently detect data types based on a sampling of entries from the raw data
        #2. by default everything is a string, but allow entries in config.json to hard-type columns by name
        schema["properties"][column] = {"type": "string" } 
        header_map.append(column)

    singer.write_schema(entity, schema, keys) 

    return header_map

def parse_args(required_config_keys):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file', required=True)
    parser.add_argument('-s', '--state', help='State file')
    args = parser.parse_args()

    config = load_json(args.config)
    check_config(config, required_config_keys)

    if args.state:
        state = load_json(args.state)
    else:
        state = {}

    return config, state

def load_json(path):
    with open(path) as f:
        return json.load(f)

def check_config(config, required_keys):
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise Exception("Config is missing required keys: {}".format(missing_keys))

conversation_schema = {
    'properties':   {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "id": {
                "type": "string"
            }
        }
    },
}

customer_schema = {
    'properties':   {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "id": {
                "type": "string"
            }
        }
    },
}

def process_conversation():
    start_date = CONFIG['start_date']
    query = """
        query {
            Conversation {
                totalCount
                nodes {
                    id
                    status
                    email
                    type
                    rating
                }
            }
        }
    """

    singer.write_schema('conversation', conversation_schema, 'id')
    # Synchronous request
    data = client.execute(query=query)

    records = data['data']['Conversation']['nodes']
    singer.write_records('conversation', records)

def process_customer():
    start_date = CONFIG['start_date']

    query = """
        query {
            Customer {
                totalCount
                nodes {
                    id
                    firstName
                    lastName
                    email
                    createdAt
                    updatedAt
                }
            }
        }
    """

    singer.write_schema('customer', customer_schema, 'id')
    # Synchronous request
    data = client.execute(query=query)

    records = data['data']['Customer']['nodes']
    singer.write_records('customer', records)

def do_sync():
    logger.info("Starting sync")

    api_key = CONFIG['api_key']
    client.inject_token(api_key,'x-richpanel-key')

    process_conversation()
    process_customer()

    logger.info("Sync completed")

def main():
    config, state = parse_args(REQUIRED_CONFIG_KEYS)
    CONFIG.update(config)
    STATE.update(state)
    do_sync()


if __name__ == '__main__':
    main()