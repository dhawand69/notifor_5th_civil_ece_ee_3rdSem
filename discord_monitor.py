```python
import asyncio
import os
import time
import aiohttp
from io import BytesIO
from datetime import datetime
from typing import Optional, List

# Configuration
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
URL = "https://results.beup.ac.in/BTech4thSem2024_B2022Results.aspx"

CHECK_INTERVAL = 2
SCHEDULED_INTERVAL = 7200
CONTINUOUS_DURATION = 900

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
        self.last_status = None
        self.last_scheduled = 0
        self.continuous_until = 0
        self.results_downloaded = False
        self.rate_limit_remaining = 5
        self.rate_limit_reset = 0

    async def send_discord_message(
        self,
        content: str,
        embeds: Optional[List[dict]] = None,
        username: str = "BEUP Monitor"
    ) -> bool:
        print("STEP: send_discord_message called")
        if not DISCORD_WEBHOOK_URL:
            print("ERROR: DISCORD_WEBHOOK_URL not set")
            return False

        now = time.time()
        if self.rate_limit_remaining <= 0 and now < self.rate_limit_reset:
            wait = self.rate_limit_reset - now
            print(f"INFO: Rate limited, sleeping for {wait:.2f}s")
            await asyncio.sleep(wait)

        payload = {"content": content, "username": username}
        if embeds:
            payload["embeds"] = embeds

        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                print(f"INFO: Discord message status {resp.status}")
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)

                if resp.status == 429:
                    retry_after = float(resp.headers.get("retry-after", 1))
                    print(f"WARNING: Hit rate limit, retrying after {retry_after}s")
                    await asyncio.sleep(retry_after)
                    return await self.send_discord_message(content, embeds, username)

                return resp.status in (200, 204)

    async def send_file(self, session: aiohttp.ClientSession, filename: str, content: str) -> bool:
        print(f"STEP: send_file called for {filename}")
        form = aiohttp.FormData()
        bio = BytesIO(content.encode("utf-8"))
        bio.seek(0)
        form.add_field("file", bio, filename=filename, content_type="text/html")

        async with session.post(DISCORD_WEBHOOK_URL, data=form) as resp:
            print(f"INFO: send_file status {resp.status} for {filename}")
            now = time.time()
            self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
            reset_after = resp.headers.get("X-RateLimit-Reset-After")
            if reset_after:
                self.rate_limit_reset = now + float(reset_after)

            if resp.status == 429:
                retry_after = float(resp.headers.get("retry-after", 1))
                print(f"WARNING: File upload rate limited, retrying after {retry_after}s")
                await asyncio.sleep(retry_after)
                return await self.send_file(session, filename, content)

            return resp.status in (200, 204)

    async def create_embed(
        self,
        title: str,
        description: str,
        color: int,
        fields: Optional[List[dict]] = None
    ) -> dict:
        print("STEP: create_embed called")
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "BEUP Result Monitor",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            }
        }
        if fields:
            embed["fields"] = fields
        return embed

    async def download_results(self) -> bool:
        print("STEP: download_results started")
        total = len(RESULT_URLS)
        success_count = 0

        async with aiohttp.ClientSession() as session:
            for idx, url in enumerate(RESULT_URLS, start=1):
                reg_no = url.split("=")[-1]
                print(f"STEP: downloading {reg_no}")
                try:
                    async with session.get(url, timeout=10) as resp:
                        print(f"INFO: GET {url} status {resp.status}")
                        if resp.status == 200:
                            html = await resp.text()
                            filename = f"result_{reg_no}.html"
                            if await self.send_file(session, filename, html):
                                success_count += 1
                except Exception as e:
                    print(f"ERROR: Exception downloading {reg_no}: {e}")

                await asyncio.sleep(1)  # Avoid bursts
                print(f"STEP: progress update {success_count}/{total}")
                await self.send_discord_message(
                    f"🔄 Download progress: {success_count}/{total} completed"
                )

        print("STEP: download_results completed")
        embed = await self.create_embed(
            title="📥 Result Download Summary",
            description=f"✅ {success_count}/{total} files uploaded",
            color=0x00ff00 if success_count == total else 0xff0000
        )
        await self.send_discord_message("", embeds=[embed])
        return success_count > 0

    async def check_site(self) -> str:
        print("STEP: check_site called")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=10) as resp:
                    print(f"INFO: site check status {resp.status}")
                    return "UP" if resp.status == 200 else "DOWN"
        except Exception as e:
            print(f"ERROR: Exception in check_site: {e}")
            return "DOWN"

    async def monitor_once(self):
        print("STEP: monitor_once called")
        status = await self.check_site()
        if status == "UP":
            embed = await self.create_embed(
                "🎉 Website is LIVE!",
                "Starting result downloads…",
                0x00ff00,
                [
                    {"name": "Status", "value": "✅ Online", "inline": True},
                    {"name": "Time",   "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": True}
                ]
            )
            await self.send_discord_message("@everyone", embeds=[embed])
            await asyncio.sleep(2)
            await self.download_results()
        else:
            embed = await self.create_embed(
                "🔴 Website is DOWN",
                "Results site not accessible",
                0xff0000,
                [
                    {"name": "Status", "value": "❌ Offline", "inline": True},
                    {"name": "Time",   "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": True}
                ]
            )
            await self.send_discord_message("", embeds=[embed])

    async def monitor_continuous(self):
        print("STEP: monitor_continuous started")
        await self.send_discord_message("🔍 Monitoring started")
        while True:
            current = await self.check_site()
            now = time.time()
            changed = current != self.last_status

            if changed:
                if current == "UP":
                    self.continuous_until = now + CONTINUOUS_DURATION
                    self.results_downloaded = False
                    embed = await self.create_embed("🎉 Site LIVE!", "Downloading results…", 0x00ff00)
                    await self.send_discord_message("@everyone", embeds=[embed])
                    asyncio.create_task(self.download_results())
                else:
                    embed = await self.create_embed("🔴 Site DOWN", "Site offline", 0xff0000)
                    await self.send_discord_message("", embeds=[embed])
                    self.results_downloaded = False

            elif current == "UP" and now < self.continuous_until:
                time_left = int(self.continuous_until - now)
                print(f"STEP: still live, {time_left}s left")
                await self.send_discord_message(f"✅ Still live ({time_left}s left)")
                if not self.results_downloaded and time_left > 60:
                    self.results_downloaded = True
                    asyncio.create_task(self.download_results())

            elif now - self.last_scheduled >= SCHEDULED_INTERVAL and now >= self.continuous_until:
                text = "✅ Live" if current == "UP" else "🔴 Down"
                print(f"STEP: scheduled check, status {text}")
                await self.send_discord_message(f"📅 Scheduled: {text}")
                self.last_scheduled = now

            self.last_status = current
            await asyncio.sleep(CHECK_INTERVAL)

async def main():
    print("STEP: main started")
    monitor = DiscordMonitor()
    if os.getenv("GITHUB_ACTIONS"):
        await monitor.monitor_once()
    else:
        await monitor.monitor_continuous()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        import traceback
        print("❌ Exception in monitor:", e)
        traceback.print_exc()
        raise
```
