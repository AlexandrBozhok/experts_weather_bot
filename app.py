import requests, telebot, os

telegram_token = os.environ.get('telegram_token')
weather_token = os.environ.get('weather_token')
bot = telebot.TeleBot(telegram_token)
author_name = os.environ.get('author_name')


thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis

@bot.message_handler(commands=['start'])
def welcome(message):
    icon = '😁'
    welcome_msg = f'Привіт, {message.from_user.first_name}! {icon}\n' \
                  f'Я бот, створений {author_name} для отримання погоди\n' \
                  f'Щоб розпочати, напиши в чат своє місто'
    bot.send_message(message.from_user.id, welcome_msg)

@bot.message_handler(content_types='text')
def home(message):
    city = message.text
    answer = get_weather(city)
    bot.reply_to(message, answer)


@bot.message_handler(content_types='voice')
def home(message):
    msg = f'{message.from_user.first_name}, не розумію)'
    bot.reply_to(message, msg)





def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_token,
        "units": "metric",
        "lang": "ua"
    }

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        my_json = response.json()
        city_name = my_json.get('name')
        country = my_json.get('sys').get('country')
        temp = my_json.get('main').get('temp')
        weather_description = my_json.get('weather')[0].get('description')
        icon_id = my_json.get('weather')[0].get('id')
        icon = get_weather_icon(icon_id)
        return f'Локація: {city_name}, {country}\nТемпература: {temp} ℃\nСтан погоди: {weather_description}{icon}'
    return "Такого міста не існує! Спробуйте ще раз"


def get_weather_icon(weatherID):
    if str(weatherID)[0] == '2' or weatherID == 900 or weatherID == 901 or weatherID == 902 or weatherID == 905:
        return thunderstorm
    elif str(weatherID)[0] == '3':
        return drizzle
    elif str(weatherID)[0] == '5':
        return rain
    elif str(weatherID)[0] == '6' or weatherID == 903 or weatherID == 906:
        return snowflake + ' ' + snowman
    elif str(weatherID)[0] == '7':
        return atmosphere
    elif weatherID == 800:
        return clearSky
    elif weatherID == 801:
        return fewClouds
    elif weatherID == 802 or weatherID == 803 or weatherID == 803:
        return clouds
    elif weatherID == 904:
        return hot
    else:
        return defaultEmoji

bot.polling()
