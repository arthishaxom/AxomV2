import discord
from discord.ext import commands
from views.typeselect import typeSelect

class PointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calculate", case_insensitive = True, aliases = ["calc"])
    async def calculate(self,ctx:commands.Context):
        em = discord.Embed(title="Choose An Option",description=
'''
`Single Match` - Points get delete after calculation
`Tournament` - Calculate Points for multiple rounds
``
''',colour=discord.Colour.gold())
        await ctx.send(embed=em,view=typeSelect())
    
async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(PointsCog(bot))