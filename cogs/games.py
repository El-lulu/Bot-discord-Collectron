import discord
from discord.ext import commands
from discord import app_commands
import random

class GamesCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @property
    def data(self):
        return self.client.get_cog("DataManager")

    # --- JEU 1 : MACHINE À SOUS (SLOTS) ---
    @app_commands.command(name="slots", description="🎰 Machine à sous (Mise min: 10 Coins)")
    async def slots(self, interaction: discord.Interaction, mise: int):
        if mise < 10:
            return await interaction.response.send_message("❌ La mise minimale est de 10 Collectron Coins !", ephemeral=True)
        
        user_id = interaction.user.id
        
        # Utilisation de remove_coins
        if not self.data.remove_coins(user_id, mise):
            return await interaction.response.send_message("❌ Tu n'as pas assez de Collectron Coins pour cette mise !", ephemeral=True)

        emojis = ["🍒", "🍇", "🍊", "7️⃣", "💎"]
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        gain = 0
        message = ""

        if a == b == c:
            if a == "7️⃣":
                gain = mise * 10
                message = "🔥 **JACKPOT LÉGENDAIRE !** (x10)"
            elif a == "💎":
                gain = mise * 5
                message = "💎 **DIAMANT !** (x5)"
            else:
                gain = mise * 3
                message = "🎉 **TRIPLE !** (x3)"
        elif a == b or b == c or a == c:
            gain = int(mise * 1.5)
            message = "✨ **Pas mal !** (x1.5)"
        else:
            gain = 0
            message = "💸 **Perdu...** Essaie encore !"

        if gain > 0:
            self.data.add_coins(user_id, gain)

        embed = discord.Embed(title="🎰 Machine à Sous", color=discord.Color.magenta())
        embed.description = f"**{interaction.user.name}** a misé **{mise}** Coins.\n\n" \
                            f"⬇️ ⬇️ ⬇️\n" \
                            f"> | {a} | {b} | {c} |\n" \
                            f"⬆️ ⬆️ ⬆️\n\n" \
                            f"{message}\n" \
                            f"💰 **Gain :** +{gain} Collectron Coins"
        
        await interaction.response.send_message(embed=embed)


    # --- JEU 2 : PIERRE FEUILLE CISEAUX ---
    @app_commands.command(name="pfc", description="🎮 Pierre-Feuille-Ciseaux (Double ou rien)")
    @app_commands.choices(choix=[
        app_commands.Choice(name="Pierre 🪨", value="pierre"),
        app_commands.Choice(name="Feuille 📄", value="feuille"),
        app_commands.Choice(name="Ciseaux ✂️", value="ciseaux")
    ])
    async def pfc(self, interaction: discord.Interaction, choix: app_commands.Choice[str], mise: int):
        if mise < 5:
            return await interaction.response.send_message("❌ Mise minimale : 5 Coins.", ephemeral=True)

        user_id = interaction.user.id
        
        if not self.data.remove_coins(user_id, mise):
            return await interaction.response.send_message("❌ Pas assez de Collectron Coins !", ephemeral=True)

        choix_joueur = choix.value
        possibilites = ["pierre", "feuille", "ciseaux"]
        choix_bot = random.choice(possibilites)
        emojis = {"pierre": "🪨", "feuille": "📄", "ciseaux": "✂️"}

        gain = 0
        resultat_texte = ""

        if choix_joueur == choix_bot:
            resultat_texte = "😐 **Égalité !** Tu récupères ta mise."
            gain = mise
        elif (choix_joueur == "pierre" and choix_bot == "ciseaux") or \
             (choix_joueur == "feuille" and choix_bot == "pierre") or \
             (choix_joueur == "ciseaux" and choix_bot == "feuille"):
            resultat_texte = "🎉 **Gagné !** Tu doubles ta mise !"
            gain = mise * 2
        else:
            resultat_texte = "💀 **Perdu !** Le bot a gagné."
            gain = 0

        if gain > 0:
            self.data.add_coins(user_id, gain)

        embed = discord.Embed(title="🎮 Pierre - Feuille - Ciseaux", color=discord.Color.orange())
        embed.add_field(name="Toi", value=emojis[choix_joueur], inline=True)
        embed.add_field(name="Bot", value=emojis[choix_bot], inline=True)
        embed.add_field(name="Résultat", value=resultat_texte, inline=False)
        embed.set_footer(text=f"Mise: {mise} Collectron Coins")

        await interaction.response.send_message(embed=embed)

    # --- TRAVAILLER ---
    @app_commands.command(name="work", description="Gagner des Collectron Coins (1x par heure)")
    @app_commands.checks.cooldown(1, 3600.0)
    async def work(self, interaction: discord.Interaction):
        gain = random.randint(10, 50)
        self.data.add_coins(interaction.user.id, gain)
        await interaction.response.send_message(f"🔨 Tu as travaillé dur et gagné **{gain}** Collectron Coins ! Reviens dans 1h.")

    @work.error
    async def work_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            secondes_restantes = int(error.retry_after)
            minutes = secondes_restantes // 60
            sec = secondes_restantes % 60
            
            await interaction.response.send_message(
                f"⏳ Doucement ! Tu es fatigué. Reviens travailler dans **{minutes} min et {sec} sec**.", 
                ephemeral=True
            )
        else:
            print(f"Erreur dans work: {error}")

async def setup(client):
    await client.add_cog(GamesCog(client))