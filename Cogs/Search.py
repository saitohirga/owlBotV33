#from discord.ext import commands
#import lxml
#from Utilities.Scraper import Scraper
#from Utilities.Logging import autoLog


#class Search(commands.Cog):
#
#   # attaches class of commands to existing client in main
#    def __init__(self, client):
#        self.scraper = Scraper()
#        self.client = client
#
#    @commands.Cog.listener()
#    async def on_ready(self):
#        autoLog('Search cog online', 'okgreen')
#    
#    @commands.command()
#   async def search(self, ctx, search: str = None):
#       # this calls a Scraper member function, which also initializes and calls a Sitemap class member function
#       self.scraper.sitemapSearch(search)

#def setup(client):
#    client.add_cog(Search(client))
