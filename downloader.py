import argparse
import io
import json
import os
import pandas as pd
import pprint
import requests
from time import gmtime, strftime

DIR_FOR_DOWNLOADS = 'dumps'

def prepare_dir_and_filename(config):
    filename = '{path}/{today}_{function}_{outputsize}.csv'.format(
        path=DIR_FOR_DOWNLOADS,
        today=strftime("%Y-%m-%d_%H:%M:%S", gmtime()),
        function=config["function"],
        outputsize=config["outputsize"]
    )
    if os.path.exists(DIR_FOR_DOWNLOADS):
        return filename
    os.mkdir(DIR_FOR_DOWNLOADS)
    return filename

def get_historical_data(config):
    page = requests.get(config["url"], params=config)

    if config['datatype'] == 'csv':
        rawData =pd.read_csv(io.StringIO(page.content.decode('utf-8')))
        rawData.to_csv(prepare_dir_and_filename(config))
    else:
        pprint.pprint(page.json())

def read_config():
    with open('config.json') as json_config_file:
        json_config = json.load(json_config_file)
        api_key = os.environ['api_key']
        json_config.update({"apikey": api_key})
        return json_config
    return None

def main():
    config = read_config()
    if config:
        get_historical_data(config)

if __name__ == '__main__':
    main()
