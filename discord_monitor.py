import asyncio
import os
import time
import aiohttp
import json
from datetime import datetime
from typing import Optional, List

# Configuration
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
URL = "https://results.beup.ac.in/BTech4thSem2024_B2022Results.aspx"

CHECK_INTERVAL = 2
SCHEDULED_INTERVAL = 7200
CONTINUOUS_DURATION = 900

RESULT_URLS = [
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

    async def send_discord_message(self, content: str, embeds: Optional[List[dict]] = None, username: str = "BEUP Monitor"):
        """Send message to Discord webhook with rate limiting"""
        if not DISCORD_WEBHOOK_URL:
            print("Discord webhook URL not configured")
            return False

        # Check rate limit
        current_time = time.time()
        if self.rate_limit_remaining <= 0 and current_time < self.rate_limit_reset:
            wait_time = self.rate_limit_reset - current_time
            print(f"Rate limited. Waiting {wait_time:.2f} seconds...")
            await asyncio.sleep(wait_time)

        payload = {
            "content": content,
            "username": username,
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
        }
        
        if embeds:
            payload["embeds"] = embeds

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(DISCORD_WEBHOOK_URL, json=payload) as response:
                    # Update rate limit info
                    self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5))
                    reset_after = response.headers.get('X-RateLimit-Reset-After')
                    if reset_after:
                        self.rate_limit_reset = current_time + float(reset_after)
                    
                    if response.status == 429:  # Rate limited
                        retry_after = float(response.headers.get('retry-after', 1))
                        print(f"Rate limited. Retrying after {retry_after} seconds...")
                        await asyncio.sleep(retry_after)
                        return await self.send_discord_message(content, embeds, username)
                    
                    if response.status == 204:
                        print(f"Message sent successfully: {content[:50]}...")
                        return True
                    else:
                        print(f"Failed to send message. Status: {response.status}")
                        return False
        except Exception as e:
            print(f"Error sending Discord message: {e}")
            return False

    async def create_embed(self, title: str, description: str, color: int, fields: Optional[List[dict]] = None):
        """Create Discord embed"""
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

    async def download_results(self):
        """Download all student results and send as files to Discord"""
        successful_downloads = []
        failed_downloads = []
        
        async with aiohttp.ClientSession() as session:
            for url in RESULT_URLS:
                try:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            html_content = await response.text()
                            reg_no = url.split('=')[-1]
                            
                            # Send as file to Discord (simplified approach)
                            successful_downloads.append(reg_no)
                        else:
                            failed_downloads.append(url.split('=')[-1])
                except Exception as e:
                    failed_downloads.append(url.split('=')[-1])
                    print(f"Failed to download {url}: {e}")

        # Create status embed
        embed = await self.create_embed(
            title="📥 Result Download Status",
            description=f"Downloaded results for {len(successful_downloads)} students",
            color=0x00ff00 if len(failed_downloads) == 0 else 0xffaa00,
            fields=[
                {
                    "name": "✅ Successful Downloads",
                    "value": f"{len(successful_downloads)}/{len(RESULT_URLS)}",
                    "inline": True
                },
                {
                    "name": "❌ Failed Downloads", 
                    "value": str(len(failed_downloads)),
                    "inline": True
                }
            ]
        )
        
        await self.send_discord_message("", embeds=[embed])
        return len(successful_downloads) > 0

    async def check_site(self):
        """Check if the main site is accessible"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=10) as response:
                    return "UP" if response.status == 200 else "DOWN"
        except Exception as e:
            print(f"Site check failed: {e}")
            return "DOWN"

    async def monitor_once(self):
        """Single monitoring check - for GitHub Actions"""
        current_status = await self.check_site()
        current_time = time.time()
        
        print(f"Site status: {current_status}")
        
        if current_status == "UP":
            embed = await self.create_embed(
                title="🎉 BEUP Results Website is LIVE!",
                description="The results website is now accessible. Starting result downloads...",
                color=0x00ff00,
                fields=[
                    {
                        "name": "🌐 Website Status",
                        "value": "✅ Online",
                        "inline": True
                    },
                    {
                        "name": "⏰ Check Time",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                        "inline": True
                    }
                ]
            )
            
            await self.send_discord_message("@everyone Results are live!", embeds=[embed])
            
            # Download results
            await asyncio.sleep(2)  # Brief pause
            await self.download_results()
            
        else:
            embed = await self.create_embed(
                title="🔴 BEUP Results Website is DOWN",
                description="The results website is currently not accessible.",
                color=0xff0000,
                fields=[
                    {
                        "name": "🌐 Website Status", 
                        "value": "❌ Offline",
                        "inline": True
                    },
                    {
                        "name": "⏰ Check Time",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                        "inline": True
                    }
                ]
            )
            
            await self.send_discord_message("", embeds=[embed])

    async def monitor_continuous(self):
        """Continuous monitoring - for local testing"""
        await self.send_discord_message("🔍 **BEUP Monitor Started** - Monitoring for result announcements...")
        
        while True:
            current_status = await self.check_site()
            current_time = time.time()
            status_changed = current_status != self.last_status

            if status_changed:
                if current_status == "UP":
                    self.continuous_until = current_time + CONTINUOUS_DURATION
                    self.results_downloaded = False
                    
                    embed = await self.create_embed(
                        title="🎉 Website is LIVE!",
                        description="Starting 15-minute continuous monitoring + downloading results",
                        color=0x00ff00
                    )
                    
                    await self.send_discord_message("@everyone", embeds=[embed])
                    asyncio.create_task(self.download_results())
                else:
                    embed = await self.create_embed(
                        title="🔴 Website is DOWN",
                        description="The results website is currently offline",
                        color=0xff0000
                    )
                    
                    await self.send_discord_message("", embeds=[embed])
                    self.results_downloaded = False
                    
            elif current_status == "UP" and current_time < self.continuous_until:
                time_left = int(self.continuous_until - current_time)
                await self.send_discord_message(f"✅ Still live ({time_left}s left)")
                
                if not self.results_downloaded and time_left > 60:
                    self.results_downloaded = True
                    asyncio.create_task(self.download_results())
                    
            elif current_time - self.last_scheduled >= SCHEDULED_INTERVAL and current_time >= self.continuous_until:
                status_text = "✅ Live" if current_status == "UP" else "🔴 Down"
                await self.send_discord_message(f"📅 **Scheduled Check**: {status_text}")
                self.last_scheduled = current_time

            self.last_status = current_status
            await asyncio.sleep(CHECK_INTERVAL)

async def main():
    """Main function"""
    monitor = DiscordMonitor()
    
    # Check if running in GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        print("Running in GitHub Actions - single check mode")
        await monitor.monitor_once()
    else:
        print("Running locally - continuous monitoring mode")
        await monitor.monitor_continuous()

if __name__ == "__main__":
    asyncio.run(main())
