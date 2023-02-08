from discord.ext import commands
import lxml
from Utilities.Scraper import Scraper
from Utilities.Logging import autoLog


class Search(commands.Cog):

    # attaches class of commands to existing client in main
    def __init__(self, client):
        self.sitemap = Scraper()
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        autoLog('Animal cog online', 'okgreen')
    
    @commands.command()
    async def search(ctx, search: str = None):
       pass

def setup(client):
    client.add_cog(Search(client))