import discord
from discord.ext import commands
from discord import app_commands

class AdminCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @property
    def data(self):
        return self.client.get_cog("DataManager")

    admin_group = app_commands.Group(
        name="admin", 
        description="Commandes réservées aux administrateurs",
        default_permissions=discord.Permissions(administrator=True)
    )

    
    @admin_group.command(name="help", description="Affiche l'aide des commandes Administrateur")
    async def admin_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛠️ Panneau d'Administration", 
            description="Commandes réservées aux admins.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🛒 Objets", 
            value="`/admin create_item`\n`/admin set_stock`",
            inline=False
        )
        embed.add_field(
            name="💰 Argent", 
            value="`/admin give_coins`\n`/admin remove_coins`",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @admin_group.command(name="create_item", description="Créer un nouvel objet")
    async def create_item(self, interaction: discord.Interaction, name: str, price: int, sell_price: int, emoji: str, stock: int, image_file: str):
        name = name.lower().replace(" ", "_")
        if self.data.get_item_info(name):
            return await interaction.response.send_message(f"❌ L'objet **{name}** existe déjà !", ephemeral=True)

        self.data.create_new_item(name, price, sell_price, emoji, stock, image_file)
        await interaction.response.send_message(f"✅ Objet créé : {emoji} **{name}** (Image: `{image_file}`)")


    @admin_group.command(name="give_coins", description="Donner des Coins")
    async def give_coins(self, interaction: discord.Interaction, membre: discord.Member, montant: int):
        self.data.add_coins(membre.id, montant)
        await interaction.response.send_message(f"💸 Tu as donné **{montant}** Coins à {membre.mention}.")


    @admin_group.command(name="remove_coins", description="Retirer des Coins")
    async def remove_coins(self, interaction: discord.Interaction, membre: discord.Member, montant: int):
        if self.data.remove_coins(membre.id, montant):
            await interaction.response.send_message(f"📉 Tu as retiré **{montant}** Coins à {membre.mention}.")
        else:
            await interaction.response.send_message(f"❌ Pas assez de Coins.", ephemeral=True)


    @admin_group.command(name="set_stock", description="Modifier le stock")
    async def set_stock(self, interaction: discord.Interaction, item_name: str, nouveau_stock: int):
        item_name = item_name.lower()
        if not self.data.get_item_info(item_name):
            return await interaction.response.send_message("❌ Objet inconnu.", ephemeral=True)

        self.data.data["shop_stock"][item_name] = nouveau_stock
        self.data.save_data()
        await interaction.response.send_message(f"📦 Stock de **{item_name}** mis à **{nouveau_stock}**.")

async def setup(client):
    await client.add_cog(AdminCog(client))
