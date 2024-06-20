import datetime
import os
import subprocess
import time
from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from . import static_text
from .utils import _get_csv_from_qs_values
from ..utils.decorators import admin_only, send_typing_action
from ...models import User


@admin_only
def admin(update: Update, context: CallbackContext) -> None:
    """ Show help info about all secret admins commands """
    update.message.reply_text(static_text.secret_admin_commands)


@admin_only
def stats(update: Update, context: CallbackContext) -> None:
    """ Show help info about all secret admins commands """
    text = static_text.users_amount_stat.format(
        user_count=User.objects.count(),  # count may be ineffective if there are a lot of users.
        active_24=User.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
    )

    update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


@admin_only
@send_typing_action
def export_users(update: Update, context: CallbackContext) -> None:
    # in values argument you can specify which fields should be returned in output csv
    users = User.objects.all().values()
    csv_users = _get_csv_from_qs_values(users)
    update.message.reply_document(csv_users)


@admin_only
@send_typing_action
def backup_db(update: Update, context: CallbackContext) -> None:
    try:
        # Attempt to perform database backup
        dump_file, metadata, error = backup_database()

        time.sleep(3)

        if error is not None:
            update.message.reply_text(f"Failed to perform database backup. Error:\n{error}")
        if dump_file:
            # If backup is successful, send the document
            update.message.reply_document(document=open(dump_file, 'rb'), filename=dump_file, caption=metadata)
            # Remove the backup file after sending
            os.remove(dump_file)
        else:
            update.message.reply_text("Failed to perform database backup. Please try again later.")
    except Exception as e:
        update.message.reply_text("An error occurred during the backup process. Please try again later.")


def db_check():
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
        return "PostgreSQL"
    elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        return "SQLite"
    elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
        return "MySQL"


def backup_database():
    dump_file = None
    metadata = None
    error = None
    try:
        if db_check() == "PostgreSQL":
            DB_NAME = settings.DATABASES['default']['NAME']
            DB_USER = settings.DATABASES['default']['USER']
            DB_PASSWORD = settings.DATABASES['default']['PASSWORD']
            DB_HOST = settings.DATABASES['default']['HOST']
            DB_PORT = settings.DATABASES['default']['PORT']
            dump_file = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            metadata = f"db_name : {DB_NAME} ,\n db_user : {DB_USER} ,\n db_password : {DB_PASSWORD} ,\n db_host : {DB_HOST} ,\n db_port : {DB_PORT} ,\n dump_file : {dump_file}"
            print(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, dump_file)
            # Dumpni olish uchun bash komandasi

            command = f"pg_dump -U {DB_USER} -h {DB_HOST} -p {DB_PORT} {DB_NAME} > {dump_file}"
            os.environ['PGPASSWORD'] = DB_PASSWORD
            # Komandani bajarish
            try:
                subprocess.run(command, shell=True, check=True)

            except subprocess.CalledProcessError as e:
                error = e
        elif db_check() == "SQLite":
            DB_NAME = settings.DATABASES['default']['NAME']
            dump_file = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
            metadata = f"db_name : {DB_NAME} ,\n dump_file : {dump_file}"
            command = f"sqlite3 {DB_NAME} .dump > {dump_file}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                error = e
    except Exception as e:
        error = e

    return dump_file, metadata, error
