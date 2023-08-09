import requests
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Job

def get_weather_data(latitude, longitude, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': latitude,
        'lon': longitude,
        'units': 'metric',
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def send_weather(context):
    api_key = "43d5cdd4e3a0fbcf264fea1da9754c30"
    latitude = -18.8211  # Replace with the latitude of the location
    longitude = 49.0712  # Replace with the longitude of the location

    weather_data = get_weather_data(latitude, longitude, api_key)

    if 'name' in weather_data:
        city_name = weather_data['name']
    else:
        city_name = 'Unknown'
    
    if 'main' in weather_data:
        temperature = weather_data['main'].get('temp', 'N/A')
    else:
        temperature = 'N/A'

    if 'weather' in weather_data and len(weather_data['weather']) > 0:
        description = weather_data['weather'][0].get('description', 'N/A')
    else:
        description = 'N/A'
    
    message = f"Prévisions météo pour {city_name} :\nTempérature : {temperature}°C\nPrécipitations : {description}"

    # Send the weather message to all subscribed users
    subscribers = context.job.context if context.job else set()
    for chat_id in subscribers:
        context.bot.send_message(chat_id=chat_id, text=message)

def start(update, context):
    # Send a welcome message with inline keyboard for subscribing/unsubscribing
    keyboard = [
        [InlineKeyboardButton("Subscribe", callback_data='subscribe')],
        [InlineKeyboardButton("Unsubscribe", callback_data='unsubscribe')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Bienvenue ! Vous êtes abonné aux mises à jour météo quotidiennes à 8h00.", reply_markup=reply_markup)

def subscribe(update, context):
    # Add the current user's chat ID to the subscribers set
    job = context.job
    if job:
        subscribers = job.context
    else:
        subscribers = set()
    subscribers.add(update.effective_user.id)

    context.job = Job(send_weather, context=subscribers)
    update.callback_query.answer()
    update.callback_query.message.reply_text("Vous êtes désormais abonné aux mises à jour météo quotidiennes à 8h00.")

def unsubscribe(update, context):
    # Remove the current user's chat ID from the subscribers set
    job = context.job
    if job:
        subscribers = job.context
        if update.effective_user.id in subscribers:
            subscribers.remove(update.effective_user.id)
            context.job = Job(send_weather, context=subscribers)
            update.callback_query.answer()
            update.callback_query.message.reply_text("Vous vous êtes désabonné des mises à jour météo.")
        else:
            update.callback_query.answer()
            update.callback_query.message.reply_text("Vous n'étiez pas abonné.")
    else:
        update.callback_query.answer()
        update.callback_query.message.reply_text("Vous n'étiez pas abonné.")

def button(update, context):
    # Handle button presses from the inline keyboard
    query = update.callback_query
    if query.data == 'subscribe':
        subscribe(update, context)
    elif query.data == 'unsubscribe':
        unsubscribe(update, context)
    else:
        query.answer("Une erreur s'est produite.")

def main():
    bot_token = "6404100838:AAHrkiS-6HWFWPCj7Lj9kJgvrFJMbTzZG4c"
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Start the job to send weather every day at 8:00 AM (local time)
    job_queue = updater.job_queue
    job_queue.run_daily(send_weather, time=datetime.time(8, 0, 0))

    # Add command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Add callback query handler for inline keyboard buttons
    callback_query_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(callback_query_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
