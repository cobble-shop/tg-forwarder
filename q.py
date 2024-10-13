import asyncio
from telethon import TelegramClient, errors # type: ignore

# Replace 'API_ID' and 'API_HASH' with your actual API ID and Hash
api_id = '22435521'
api_hash = 'c21b7141e3b89e0fa26267f855cfede1'

# Replace 'PHONE_NUMBER' with your phone number associated with Telegram
phone_number = '+32468540307'

# Message link to fetch content from
message_link = 'https://t.me/arsiismm/17'

# List of channel IDs or usernames
channels = [
    'https://t.me/wheretosell',
    'https://t.me/ezbadgechat',
    'https://t.me/badgeswtbs',
    'https://t.me/nitrouhq',
    'https://t.me/discorduhqwts',
    'https://t.me/badgeswts',
    'https://t.me/badgewts',
    'https://t.me/citybadgechat',
    'https://t.me/wtbwtsgroup',
    'https://t.me/discordwtswtb',
    'https://t.me/channelwts',
    'https://t.me/dswtbwts',
    'https://t.me/spongeservices',
    'https://t.me/badgechat',
    'https://t.me/iswtswtb',
    'https://t.me/wtbwtsdiscord',
    'https://t.me/discordpms',
    'https://t.me/empyrusWB'
]

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    print("Client Created")

    # Parse the link to get the channel ID and message ID
    parts = message_link.split('/')
    channel_username = parts[-2]
    message_id = int(parts[-1])

    try:
        # Retrieve the original message entity
        original_channel = await client.get_entity(channel_username)
        original_message = await client.get_messages(original_channel, ids=message_id)

        if not original_message:
            print("Failed to fetch the message content.")
            return
    except errors.ChannelPrivateError:
        print("The original channel is private, and you do not have access.")
        return
    except Exception as e:
        print(f'Failed to retrieve the original message: {e}')
        return

    for channel in channels:
        try:
            # Retrieve the entity for the target channel
            target_channel = await client.get_entity(channel)
            # Forward the fetched message to the target channel
            await client.forward_messages(target_channel, original_message)
            print(f'Message forwarded to {channel}')
            # Wait for 2 seconds before sending the next message
            await asyncio.sleep(5)

        except errors.rpcerrorlist.FloodWaitError as e:
            print(f'Flood wait error: need to wait {e.seconds} seconds')
            await asyncio.sleep(e.seconds)  # Use await here instead of time.sleep
        except errors.rpcerrorlist.ChatWriteForbiddenError:
            print(f'Cannot send message to {channel}: write access forbidden')
        except errors.ChannelPrivateError:
            print(f'Target channel {channel} is private, access denied.')
        except errors.EntityNotFoundError:
            print(f'Channel {channel} not found or you are not a member.')
        except Exception as e:
            print(f'Failed to send message to {channel}: {e}')

with client:
    client.loop.run_until_complete(main())
