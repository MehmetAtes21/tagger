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

tekli_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Merhaba 👋 !\nBen  @BlackTaggerBot\nGrubunun üyelerini etiketlemek için buradayım.\nKomutlar hakkında bilgi almak için /help yazabilirsiniz.\n\nKanal: @FlexBots**",
                    buttons=(
                      [
                      Button.url('➕ Beni Gruba Ekle', 'https://t.me/BlackTaggerBot?startgroup=a'),
                      Button.url('🛠️ Developer', 'https://t.me/FlexDevs')
                      ],
                      [
                      Button.url('⚙️ Support', 'https://t.me/FlexBots')
                      ]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = """**Nasıl Çalışırım:

/all <Mesajınız> - Kullanıcıları Etiketlerim
/atag <Mesajınız> - Sadece Yöneticileri Etiketlerim.
/cancel - Etiket işlemini iptal ederim.
❕ Yalnızca yöneticileri bu komutları kullanabilir.**"""
  await event.reply(helptext,
                    buttons=(
                      [
                      Button.url('➕ Beni Gruba Ekle', 'https://t.me/CosmicTaggerBot?startgroup=a'),
                      Button.url('🛠️ Developer', 'https://t.me/DexRoFF')
                      ],
                      [
                      Button.url('⚙️ Support', 'https://t.me/FlexBots')
                      ]
                    ),
                    link_preview=False
                   )

@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
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
        return await event.respond("**Eski mesajları göremiyorum! (bu mesaj beni gruba eklemeden önce yazılmış)**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**Etiketleme mesajı yazmadın!**")
  else:
    return await event.respond("**Etiketleme için bir mesajı yanıtlayın veya bir mesaj yazın!**")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, ("📢 **İşlem Başarıyla Başladı**")
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"➤ [{usr.first_name}](tg://user?id={usr.id})  \n"
      if event.chat_id not in anlik_calisan:
        await event.respond(f"**Etikeletme İşlemi Bitti\n\n Başlatan:[{user.first_name}](tg://user?id={user.id})**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(4)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"➤ [{usr.first_name}](tg://user?id={usr.id})  \n"
      if event.chat_id not in anlik_calisan:
        await event.respond(f"**Etiket İşlemi Durduruldu!\n\Başlatan: [{user.first_name}](tg://user?id={user.id})**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(4)
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
      usrtxt += f"➤ [{usr.first_name}](tg://user?id={usr.id})  \n"
      if event.chat_id not in anlik_calisan:
        await event.respond(f"**Etiketleme işlemi Bitti\n\nBaşlatan: [{user.first_name}](tg://user?id={user.id})**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n\n{usrtxt}")
        await asyncio.sleep(3)
        usrnum = 0
        usrtxt = ""
    anlik_calisan.remove(event.chat_id)
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id,filter=ChannelParticipantsAdmins):
      usrnum += 1
      usrtxt += f"➤ [{usr.first_name}](tg://user?id={usr.id})  \n"
      if event.chat_id not in anlik_calisan:
        await event.respond(f"**Etiket İşlemi Durduruldu!\n\n Başlatan: [{user.first_name}](tg://user?id={user.id})**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(4)
        usrnum = 0
        usrtxt = ""
    anlik_calisan.remove(event.chat_id)
    
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global tekli_calisan
  tekli_calisan.remove(event.chat_id)

@client.on(events.NewMessage(pattern="^/tektag ?(.*)"))
async def mentionall(event):
  global tekli_calisan
  if event.is_private:
    return await event.respond("**Bu Komut Ancak Grub ve Kanallarda geçerli**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Bu Komutu Ancak Yöneticiler Kullana Bilir〽**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("**Önceki Mesajları Etiketleye bilmiyorum *")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Başlamak için bi sebeb yazın❗️")
  else:
    return await event.respond("**İşleme Başlanan için Bir sebeb yazın**")
  
  if mode == "text_on_cmd":
    tekli_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"**[{usr.first_name}](tg://user?id={usr.id}) **"
      if event.chat_id not in tekli_calisan:
        await event.respond("**Tek Tek Etiket işlemi başarıya bitti ✊**")
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    tekli_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in tekli_calisan:
        await event.respond("**Tek Tek Etiket işlemi başarıya durduruldu⛔**")
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Bot çalışıyor merak etme 👮‍♂️ @DexRoFF bilgi alabilirsin <<")
client.run_until_disconnected()
