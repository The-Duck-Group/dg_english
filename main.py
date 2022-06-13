import time
import logging
import shutil
from pathlib import Path, PosixPath
from telegram import Bot, InputMediaAudio, Message, ParseMode
from telegram.utils.request import Request

req = Request(proxy_url="socks5h://127.0.0.1:9050", connect_timeout=None, read_timeout=None)

token = "your token"
channel_username = "your channel username"
bot: Bot = Bot(token,
               request=req
               )
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

data = Path('data')

elem = data / 'Elementary'
inter = data / 'Intermediate'
# and so on..

elem_folders = [f for f in elem.iterdir()]
inter_folders = [f for f in inter.iterdir()]

text = "text to send as caption"


def send_folder_to_tel(path: Path):
    """
    first send the pdf
    then send podcasts replying to that msg..also log the shit..

    :return:
    """
    album = []
    for file in path.iterdir():
        # check if file is pdf, send it..
        if file.match('*.pdf'):
            logging.info("sending pdf to telegram")
            msg: Message = bot.send_document(channel_username, file.open('rb'), caption=text,
                                             parse_mode=ParseMode.MARKDOWN,
                                             disable_notification=True,
                                             )
            time.sleep(1.5)
            logging.info(f"~~ sending audio files replying to #{msg.message_id}")
        elif file.match('*.mp3'):
            # it is .mp3!
            album.append(file)

    media_group = []
    for _, track in enumerate(album):
        if _ == 2:
            media_group.append(InputMediaAudio(media=track.open('rb'), caption=text, parse_mode=ParseMode.MARKDOWN))
        else:
            media_group.append(InputMediaAudio(media=track.open('rb')))

    # media_group = [InputMediaAudio(media=f.open('rb'), caption=text, parse_mode=ParseMode.MARKDOWN) for f in album]
    bot.send_media_group(channel_username, media=media_group, reply_to_message_id=msg.message_id, timeout=5000,
                         disable_notification=True,

                         )
    logging.info("~~ done sending..sleep for 10 sec ~~")
    time.sleep(10)
    shutil.rmtree(path)  # delete sent files!


for folder in elem_folders:
    send_folder_to_tel(folder)

for folder in inter_folders:
    send_folder_to_tel(folder)
