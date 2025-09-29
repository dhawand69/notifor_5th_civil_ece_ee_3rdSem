import asyncio
import os
import time
import aiohttp
import json
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
        if not DISCORD_WEBHOOK_URL:
            print("Discord webhook URL not configured")
            return False

        current_time = time.time()
        if self.rate_limit_remaining <= 0 and current_time < self.rate_limit_reset:
            await asyncio.sleep(self.rate_limit_reset - current_time)

        payload = {"content": content, "username": username}
        if embeds:
            payload["embeds"] = embeds

        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = current_time + float(reset_after)

                if resp.status == 429:
                    retry_after = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry_after)
                    return await self.send_discord_message(content, embeds, username)

                return resp.status in (200, 204)

    async def send_file(self, filename: str, content: str) -> bool:
        if not DISCORD_WEBHOOK_URL:
            return False

        form = aiohttp.FormData()
        bio = BytesIO(content.encode("utf-8"))
        bio.seek(0)
        form.add_field("file", bio, filename=filename, content_type="text/html")
        form.add_field(
            "payload_json",
            json.dumps({
                "content": f"📄 Uploaded result: `{filename}`",
                "username": "BEUP Result Monitor"
            }),
            content_type="application/json"
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, data=form) as resp:
                return resp.status in (200, 204)

    async def create_embed(
        self,
        title: str,
        description: str,
        color: int,
        fields: Optional[List[dict]] = None
    ) -> dict:
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
        success, fail = [], []
        total = len(RESULT_URLS)
        for index, url in enumerate(RESULT_URLS, start=1):
            reg_no = url.split("=")[-1]
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=10) as r:
                        if r.status == 200:
                            html = await r.text()
                            filename = f"result_{reg_no}.html"
                            if await self.send_file(filename, html):
                                success.append(reg_no)
                            else:
                                fail.append(reg_no)
                        else:
                            fail.append(reg_no)
            except Exception:
                fail.append(reg_no)

            # Send progress update after each download
            await self.send_discord_message(
                f"🔄 Download progress: {len(success)}/{total} completed"
            )

        # Final summary embed
        embed = await self.create_embed(
            title="📥 Result Download Summary",
            description=f"✅ {len(success)} succeeded, ❌ {len(fail)} failed",
            color=0x00ff00 if not fail else 0xff0000,
            fields=[
                {"name": "Successes", "value": str(len(success)), "inline": True},
                {"name": "Failures",  "value": str(len(fail)),    "inline": True},
                {"name": "Total",     "value": str(total),          "inline": True},
            ]
        )
        await self.send_discord_message("", embeds=[embed])
        return bool(success)

    async def check_site(self) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=10) as resp:
                    return "UP" if resp.status == 200 else "DOWN"
        except:
            return "DOWN"

    async def monitor_once(self):
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
                await self.send_discord_message(f"✅ Still live ({time_left}s left)")
                if not self.results_downloaded and time_left > 60:
                    self.results_downloaded = True
                    asyncio.create_task(self.download_results())

            elif now - self.last_scheduled >= SCHEDULED_INTERVAL and now >= self.continuous_until:
                text = "✅ Live" if current == "UP" else "🔴 Down"
                await self.send_discord_message(f"📅 Scheduled: {text}")
                self.last_scheduled = now

            self.last_status = current
            await asyncio.sleep(CHECK_INTERVAL)

async def main():
    monitor = DiscordMonitor()
    if os.getenv("GITHUB_ACTIONS"):
        await monitor.monitor_once()
    else:
        await monitor.monitor_continuous()

if __name__ == "__main__":
    asyncio.run(main())
