import asyncio
import os
import time
import aiohttp
import zipfile
from io import BytesIO
from datetime import datetime
from typing import Optional, List

# Configuration
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
URL = "https://results.beup.ac.in/BTech4thSem2024_B2022Results.aspx"

CHECK_INTERVAL = 2            # seconds between checks
CONTINUOUS_DURATION = 900     # 15 minutes in seconds

RESULT_URLS = [
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148040",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148042",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148051",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148018",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148012",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22104148015",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22101148008",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148023",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148001",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=23156148904",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148039",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148021",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148007",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148026",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148036",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148019",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148041",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148038",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148006",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148027",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148031",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148035",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148013",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148050",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148053",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148016",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148022",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148032",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148009",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148028",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148033",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148015",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148024",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148048",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148017",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148037",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148052",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148045",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148005",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148003",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148020",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148044",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148034",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148030",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148008",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148046",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148047",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148002",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148029",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148004",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148011",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22156148014",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=23156148901",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=23156148903",
    "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=23156148902"
]


class DiscordMonitor:
    def __init__(self):
        self.rate_limit_remaining = 5
        self.rate_limit_reset = 0

    async def send_discord_message(self, content: str, username: str = "BEUP Monitor") -> bool:
        if not DISCORD_WEBHOOK_URL:
            print("ERROR: DISCORD_WEBHOOK_URL not set")
            return False
        now = time.time()
        if self.rate_limit_remaining <= 0 and now < self.rate_limit_reset:
            await asyncio.sleep(self.rate_limit_reset - now)
        payload = {"content": content, "username": username}
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)
                if resp.status == 429:
                    retry = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry)
                    return await self.send_discord_message(content, username)
                return resp.status in (200, 204)

    async def send_file(self, filename: str, data: BytesIO) -> bool:
        form = aiohttp.FormData()
        data.seek(0)
        form.add_field(
            "file", data,
            filename=filename,
            content_type="application/zip" if filename.endswith(".zip") else "text/html"
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, data=form) as resp:
                now = time.time()
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)
                if resp.status == 429:
                    retry = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry)
                    return await self.send_file(filename, data)
                return resp.status in (200, 204)

    async def check_site(self) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=10) as resp:
                    return "UP" if resp.status == 200 else "DOWN"
        except:
            return "DOWN"

    async def download_and_zip(self) -> BytesIO:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            async with aiohttp.ClientSession() as session:
                for idx, url in enumerate(RESULT_URLS, start=1):
                    reg = url.split("=")[-1]
                    try:
                        async with session.get(url, timeout=10) as resp:
                            if resp.status == 200:
                                html = await resp.text()
                                zf.writestr(f"result_{reg}.html", html)
                    except Exception as e:
                        print(f"ERROR downloading {reg}: {e}")
                    if idx % 10 == 0 or idx == len(RESULT_URLS):
                        await self.send_discord_message(
                            f"🔄 Downloaded & added to ZIP: {idx}/{len(RESULT_URLS)}"
                        )
        zip_buffer.seek(0)
        return zip_buffer

    async def continuous_status(self, duration: int):
        end_time = time.time() + duration
        while time.time() < end_time:
            await self.send_discord_message("✅ Website is still UP")
            await asyncio.sleep(CHECK_INTERVAL)

    async def monitor_once(self):
        status = await self.check_site()
        if status != "UP":
            await self.send_discord_message("🔴 Website is DOWN")
            return

        await self.send_discord_message("🎉 Website is LIVE! Starting downloads…")
        zip_data = await self.download_and_zip()

        # Attempt ZIP upload
        if zip_data and await self.send_file("results.zip", zip_data):
            await self.send_discord_message(
                f"📥 Successfully uploaded all {len(RESULT_URLS)} results in a single ZIP"
            )
        else:
            # Fallback to individual uploads
            await self.send_discord_message(
                "⚠️ ZIP upload failed; falling back to individual uploads"
            )
            async with aiohttp.ClientSession() as session:
                for idx, url in enumerate(RESULT_URLS, start=1):
                    reg = url.split("=")[-1]
                    try:
                        async with session.get(url, timeout=10) as resp:
                            if resp.status == 200:
                                bio = BytesIO((await resp.text()).encode("utf-8"))
                                await self.send_file(f"result_{reg}.html", bio)
                    except:
                        pass
                    if idx % 10 == 0 or idx == len(RESULT_URLS):
                        await self.send_discord_message(
                            f"🔄 Fallback uploaded {idx}/{len(RESULT_URLS)}"
                        )
            await self.send_discord_message(
                "📥 Fallback: individual files uploaded"
            )

        # Continue sending "site is up" for next 15 minutes
        await self.continuous_status(CONTINUOUS_DURATION)

async def main():
    monitor = DiscordMonitor()
    try:
        await monitor.monitor_once()
    except Exception as e:
        print("❌ Exception in monitor:", e)
        raise

if __name__ == "__main__":
    asyncio.run(main())
