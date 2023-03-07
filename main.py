# İstek Üzerine Paylaşıldı , Hadi Biraz Sevinin .d
import random
import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.events import StopPropagation
from config import client, USERNAME, log_qrup, startmesaj, qrupstart, komutlar, sahib, support
import heroku3
import random
import asyncio
import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.events import StopPropagation
from pyrogram import Client 
from pyrogram import filters 
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
from time import sleep




logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)



anlik_calisan = []
etiket_tagger = [] 


#tektag
@client.on(events.NewMessage(pattern="^/start$"))
async def cancel(event):
  global etiket_tagger
  etiket_tagger.remove(event.chat_id)

  
# Başlanğıc Mesajı
@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  if event.is_private:
    async for usr in client.iter_participants(event.chat_id):
     ad = f"• 𝖬𝖾𝗋𝗁𝖺𝖻𝖺 [{usr.first_name}](tg://user?id={usr.id}) "
     await client.send_message(log_qrup, f"ℹ️ **Yeni Kullanıcı -** \n {ad}")
     return await event.reply(f"{ad} {startmesaj}", buttons=(
                      [
                       Button.url('🎉  𝖡𝖾𝗇𝗂 𝖦𝗋𝗎𝖻𝖺 𝖤𝗄𝗅𝖾  🎉', f'https://t.me/{USERNAME}?startgroup=a')],
                      [
                       Button.url('📚  𝖪𝗈𝗆𝗎𝗍𝗅𝖺𝗋  ', f'https://t.me/StrTagger'),
                       Button.url('👨‍💻  𝖮𝗐𝗇𝖾𝗋  ', f'https://t.me/StarBotOwner')],
                       [Button.url('📝  𝖢𝗁𝖺𝗇𝗇𝖾𝗅  ', f'https://t.me/{support}')]
                    ),
                    link_preview=False)


  if event.is_group:
    return await client.send_message(event.chat_id, f"{qrupstart}")

# Başlanğıc Button
@client.on(events.callbackquery.CallbackQuery(data="start"))
async def handler(event):
    async for usr in client.iter_participants(event.chat_id):
     ad = f"• 𝖬𝖾𝗋𝗁𝖺𝖻𝖺 [{usr.first_name}](tg://user?id={usr.id}) "
     await event.edit(f"{ad} {startmesaj}", buttons=(
                      [
                       Button.url('🎉  𝖡𝖾𝗇𝗂 𝖦𝗋𝗎𝖻𝖺 𝖤𝗄𝗅𝖾  🎉', f'https://t.me/{USERNAME}?startgroup=a')],
                      [Button.url("📚  𝖪𝗈𝗆𝗎𝗍𝗅𝖺𝗋  ", f'https://t.me/StarTagger'),
                       Button.url('👨‍💻  𝖮𝗐𝗇𝖾𝗋  ', f'https://t.me/StarBotOwner')]
                       [Button.url('📝  𝖢𝗁𝖺𝗇𝗇𝖾𝗅  ', f'https://t.me/{support}')]
                    ),
                    link_preview=False)

# Samilben
@client.on(events.callbackquery.CallbackQuery(data="komutlar"))
async def handler(event):
    await event.edit(f"{komutlar}", buttons=(
                      [
                      Button.url('📣  𝖲𝗎𝗉𝗉𝗈𝗋𝗍  ', f'https://t.me/StarTagger'),
                      Button.url('🇹🇷  𝖮𝗐𝗇𝖾𝗋  ', f'https://t.me/{sahib}')
                      ],
                      [
                      Button.inline("<  𝖦𝖾𝗋𝗂  >", data="start"),
                      ]
                    ),
                    link_preview=False)

