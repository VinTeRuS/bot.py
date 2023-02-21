import discord
from discord.ext import commands

# создаем объект бота
client = commands.Bot(command_prefix='!')

# счетчики для статистики
channel_usage = {}
user_message_count = {}
emoji_usage = {}

# обработчик события "сообщение было отправлено"
@client.event
async def on_message(message):
    # собираем статистику использования каналов
    if message.channel.id not in channel_usage:
        channel_usage[message.channel.id] = 1
    else:
        channel_usage[message.channel.id] += 1

    # собираем статистику количества сообщений, отправленных пользователями
    if message.author.id not in user_message_count:
        user_message_count[message.author.id] = 1
    else:
        user_message_count[message.author.id] += 1

    # собираем статистику использования эмодзи
    for emoji in message.guild.emojis:
        if str(emoji) in message.content:
            if emoji.id not in emoji_usage:
                emoji_usage[emoji.id] = 1
            else:
                emoji_usage[emoji.id] += 1

    # передаем управление стандартной обработке сообщений
    await client.process_commands(message)

# команда для вывода статистики использования сервера
@client.command()
async def stats(ctx):
    # формируем сообщение со статистикой
    message = "Статистика использования сервера:\n\n"

    # добавляем статистику использования каналов
    message += "Использование каналов:\n"
    for channel_id, usage_count in channel_usage.items():
        channel = client.get_channel(channel_id)
        message += f"{channel.name}: {usage_count}\n"

    # добавляем статистику количества сообщений, отправленных пользователями
    message += "\nКоличество сообщений, отправленных пользователями:\n"
    for user_id, message_count in user_message_count.items():
        user = client.get_user(user_id)
        message += f"{user.name}: {message_count}\n"

    # добавляем статистику использования эмодзи
    message += "\nИспользование эмодзи:\n"
    for emoji_id, usage_count in emoji_usage.items():
        emoji = client.get_emoji(emoji_id)
        message += f"{emoji.name}: {usage_count}\n"

    # отправляем сообщение со статистикой в канал
    await ctx.send(message)

# запускаем бота
client.run('TOKEN')


