#!/usr/bin/env python3

import singer
import argparse
import json
import sys
import time
import backoff
import requests
from requests.exceptions import HTTPError

from tap_richpanel import utils

# from python_graphql_client import GraphqlClient

# Instantiate the client with an endpoint.
# client = GraphqlClient(endpoint="https://graph.richpanel.com/data-api")

REQUIRED_CONFIG_KEYS = ['api_key', 'start_date']
BASE_URL = "https://api.richpanel.com"
PER_PAGE = 10
STATE = {}
CONFIG = {}

endpoints = {
    "tickets": "/v1/tickets",
    "sub_ticket": "/v1/tickets/{id}"
}

logger = singer.get_logger()
session = requests.Session()

def get_url(endpoint, **kwargs):
    return BASE_URL + endpoints[endpoint].format(**kwargs)

@backoff.on_exception(backoff.expo,
                      (requests.exceptions.RequestException),
                      max_tries=5,
                      giveup=lambda e: e.response is not None and 400 <= e.response.status_code < 500,
                      factor=2)
@utils.ratelimit(1, 2)
def request(url, params=None):
    params = params or {}
    headers = {
        "x-richpanel-key": CONFIG['api_key']
    }

    req = requests.Request('GET', url, params=params, headers=headers).prepare()
    logger.info("GET {}".format(req.url))
    resp = session.send(req)

    if 'Retry-After' in resp.headers:
        retry_after = int(resp.headers['Retry-After'])
        logger.info("Rate limit reached. Sleeping for {} seconds".format(retry_after))
        time.sleep(retry_after)
        return request(url, params)

    resp.raise_for_status()

    return resp


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

def process_tickets():
    bookmark_property = 'updated_at'
    state_entity = 'tickets'

    start = get_start(state_entity)

    params = {
        'updated_at': start
    }

    # start_date = CONFIG['start_date']
    singer.write_schema('tickets', utils.load_schema("tickets"), ['id'])
    # Synchronous request
    for row in gen_request(get_url("tickets"), params):
        utils.update_state(STATE, state_entity, row[bookmark_property])
        singer.write_record('tickets', row)
        singer.write_state(STATE)


def process_customer():
    start_date = CONFIG.get('start_date', None)
    pass

def get_start(entity):
    if entity not in STATE:
        STATE[entity] = CONFIG.get('start_date', None)
    return STATE[entity]

def gen_request(url, params=None):
    params = params or {}
    params["per_page"] = PER_PAGE
    page = 1
    while True:
        params['page'] = page
        data = request(url, params).json()
        for row in data['ticket']:
            yield row

        if len(data['ticket']) == PER_PAGE:
            page += 1
        else:
            break

def do_sync():
    logger.info("Starting sync")

    # api_key = CONFIG['api_key']
    # client.inject_token(api_key,'x-richpanel-key')

    # process_conversation()
    # process_customer()

    try:
        process_tickets()
    except HTTPError as e:
        logger.critical(
            "Error making request to Richpanel API: GET %s: [%s - %s]",
            e.request.url, e.response.status_code, e.response.content)
        sys.exit(1)
    logger.info("Sync completed")

def main_impl():
    config, state = utils.parse_args(REQUIRED_CONFIG_KEYS)
    CONFIG.update(config)
    STATE.update(state)
    do_sync()

def main():
    # config, state = parse_args(REQUIRED_CONFIG_KEYS)
    # CONFIG.update(config)
    # STATE.update(state)
    # do_sync()

    try:
        main_impl()
    except Exception as exc:
        logger.critical(exc)
        raise exc


if __name__ == '__main__':
    main()