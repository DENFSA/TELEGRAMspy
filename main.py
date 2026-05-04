import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

TOKEN = "8675416046:AAECDb2UYJuODlIDzhV1yQSndNxOmlsKtcY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Global data storage
rooms = {}

# Game Packs
PACKS = {
    "dota": {
        "name": "Dota 2 ⚔️",
        "items": ["Axe", "Anti-Mage", "Bane", "Bloodseeker", "Crystal Maiden", "Drow Ranger", "Earthshaker",
                  "Juggernaut", "Mirana", "Morphling", "Shadow Fiend", "Phantom Lancer", "Puck", "Pudge", "Razor",
                  "Sand King", "Storm Spirit", "Sven", "Tiny", "Vengeful Spirit", "Windranger", "Zeus", "Kunkka",
                  "Lina", "Lion", "Shadow Shaman", "Slardar", "Tidehunter", "Witch Doctor", "Lich", "Riki", "Enigma",
                  "Tinker", "Sniper", "Necrophos", "Warlock", "Beastmaster", "Queen of Pain", "Venomancer",
                  "Faceless Void", "Wraith King", "Death Prophet", "Phantom Assassin", "Pugna", "Templar Assassin",
                  "Viper", "Luna", "Dragon Knight", "Dazzle", "Clockwerk", "Leshrac", "Nature's Prophet", "Lifestealer",
                  "Dark Seer", "Clinkz", "Omniknight", "Enchantress", "Huskar", "Night Stalker", "Broodmother",
                  "Bounty Hunter", "Weaver", "Jakiro", "Batrider", "Chen", "Spectre", "Ancient Apparition", "Doom",
                  "Ursa", "Spirit Breaker", "Gyrocopter", "Alchemist", "Invoker", "Silencer", "Outworld Destroyer",
                  "Lycan", "Brewmaster", "Shadow Demon", "Lone Druid", "Chaos Knight", "Meepo", "Treant Protector",
                  "Ogre Magi", "Undying", "Rubick", "Disruptor", "Nyx Assassin", "Naga Siren", "Keeper of the Light",
                  "Io", "Visage", "Slark", "Medusa", "Troll Warlord", "Centaur Warrunner", "Magnus", "Timbersaw",
                  "Bristleback", "Tusk", "Skywrath Mage", "Abaddon", "Elder Titan", "Legion Commander", "Techies",
                  "Ember Spirit", "Earth Spirit", "Underlord", "Terrorblade", "Phoenix", "Oracle", "Winter Wyvern",
                  "Arc Warden", "Monkey King", "Dark Willow", "Pangolier", "Grimstroke", "Hoodwink", "Void Spirit",
                  "Snapfire", "Mars", "Dawnbreaker", "Marci", "Primal Beast", "Muerta"]
    },
    "clash": {
        "name": "Clash Royale 👑",
        "items": ["Knight", "Archers", "Goblins", "Giant", "P.E.K.K.A", "Baby Dragon", "Prince", "Skeletons", "Witch",
                  "Valkyrie", "Musketeer", "Skeleton Army", "Balloon", "Giant Skeleton", "Rage", "Freeze", "Mirror",
                  "Minion Horde", "Inferno Tower", "Elite Barbarians", "Ram Rider", "Electro Giant", "Miner",
                  "Princess", "Ice Wizard", "Sparky", "Inferno Dragon", "Bandit", "Night Witch", "Magic Archer",
                  "Fisherman", "Mega Knight", "Royal Ghost", "Goblin Barrel", "Skeleton Barrel", "Electro Wizard",
                  "Lava Hound", "Mega Minion", "Bomber", "Arrows", "Fireball", "Rocket", "Lightning", "The Log", "Zap",
                  "Poison", "Tornado", "Graveyard", "Hog Rider", "Battle Ram", "Three Musketeers", "Golem", "Ice Golem",
                  "Rascals", "Royal Hogs", "Flying Machine", "Furnace", "Goblin Hut", "Barbarian Hut", "Tombstone",
                  "Tesla", "Cannon", "Mortar", "X-Bow", "Bomb Tower", "Elixir Collector", "Hunter", "Executioner",
                  "Royal Giant", "Electro Dragon", "Battle Healer", "Royal Delivery", "Skeleton Dragons", "Heal Spirit",
                  "Electro Spirit", "Fire Spirit", "Ice Spirit", "Mother Witch", "Golden Knight", "Skeleton King",
                  "Archer Queen", "Monk", "Mighty Miner", "Little Prince", "Phoenix", "Guards", "Dark Prince", "Bowler",
                  "Cannon Cart"]
    },
    "brawl": {
        "name": "Brawl Stars ⭐",
        "items": ["Shelly", "Colt", "Nita", "El Primo", "Poco", "Rosa", "Barley", "Dynamike", "Tick", "Rico", "Darryl",
                  "Penny", "Carl", "Jacky", "Piper", "Pam", "Frank", "Bibi", "Bea", "Nani", "Edgar", "Griff", "Grom",
                  "Bonnie", "Mortis", "Tara", "Gene", "Max", "Mr. P", "Sprout", "Byron", "Squeak", "Spike", "Crow",
                  "Leon", "Sandy", "Amber", "Meg", "Chester"]
    },
    "anime": {
        "name": "Anime ⛩",
        "items": ["Naruto", "Sasuke", "Sakura", "Kakashi", "Itachi", "Madara", "Gaara", "Jiraiya", "Tsunade",
                  "Orochimaru", "Luffy", "Zoro", "Sanji", "Nami", "Chopper", "Robin", "Usopp", "Brook", "Franky", "Ace",
                  "Law", "Kaido", "Goku", "Vegeta", "Gohan", "Piccolo", "Frieza", "Cell", "Majin Buu", "Broly",
                  "Trunks", "Eren", "Mikasa", "Armin", "Levi", "Erwin", "Hange", "Reiner", "Bertholdt", "Zeke", "Annie",
                  "Saitama", "Genos", "Boros", "Garou", "Bang", "Tatsumaki", "Fubuki", "King", "Mumen Rider", "Tanjiro",
                  "Nezuko", "Zenitsu", "Inosuke", "Giyu", "Shinobu", "Rengoku", "Akaza", "Muzan", "Light Yagami", "L",
                  "Ryuk", "Misa", "Near", "Mello", "Rem", "Edward Elric", "Alphonse", "Mustang", "Scar", "Envy",
                  "Greed", "Hohenheim", "Guts", "Griffith", "Casca", "Zodd", "Puck", "Jotaro", "Dio", "Jonathan",
                  "Joseph", "Giorno", "Jolyne", "Yoshikage Kira", "Kakyoin", "Polnareff", "Deku", "Bakugo", "Shoto",
                  "All Might", "Shigaraki", "Dabi", "Toga", "Endeavor", "Ken Kaneki", "Touka", "Rize", "Uta", "Juuzou",
                  "Yamori", "Kirito", "Asuna", "Sinon", "Alice", "Eugeo", "Klein", "Gon", "Killua", "Kurapika",
                  "Leorio", "Hisoka", "Chollo", "Meruem", "Neferpitou", "Asta", "Yuno", "Yami", "Noelle", "Mereoleona",
                  "Licht", "Meliodas", "Elizabeth", "Ban", "King", "Escanor", "Merlin", "Zeldris", "Rimuru", "Benimaru",
                  "Milim", "Shion", "Diablo", "Veldora", "Natsu", "Lucy", "Erza", "Gray", "Happy", "Gajeel", "Jellal",
                  "Zeref", "Yuji Itadori", "Gojo Satoru", "Megumi", "Nobara", "Sukuna", "Mahito", "Nanami", "Toji",
                  "Denji", "Makima", "Power", "Aki", "Reze", "Quanxi", "Pochita", "Shinra", "Arthur", "Maki", "Tamaki",
                  "Benimaru Shinmon", "Sho", "Senku", "Taiju", "Kohaku", "Chrome", "Gen", "Tsukasa", "Anya Forger",
                  "Loid", "Yor", "Bond", "Yuri Briar", "Bojji", "Kage", "Daida", "Hiling", "Thorfin", "Askeladd",
                  "Thorkell", "Canute", "Thors", "Vash the Stampede", "Wolfwood", "Knives", "Ray", "Emma", "Norman",
                  "Isabella", "Mugen", "Jin", "Fuu", "Shinji", "Rei", "Asuka", "Kaworu", "Misato", "Alucard", "Integra",
                  "Seras", "Anderson", "Subaru", "Emilia", "Rem", "Ram", "Beatrice", "Roswaal", "Echidna", "Kazuma",
                  "Aqua", "Megumin", "Darkness", "Wiz", "Naofumi", "Raphtalia", "Filo", "Motoyasu", "Rudeus", "Eris",
                  "Sylphiette", "Roxy", "Ghislaine", "Koro-sensei", "Nagisa", "Karma", "Yato", "Hiyori", "Yukine",
                  "Bishamon", "Momonosuke", "Yamato", "Vivi", "Enel", "Whitebeard", "Shanks", "Teach", "Gowther",
                  "Diane", "Gabriel", "Victor", "Yuri Katsuki", "Ryuko", "Satsuki", "Mako", "Usagi", "Mamoru", "Rei",
                  "Ami", "Minako", "Makoto", "Sailor Moon", "Tuxedo Mask", "Speedwagon", "Caesar", "Bruno Bucciarati",
                  "Mista", "Lelouch", "C.C.", "Suzaku", "Kallen", "Spiegel", "Faye Valentine", "Jet Black", "Mob",
                  "Reigen", "Ekubo", "Teru", "Boruto", "Sarada", "Mitsuki", "Kawaki", "Bocchi", "Nijika", "Ryo",
                  "Ikumi", "Chihiro", "Haku", "No-Face", "Totoro", "Satsuki", "Mei", "Sophie", "Howl", "Calcifer",
                  "Mononoke", "Ashitaka"]
    },
    "cartoons": {
        "name": "Cartoons 📺",
        "items": ["Mickey Mouse", "Donald Duck", "SpongeBob", "Patrick Star", "Shrek", "Donkey", "Simba", "Timon",
                  "Pumbaa", "Bugs Bunny", "Tom", "Jerry", "Homer Simpson", "Bart Simpson", "Peter Griffin",
                  "Rick Sanchez", "Morty Smith", "Finn", "Jake", "Bill Cipher", "Mabel Pines", "Dipper Pines", "Stitch",
                  "Toothless", "Kung Fu Panda", "Squidward", "Elsa", "Olaf", "Lightning McQueen"]
    }
}


