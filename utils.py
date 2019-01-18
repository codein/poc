import logging
import os
import datetime
import pandas as pd
import xml.etree.ElementTree as ET
import json
import subprocess
import re
import settings

def get_logger(name):
    FORMAT = '%(asctime)-15s %(name)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger = logging.getLogger(name)
    return logger

def touch_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def expanduser(location):
    return os.path.expanduser(location)

def get_now_ts():
    now = datetime.datetime.now()
    return now.strftime('%m-%d-%y %H:%M:%S')

def convert_xml_to_df(input_file_location):
    tree = ET.parse(input_file_location)
    root = tree.getroot()

    quotes = []

    for quote_record in root:
        # print quote_record.tag
        quote = {}
        for quote_attribute in quote_record:
            # print quote_attribute.tag, quote_attribute.attrib, quote_attribute.text
            quote[quote_attribute.tag] = quote_attribute.text
            # if quote_attribute.text != None:
                # attribut_counter[quote_attribute.tag] += 1
        quotes.append(quote)
    df = pd.DataFrame(quotes)
    return df

def df_to_excel(output_file_location, df):
    writer = pd.ExcelWriter(output_file_location)
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()

def convert_xml_to_xlsx(input_file_location, output_file_location):
    df = convert_xml_to_df(input_file_location)
    df_to_excel(output_file_location, df)

def to_excel(output_file_location, objects):
    df = pd.DataFrame(objects)
    df_to_excel(output_file_location, df)

def save_as_json(output_file_location, data):
    with open(output_file_location, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

def read_json(input_file_location,):
    data = None
    with open(input_file_location, 'r') as json_file:
        data = json.load(json_file)
    return data

def run(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(out,err)
    return out,err

def notify(event):
    """send notification"""
    pass

def run_notify(job):
    run(job)

def run_notify_on_failure(job):
    run(job)

def add_event_log(event):
    """log to a db"""
    pass

