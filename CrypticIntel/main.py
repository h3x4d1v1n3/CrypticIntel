from CrypticIntel.bot import CrypticIntel
from CrypticIntel.bot.config import DISCORD_BOT_API

if __name__ == "__main__":
    bot = CrypticIntel(debug=True)
    bot.run(DISCORD_BOT_API)