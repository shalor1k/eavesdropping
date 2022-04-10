from telethon import TelegramClient, sync, events, utils

api_id = int('id')
api_hash = 'hash'

chats = ['eavesdropping']
client = TelegramClient('session_name', api_id, api_hash)
client.start()
client.get_dialogs()


@client.on(events.NewMessage(incoming=True))
async def normal_handler(event):
    with open("chats.txt", "w", encoding='utf-8') as f:
        async for dialog in client.iter_dialogs():
            if dialog not in chats:
                f.write(str(dialog.title + '\n'))
    chat_id = event.chat_id
    print(chat_id)
    if chat_id == int('chat_id your bot'):
        if 'Чат добавлен' in str(event.message.to_dict()['message']):
            string = str(event.message.to_dict()['message'])[str(event.message.to_dict()['message']).index('?'):]
            chats = ['eavesdropping']
            for i in string.split('\n'):
                chats.append(i.strip())

        elif 'Чат успешно удалён' in str(event.message.to_dict()['message']):
            string = str(event.message.to_dict()['message'])[str(event.message.to_dict()['message']).index(':'):]
            chats = ['eavesdropping']
            for i in string.split('\n'):
                chats.append(i.strip())

        elif 'Запускаем парсинг' in str(event.message.to_dict()['message']):
            string = str(event.message.to_dict()['message'])[str(event.message.to_dict()['message']).index(':'):]
            keywords = []
            for i in string.split(','):
                keywords.append(i.strip())

    global codes
    try:
        chat = await client.get_entity(event.message.chat_id)
        if chat.title in chats:
            if '#ищу' in str(event.message.to_dict()['message']):
                send = []
                for i in codes:
                    if i in str(event.message.to_dict()['message']):
                        if event.message.to_dict()['message'] not in send:
                            await client.send_message('chat', event.message.to_dict()['message'])
                            send.append(event.message.to_dict()['message'])
    except Exception:
        pass

client.run_until_disconnected()
