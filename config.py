import re, os, time, logging
from pyrogram.errors import FloodWait, RPCError

logging.basicConfig(level=logging.INFO, filename='error.log')
LOG = logging.getLogger("Bot by @YUITOAKASH")
LOG.setLevel(level=logging.INFO)

id_pattern = re.compile(r'^.\d+$')

class Config(object):
    # pyro client config
    API_ID = os.environ.get("API_ID", "14712540")
    API_HASH = os.environ.get("API_HASH", "e61b996dc037d969a4f8cf6411bb6165")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_NAME = os.environ.get("BOT_NAME", "ya_renamebot")
    TOKEN_TIMEOUT = int(os.environ.get("TOKEN_TIMEOUT", 86400))
    SESSION_STRING = os.environ.get("SESSION_STRING","None") # either give session string or let it be None value 
    # database config
    DB_NAME = os.environ.get("DB_NAME","pyro-botz")
    DB_URL = os.environ.get("DB_URL","")
    # other configs
    BOT_UPTIME = time.time()
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '2009088107').split()]
    FORCE_SUB = os.environ.get("FORCE_SUB", "")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1001682783965))
    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    Text = os.environ.get("Text", """●     °    •      ○    ●   •  ●    ○   •  ●

○       ●      °    ●    •     ○   ●   ○  •
ㅤㅤㅤㅤㅤㅤ(*≧ω≦*)
┏━━━━━━━  ✦  ✦ ━━━━━━━━┓
┃🔈𝙽𝙰𝙼𝙴   ○○○   {first_name}●●●
┃👥 𝙼𝙴𝙽𝚃𝙸𝙾𝙽   ○○○   {mention}●●●
┃🆔 𝙸𝙳   ○○○   {id}●●●
┗━━━━━━━━ ✦ ✦━━━━━━━━┛""")
    Text1 = os.environ.get("Text1", """☞☞☞ ☞☞ 𝐻𝐸𝐿𝑃 𝑃𝐴𝐺𝐸 ☚☚ ☚☚

☞ ┃ /ping 𝗙ᴏʀ 𝗖ʜᴇᴄᴋɪɴɢ 𝗕ᴏᴛ 𝗔ʟɪᴠᴇ
    ┏━━━━━━━━━━━━━━┓
     🖼 𝗛ᴏᴡ 𝗧ᴏ 𝗦ᴇᴛ 𝗧ʜᴜᴍʙɴɪʟ
    ┗━━━━━━━━━━━━━━┛
☞ ┃ 📸 𝗦ᴇɴᴅ 𝗔ɴ𝘆 𝗣ʜᴏᴛᴏ 𝗧ᴏ 𝗔ᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟ𝘆 𝗦ᴇᴛ 𝗧ʜᴜᴍʙɴᴀʟᴇ.
☞ ┃ 🗑 /del_thumb 𝗧ᴏ 𝗗ᴇʟᴇᴛᴇ 𝗬ᴏᴜʀ 𝗢ʟᴅ 𝗧ʜᴜᴍʙɴɪʟᴇ.
☞ ┃ 👁 /view_thumb 𝗧ᴏ 𝗩ɪᴇᴡ 𝗬ᴏᴜʀ 𝗖ᴜʀʀᴇɴᴛ 𝗧ʜᴜᴍʙɴɪʟᴇ.
    ┏━━━━━━━━━━━━━━━━━━━┓ 
     📑 𝗛ᴏᴡ 𝗧ᴏ 𝗦ᴇᴛ 𝗖ᴜꜱᴛᴏᴍ 𝗖ᴀᴩᴛɪᴏɴ
    ┗━━━━━━━━━━━━━━━━━━━┛
☞ ┃ 📝 /set_caption - 𝗧ᴏ 𝗦ᴇᴛ ᴀ 𝗖ᴜꜱᴛᴏᴍ 𝗖ᴀᴩᴛɪᴏɴ
☞ ┃ 👁‍🗨 /see_caption - 𝗧ᴏ 𝗩ɪᴇᴡ 𝗬ᴏᴜʀ 𝗖ᴜꜱᴛᴏᴍ 𝗖ᴀᴩᴛɪᴏɴ
☞ ┃ 🗑 /del_caption - 𝗧ᴏ 𝗗ᴇʟᴇᴛᴇ 𝗬ᴏᴜʀ 𝗖ᴜꜱᴛᴏᴍ 𝗖ᴀᴩᴛɪᴏɴ
☞ ┃ 🏷 𝗡ᴏᴛᴇ:- /set_caption 𝗨𝘀ᴇ 𝗙ᴏʀ 𝗙ᴇᴡ 𝗣ʀᴇ_𝗗ᴇғɪɴᴇᴅ 𝗖ᴀᴘᴛɪᴏɴ𝘀.

☞ ┃ ✏️ 𝗛ᴏᴡ 𝗧ᴏ 𝗥ᴇɴᴀᴍᴇ 𝗔 𝗙ɪʟᴇ
📥 𝗦ᴇɴᴅ 𝗔ɴ𝘆 𝗙ɪʟᴇ 
🏷 𝗧𝘆ᴩᴇ 𝗡ᴇᴡ 𝗙ɪʟᴇ 𝗡ᴀᴍᴇ 
📤 𝗦ᴇʟᴇᴄᴛ 𝗧ʜᴇ 𝗙ᴏʀᴍᴀᴛ [ 𝗱𝗼𝗰𝘂𝗺𝗲𝗻𝘁, 𝘃𝗶𝗱𝗲𝗼, 𝗮𝘂𝗱𝗶𝗼 ].
           ┏━━━━━━━━━━┓ 
ㅤㅤ    ℹ️ 𝗔𝗻𝘆 𝗢𝘁𝗵𝗲𝗿 𝗛𝗲𝗹𝗽
           ┗━━━━━━━━━━┛
☛┃ [𝗖𝗼𝗻𝘁𝗮𝗰𝘁](https://t.me/devil_testing_bot) 
☛┃ [𝗚𝗿𝗼𝘂𝗽](https://t.me/KIRIGAYA_ASUNA)
☛┃ [𝗖𝗵𝗮𝗻𝗻𝗲𝗹](https://t.me/kirigayaakash)""")
    Text2 = os.environ.get("Text2", """👋 𝙺𝙾𝙽𝙸𝙲𝙷𝙸𝚆𝙰;  {first_name}

1.》😏𝚃𝙷𝙸𝚂 𝙱𝙾𝚃 𝚁𝙴𝙿𝙾 𝙸𝚂 𝙿𝚁𝙸𝚅𝙰𝚃𝙴 𝙱𝚄𝚃 𝙽𝙾𝚃 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴𝙻𝚈 𝙿𝚁𝙸𝚅𝙰𝚃𝙴 .....

2.》🧑‍💻 𝙸 𝙰𝙼 𝚄𝚂𝙸𝙽𝙶 𝙿𝚈𝚁𝙾-𝙱𝙾𝚃𝚉 𝚁𝙴𝙿𝙾 𝙰𝚂 𝙱𝙰𝚂𝙴 𝚁𝙴𝙿𝙾 𝙰𝙽𝙳 𝙾𝚃𝙷𝙴𝚁 𝙴𝚇𝚃𝚁𝙰 𝚄𝙿𝙳𝙰𝚃𝙴𝚂 𝙸𝚂 𝙳𝙾𝙽𝙴 𝙱𝚈 𝙼𝙴.....

3.》📮𝙱𝙰𝚂𝙸𝙲𝙰𝙻𝙻𝚈 𝙽𝙾𝚃 𝙼𝙸𝙽𝙴 𝙸𝙳𝙴𝙰𝚂 𝙱𝚄𝚃 𝙸 𝙷𝙰𝚅𝙴 𝚃𝙰𝙺𝙴𝙽 𝚃𝙷𝙴 𝙸𝙳𝙴𝙰𝚂 𝙵𝚁𝙾𝙼 𝙾𝚃𝙷𝙴𝚁 𝙱𝙾𝚃𝚂.....

4.》❌𝙸 𝙰𝙼 𝙽𝙾𝚃 𝙰 𝙿𝚁𝙾𝙵𝙴𝚂𝚂𝙸𝙾𝙽𝙰𝙻 𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁 𝙱𝚄𝚃 𝙹𝚄𝚂𝚃 𝙻𝙸𝙺𝙴𝙳 𝚃𝙷𝙴 𝙾𝚃𝙷𝙴𝚁 𝙱𝙾𝚃 𝙵𝙴𝙰𝚃𝚄𝚁𝙴𝚂 𝚂𝙾 𝙸 𝙰𝙳𝙳𝙴𝙳 𝙸𝙽 𝙸𝚃...""")
    Text3 = os.environ.get("Text3", """ㅤㅤㅤㅤㅤㅤ[ᴄʀᴇᴅɪᴛs](tg://user?id={id})
ㅤㅤㅤ  ●●●●●●●●●●●●●●●●ㅤㅤㅤ
ㅤㅤㅤ    𝙲𝚛𝚎𝚊𝚝𝚘𝚛𝚜 𝙾𝚏 𝙿𝚢𝚛𝚘-𝙱𝚘𝚝𝚣.
          2gb+ credit to Shadow Blade....
ㅤㅤ      ㅤ 𝙾𝚝𝚑𝚎𝚛 𝙲𝚛𝚎𝚊𝚝𝚘𝚛𝚜 𝙸𝚍𝚎𝚊𝚜...ㅤㅤㅤ
ㅤㅤ        ㅤ𝙰𝚗𝚍 𝙼𝚢𝚜𝚎𝚕𝚏ㅤㅤㅤㅤㅤㅤㅤ
ㅤㅤㅤㅤㅤㅤ  ●●●●●●●●●●●●●●●●ㅤㅤ

𝚃𝙷𝙸𝚂 𝙱𝙾𝚃 𝙸𝚂 𝙼𝙰𝙳𝙴 𝙱𝚈 𝙲𝚁𝙴𝙰𝚃𝙾𝚁 𝙾𝙵 [{first_name}](tg://user?id={id}) ....ㅤ

  -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

🏷 ℂ𝕠𝕟𝕥𝕒𝕔𝕥 𝕥𝕠 [ℂ𝕣𝕖𝕒𝕥𝕠𝕣](tg://user?id={id})
👨🏻‍💻 𝕆𝕨𝕟𝕖𝕣 [ℂ𝕣𝕖𝕒𝕥𝕠𝕣](http://t.me/devil_testing_bot)
👨🏻‍🔧 𝕄𝕠𝕕𝕚𝕗𝕚𝕖𝕕 𝕓𝕪 [ℕ𝕆𝕆𝔹_𝕂𝔸ℕ𝔾𝔼ℝ](https://t.me/kirigayaakash)""")

    LOGGER = LOG
    shorteners_list = []

    def __init__(self):
        if os.path.exists('shorteners.txt'):
            with open('shorteners.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    temp = line.strip().split()
                    if len(temp) == 2:
                        self.shorteners_list.append({'domain': temp[0], 'api_key': temp[1]})

LOG.info('Config loaded successfully')


class Txt(object):

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""
