import discord
from discord.ext import commands
import json
import os

DATA_FILE = "data.json"
IMAGE_DIR = "images"

DEFAULT_ITEMS = {
    "potion":   {"buy": 50,   "sell": 25,  "emoji": "🧪", "image": "potion.png"},
    "katana":     {"buy": 1000,  "sell": 750,  "emoji": "⚔️", "image": "katana.png"},
    "clé egyptienne": {"buy": 2000,   "sell": 1500, "emoji": "🗝️", "image": "egypt.png"},
    "master ball": {"buy": 5000,  "sell": 3000,  "emoji": "🔴⚪", "image": "master.png"}
}

DEFAULT_STOCK = {
    "potion": 10,
    "katana": 3,
    "clé egyptienne": 5,
    "master ball": 1
}

class DataManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except:
                self.data = {}
        else:
            self.data = {}

        if "users" not in self.data: self.data["users"] = {}
        if "shop_stock" not in self.data: self.data["shop_stock"] = DEFAULT_STOCK.copy()
        
        if "items_config" not in self.data: 
            self.data["items_config"] = DEFAULT_ITEMS.copy()
        else:
            for item, details in DEFAULT_ITEMS.items():
                if item in self.data["items_config"]:
                    if "image" not in self.data["items_config"][item]:
                        self.data["items_config"][item]["image"] = details["image"]
                else:
                    self.data["items_config"][item] = details

        self.save_data()
        print("📂 Données JSON chargées.")

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def check_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.data["users"]:
            # On garde la clé "points" dans le JSON pour ne pas perdre la sauvegarde actuelle
            self.data["users"][user_id] = {"points": 100, "inventory": []}
            self.save_data()

    # --- Gestion des Collectron Coins (Renommé) ---
    def get_coins(self, user_id):
        self.check_user(user_id)
        return self.data["users"][str(user_id)]["points"]

    def add_coins(self, user_id, amount):
        self.check_user(user_id)
        self.data["users"][str(user_id)]["points"] += amount
        self.save_data()

    def remove_coins(self, user_id, amount):
        self.check_user(user_id)
        if self.data["users"][str(user_id)]["points"] >= amount:
            self.data["users"][str(user_id)]["points"] -= amount
            self.save_data()
            return True
        return False

    # --- Inventaire ---
    def get_inventory(self, user_id):
        self.check_user(user_id)
        return self.data["users"][str(user_id)]["inventory"]

    def add_item_to_user(self, user_id, item_name):
        self.check_user(user_id)
        self.data["users"][str(user_id)]["inventory"].append(item_name)
        self.save_data()

    def remove_item_from_user(self, user_id, item_name):
        self.check_user(user_id)
        inventory = self.data["users"][str(user_id)]["inventory"]
        if item_name in inventory:
            inventory.remove(item_name)
            self.save_data()
            return True
        return False

    # --- Gestion Items & Images ---
    def get_all_items_config(self):
        return self.data["items_config"]

    def get_item_info(self, item_name):
        return self.data["items_config"].get(item_name)

    def get_stock(self, item_name):
        return self.data["shop_stock"].get(item_name, 0)

    def remove_stock(self, item_name, amount=1):
        if self.data["shop_stock"].get(item_name, 0) >= amount:
            self.data["shop_stock"][item_name] -= amount
            self.save_data()
            return True
        return False

    def add_stock(self, item_name, amount=1):
        self.data["shop_stock"][item_name] = self.data["shop_stock"].get(item_name, 0) + amount
        self.save_data()

    def create_new_item(self, name, price, sell_price, emoji, stock, image_filename="default.png"):
        self.data["items_config"][name] = {
            "buy": price,
            "sell": sell_price,
            "emoji": emoji,
            "image": image_filename
        }
        self.data["shop_stock"][name] = stock
        self.save_data()

    def get_item_file(self, item_name):
        info = self.get_item_info(item_name)
        if not info or "image" not in info:
            return None
        
        filename = info["image"]
        path = os.path.join(IMAGE_DIR, filename)
        
        if os.path.exists(path):
            return discord.File(path, filename=filename)
        else:
            print(f"⚠️ Image introuvable : {path}")
            return None

async def setup(client):
    await client.add_cog(DataManager(client))