# --- HELPER FUNCTIONS ---

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🏠 Create Room")
    builder.button(text="👥 Join Room")
    builder.button(text="📊 Status")
    builder.button(text="🎮 Start Game")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def leave_all_rooms(user_id):
    for room_id in list(rooms.keys()):
        rooms[room_id]["players"] = [p for p in rooms[room_id]["players"] if p["id"] != user_id]
        if not rooms[room_id]["players"]:
            del rooms[room_id]


def get_room_ui(room_id, is_creator=False):
    if room_id not in rooms: return "Room not found.", None
    data = rooms[room_id]
    pack_name = PACKS[data['pack']]['name'] if data['pack'] else "Not selected"

    mode_status = "Selected 🕵️" if data.get("mode_chosen") else "Waiting for selection... ⏳"
    if is_creator and data.get("mode_chosen"):
        mode_status = "🕵️ Normal" if not data.get("fake_mode") else "🎭 Fake Hero"

    status = f"📍 **ID: {room_id}**\n📦 Pack: {pack_name}\n⚙️ Mode: {mode_status}\n👥 Players: {len(data['players'])}\n" + "-" * 15 + "\n"
    status += "\n".join([f"{i}. {p['name']}" for i, p in enumerate(data['players'], 1)])

    builder = InlineKeyboardBuilder()
    builder.button(text="Quick Join ✨", callback_data=f"quick_join_{room_id}")

    if is_creator and not data.get("game_started"):
        builder.button(text="Change Mode 🔄", callback_data=f"toggle_mode_{room_id}")

    builder.adjust(1)
    return status, builder.as_markup()


