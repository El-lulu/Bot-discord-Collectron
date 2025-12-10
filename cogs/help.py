import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="help", description="Affiche la liste des commandes")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📜 Guide des Commandes", color=discord.Color.blurple())
        
        embed.add_field(
            name="💰 Économie", 
            value="`/coins` : Voir ton solde\n`/work` : Travailler (1h cooldown)\n`/leaderboard` : Classement des riches", 
            inline=False
        )
        
        embed.add_field(
            name="🛒 Commerce", 
            value="`/boutique` : Ouvrir le shop\n`/inspect [objet]` : Voir image & détails\n`/buy [objet]` : Acheter\n`/sell [objet]` : Vendre\n`/inventory` : Ton sac", 
            inline=False
        )
        
        embed.add_field(
            name="🎲 Jeux", 
            value="`/slots [mise]` : Machine à sous\n`/pfc [choix] [mise]` : Pierre-Feuille-Ciseaux", 
            inline=False
        )

        embed.set_footer(text="Bot créé par Toi • Collectron Coins")
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(HelpCog(client))