from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from config import API_ID, API_HASH

PHONE = "+918882230066"

async def main():
    client = TelegramClient("session", API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        print("OTP sent to your Telegram app!")
        print("Check your Telegram and enter the code below.")

        code = input("Enter OTP code: ")
        try:
            await client.sign_in(PHONE, code)
        except SessionPasswordNeededError:
            password = input("2FA enabled. Enter your password: ")
            await client.sign_in(password=password)

    print("Logged in successfully!")
    print(f"You are: {(await client.get_me()).first_name}")
    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
