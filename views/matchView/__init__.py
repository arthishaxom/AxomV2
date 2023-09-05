import discord
from discord.interactions import Interaction 
import discord.ui
from typing import Optional,List
import re
from tabulate import tabulate
class slotlistModal(discord.ui.Modal,title="Enter Slotlist"):
    def __init__(self,teamNameList,teamNoList,*args,**kwargs):
        super().__init__()
        self.teamNameList = teamNameList
        self.teamNoList = teamNoList

    slotlist = discord.ui.TextInput(label="Slotlist",required=True,min_length=20,style=discord.TextStyle.long)
    delimeter = discord.ui.TextInput(label="Delimeter",required=True,style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        for row in self.slotlist.value.splitlines():
            self.teamNameList.append(row.split(self.delimeter.value)[1].strip())
            self.teamNoList.append(re.findall(r'\d+', row.split(self.delimeter.value)[0])[0])
        em = discord.Embed(title="Choose An Option",description=
f'''
```
{tabulate({"Slot":self.teamNoList,"TeamName":self.teamNameList},headers="keys",tablefmt="presto")}
```
''',colour=discord.Colour.gold())
        await interaction.message.edit(embed=em,view=matchView(self.teamNameList,self.teamNoList))

class matchView(discord.ui.View):
    def __init__(self,teamNameList:List[str] = [],teamNoList:List[str] = [],tourneyMode:bool=False):
        super().__init__()
        self.teamNameList:List[str] = teamNameList
        self.teamNoList:List[str] = teamNoList
        self.records:List = []
        self.rankCount:int = 1
        self.matchCount:int = 1
        self.tourneyName:str = "oneMatch"
        self.tourneyMode:bool = tourneyMode
        if self.tourneyMode == True:
            pass #! add a "Add Match" Button for tourney mode
    @discord.ui.button(label="Set Slotlist",style=discord.ButtonStyle.grey)
    async def setSlotlist(self,interaction:discord.Integration,button:discord.Button):
        modalForSlotlist = slotlistModal(self.teamNameList,self.teamNoList)
        await interaction.response.send_modal(modalForSlotlist)

    @discord.ui.button(label="Set Team Ranks",style=discord.ButtonStyle.grey)
    async def setTeamRanks(self,interaction:discord.Integration,button:discord.Button):
        await interaction.response.defer()
        em = discord.Embed(title="Select Teams in Order",colour=discord.Colour.gold())
        await interaction.followup.send(embed=em,view=addRanks())

    @discord.ui.button(label="Set Team Kills",style=discord.ButtonStyle.grey)
    async def setTeamKills(self,interaction:discord.Integration,button:discord.Button):
        await interaction.response.defer()


class addRanks(matchView):
    def __init__(self):
        super().__init__()
    @discord.ui.button(label="Save",style=discord.ButtonStyle.green)
    async def setTeamKills(self,interaction:discord.Integration,button:discord.Button):
        await interaction.response.defer()
        await interaction.followup.send(self.teamNameList)


class teamDropdown(discord.ui.Select):
    def __init__(self,teamNameList:List[str],rankCount):
        super().__init__()
