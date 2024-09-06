import random

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from .default_handlers.check_subscription.handlers import add_ask_subscribe_channel, check_subscription_channel_always
from .default_handlers.language.handlers import ask_language
from .default_handlers.onboarding import static_text
from .default_handlers.utils.decorators import admin_only
from .filter_caption import clean_caption
from .keyboard.keyboard import make_movie_share_keyboard, default_keyboard, make_movie_share_keyboard_with_code, \
    start_with_code_keyboard, movie_share_keyboard
from .main_bot.bot import Bot_settings
from .models import User, Movie, MovieTrailer, SuperSettings
from telegram import Bot, InputFile
from telegram.error import TelegramError


def send_video(bot, chat_id, video_file_id, caption):
    try:
        # Send the video
        bot.send_video(
            chat_id=chat_id,
            video=video_file_id,
            caption=caption,
            parse_mode=ParseMode.HTML
        )
        print("Video sent successfully.")
        return "Video sent successfully."
    except TelegramError as e:
        print(f"Failed to send video. Error: {e}")
        return f"Failed to send video. Error: {e}"


def not_movie_data(update: Update, context: CallbackContext):
    if not Movie.objects.exists():
        return update.message.reply_text("Bazada hech qanday kino topilmadi")


def movie_channel_username():
    if SuperSettings.objects.exists():
        return SuperSettings.objects.last().movie_channel_username, SuperSettings.objects.last().movie_bot_username
    return "@uzbek_kino_time", "@uzbek_kino_time_bot"


def get_trailer_chat_id():
    if SuperSettings.objects.exists():
        return SuperSettings.objects.last().trailer_chat_id
    return -1002080046544


@add_ask_subscribe_channel
def start(update: Update, context: CallbackContext, subscribe: bool) -> None:
    u, created = User.get_user_and_created(update, context)
    if update.message and update.message.entities and update.message.entities[0] and update.message.entities[
        0].type == "bot_command" and update.message.text != "/start":
        preparing_code = update.message.text.split("/start ")[1]
        if preparing_code.isdigit():
            get_movie_by_code(update, context)
            return

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    if Bot_settings.force_language:
        ask_language(update, context)

    if subscribe:
        update.message.reply_text(text=text,
                                  reply_markup=default_keyboard())


