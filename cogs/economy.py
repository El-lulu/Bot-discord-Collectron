import discord
from discord.ext import commands
from discord import app_commands
import math

class ShopPaginationView(discord.ui.View):
    def __init__(self, data_cog, items_list, items_per_page=5):
        super().__init__(timeout=60)
        self.data_cog = data_cog
        self.items_list = items_list
        self.items_per_page = items_per_page
        self.current_page = 0
        self.total_pages = math.ceil(len(items_list) / items_per_page)

    def get_embed(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        current_items = self.items_list[start:end]

        embed = discord.Embed(title="🛒 La Boutique", color=discord.Color.gold())
        embed.description = f"Page {self.current_page + 1}/{self.total_pages}\nUtilise `/inspect [nom]` pour voir l'image !"

        for item_name in current_items:
            infos = self.data_cog.get_item_info(item_name)
            stock = self.data_cog.get_stock(item_name)
            stock_str = f"📦 Stock: {stock}" if stock > 0 else "🔴 **RUPTURE**"
            
            if infos:
                # Affichage en Coins
                embed.add_field(
                    name=f"{infos['emoji']} {item_name.capitalize()}",
                    value=f"Prix: **{infos['buy']}** Coins | Vente: **{infos['sell']}** Coins\n{stock_str}",
                    inline=False
                )
        return embed

    def update_buttons(self):
        self.prev_button.disabled = (self.current_page == 0)
        self.next_button.disabled = (self.current_page == self.total_pages - 1)

    @discord.ui.button(label="◀️ Précédent", style=discord.ButtonStyle.blurple)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Suivant ▶️", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)


class EconomyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @property
    def data(self):
        return self.client.get_cog("DataManager")

    # Renommé en "coins" pour l'utilisateur, mais la commande reste /points ou /coins selon ton choix
    # Gardons /coins pour être cohérent
    @app_commands.command(name="coins", description="Voir ton solde de Collectron Coins")
    async def coins(self, interaction: discord.Interaction):
        # Appel à get_coins
        solde = self.data.get_coins(interaction.user.id)
        await interaction.response.send_message(f"💰 Tu as **{solde}** Collectron Coins.")

    @app_commands.command(name="leaderboard", description="🏆 Voir le top 10 des joueurs")
    async def leaderboard(self, interaction: discord.Interaction):
        users_data = self.data.data["users"]
        classement = []
        for u_id, u_info in users_data.items():
            classement.append((u_id, u_info["points"])) # La clé interne reste "points"
        classement.sort(key=lambda x: x[1], reverse=True)
        top_10 = classement[:10]
        
        desc = ""
        for index, (u_id, pts) in enumerate(top_10):
            medal = "🥇" if index == 0 else "🥈" if index == 1 else "🥉" if index == 2 else f"#{index + 1}"
            desc += f"{medal} <@{u_id}> : **{pts}** Collectron Coins\n"
            
        embed = discord.Embed(title="🏆 Classement des Riches", description=desc if desc else "Aucun joueur.", color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="boutique", description="Ouvrir la boutique")
    async def shop(self, interaction: discord.Interaction):
        all_items = list(self.data.get_all_items_config().keys())
        if not all_items:
            return await interaction.response.send_message("La boutique est vide !", ephemeral=True)
        view = ShopPaginationView(self.data, all_items, items_per_page=5)
        view.update_buttons()
        await interaction.response.send_message(embed=view.get_embed(), view=view)

    @app_commands.command(name="inspect", description="Voir détails et image d'un objet")
    async def inspect(self, interaction: discord.Interaction, item_name: str):
        item_name = item_name.lower()
        infos = self.data.get_item_info(item_name)
        if not infos:
            return await interaction.response.send_message("❌ Objet inconnu.", ephemeral=True)

        file = self.data.get_item_file(item_name)
        embed = discord.Embed(title=f"{infos['emoji']} {item_name.capitalize()}", color=discord.Color.teal())
        embed.add_field(name="Prix", value=f"{infos['buy']} Coins", inline=True)
        embed.add_field(name="Vente", value=f"{infos['sell']} Coins", inline=True)
        stock = self.data.get_stock(item_name)
        embed.add_field(name="Stock", value=str(stock) if stock > 0 else "Rupture", inline=True)

        if file:
            embed.set_thumbnail(url=f"attachment://{file.filename}")
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory", description="Voir tes objets")
    async def inventory(self, interaction: discord.Interaction):
        inventory_list = self.data.get_inventory(interaction.user.id)
        if not inventory_list:
            return await interaction.response.send_message(f"🎒 Inventaire vide !", ephemeral=True)

        counts = {}
        for item in inventory_list:
            counts[item] = counts.get(item, 0) + 1

        description = ""
        for item_name, count in counts.items():
            infos = self.data.get_item_info(item_name)
            if infos:
                description += f"- {infos['emoji']} **{item_name.capitalize()}** (x{count})\n"
            else:
                description += f"- ❓ **{item_name}** (x{count})\n"

        embed = discord.Embed(title=f"🎒 Inventaire de {interaction.user.display_name}", description=description, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Acheter un objet")
    async def buy(self, interaction: discord.Interaction, item_name: str):
        item_name = item_name.lower()
        infos = self.data.get_item_info(item_name)
        if not infos: return await interaction.response.send_message("Objet inconnu.", ephemeral=True)
        
        if self.data.get_stock(item_name) <= 0:
            return await interaction.response.send_message(f"❌ Rupture de stock !", ephemeral=True)

        # Appel à remove_coins
        if self.data.remove_coins(interaction.user.id, infos["buy"]):
            self.data.remove_stock(item_name)
            self.data.add_item_to_user(interaction.user.id, item_name)
            await interaction.response.send_message(f"✅ Acheté : {infos['emoji']} **{item_name}** !")
        else:
            await interaction.response.send_message(f"❌ Pas assez de Collectron Coins.", ephemeral=True)

    @app_commands.command(name="sell", description="Vendre un objet")
    async def sell(self, interaction: discord.Interaction, item_name: str):
        item_name = item_name.lower()
        infos = self.data.get_item_info(item_name)
        if not infos: return await interaction.response.send_message("Objet inconnu.", ephemeral=True)

        if self.data.remove_item_from_user(interaction.user.id, item_name):
            # Appel à add_coins
            self.data.add_coins(interaction.user.id, infos["sell"])
            self.data.add_stock(item_name)
            await interaction.response.send_message(f"🤝 Vendu : {infos['emoji']} **{item_name}**.")
        else:
            await interaction.response.send_message("Tu n'as pas cet objet.", ephemeral=True)

async def setup(client):
    await client.add_cog(EconomyCog(client))