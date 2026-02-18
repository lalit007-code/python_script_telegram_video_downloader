import os
import time
from telethon import TelegramClient
from config import API_ID, API_HASH, CHANNEL, DOWNLOAD_PATH

# Ensure download directory exists
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def progress_callback(current, total):
    percent = current / total * 100
    print(f"\rProgress: {percent:.1f}%", end="", flush=True)

async def main():
    client = TelegramClient("session", API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("Error: Not logged in. Run 'python login.py' first.")
        return

    print("Connected to Telegram!")

    # Get the channel
    channel = await client.get_entity(CHANNEL)
    print(f"Accessing channel: {channel.title}")

    # Count videos first
    video_count = 0
    async for message in client.iter_messages(channel):
        if message.video:
            video_count += 1
    print(f"Found {video_count} videos in channel")

    # Download videos
    downloaded = 0
    async for message in client.iter_messages(channel):
        if message.video:
            downloaded += 1
            filename = f"video_{message.id}.mp4"
            filepath = os.path.join(DOWNLOAD_PATH, filename)

            # Skip if already downloaded
            if os.path.exists(filepath):
                print(f"[{downloaded}/{video_count}] Skipping {filename} (already exists)")
                continue

            print(f"\n[{downloaded}/{video_count}] Downloading {filename}...")
            await client.download_media(
                message.video,
                file=filepath,
                progress_callback=progress_callback
            )
            print(f" Done!")

            # Small delay to avoid rate limiting
            time.sleep(1)

    print(f"\nCompleted! Downloaded videos to {DOWNLOAD_PATH}")
    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
