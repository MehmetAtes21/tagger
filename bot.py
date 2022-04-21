import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

from datetime import datetime

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message, User
from pyrogram.types.messages_and_media import Message
from pyrogram import Client, filters
import time


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

app = Client("GUNC",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token
             )

anlik_calisan = []

ozel_list = [5288143542]
anlik_calisan = []
grup_sayi = []
etiketuye = []
rxyzdev_tagTot = {}
rxyzdev_initT = {}


@client.on(events.NewMessage(pattern="^/info$"))
async def info(event):
  await event.reply("**Merhaba Benim Ve Sahibim Hakkında Bilgi\n\nPython: 3.8.2\nKütüphanem: Telethon\n\nSahibim: @Pyhchistion\n\Ben Gruplarınızda Üyeleri Etiketlemek için Yaratılmışım**",
                    buttons=(
                      [
                       Button.url('Beni Grubuna Ekle ➕', 'https://t.me/TagAllPyBot?startgroup=a'),
                       Button.url('Kanal 📣', 'https://t.me/PyBotLog')
                      ],
                      [
                       Button.url('Sahibim 🖥️', 'https://t.me/Pyhchistion')
                      ],
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)
  
  if event.chat_id in rxyzdev_tagTot:await event.respond(f"❌ Etiket işlemi durduruldu.\n\n Etiketlerin Sayı: {rxyzdev_tagTot[event.chat_id]}")


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**@TagAllPyBot, Grubunuzda Üyeleri Etiketleyerek Çağıra Bilirim.\nDestek için ==> /help**",
                    buttons=(
                      [
                       Button.url('Beni Grubuna Ekle ➕', 'https://t.me/TagAllPyBot?startgroup=a'),
                       Button.url('Kanal 📣', 'https://t.me/PyBotLog')
                      ],
                      [
                       Button.url('Sahibim 🖥️', 'https://t.me/Pyhchistion')
                      ],
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = """**Komutlarım:
/all -text-
/atag -text-
/cancel - İşlemi Durdururum...

❕ Yalnızca yöneticileri bu komutları kullanabilir.**"""
  await event.reply(helptext,
                    buttons=(
                      [
                       Button.url('Beni Grubuna Ekle ➕', 'https://t.me/TagAllPyBot?startgroup=a'),
                       Button.url('Kanal 📣', 'https://t.me/PyBotLog')
                      ],
                      [
                       Button.url('Sahibim 🖥️', 'https://t.me/Pyhchistion')
                      ],
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage())
async def mentionalladmin(event):
  global etiketuye
  if event.is_group:
    if event.chat_id in etiketuye:
      pass
    else:
      etiketuye.append(event.chat_id)

@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  rxyzdev_tagTot[event.chat_id] = 0
  if event.is_private:
    return await event.respond("**Bu Komut Sadace Grublarda ve Kanallarda Kullanıma Bilir**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Yalnızca Yöneticiler Etiket işlemini Yapabilir**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("**Eski Mesajlar için Üyelerden Bahsedemem! (gruba eklemeden önce gönderilen mesajlar)**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**Bana Bir Metin Ver!**")
  else:
    return await event.respond("**Bir Mesajı Yanıtlayın veya Başkalarından Bahsetmem için Bana Bir Betin Verin!!**")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    await event.respond(f"**Etiket işlemi Başarıyla Başlatıldı.!**")
        
    async for usr in client.iter_participants(event.chat_id, aggressive=False):
      rxyzdev_tagTot[event.chat_id] += 1
      usrnum += 1
      usrtxt += f"\n👤 - [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n{usrtxt}")
        await asyncio.sleep(3)
        usrnum = 0
        usrtxt = ""
        
    sender = await event.get_sender()
    rxyzdev_initT = f"[{sender.first_name}](tg://user?id={sender.id})"
    if event.chat_id in rxyzdev_tagTot:await event.respond(f"**✅ Etiket İşlemi Başarıyla Tamamlandı !.\n\nEtiketlerin Sayları: {rxyzdev_tagTot[event.chat_id]}\n\nEtiket İşlemini Başlatan: {rxyzdev_initT}**")
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id, aggressive=False):
      rxyzdev_tagTot[event.chat_id] += 1
      usrnum += 1
      usrtxt += f"\n👤 - [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
     
    sender = await event.get_sender()
    rxyzdev_initT = f"[{sender.first_name}](tg://user?id={sender.id})"      
    if event.chat_id in rxyzdev_tagTot:await event.respond(f"**✅ Etiket İşlemi Başarıyla Tamamlandı !.\n\nEtiketlerin Sayları: {rxyzdev_tagTot[event.chat_id]}\n\nEtiket İşlemini Başlatan: {rxyzdev_initT}**")

@client.on(events.NewMessage(pattern="^/atag ?(.*)"))
async def mentionalladmin(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("**Bu Komut Yalnızca Grublarda Ve Kanallarda Kullanıma Bilir!**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Yalnızca Yöneticiler Etiket İşlemini Yapabilir**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("**Eski Mesajlar için Üyelerden Bahsedemem! (gruba eklemeden önce gönderilen mesajlar)**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("**Bana Bir Metin Ver!**")
  else:
    return await event.respond("**Bir Mesajı Yanıtlayın veya Başkalarından Bahsetmem için Bana Bir Betin Verin!**")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    await event.respond("**Admin Etiket işlemi Başarıyla Başlatıldı.!**")
  
    async for usr in client.iter_participants(event.chat_id,filter=ChannelParticipantsAdmins):
      usrnum += 1
      usrtxt += f"\n**👤 - [{usr.first_name}](tg://user?id={usr.id}) **"
      if event.chat_id not in anlik_calisan:
        await event.respond("**Etiket İşlemi Bitti.!**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n\n{usrtxt}")
        await asyncio.sleep(3)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id,filter=ChannelParticipantsAdmins):
      usrnum += 1
      usrtxt += f"\n**👤 - [{usr.first_name}](tg://user?id={usr.id}) **"
      if event.chat_id not in anlik_calisan:
        await event.respond("**İşlem Durduruldu.!**")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(3)
        usrnum = 0
        usrtxt = ""

    sender = await event.get_sender()
    rxyzdev_initT = f"[{sender.first_name}](tg://user?id={sender.id})"
    if event.chat_id in rxyzdev_tagTot:await event.respond(f"**Etiket İşlemi Başarıyla Tamamlandı !.\n\n**Etiketlerin Sayları: {rxyzdev_tagTot[event.chat_id]}\n\nEtiket İşlemini Başlatan: {rxyzdev_initT}")



@app.on_message(filters.command(["tag"], ["@"]) & ~filters.private)
def tag(_, message: Message):

    kısa = False

    try:
        message.text.split()[1]
    except IndexError:

        kısa = True

    if kısa == False:

        if message.text.split()[1].isnumeric() == True:
            uye_sayi = int(app.get_chat_members_count(message.chat.id))
            metin = ""
            sayi = int(message.text.split()[1])
            sayac = 0
            kisiler = app.get_chat_members(message.chat.id)

            if uye_sayi < sayi:
                message.reply(
                        "__🇹🇷 Girdiğiniz Sayı Grup Üye Sayısından Fazla !!\n\nEtiketleme İşlemi Yapılmıyor...")

            else:
                for i in message.text.split()[2:]:
                    metin += i + " "

                chat_id = message.chat.id

                message.reply(
                    f"🇹🇷 {sayi} ** Kişi Etiketleniyor**...\n\n**Sebep** :  __{metin}__")

                for kisi in kisiler:

                    if kisi.user.is_bot == False:

                        isim = kisi.user.first_name
                        try:
                                app.send_message(chat_id, f"\n·{isim}\n\n[{metin}](tg://user?id={kisi.user.id}) ")
                        except:
                            pass
                        time.sleep(3)

                        sayac += 1
                        if sayac == sayi:
                            app.send_message(chat_id,
                                                 f"🇹🇷 {sayi} **Kişi Etiketlendi...**")
                            break
        elif message.text.split()[1].isnumeric() == False:


            metin = ""
            sayi = 50
            sayac = 0
            kisiler = app.get_chat_members(message.chat.id)


            for i in message.text.split()[1:]:
                metin += i + " "

            print(metin)
            message.reply(f"🇹🇷 ** Üyeler Etiketleniyor**...\n**Sebep** :  __{metin}__\n\n🇬🇧 **I'm tagging users...")

            for kisi in kisiler:
                if kisi.user.is_bot == False:
                    isim = kisi.user.first_name
                    try:
                        app.send_message(message.chat.id, f"\n·{metin} [{isim}](tg://user?id={kisi.user.id}) ")
                    except:
                        pass
                    time.sleep(3)

                    sayac += 1

                    if sayac == sayi:
                        app.send_message(message.chat.id,
                                         "🇹🇷 **Etiketleme bitti...**")
                        break


    elif kısa == True:

        metin = ""
        sayi = 50
        sayac = 0
        kisiler = app.get_chat_members(message.chat.id)

        message.reply(f"🇹🇷 ** Üyeler Etiketleniyor**...\n**Sebep** :  __{metin}__")

        for kisi in kisiler:
            if kisi.user.is_bot == False:
                isim = kisi.user.first_name
                try:
                    app.send_message(message.chat.id, f"\n·{metin} [{isim}](tg://user?id={kisi.user.id}) ")
                except:
                    pass
                time.sleep(3)

                sayac += 1
                if sayac == sayi:
                    app.send_message(message.chat.id, "🇹🇷 **Etiketleme bitti...**")
                    break





@client.on(events.NewMessage())
async def mentionalladmin(event):
  global grup_sayi
  if event.is_group:
    if event.chat_id in grup_sayi:
      pass
    else:
      grup_sayi.append(event.chat_id)

@client.on(events.NewMessage(pattern='^/stats ?(.*)'))
async def son_durum(event):
    global anlik_calisan,grup_sayi,ozel_list
    sender = await event.get_sender()
    if sender.id not in ozel_list:
      return
    await event.respond(f"**@TagAllPyBot Güncel Verileri 🖥️**\n\n**Toplam Grub: `{len(grup_sayi)}`\n\nAnlık Çalışan Grub: `{len(anlik_calisan)}`**")


@client.on(events.NewMessage(pattern='^/reklam ?(.*)'))
async def duyuru(event):
 
  global grup_sayi,ozel_list
  sender = await event.get_sender()
  if sender.id not in ozel_list:
    return
  reply = await event.get_reply_message()
  await event.respond(f"Toplam {len(grup_sayi)} Gruba'a mesaj gönderiliyor...")
  for x in grup_sayi:
    try:
      await client.send_message(x,f"**📣 Sponsor**\n\n{reply.message}")
    except:
      pass
  await event.respond(f"Gönderildi.")

@client.on(events.NewMessage(pattern='^/duyuru ?(.*)'))
async def duyuru(event):
 
  global grup_sayi,ozel_list
  sender = await event.get_sender()
  if sender.id not in ozel_list:
    return
  reply = await event.get_reply_message()
  await event.respond(f"Toplam {len(grup_sayi)} Gruba'a mesaj gönderiliyor...")
  for x in grup_sayi:
    try:
      await client.send_message(x,f"**📣 Duyuru**\n\n{reply.message}")
    except:
      pass
  await event.respond(f"Gönderildi.")

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


infotext = (
    "**[{full_name}](tg://user?id={user_id})**\n"
    " * ID: `{user_id}`\n"
    " * İlk adı: `{first_name}`\n"
    " * Soyadı: `{last_name}`\n"
    " * Kullanıcı adı: `{username}`\n"
    " * Son Çevrimiçi: `{last_online}`\n"
    " * Bio: {bio}"
)


def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "Recently"
    elif user.status == "within_week":
        return "Within the last week"
    elif user.status == "within_month":
        return "Within the last month"
    elif user.status == "long_time_ago":
        return "A long time ago :("
    elif user.status == "online":
        return "Currently Online"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.status.date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@pbot.on_message(filters.command("info") & ~filters.edited & ~filters.bot)
async def info(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("O Kullanıcıyı tanımıyorum.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    await message.reply_text(
        infotext.format(
            full_name=FullName(user),
            user_id=user.id,
            user_dc=user.dc_id,
            first_name=user.first_name,
            last_name=user.last_name if user.last_name else "",
            username=user.username if user.username else "",
            last_online=LastOnline(user),
            bio=desc if desc else "`Biyo kurulum yok.`",
        ),
        disable_web_page_preview=True,
    )


app.run()
print(">> Bot çalışıyor <<")
client.run_until_disconnected()
