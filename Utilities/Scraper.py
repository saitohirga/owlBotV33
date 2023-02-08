import lxml
from Resources.sitemap.Sitemap import SitemapLoader
from Utilities.Logging import autoLog
"""

    All scraping utilities will end up here as a member function of Scraper. 
    Not sure which scraper library I want to use but it will probably be beautifulsoup/lxml,

"""
class Scraper():

    # Organizes the sitemp into a readable //thing//
    def __init__(self):
        self.sm = SitemapLoader()
        self.sitemap = self.sm.getCurrentSitemap()
        # logic to get a new copy of sitemap if the last check date is a week out of date
        # I am way too laxy to think about setting up another service rn so a really goofy checker is the best we'll get
        pass
    
    # I'm building a search but it might be convenient to also have a dictionary of most common destinations to
    # be prioritized in a search. I could also, in theory read 
    def commonDestination():
        pass
    
    # This searches through the sitemap after the constructor made it pretty
    def sitemapSearch(self, search=""):
        matches = []
        pass

