import datetime
import os
import subprocess

import environ
import requests

from .models import LogSenderBot, BackupDbBot

env = environ.Env()
env.read_env(".env")


# Corrected class name to "Commands"
def send_to_telegram(bot_token, chat_id, filename, caption):
    caption += f"\nDate: {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    files = {'document': open(f"{filename}", 'rb')}
    data = {'chat_id': chat_id, 'caption': caption} if caption else {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    return response.json()


def send_msg_log(message):
    # Define maximum length for each message chunk
    max_length = 4096
    if LogSenderBot.objects.all().count() > 0:
        token = LogSenderBot.objects.last().token
        chat_id = LogSenderBot.objects.last().channel_id
    else:
        token = env.str("ADMIN_BOT_TOKEN")
        chat_id = env.str("LOG_SENTRY_CHANNEL_ID")

    # Split the message into chunks
    message_chunks = [message[i:i + max_length] for i in range(0, len(message), max_length)]

    for chunk in message_chunks:
        # Format the chunk as code (HTML-style markdown)
        formatted_chunk = f"<code>{chunk}</code>"

        url = f'https://api.telegram.org/bot{token}/sendMessage'
        params = {
            'chat_id': chat_id,
            'text': formatted_chunk,
            'parse_mode': 'HTML'
        }
        r = requests.post(url, data=params)
        print("r: ", r.status_code)
        print("r: ", r.text)
        if r.status_code != 200:
            return False

    return True


def backup_database():
    try:

        DB_NAME = env.str("DB_NAME")
        DB_USER = env.str("DB_USER")
        DB_PASSWORD = env.str("DB_PASSWORD")
        DB_HOST = env.str("DB_HOST")
        DB_PORT = env.str("DB_PORT")

        dump_file = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

        # Dumpni olish uchun bash komandasi

        command = f"pg_dump -U {DB_USER} -h {DB_HOST} -p {DB_PORT} {DB_NAME} > {dump_file}"
        os.environ['PGPASSWORD'] = DB_PASSWORD
        # Komandani bajarish
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while executing command: {e}")
            send_msg_log(f"Central system backup\nError occurred while executing command: {e}")
            return

        # sending backup file
        if BackupDbBot.objects.all().count() > 0:
            token = BackupDbBot.objects.last().token
            channel_id = BackupDbBot.objects.last().channel_id
        else:
            token = env.str("ADMIN_BOT_TOKEN")
            channel_id = env.str("BACUP_TG_CHANNEL_ID")

        send_to_telegram(token, channel_id, dump_file, f"All bots: > Backup file: {dump_file}")

        # delete backup file
        txt = f"Central system backup\ndelete dump database after send::\n"

        if os.path.exists(dump_file):
            os.remove(dump_file)
            txt += f"delete = {dump_file}\n"
        else:
            txt += f"error delete = {dump_file}\n"

        send_msg_log(txt)
    except Exception as e:
        # all files finish with .sqlite3
        send_msg_log(f"Central system backup\nError occurred while executing command: {e}")


__all__ = ["backup_database"]