# 5 li etiketleme modulü
@client.on(events.NewMessage(pattern="^/utag ?(.*)"))
async def mentionall(event):
  global etiket_tagger
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("𝖤𝗌𝗄𝗂 𝖬𝖾𝗌𝖺𝗃𝗅𝖺𝗋𝗂 𝖦𝗈𝗋𝖾𝗆𝗂𝗒𝗈𝗋𝗎𝗆 ! ")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝖬𝖾𝗌𝖺𝗃𝗂 𝖸𝖺𝗓𝗆𝖺𝖽𝗂𝗇 ! ")
  else:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍 𝗂𝗌𝗅𝖾𝗆𝗂𝗇𝖾 𝖻𝖺𝗌𝗅𝖺𝗆𝖺𝗆 𝗂𝖼𝗂𝗇 𝖻𝗂𝗋 𝗌𝖾𝖻𝖾𝗉 𝗒𝖺𝗓𝗂𝗇 ! ")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "✅ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖻𝖺𝗌𝗅𝖺𝖽𝗂 . . .",
                    buttons=(
                      [
                      Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    etiket_tagger.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) , "
      if event.chat_id not in etiket_tagger:
        await event.respond("⛔ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg} \n {usrtxt}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    

#########################

# admin etiketleme modülü
@client.on(events.NewMessage(pattern="^/atag ?(.*)"))
async def mentionalladmin(event):
  global etiket_tagger
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("𝖤𝗌𝗄𝗂 𝖬𝖾𝗌𝖺𝗃𝗅𝖺𝗋𝗂 𝖦𝗈𝗋𝖾𝗆𝗂𝗒𝗈𝗋𝗎𝗆 ! ")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝖬𝖾𝗌𝖺𝗃𝗂 𝖸𝖺𝗓𝗆𝖺𝖽𝗂𝗇 ! ")
  else:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍 𝗂𝗌𝗅𝖾𝗆𝗂𝗇𝖾 𝖻𝖺𝗌𝗅𝖺𝗆𝖺𝗆 𝗂𝖼𝗂𝗇 𝖻𝗂𝗋 𝗌𝖾𝖻𝖾𝗉 𝗒𝖺𝗓𝗂𝗇 ! ")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "✅ 𝖠𝖽𝗆𝗂𝗇 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖻𝖺𝗌𝗅𝖺𝖽𝗂 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    etiket_tagger.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"• [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in etiket_tagger:
        await event.respond("⛔ 𝖠𝖽𝗆𝗂𝗇 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} \n {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    

#########################

# tek tek etiketleme modülü
@client.on(events.NewMessage(pattern="^/tag ?(.*)"))
async def tektag(event):
  global etiket_tagger
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("𝖤𝗌𝗄𝗂 𝖬𝖾𝗌𝖺𝗃𝗅𝖺𝗋𝗂 𝖦𝗈𝗋𝖾𝗆𝗂𝗒𝗈𝗋𝗎𝗆 ! ")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝖬𝖾𝗌𝖺𝗃𝗂 𝖸𝖺𝗓𝗆𝖺𝖽𝗂𝗇 ! ")
  else:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍 𝗂𝗌𝗅𝖾𝗆𝗂𝗇𝖾 𝖻𝖺𝗌𝗅𝖺𝗆𝖺𝗆 𝗂𝖼𝗂𝗇 𝖻𝗂𝗋 𝗌𝖾𝖻𝖾𝗉 𝗒𝖺𝗓𝗂𝗇 ! ")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "✅ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖻𝖺𝗌𝗅𝖺𝖽𝗂 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    etiket_tagger.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"• [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in etiket_tagger:
        await event.respond("⛔ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} \n {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    

#########################

# Emoji ile etiketleme modülü

anlik_calisan = []

tekli_calisan = []




emoji = " ❤️ 🧡 💛 💚 💙 💜 🖤 🤍 🤎 🙂 🙃 😉 😌 😍 🥰 😘 😗 😙 😚 😋 😛 😝 😜 🤪 🤨 🧐 🤓 😎 🤩 🥳 😏 😒 " \
        "😞 😔 😟 😕 🙁 😣 😖 😫 😩 🥺 😢 😭 😤 😠 😡  🤯 😳 🥵 🥶 😱 😨 😰 😥 😓 🤗 🤔 🤭 🤫 🤥 😶 😐 😑 😬 🙄 " \
        "😯 😦 😧 😮 😲 🥱 😴 🤤 😪 😵 🤐 🥴 🤢 🤮 🤧 😷 🤒 🤕 🤑 🤠 😈 👿 👹 👺 🤡  👻 💀 👽 👾 🤖 🎃 😺 😸 😹 " \
        "😻 😼 😽 🙀 😿 😾 ❄️ 🌺 🌨 🌩 ⛈ 🌧 ☁️ ☀️ 🌈 🌪 ✨ 🌟 ☃️ 🪐 🌏 🌙 🌔 🌚 🌝 🕊 🦩 🦦 🌱 🌿 ☘ 🍂 🌹 🥀 🌾 " \
        "🌦 🍃 🎋🦓 🐅 🐈‍⬛ 🐄 🦄 🐇 🐁 🐷 🐶 🙈 🙊 🐻 🐼 🦊 🐮 🐍 🐊 🦨 🦔 🐒 🦣 🦘 🦥 🦦 🦇 🦍 🐥 🐦 🦜 🕊️ 🦤 🦢 " \
        "🦩 🦚 🦃 🐣 🐓 🐬 🦈 🐠 🐳 🦗 🪳 🐝 🐞 🦋 🐟 🕷️ 🦑".split(" ")


@client.on(events.NewMessage(pattern="^/etag ?(.*)"))
async def etag(event):
  global etiket_tagger
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("𝖤𝗌𝗄𝗂 𝖬𝖾𝗌𝖺𝗃𝗅𝖺𝗋𝗂 𝖦𝗈𝗋𝖾𝗆𝗂𝗒𝗈𝗋𝗎𝗆 ! ")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝖬𝖾𝗌𝖺𝗃𝗂 𝖸𝖺𝗓𝗆𝖺𝖽𝗂𝗇 ! ")
  else:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍 𝗂𝗌𝗅𝖾𝗆𝗂𝗇𝖾 𝖻𝖺𝗌𝗅𝖺𝗆𝖺𝗆 𝗂𝖼𝗂𝗇 𝖻𝗂𝗋 𝗌𝖾𝖻𝖾𝗉 𝗒𝖺𝗓𝗂𝗇 ! ")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "✅ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖻𝖺𝗌𝗅𝖺𝖽𝗂 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    etiket_tagger.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.id}) , "
      if event.chat_id not in etiket_tagger:
        await event.respond("⛔ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt} \n {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    

#########################

# söz ile etiketleme modülü

soz = (
'ᴜsʟᴜᴘ ᴋᴀʀᴀᴋᴛᴇʀɪᴅɪʀ ʙɪʀ ɪɴsᴀɴɪɴ', 
'ɪʏɪʏɪᴍ ᴅᴇsᴇᴍ ɪɴᴀɴᴀᴄᴀᴋ , ᴏ ᴋᴀᴅᴀʀ ʜᴀʙᴇʀsɪᴢ ʙᴇɴᴅᴇɴ', 
'ᴍᴇsᴀғᴇʟᴇʀ ᴜᴍʀᴜᴍᴅᴀ ᴅᴇɢɪʟ , ɪᴄɪᴍᴅᴇ ᴇɴ ɢᴜᴢᴇʟ ʏᴇʀᴅᴇsɪɴ',
'ʙɪʀ ᴍᴜᴄɪᴢᴇʏᴇ ɪʜᴛɪʏᴀᴄɪᴍ ᴠᴀʀᴅɪ , ʜᴀʏᴀᴛ sᴇɴɪ ᴋᴀʀsɪᴍᴀ ᴄɪᴋᴀʀᴅɪ', 
'ᴏʏʟᴇ ɢᴜᴢᴇʟ ʙᴀᴋᴛɪɴ ᴋɪ , ᴋᴀʟʙɪɴ ᴅᴇ ɢᴜʟᴜsᴜɴ ᴋᴀᴅᴀʀ ɢᴜᴢᴇʟ sᴀɴᴍɪsᴛɪᴍ', 
'ʜᴀʏᴀᴛ ɴᴇ ɢɪᴅᴇɴɪ ɢᴇʀɪ ɢᴇᴛɪʀɪʀ , ɴᴇ ᴅᴇ ᴋᴀʏʙᴇᴛᴛɪɢɪɴ ᴢᴀᴍᴀɴɪ ɢᴇʀɪ ɢᴇᴛɪʀɪʀ', 
'sᴇᴠᴍᴇᴋ ɪᴄɪɴ sᴇʙᴇᴘ ᴀʀᴀᴍᴀᴅɪᴍ , ʙɪʀ ᴛᴇᴋ sᴇsɪ ʏᴇᴛᴛɪ ᴋᴀʟʙɪᴍᴇ', 
'ᴍᴜᴛʟᴜʏᴜɴ ᴀᴍᴀ sᴀᴅᴇᴄᴇ sᴇɴɪɴʟᴇ', 
'ʙᴇɴ ʜᴇᴘ sᴇᴠɪʟᴍᴇᴋ ɪsᴛᴇᴅɪɢɪᴍ ɢɪʙɪ sᴇᴠɪɴᴅɪᴍ', 
'ʙɪʀɪ ᴠᴀʀ ɴᴇ ᴏᴢʟᴇᴍᴇᴋᴛᴇɴ ʏᴏʀᴜʟᴅᴜᴍ ɴᴇ sᴇᴠᴍᴇᴋᴛᴇɴ', 
'ᴄᴏᴋ ᴢᴏʀ ʙᴇ sᴇɴɪ sᴇᴠᴍᴇʏᴇɴ ʙɪʀɪɴᴇ ᴀsɪᴋ ᴏʟᴍᴀᴋ', 
'ᴄᴏᴋ ᴏɴᴇᴍsɪᴢʟɪᴋ ɪsᴇ ʏᴀʀᴀᴍᴀᴅɪ ᴀʀᴛɪᴋ ʙᴏs ᴠᴇʀɪʏᴏʀᴜᴢ', 
'ʜᴇʀᴋᴇsɪɴ ʙɪʀ ɢᴇᴄᴍɪsɪ ᴠᴀʀ , ʙɪʀ ᴅᴇ ᴠᴀᴢɢᴇᴄᴍɪsɪ', 
'ᴀsɪᴋ ᴏʟᴍᴀᴋ ɢᴜᴢᴇʟ ʙɪʀ sᴇʏ ᴀᴍᴀ sᴀᴅᴇᴄᴇ sᴀɴᴀ', 
'ᴀɴʟᴀʏᴀɴ ʏᴏᴋᴛᴜ , sᴜsᴍᴀʏɪ ᴛᴇʀᴄɪʜ ᴇᴛᴛɪᴍ', 
'sᴇɴ ᴄᴏᴋ sᴇᴠ ᴅᴇ ʙɪʀᴀᴋɪᴘ ɢɪᴅᴇɴ ʏᴀʀ ᴜᴛᴀɴsɪɴ', 
'ᴏ ɢɪᴛᴛɪᴋᴛᴇɴ sᴏɴʀᴀ ɢᴇᴄᴇᴍ ɢᴜɴᴅᴜᴢᴇ ʜᴀsʀᴇᴛ ᴋᴀʟᴅɪ', 
'ʜᴇʀ sᴇʏɪɴ ʙɪᴛᴛɪɢɪ ʏᴇʀᴅᴇ ʙᴇɴᴅᴇ ʙɪᴛᴛɪᴍ ᴅᴇɢɪsᴛɪɴ ᴅɪʏᴇɴʟᴇʀɪɴ ᴇsɪʀɪʏɪᴍ', 
'ɢᴜᴠᴇɴᴍᴇᴋ  sᴇᴠᴍᴇᴋᴛᴇɴ ᴅᴀʜᴀ ᴅᴇɢᴇʀʟɪ , ᴢᴀᴍᴀɴʟᴀ ᴀɴʟᴀʀsɪɴ', 
'ɪɴsᴀɴ ʙᴀᴢᴇɴ ʙᴜʏᴜᴋ ʜᴀʏᴀʟʟᴇʀɪɴɪ ᴋᴜᴄᴜᴋ ɪɴsᴀɴʟᴀʀʟᴀ ᴢɪʏᴀɴ ᴇᴅᴇʀ', 
'ᴋɪᴍsᴇ ᴋɪᴍsᴇʏɪ ᴋᴀʏʙᴇᴛᴍᴇᴢ  ɢɪᴅᴇɴ ʙᴀsᴋᴀsɪɴɪ ʙᴜʟᴜʀ , ᴋᴀʟᴀɴ ᴋᴇɴᴅɪɴɪ', 
'ɢᴜᴄʟᴜ ɢᴏʀᴜɴᴇʙɪʟɪʀɪᴍ ᴀᴍᴀ ɪɴᴀɴ ʙᴀɴᴀ ʏᴏʀɢᴜɴᴜᴍ', 
'ᴏᴍʀᴜɴᴜᴢᴜ sᴜsᴛᴜᴋʟᴀʀɪɴɪᴢɪ ᴅᴜʏᴀɴ  ʙɪʀɪʏʟᴇ ɢᴇᴄɪʀɪɴ', 
'ʜᴀʏᴀᴛ ɪʟᴇʀɪʏᴇ ʙᴀᴋɪʟᴀʀᴀᴋ ʏᴀsᴀɴɪʀ ɢᴇʀɪʏᴇ ʙᴀᴋᴀʀᴀᴋ ᴀɴʟᴀsɪʟɪʀ', 
'ᴀʀᴛɪᴋ ʜɪᴄʙɪʀ sᴇʏ ᴇsᴋɪsɪ ɢɪʙɪ ᴅᴇɢɪʟ ʙᴜɴᴀ ʙᴇɴᴅᴇ ᴅᴀʜɪʟɪᴍ', 
'ᴋɪʏᴍᴇᴛ ʙɪʟᴇɴᴇ ɢᴏɴᴜʟᴅᴇ ᴠᴇʀɪʟɪʀ ᴏᴍᴜʀᴅᴇ', 
'ʙɪʀ ᴄɪᴄᴇᴋʟᴇ ɢᴜʟᴇʀ ᴋᴀᴅɪɴ , ʙɪʀ ʟᴀғʟᴀ ʜᴜᴢᴜɴ', 
'ᴋᴀʟʙɪ ɢᴜᴢᴇʟ ᴏʟᴀɴ ɪɴsᴀɴɪɴ ɢᴏᴢᴜɴᴅᴇɴ ʏᴀs ᴇᴋsɪᴋ ᴏʟᴍᴀᴢᴍɪs', 
'ʜᴇʀ sᴇʏɪ ʙɪʟᴇɴ ᴅᴇɢɪʟ ᴋɪʏᴍᴇᴛ ʙɪʟᴇɴ ɪɴsᴀɴʟᴀʀ ᴏʟsᴜɴ ʜᴀʏᴀᴛɪɴɪᴢᴅᴀ', 
'ᴍᴇsᴀғᴇ ɪʏɪᴅɪʀ ɴᴇ ʜᴀᴅᴅɪɴɪ ᴀsᴀɴ ᴏʟᴜʀ , ɴᴇ ᴅᴇ ᴄᴀɴɪɴɪ sɪᴋᴀɴ', 
'ʏᴜʀᴇɢɪᴍɪɴ ᴛᴀᴍ ᴏʀᴛᴀsɪɴᴅᴀ ʙᴜʏᴜᴋ ʙɪʀ ʏᴏʀɢᴜɴʟᴜᴋ ᴠᴀʀ', 
'ᴠᴇʀɪʟᴇɴ ᴅᴇɢᴇʀɪɴ ɴᴀɴᴋᴏʀᴜ ᴏʟᴍᴀʏɪɴ ɢᴇʀɪsɪ ʜᴀʟʟ ᴏʟᴜʀ', 
'ʜᴇᴍ ɢᴜᴄʟᴜ ᴏʟᴜᴘ ʜᴇᴍ ʜᴀssᴀs ᴋᴀʟᴘʟɪ ʙɪʀɪ ᴏʟᴍᴀᴋ ᴄᴏᴋ ᴢᴏʀ', 
'ᴍᴜʜᴛᴀᴄ ᴋᴀʟɪɴ ʏᴜʀᴇɢɪ ɢᴜᴢᴇʟ  ɪɴsᴀɴʟᴀʀᴀ', 
'ɪɴsᴀɴ ᴀɴʟᴀᴅɪɢɪ ᴠᴇ ᴀɴʟᴀsɪʟᴅɪɢɪ ɪɴsᴀɴᴅᴀ ᴄɪᴄᴇᴋ ᴀᴄᴀʀ', 
'ɪsᴛᴇʏᴇɴ ᴅᴀɢʟᴀʀɪ ᴀsᴀʀ ɪsᴛᴇᴍᴇʏᴇɴ ᴛᴜᴍsᴇɢɪ ʙɪʟᴇ ɢᴇᴄᴇᴍᴇᴢ', 
'ɪɴsᴀʟʟᴀʜ sᴀʙɪʀʟᴀ ʙᴇᴋʟᴇᴅɪɢɪɴ sᴇʏ ɪᴄɪɴ ʜᴀʏɪʀʟɪ ʙɪʀ ʜᴀʙᴇʀ ᴀʟɪʀsɪɴ', 
'ɪʏɪ ᴏʟᴀɴ ᴋᴀʏʙᴇᴛsᴇ ᴅᴇ ᴋᴀᴢᴀɴɪʀ', 
'ɢᴏɴʟᴜɴᴜᴢᴇ ᴀʟᴅɪɢɪɴɪᴢ , ɢᴏɴʟᴜɴᴜᴢᴜ ᴀʟᴍᴀʏɪ ʙɪʟsɪɴ', 
'ʏɪɴᴇ ʏɪʀᴛɪᴋ ᴄᴇʙɪᴍᴇ ᴋᴏʏᴍᴜsᴜᴍ ᴜᴍᴜᴅᴜᴍᴜ', 
'ᴏʟᴍᴇᴋ ʙɪʀ sᴇʏ ᴅᴇɢɪʟ ʏᴀsᴀᴍᴀᴋ ᴋᴏʀᴋᴜɴᴄ', 
'ɴᴇ ɪᴄɪᴍᴅᴇᴋɪ sᴏᴋᴀᴋʟᴀʀᴀ sɪɢᴀʙɪʟᴅɪᴍ ɴᴇ ᴅᴇ ᴅɪsᴀʀɪᴅᴀᴋɪ ᴅᴜɴʏᴀʏᴀ', 
'ɪɴsᴀɴ sᴇᴠɪʟᴍᴇᴋᴛᴇɴ ᴄᴏᴋ ᴀɴʟᴀsɪʟᴍᴀʏɪ ɪsᴛɪʏᴏʀᴅᴜ ʙᴇʟᴋɪ ᴅᴇ', 
'ᴇᴋᴍᴇᴋ ᴘᴀʜᴀʟɪ , ᴇᴍᴇᴋ ᴜᴄᴜᴢᴅᴜʀ', 
'sᴀᴠᴀsᴍᴀʏɪ ʙɪʀᴀᴋɪʏᴏʀᴜᴍ ʙᴜɴᴜ ᴠᴇᴅᴀ sᴀʏ'
) 


@client.on(events.NewMessage(pattern="^/stag ?(.*)"))
async def stag(event):
  global etiket_tagger
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("𝖤𝗌𝗄𝗂 𝖬𝖾𝗌𝖺𝗃𝗅𝖺𝗋𝗂 𝖦𝗈𝗋𝖾𝗆𝗂𝗒𝗈𝗋𝗎𝗆 ! ")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝖬𝖾𝗌𝖺𝗃𝗂 𝖸𝖺𝗓𝗆𝖺𝖽𝗂𝗇 ! ")
  else:
    return await event.respond("• 𝖤𝗍𝗂𝗄𝖾𝗍 𝗂𝗌𝗅𝖾𝗆𝗂𝗇𝖾 𝖻𝖺𝗌𝗅𝖺𝗆𝖺𝗆 𝗂𝖼𝗂𝗇 𝖻𝗂𝗋 𝗌𝖾𝖻𝖾𝗉 𝗒𝖺𝗓𝗂𝗇 ! ")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "• 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖻𝖺𝗌𝗅𝖺𝖽𝗂 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    etiket_tagger.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(soz)}](tg://user?id={usr.id}) "
      if event.chat_id not in etiket_tagger:
        await event.respond("⛔ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} \n {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    
#########################

# bayrak ile etiketleme modülü
renk = " 🇿🇼 🇿🇲 🇿🇦 🇾🇹 🇾🇪 🇽🇰 🇼🇸 🇼🇫 🏴󠁧󠁢󠁷󠁬󠁳󠁿 🇻🇺 🇻🇳 🇻🇮 🇻🇬 🇻🇪 🇻🇨 🇻🇦 🇺🇿 🇺🇾 🇺🇸 🇺🇳 🇺🇬 🇺🇦 🇹🇿 🇹🇼 🇹🇻 🇹🇹 🇹🇷 🇹🇴 🇹🇳 🇹🇲 🇹🇱 🇹🇰 🇹🇭 🇹🇫 🇹🇨 🇹🇦 🇸🇿 🇸🇾 🇸🇽 " \
         " 🇸🇻 🇸🇸 🇸🇴 🇸🇲 🇸🇱 🇸🇰 🇸🇮 🇸🇭 🇸🇬 🇸🇪 🇸🇩 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🇸🇦 🇷🇼 🇷🇺 🇷🇸 🇷🇴 🇷🇪 🇶🇦 🇵🇾 🇵🇼 🇵🇹 🇵🇸 🇵🇷 🇵🇳 🇵🇲 🇵🇱 🇵🇰 🇵🇭 🇵🇫 🇵🇪 " \
         " 🇵🇦 🇴🇲 🇳🇿 🇳🇷 🇳🇵 🇳🇴 🇳🇱 🇳🇮 🇳🇬 🇳🇫 🇳🇪 🇳🇨 🇳🇦 🇲🇾 🇲🇽 🇲🇼 🇲🇻 🇲🇹 🇲🇷 🇲🇶 🇲🇵 🇲🇴 🇲🇳 🇲🇰 🇲🇭 🇲🇬 🇲🇪 🇲🇩 🇲🇨 🇲🇦 🇱🇾 🇱🇻 " \
         " 🇱🇺 🇱🇸 🇱🇷 🇱🇰 🇱🇮 🇱🇨 🇱🇧 🇱🇦 🇰🇿 🇰🇾 🇰🇼 🇰🇷 🇰🇵 🇰🇳 🇰🇲 🇰🇮 🇰🇭  🇰🇬 🇰🇪 🇯🇵 🇯🇴 🇯🇲 🇯🇪 🇮🇹 🇮🇸 🇮🇷 🇮🇶 🇮🇴 🇮🇳 🇮🇲 🇮🇱 🇮🇪 " \
         " 🇮🇩 🇮🇨 🇭🇺 🇭🇹 🇭🇷 🇭🇳 🇭🇰 🇬🇺 🇬🇹 🇬🇸 🇬🇷 🇬🇶 🇬🇵 🇬🇲 🇬🇱 🇬🇮 🇬🇬 🇬🇪 🇬🇧 🇬🇦 🇫🇷 🇫🇴 🇫🇲 🇫🇰 🇫🇮 🇪🇺 🇪🇸 🇪🇷 🇪🇭 🇪🇪 " \
         " 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇪🇨 🇩🇿 🇩🇴 🇩🇲 🇩🇰 🇩🇯 🇩🇪 🇨🇿 🇨🇾 🇨🇽 🇨🇼 🇨🇻 🇨🇺 🇨🇷 🇨🇭 🇨🇦 🇦🇿 " .split(" ") 
        

@client.on(events.NewMessage(pattern="^/btag ?(.*)"))
async def rtag(event):
  global etiket_tagger
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("** Eski mesajları göremiyorum !**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**• Etiketleme mesajı yazmadın !**")
  else:
    return await event.respond("**• Etiketleme için bir mesaj yazın !**")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "✅ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖻𝖺𝗌𝗅𝖺𝖽𝗂 . . .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    etiket_tagger.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(renk)}](tg://user?id={usr.id}) "
      if event.chat_id not in etiket_tagger:
        await event.respond("⛔ 𝖴𝗒𝖾 𝖾𝗍𝗂𝗄𝖾𝗍𝗅𝖾𝗆𝖾 𝗂𝗌𝗅𝖾𝗆𝗂 𝖽𝗎𝗋𝖽𝗎𝗋𝗎𝗅𝖽𝗎 .",
                    buttons=(
                      [
                       Button.url('📝  𝖪𝖺𝗇𝖺𝗅  📝', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt} \n {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


###


print(">> Bot aktif merak etme ... <<")
client.run_until_disconnected()
run_until_disconnected()
