import discord 
import discord.ui
from views.matchView import matchView
from tabulate import tabulate
class typeSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Single Match",style=discord.ButtonStyle.grey)
    async def singleMatch(self,interaction:discord.Integration,button:discord.Button):
        await interaction.response.defer()
        table = []
        em = discord.Embed(title="Choose An Option",description=
f'''
```
{tabulate(table,headers=["Slot","TeamName"],tablefmt="presto")}
```
''',colour=discord.Colour.gold())
        await interaction.message.edit(embed=em, view=matchView())
    @discord.ui.button(label="Tournament",style=discord.ButtonStyle.grey)
    async def Tournament(self,interaction:discord.Integration,button:discord.Button):
        pass