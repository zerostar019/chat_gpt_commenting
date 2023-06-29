import sys
import logging
import time
import random
import asyncio
from random import randint
from asyncio import sleep
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors.exceptions import ChannelPrivate
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.errors.exceptions.bad_request_400 import UserBannedInChannel
from pyrogram.errors.exceptions.forbidden_403 import Forbidden
from pyrogram.types import Chat

# Channel Spam - switch between profile (False) and channel (True)
spam_from_channel = True
# Chat (Sender) - stores chat from which bot will spam (profile or channels)
send_chat = None
# Using to avoid media group bug
last_media_group = 123
# Spam Posts - stores posts to spam, supported types: TextPost, PicturePost, StickerPost, RandomPost
# App - stores Pyrogram instance
app = Client("data/my_account", api_id="API ID СЮДА", api_hash="API HASH СЮДА", workers=1)
# Delay - delay between requests
delay = 3
sys.tracebacklimit = 0
pyrogram_logging = logging.WARNING
userbot_logging = logging.INFO
logging.basicConfig(level=pyrogram_logging)
logger = logging.getLogger("userbot")
logger.setLevel(userbot_logging)

bot_id = '@chat9pt_bot'
channel_to_join_id = "aitgru"
channel_comment = "dfgdfgsdfs423" # СЮДА ПИШЕТСЯ ЮЗЕРНЕЙМ КАНАЛА БЕЗ @


@app.on_message(filters.channel)
async def answer(_, message):
    message_log = message.text
    chat_id = message.chat.id
    message_id = message.id
    await app.join_chat(channel_to_join_id)
    
        
    if message.text and len(message.text) <= 2800:
        try:
            await app.send_message(bot_id, "/reset")
            await app.send_message(bot_id, f"""Напиши комментарий от женского пола на этот пост в 70 символов без хештегов на русском языке не используя кавычки: {message.text.replace('"', '')}
| Пост из канала {chat_id} {message_id}""")
        except:
            pass

    if message.caption and len(message.caption) <= 2800:
        if None != message.caption:
            try:
                await app.send_message(bot_id, "/reset")
                await app.send_message(bot_id,f"""Напиши комментарий от женского пола на этот пост в 70 символов без хештегов на русском языке не используя кавычки: {message.caption.replace('"', '')}
| Пост из канала {chat_id} {message_id}""")
            except:
                pass

    print(f"\nПолучено сообщение:\nКанал {message.chat.title}\nПост: {message_log}\n")




@app.on_message(filters.bot)
async def handle_bot_message(client, message):
    if str(message.from_user.username) in bot_id:
        comment_text = message.text
        if not message.reply_to_message:
            return
            asyncio.sleep(10)
        try:
            replied_message_text = message.reply_to_message.text
        except:
            replied_message_text = message.reply_to_message.caption

        replied_message_text = replied_message_text.replace('"', '')

        msg_object = replied_message_text.replace("Напиши комментарий от женского пола на этот пост в 70 символов без хештегов на русском языке не используя кавычки: ","").split('\n| ', 2)[1].replace('Пост из канала ', '').replace('\n', '')
        chat_id, message_id = msg_object.split(' ', 2)[0], int(msg_object.split(' ', 2)[1])
        try:
            await asyncio.sleep(4)
            if spam_from_channel:
                try:
                    print("Пожалуйста, подождите, формируем ответ...\n")
                    msg_info = await app.get_discussion_message(chat_id, message_id)
                    await asyncio.sleep(3)
                    chaaaat = await app.get_chat(channel_comment)
                    await app.set_send_as_chat(chat_id=msg_info.chat.id, send_as_chat_id=chaaaat.id)
                    await msg_info.reply(comment_text, quote=True)
                    print(f"ОТВЕЧЕНО в канале: {msg_info.chat.title}\n")
                except Exception as e:
                    print("ПРОИЗОШЛА ОШИБКА ПРИ ОТВЕТЕ: либо бан на канале, либо нет комментариев, либо чат приватный...\n")
                    raise Forbidden
                
                
                
        except ChannelPrivate:
            try:
                await app.leave_chat(chat_id)
            except:
                pass
            await app.send_message('@spambot', '/start')
            await asyncio.sleep(3)
            await app.send_message('@spambot', 'OK')
            await asyncio.sleep(3)
            await app.send_message('@spambot', '/start')
        except UserBannedInChannel:
            await app.send_message('@spambot', '/start')
            await asyncio.sleep(3)
            await app.send_message('@spambot', 'OK')
            await asyncio.sleep(3)
            await app.send_message('@spambot', '/start')
        except Forbidden:
            chat: Chat
            try:
                chat = await app.get_chat(chat_id)
                await chat.linked_chat.join()
            except Exception as e:
                print('Не удалось вступить в чат', e)
        except Exception as e:
            print('Ошибка', e)

        await asyncio.sleep(10)


async def sleep_if_required(_delay):
    if _delay != 0:
        logger.debug(f'Sleeping {_delay}s due to delay')
        await sleep(_delay)
try:
    text = 'Started!' if not spam_from_channel \
        else 'Started! Wait for a new message to set up the bot.'
    logger.info(text)
    app.run()
except ValueError:
    logger.error("The config.ini is configured incorrectly!")