@admin_only
def get_movie_from_admin(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.username
    print(update.message.to_dict())
    video = update.message.video
    caption = update.message.caption

    channel_username, movie_bot_username = movie_channel_username()

    sign_text = f"\n﷽Aใhล๓dนใเใใลh﷽ ♥️ 🐾\n♥️ 🐾{channel_username}\n♥️ 🐾{movie_bot_username}"
    if video.duration <= 1200:
        if caption.isdigit():
            movie_code = int(caption)
            movie = Movie.objects.filter(code=movie_code).first()

            if movie:
                trailer_exists = MovieTrailer.objects.filter(file_unique_id=video.file_unique_id).exists()
                if trailer_exists:
                    movie_trailer = MovieTrailer.objects.get(file_unique_id=video.file_unique_id)
                    movie_trailer.metadata = video.to_dict()
                    movie.trailer = movie_trailer
                    movie_trailer.save()
                    movie.save()
                    update.message.reply_text("Trailer added to the movie successfully")

                    # First video send operation
                    context.bot.send_video(
                        chat_id=update.message.chat_id,
                        video=movie_trailer.metadata.get('file_id'),
                        caption=f"Kino kodi: {movie.code}\n{movie.caption}" + sign_text,
                        reply_markup=start_with_code_keyboard(bot_username, code=movie.code)
                    )
                    send_video(
                        bot=context.bot,
                        chat_id=get_trailer_chat_id(),
                        video_file_id=movie_trailer.metadata.get('file_id'),
                        caption=f"Kino kodi: {movie.code}\n{movie.caption}" + f"\n<a href='https://t.me/{context.bot.username}?start={movie.code}'>To'liq kino</a>\n" + sign_text,
                    )

                else:
                    movie_trailer = MovieTrailer.objects.create(file_unique_id=video.file_unique_id,
                                                                metadata=video.to_dict())
                    movie.trailer = movie_trailer
                    movie.save()
                    update.message.reply_text("New trailer added to the database successfully")

                    # First video send operation
                    context.bot.send_video(
                        chat_id=update.message.chat_id,
                        video=movie_trailer.metadata.get('file_id'),
                        caption=f"Kino kodi: {movie.code}\n{movie.caption}" + sign_text,
                        reply_markup=start_with_code_keyboard(bot_username, code=movie.code)
                    )

                    # Second video send operation
                    send_video(
                        bot=context.bot,
                        chat_id=get_trailer_chat_id(),
                        video_file_id=movie_trailer.metadata.get('file_id'),
                        caption=f"Kino kodi: {movie.code}\n{movie.caption}" + f"\n<a href='https://t.me/{context.bot.username}?start={movie.code}'>To'liq kino</a>\n" + sign_text,
                    )


            else:

                update.message.reply_text(f"Movie not found with code {movie_code}")
        else:
            update.message.reply_text("Please upload a trailer video with a digital caption 🥺😢🙃")
        return

    try:
        movie = Movie.objects.get(file_unique_id=video.file_unique_id)
        movie.metadata = video.to_dict()
        movie.caption = clean_caption(caption)
        movie.save()
        update.message.reply_text(f"Movie {movie.code} updated successfully")
    except Movie.DoesNotExist:
        movie = Movie.objects.create(
            file_unique_id=video.file_unique_id,
            metadata=video.to_dict(),
            caption=clean_caption(caption)
        )
        movie.code = 1000 - movie.id
        movie.save()
        update.message.reply_text(f"Movie {movie.code} added successfully")


@check_subscription_channel_always
def get_movie_by_code(update: Update, context: CallbackContext) -> None:
    not_movie_data(update, context)
    sign_text = "\n﷽Aใhล๓dนใเใใลh﷽ ♥️ 🐾\n♥️ 🐾@uzbek_kino_time\n♥️ 🐾@uzbek_kino_time_bot"
    bot_username = context.bot.username
    if update.message.text.startswith("/start"):
        code = int(update.message.text.split("/start ")[1])
    else:
        code = int(update.message.text)
    try:

        movie = Movie.objects.filter(code=code).first()
        if movie:
            movie.view_count += 1
            movie.save()
            # Assuming `reply_video` sends a video by file ID
            update.message.reply_video(video=movie.metadata.get('file_id'),
                                       caption=f"Movie code: {movie.code}\n{movie.caption}" + sign_text,
                                       protect_content=True,
                                       parse_mode="HTML",
                                       reply_markup=make_movie_share_keyboard_with_code(code=movie.code,
                                                                                        bot_username=bot_username)
                                       )
        else:
            update.message.reply_text("Movie not found with this code 🥺😢🙃")
    except ValueError:
        update.message.reply_text("Invalid input. Please enter a valid movie code.")


@check_subscription_channel_always
def search_movies(update: Update, context: CallbackContext) -> None:
    not_movie_data(update, context)
    if update and update.message and update.message.text == "🔍 Search Movies":
        update.message.reply_text("Can you please tell me the name of the movie you are looking for? 🤔🤔🤔")
    if update and update.message and update.message.text and update.message.text != "🔍 Search Movies":
        movie_name = update.message.text
        movies = list(Movie.objects.filter(caption__icontains=movie_name))
        if movies:
            # Calculate the number of movies to send
            num_movies_to_send = min(len(movies), 3)  # Send a maximum of 3 movies
            # Shuffle the movies list to randomize the selection
            random.shuffle(movies)
            for movie in movies[:num_movies_to_send]:
                # Check if a randomly generated number is less than 30% for each movie
                if random.random() < 0.3:
                    movie.view_count += 1
                    movie.save()
                    # Assuming `reply_video` sends a video by file ID
                    update.message.reply_video(video=movie.metadata.get('file_id'),
                                               caption=f"Movie code: {movie.code}\n{movie.caption}",
                                               protect_content=True,
                                               parse_mode="HTML",
                                               reply_markup=make_movie_share_keyboard()
                                               )
        else:
            update.message.reply_text("Movie not found with this name 🥺😢🙃")


@check_subscription_channel_always
def top_movies(update: Update, context: CallbackContext) -> None:
    not_movie_data(update, context)
    if update and update.message and update.message.text == "🎲 Random Movie":
        movie = Movie.objects.order_by("?").first()
        if movie:
            movie.view_count += 1
            movie.save()
            # Assuming `reply_video` sends a video by file ID
            update.message.reply_video(video=movie.metadata.get('file_id'),
                                       caption=f"Movie code: {movie.code}\n{movie.caption}",
                                       protect_content=True,
                                       parse_mode="HTML",
                                       reply_markup=make_movie_share_keyboard()
                                       )
    if update and update.message and update.message.text == "🎥 Top 1 Movies":
        movies = Movie.objects.order_by('-view_count')[:1]
        for movie in movies:
            # Assuming `reply_video` sends a video by file ID
            update.message.reply_video(video=movie.metadata.get('file_id'),
                                       caption=f"Movie code: {movie.code}\n{movie.caption}",
                                       protect_content=True,
                                       parse_mode="HTML",
                                       reply_markup=make_movie_share_keyboard()
                                       )

    if update and update.message and update.message.text == "🎥 Top 3 Movies":
        movies = Movie.objects.order_by('-view_count')[:3]
        for movie in movies:
            # Assuming `reply_video` sends a video by file ID
            update.message.reply_video(video=movie.metadata.get('file_id'),
                                       caption=f"Movie code: {movie.code}\n{movie.caption}",
                                       protect_content=True,
                                       parse_mode="HTML",
                                       reply_markup=make_movie_share_keyboard()
                                       )


@check_subscription_channel_always
def share_bot(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Share this bot with your friends and family 🥰🥰🥰",
                              reply_markup=movie_share_keyboard())


@admin_only
def random_no_trailers_movie(update: Update, context: CallbackContext) -> None:
    not_movie_data(update, context)
    movie = Movie.objects.filter(has_trailer=False).order_by("?").first()
    if movie:
        # Assuming `reply_video` sends a video by file ID
        update.message.reply_video(video=movie.metadata.get('file_id'),
                                   caption=f"Movie code: {movie.code}\n{movie.caption}",
                                   protect_content=True,
                                   parse_mode="HTML",
                                   reply_markup=make_movie_share_keyboard()
                                   )
