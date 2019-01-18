import os
import requests
import json
import urllib
from urllib import urlencode
import pandas as pd
import argparse
import numpy as np
import datetime

import settings
import utils

base_url = 'https://api.github.com'
issue_attributes = ['title', 'html_url']

def extract_issue_attributes(raw_issue):
    try:
        issue = {}
        for key in issue_attributes:
            issue[key] = raw_issue[key]
        hours = raw_issue['body'].split('\n')[0].lower().replace('p', '')
        issue['hours'] = int(hours)
        raw_date = raw_issue['closed_at']
        date = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
        issue['date'] = date.strftime('%m/%d/%y')
        return issue
    except Exception as e:
        print(e)
        print(raw_issue['html_url'])

def get_issues(url, issues=None):
    if issues is None:
        issues = []

    request_headers = {
        'content-type': 'application/json; charset=utf8',
        # 'Accept': 'application/vnd.bindo-' + settings.BINDO_API['api_version'] + '+json',
        'Authorization': 'token ' + settings.GITHUB_OAUTH_TOKEN,
    }
    print(url)
    payload = {
        'state': 'closed',
        'sort': 'created',
    }
    response = requests.get(url, headers=request_headers, params=payload)
    if response.status_code == requests.codes.ok:
        issues= issues + (response.json())
    if 'next' in response.links:
        next_url = response.links['next']
        issues = get_issues(next_url['url'], issues)
    return issues

for repo_dict in settings.GITHUB_REPOSITORIES:
    issues_url = '/repos/{org}/{repo}/issues'.format(**repo_dict)
    url = urllib.basejoin(base_url, issues_url)

    raw_issues = get_issues(url)
    issues = []
    if len(raw_issues) > 0:

        for raw_issue in raw_issues:
            issue = extract_issue_attributes(raw_issue)
            if issue:
                issues.append(issue)

        df = pd.DataFrame(issues)
        copy_columns = [
            ('title', 'comments'),
        ]

        for from_column, to_column in copy_columns:
            df[to_column] = df[from_column]

        output_columns = [
            'date',
            'hours',
            'comments',
            'html_url',
        ]

        df = df[output_columns]


        output_file_location = '~/{repo}-issues.xlsx'.format(**repo_dict)
        output_file_location = utils.expanduser(output_file_location)
        utils.df_to_excel(output_file_location, df)
