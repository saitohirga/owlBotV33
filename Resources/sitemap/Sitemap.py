from lxml import etree
from datetime import datetime, timedelta
import requests, os
from Utilities.Logging import autoLog

"""
    
    This is a simple helper to get the most current sitemap from fau's sitemap.xml, 
    and update the current one if it's been a week

"""
class SitemapLoader():
    def __init__(self):
        autoLog(f'Sitemap loading...', 'warning')

        self.sitemap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sitemap.xml')
        self.date_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'date.txt')
        with open(self.sitemap_path, 'r') as fin: sitemap_latest = fin.read()
        self.site_path = 'https://fau.edu/sitemap.xml'
        self.date_frequency = 14 # days
        self.existing_tree = None

    def getCurrentSitemap(self): # gets sitemap after checking to make sure it's not too up to date
        with open(self.date_path, 'r') as fin: date_latest = fin.read()
        last_date = datetime.strptime(date_latest, '%Y-%m-%d')
        # checks for date diff 
        if(last_date + timedelta(days=self.date_frequency) < datetime.now()):
            self.getNewSitemap()

        # checks to see if it has to generate a tree from the xml or not. Will save resources instead of building a new one each time
        if self.existing_tree is None:
            # since we can assume there is already xml in sitemap.xml,
            # we can just parse from file path rather than read it all in again
            self.existing_tree = etree.parse(self.sitemap_path)

            autoLog(f'Sitemap loaded: last@{self.getLastDate()}', 'okblue')

        return self.existing_tree

    def getNewSitemap(self): # updates both latest date and 
        autoLog(f'Getting updated sitemap from {self.site_path}', 'warning')

        r = requests.get(self.site_path)
        root = etree.fromstring(r.content)
        root_to_str = etree.tostring(root, pretty_print=True)
        root_to_str.write('output.xml', pretty_print=True)
        existing_tree = root

        with open("date.txt", "w") as new_date:
            new_date.write(f'{datetime.now().strftime("%Y-%m-%d")}')



    def getLastDate(self):
        with open(self.date_path, 'r') as fin: date_latest = fin.read()
        return date_latest
