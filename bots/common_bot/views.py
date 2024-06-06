import random

from telegram import Update
from telegram.ext import CallbackContext

from .default_handlers.check_subscription.handlers import add_ask_subscribe_channel, check_subscription_channel_always
from .default_handlers.language.handlers import ask_language
from .default_handlers.onboarding import static_text
from .default_handlers.utils.decorators import admin_only
from .filter_caption import clean_caption
from .keyboard.keyboard import make_movie_share_keyboard, default_keyboard, make_movie_share_keyboard_with_code, \
    start_with_code_keyboard
from .main_bot.bot import Bot_settings
from .models import User, Movie, MovieTrailer


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
    print(update.message.to_dict())
    video = update.message.video
    caption = update.message.caption
    sign_text = "\n﷽Aใhล๓dนใเใใลh﷽ ♥️ 🐾\n♥️ 🐾@uzbek_kino_time\n♥️ 🐾@uzbek_kino_time_bot"
    if video.duration <= 1800:
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
                    context.bot.send_video(chat_id=update.message.chat_id, video=movie_trailer.metadata.get('file_id'),
                                           caption=f"Kino kodi: {movie.code}\n{movie.caption}" + sign_text,
                                           reply_markup=start_with_code_keyboard(code=movie.code))
                else:
                    movie_trailer = MovieTrailer.objects.create(file_unique_id=video.file_unique_id,metadata=video.to_dict())
                    movie.trailer = movie_trailer
                    movie.save()
                    update.message.reply_text("New trailer added to the database successfully")
                    context.bot.send_video(chat_id=update.message.chat_id, video=movie_trailer.metadata.get('file_id'),
                                             caption=f"Kino kodi: {movie.code}\n{movie.caption}" + sign_text,
                                             reply_markup=start_with_code_keyboard(code=movie.code))

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
    sign_text = "\n﷽Aใhล๓dนใเใใลh﷽ ♥️ 🐾\n♥️ 🐾@uzbek_kino_time\n♥️ 🐾@uzbek_kino_time_bot"
    bot_username=context.bot.username
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
                                       reply_markup=make_movie_share_keyboard_with_code(code=movie.code,bot_username=bot_username)
                                       )
        else:
            update.message.reply_text("Movie not found with this code 🥺😢🙃")
    except ValueError:
        update.message.reply_text("Invalid input. Please enter a valid movie code.")


@check_subscription_channel_always
def search_movies(update: Update, context: CallbackContext) -> None:
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
                              reply_markup=make_movie_share_keyboard())


@admin_only
def random_no_trailers_movie(update: Update, context: CallbackContext) -> None:
    movie = Movie.objects.filter(has_trailer=False).order_by("?").first()
    if movie:
        # Assuming `reply_video` sends a video by file ID
        update.message.reply_video(video=movie.metadata.get('file_id'),
                                   caption=f"Movie code: {movie.code}\n{movie.caption}",
                                   protect_content=True,
                                   parse_mode="HTML",
                                   reply_markup=make_movie_share_keyboard()
                                   )
