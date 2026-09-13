import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading
from utils import check_ban

app = Flask(__name__)

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

nomBot = "PX Ban Checker"

@app.route('/')
def home():
    return f"Bot {nomBot} is running healthy!"

@app.route('/healthz')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

# Background Flask server for Render keep-alive
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

@bot.event
async def on_ready():
    global nomBot
    nomBot = f"{bot.user}"
    print(f"[ONLINE] Logged in as {bot.user}")

@bot.command(name="check", aliases=["ID", "id"])
async def check_ban_command(ctx, user_id: str = None):
    if not user_id or not user_id.isdigit():
        await ctx.send(f"{ctx.author.mention} ❌ **Invalid UID!**\n➡️ Format: `!check 123456789`")
        return

    async with ctx.typing():
        ban_status, error_msg = await check_ban(user_id)

        if ban_status is None:
            err_detail = f" (`{error_msg}`)" if error_msg else ""
            await ctx.send(f"{ctx.author.mention} ❌ **Could not get information.**{err_detail}\nPlease try again later.")
            return

        is_banned = int(ban_status.get("is_banned", 0))
        period = ban_status.get("period", "N/A")
        nickname = ban_status.get("nickname", "NA")
        region = ban_status.get("region", "N/A")
        id_str = f"`{user_id}`"

        period_str = f"more than {period} months" if isinstance(period, int) else "unavailable"

        embed = discord.Embed(
            color=0xFF0000 if is_banned else 0x00FF00,
            timestamp=ctx.message.created_at
        )

        file = None
        if is_banned:
            embed.title = "**▌ Banned Account 🛑 **"
            embed.description = (
                f"**• Reason :** This account was confirmed for using cheats.\n"
                f"**• Suspension duration :** {period_str}\n"
                f"**• Nickname :** `{nickname}`\n"
                f"**• Player ID :** `{id_str}`\n"
                f"**• Region :** `{region}`"
            )
            if os.path.exists("assets/banned.gif"):
                file = discord.File("assets/banned.gif", filename="banned.gif")
                embed.set_image(url="attachment://banned.gif")
        else:
            embed.title = "**▌ Clean Account ✅ **"
            embed.description = (
                f"**• Status :** No sufficient evidence of cheat usage on this account.\n"
                f"**• Nickname :** `{nickname}`\n"
                f"**• Player ID :** `{id_str}`\n"
                f"**• Region :** `{region}`"
            )
            if os.path.exists("assets/notbanned.gif"):
                file = discord.File("assets/notbanned.gif", filename="notbanned.gif")
                embed.set_image(url="attachment://notbanned.gif")

        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="DEVELOPED BY PERSISTX•")

        if file:
            await ctx.send(f"{ctx.author.mention}", embed=embed, file=file)
        else:
            await ctx.send(f"{ctx.author.mention}", embed=embed)

if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: TOKEN environment variable is missing!")
    else:
        bot.run(TOKEN)
