import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def check_ban(uid: str) -> tuple[dict | None, str | None]:
    api_url = f"http://raw.thug4ff.xyz/check_ban/{uid}/great"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    timeout = aiohttp.ClientTimeout(total=15)

    try:
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    response_data = await response.json()
                    data = response_data.get("data")
                    if data:
                        return {
                            "is_banned": data.get("is_banned", 0),
                            "nickname": data.get("nickname", "NA"),
                            "period": data.get("period", 0),
                            "region": data.get("region", "N/A")
                        }, None
                    return None, "Empty data received"
                else:
                    return None, f"API Status {response.status}"
    except asyncio.TimeoutError:
        return None, "API Timeout"
    except aiohttp.ClientError as e:
        return None, f"Network Error: {type(e).__name__}"
    except Exception as e:
        return None, str(e)
