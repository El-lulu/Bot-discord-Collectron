import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio # Important pour le chargement

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            help_command=None
        )

    async def setup_hook(self):
        print("--- Chargement des extensions ---")
        # Note le "cogs." devant les noms
        try:
            await self.load_extension("cogs.database")
            print("✅ Database chargée")
            await self.load_extension("cogs.economy")
            print("✅ Economy chargée")
            await self.load_extension("cogs.games")
            print("✅ Games chargée")
            await self.load_extension("cogs.admin")
            print("✅ Admin chargé")
            await self.load_extension("cogs.help")
            print("✅ Help chargé")
            
            await self.tree.sync()
            print("✅ Tout est synchronisé !")
        except Exception as e:
            print(f"❌ ERREUR lors du chargement : {e}")

    async def on_ready(self):
        print(f"🚀 Connecté sur {self.user} (ID: {self.user.id})")
        print("------")

async def main():
    async with MyBot() as bot:
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            print("❌ ERREUR : Le token est introuvable. Vérifie ton fichier .env")
            return
        await bot.start(token)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Permet d'arrêter le bot proprement avec Ctrl+C
        pass