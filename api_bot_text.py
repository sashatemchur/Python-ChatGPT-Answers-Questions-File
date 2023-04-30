import openai, asyncio
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot('5619487724:AAFeBptlX1aJ9IEAFLMUXN3JZBImJ35quWk') 
openai.api_key = "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"


@bot.message_handler(content_types=['document'])
async def start(message):
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    src = message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    with open(src, 'r') as data:
        data_tg = data.read()
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "user", "content": data_tg},
            ]
    )
    await bot.send_message(message.chat.id, response['choices'][0]['message']['content'])


asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))