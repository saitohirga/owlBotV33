from pathlib import Path
from lxml import etree
from datetime import datetime, timedelta
import requests, os
from Utilities.Logging import autoLog

"""
    
    This is a simple helper to get the most current sitemap from fau's sitemap.xml, 
    and update the current one if it's been a week

"""

sitemap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sitemap.xml')
date_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'date.txt')
with open(sitemap_path, 'r') as fin: sitemap_latest = fin.read()
site_path = 'https://fau.edu/sitemap.xml'
date_frequency = 14 # days

def getCurrentSitemap(): # gets sitemap after checking to make sure it's not too up to date
    with open(date_path, 'r') as fin: date_latest = fin.read()
    last_date = datetime.strptime(date_latest, '%Y-%m-%d')
    # checks for date diff 
    if(last_date + timedelta(days=date_frequency) < datetime.now()):
        getNewSitemap()

    with open(sitemap_path, 'r') as fin: sitemap = fin.read()

    return sitemap

def getNewSitemap(): # updates both latest date and 
    autoLog(f'Getting updated sitemap from {site_path}', 'warning')

    r = requests.get(site_path)
    root = etree.fromstring(r.content)
    root_to_str = etree.tostring(root, pretty_print=True)
    root_to_str.write('output.xml', pretty_print=True)

    with open("date.txt", "w") as new_date:
        new_date.write(f'{datetime.now().strftime("%Y-%m-%d")}')

def getLastDate():
    with open(date_path, 'r') as fin: date_latest = fin.read()
    return date_latest