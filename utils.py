import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def check_ban(uid: str) -> dict | None:
    api_url = f"http://raw.thug4ff.xyz/check_ban/{uid}/great"
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    response_data = await response.json()
                    data = response_data.get("data")
                    if data:
                        return {
                            "is_banned": data.get("is_banned", 0),
                            "nickname": data.get("nickname", "N/A"),
                            "period": data.get("period", 0),
                            "region": data.get("region", "N/A")
                        }
                return None
    except Exception as e:
        print(f"Ban check API error for UID {uid}: {e}")
        return None

async def get_player_info(uid: str) -> dict | None:
    api_url = f"https://info.killersharmabot.online/player-info?uid={uid}"
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        print(f"Player info API error for UID {uid}: {e}")
        return None
