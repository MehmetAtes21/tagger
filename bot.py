import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/bitir'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Merhaba Ben @CosmicTaggerBot \n Grubunuzda Üyeleri Etiketleye bilirim \n\n Nasıl Çalıştığıma Bakmak için /help yaza bilirsin**",
                    buttons=(
                      [Button.url('➕Beni Gruba Ekle➕', 'https://t.me/CosmicTaggerBot?startgroup=a'),
                       Button.url('🛠️ Creator 🛠️', 'https://t.me/DexRoFF'),
                      Button.url('📣 Resmi Kanal 📣', 'https://t.me/Cosmic_MMC')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = """**Nasıl Çalışırım:

/all <Mesajınız> - Kullanıcıları Etiketlerim
/atag <Mesajınız> - Sadece Yöneticileri Etiketlerim.
/bitir - Etiket işlemini iptal ederim.
❕ Yalnızca yöneticileri bu komutları kullanabilir.**"""
  await event.reply(helptext,
                    buttons=(
                      [Button.url('➕ Beni Gruba Ekle ➕', 'https://t.me/CosmicTaggerBot?startgroup=a'),
                       Button.url('🛠️ Creator 🛠️', 'https://t.me/DexRoFF'),
                      Button.url('📣Resmi Kanal 📣', 'https://t.me/Cosmic_MMC')]
                    ),
                    link_preview=False
                   )

@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  user = await event.get_sender()
  global anlik_calisan
  if event.is_private:
    return await event.respond("**Bu Komut Gruplarda ve Kanallarda Kullanılabilir.!**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Yalnızca Yöneticiler Hepsinden Bahsedebilir!**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("**Eski mesajlar için üyelerden bahsedemem! (gruba eklemeden önce gönderilen mesajlar)**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**Bana bir argüman ver!**")
  else:
    return await event.respond("**Bir mesajı yanıtlayın veya başkalarından bahsetmem için bana bir metin verin!**")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"➤ [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond(f"**Etikeletme İşlemi Bitti\n\n Başlatan:[{user.first_name}](tg://user?id={user.id})**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"➤ [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond(f"**Etiket İşlemi Durduruldu!\n\Başlatan: [{user.first_name}](tg://user?id={user.id})**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

@client.on(events.NewMessage(pattern="^/atag ?(.*)"))
async def mentionalladmin(event):

  if event.is_private:
    return await event.respond("**Bu Komut Grublarda ve Kanallarda Kullanılabilir.!**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Yalnızca Yöneticiler Etiket İşlemini Başlata Bilir!**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("**Eski Mesajlar için Üyelerden Bahsedemem! (gruba eklemeden önce gönderilen mesajlar)**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**Bana bir argüman ver!**")
  else:
    return await event.respond("**Bir Mesajı Yanıtlayın veya Üyeleri Etiketlemek için Bana Bir Metin Verin!__")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id,filter=ChannelParticipantsAdmins):
      usrnum += 1
      usrtxt += f"➤ [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond(f"**Etiketleme işlemi Bitti\n\nBaşlatan: [{user.first_name}](tg://user?id={user.id})**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n\n{usrtxt}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
    anlik_calisan.remove(event.chat_id)
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id,filter=ChannelParticipantsAdmins):
      usrnum += 1
      usrtxt += f"➤ [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond(f"**Etiket İşlemi Durduruldu!\n\n Başlatan: [{user.first_name}](tg://user?id={user.id})**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
    anlik_calisan.remove(event.chat_id)
    
print(">> Bot çalışıyor merak etme 👮‍♂️ @DexRoFF bilgi alabilirsin <<")
client.run_until_disconnected()
