import discord
from discord.ext import commands

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot IS ONLINE")

    
async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(EventsCog(bot))