# --- HANDLERS ---

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Dota 2 Spy Bot is ready! Use the menu:", reply_markup=main_menu())


@dp.message(F.text == "🏠 Create Room")
async def start_creation(message: types.Message):
    leave_all_rooms(message.from_user.id)
    builder = InlineKeyboardBuilder()
    for key, pack in PACKS.items():
        builder.button(text=pack["name"], callback_data=f"select_pack_{key}")
    builder.adjust(1)
    await message.answer("Choose a game pack for the new room:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("select_pack_"))
async def choose_mode_step(callback: types.Callback_query):
    pack_key = callback.data.replace("select_pack_", "")
    room_id = str(random.randint(1000, 9999))

    rooms[room_id] = {
        "creator_id": callback.from_user.id,
        "players": [{"id": callback.from_user.id, "name": callback.from_user.full_name}],
        "pack": pack_key,
        "votes": {},
        "spy_id": None,
        "fake_mode": False,
        "mode_chosen": False,
        "game_started": False
    }

    builder = InlineKeyboardBuilder()
    builder.button(text="🕵️ Normal", callback_data=f"set_mode_normal_{room_id}")
    builder.button(text="🎭 Fake Hero", callback_data=f"set_mode_fake_{room_id}")
    builder.adjust(1)

    await callback.message.edit_text("Great! Now choose a secret game mode (only you will know about this):",
                                     reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(F.data.startswith("set_mode_"))
async def finalize_room(callback: types.Callback_query):
    data_parts = callback.data.split("_")
    mode = data_parts[2]
    room_id = data_parts[3]

    if room_id in rooms:
        rooms[room_id]["fake_mode"] = (mode == "fake")
        rooms[room_id]["mode_chosen"] = True

        text, kb = get_room_ui(room_id, is_creator=True)
        await callback.message.edit_text(f"Room created!\n\n{text}", parse_mode="Markdown", reply_markup=kb)
    await callback.answer("Mode set!")


@dp.callback_query(F.data.startswith("toggle_mode_"))
async def toggle_mode(callback: types.Callback_query):
    room_id = callback.data.replace("toggle_mode_", "")
    if room_id in rooms:
        if callback.from_user.id != rooms[room_id]["creator_id"]:
            await callback.answer("Only the creator can change the mode!", show_alert=True)
            return

        rooms[room_id]["fake_mode"] = not rooms[room_id].get("fake_mode", False)
        text, kb = get_room_ui(room_id, is_creator=True)
        await callback.message.edit_text(f"Mode changed!\n\n{text}", parse_mode="Markdown", reply_markup=kb)
    await callback.answer()


@dp.callback_query(F.data.startswith("quick_join_"))
async def quick_join(callback: types.Callback_query):
    room_id = callback.data.replace("quick_join_", "")
    if room_id in rooms:
        if any(p['id'] == callback.from_user.id for p in rooms[room_id]["players"]):
            await callback.answer("You are already here!", show_alert=True)
            return

        leave_all_rooms(callback.from_user.id)
        rooms[room_id]["players"].append({"id": callback.from_user.id, "name": callback.from_user.full_name})

        text, kb = get_room_ui(room_id, is_creator=False)
        await callback.message.edit_text(f"Updating roster:\n\n{text}", parse_mode="Markdown", reply_markup=kb)
        await callback.answer("You joined the room!")
    else:
        await callback.answer("Room not found", show_alert=True)


@dp.message(F.text == "👥 Join Room")
async def join_guide(message: types.Message):
    await message.answer("To join, enter the command `/join ID` (e.g., `/join 1234`)", parse_mode="Markdown")


@dp.message(Command("join"))
async def join_room(message: types.Message):
    args = message.text.split()
    if len(args) < 2: return
    room_id = args[1]
    if room_id in rooms:
        leave_all_rooms(message.from_user.id)
        rooms[room_id]["players"].append({"id": message.from_user.id, "name": message.from_user.full_name})
        text, kb = get_room_ui(room_id, is_creator=False)
        await message.answer(f"Joined successfully!\n\n{text}", parse_mode="Markdown", reply_markup=kb)
    else:
        await message.answer("Invalid ID.")


@dp.message(F.text == "📊 Status")
async def show_status(message: types.Message):
    for room_id, data in rooms.items():
        if any(p['id'] == message.from_user.id for p in data["players"]):
            is_creator = (message.from_user.id == data["creator_id"])
            text, kb = get_room_ui(room_id, is_creator=is_creator)
            await message.answer(text, parse_mode="Markdown", reply_markup=kb)
            return
    await message.answer("You are not in a room.")


@dp.message(F.text == "🎮 Start Game")
async def start_game_logic(message: types.Message):
    for room_id, data in rooms.items():
        if any(p['id'] == message.from_user.id for p in data["players"]):
            if not data.get("mode_chosen"):
                await message.answer("Creator hasn't chosen a mode yet!")
                return

            players = data["players"]
            if len(players) < 2:
                await message.answer("Not enough players!")
                return

            data["game_started"] = True
            pack_items = PACKS[data["pack"]]["items"]
            main_hero = random.choice(pack_items)
            spy = random.choice(players)
            data["spy_id"], data["votes"] = spy["id"], {}

            fake_hero = None
            if data.get("fake_mode"):
                remaining_items = [i for i in pack_items if i != main_hero]
                fake_hero = random.choice(remaining_items)

            turn_order = players.copy()
            random.shuffle(turn_order)

            for p in players:
                try:
                    if p['id'] == spy['id']:
                        msg = f"🎭 Your character: {fake_hero}\n⚠️ (You are the spy!)" if data.get(
                            "fake_mode") else "🤫 You are the Spy"
                    else:
                        msg = f"Your word: {main_hero}"
                    await bot.send_message(p['id'], msg)
                except:
                    pass

            order_msg = f"🎯 **Turn Order:**\n" + "\n".join([f"{i}. {p['name']}" for i, p in enumerate(turn_order, 1)])
            builder = InlineKeyboardBuilder()
            builder.button(text="Vote 🗳", callback_data=f"vote_start_{room_id}")
            await message.answer(
                f"🚀 Game Started! Mode: {'Fake Hero' if data.get('fake_mode') else 'Normal'}\n\n{order_msg}",
                reply_markup=builder.as_markup())
            return
    await message.answer("Join a room first!")


# --- VOTING AND RESTART ---

@dp.callback_query(F.data.startswith("vote_start_"))
async def vote_init(callback: types.Callback_query):
    room_id = callback.data.split("_")[2]
    players = rooms[room_id]["players"]
    builder = InlineKeyboardBuilder()
    for p in players:
        builder.button(text=p["name"], callback_data=f"vote_for_{room_id}_{p['id']}")
    builder.adjust(2)
    await callback.message.answer("Who is the spy?", reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(F.data.startswith("vote_for_"))
async def vote_process(callback: types.Callback_query):
    _, _, room_id, target_id = callback.data.split("_")
    room = rooms[room_id]
    room["votes"][callback.from_user.id] = int(target_id)
    await callback.answer("Vote accepted!")

    if len(room["votes"]) == len(room["players"]):
        v_counts = {}
        for t_id in room["votes"].values(): v_counts[t_id] = v_counts.get(t_id, 0) + 1

        max_votes = max(v_counts.values())
        leaders = [t_id for t_id, count in v_counts.items() if count == max_votes]

        if len(leaders) > 1:
            res = f"⚖️ **Draw!**\nVotes are split, no one was kicked."
            builder = InlineKeyboardBuilder()
            builder.button(text="Vote Again 🗳", callback_data=f"vote_start_{room_id}")
            builder.button(text="Restart 🔄", callback_data=f"restart_{room_id}")
            builder.adjust(1)
            await callback.message.answer(res, reply_markup=builder.as_markup())
        else:
            voted_id = leaders[0]
            voted_name = next(p["name"] for p in room["players"] if p["id"] == voted_id)
            is_spy = voted_id == room["spy_id"]
            res = f"📊 **Results:**\nKicked {voted_name}.\n\n" + (
                "✅ VICTORY! Spy caught." if is_spy else "❌ DEFEAT! Spy survived.")
            builder = InlineKeyboardBuilder()
            builder.button(text="Restart 🔄", callback_data=f"restart_{room_id}")
            await callback.message.answer(res, reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("restart_"))
async def restart_handler(callback: types.Callback_query):
    room_id = callback.data.split("_")[1]
    if room_id in rooms:
        rooms[room_id]["game_started"] = False
    await start_game_logic(callback.message)
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())