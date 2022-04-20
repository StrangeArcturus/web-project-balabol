from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.vk_api import VkApiMethod

from random import randint

from config import config
from generate_text import get_text_from_history


inv_message = """
Всем привет! Я Балабол, я учусь человеческой речи, и для каждого чата
"обучен" я буду в зависимости от ваших сообщений)
А для работы мне нужно выдать доступ к переписке или права администратора.
Для сброса базы данных этого чата используйте команды /сброс или /reset
""".strip(' ').strip('\n').strip(' ').replace('\n', '. ')


def send_on_invite(vk: VkApiMethod, peer_id: int) -> None:
    vk.messages.send(
        peer_id=peer_id,
        massage=inv_message,
        random_id=randint(0, 2 ** 32)
    )


def main():
    vk_session = VkApi(
        token=config.token
    )
    longpoll = VkBotLongPoll(vk_session, config.ID)
    print("бот начал слушать сообщения")
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message: dict = dict(event.obj.message)
            # pprint(message, depth=7)
            if 'action' in message:
                if message['action']['type'] == 'chat_invite_user':
                    if event.group_id == -message['action']['member_id']:
                        print("пригласили в новый чат")
                        try:
                            # send_on_invite(vk, message['peer_id'])
                            # по какой-то причине вылетает ошибка api с кодом 100
                            ...
                        except Exception as e:
                            print(e)
                        finally:
                            continue


            print('Новое сообщение:')
            print('Для меня от:', message['from_id'])
            print('Текст:', message['text'])
            history = vk.messages.getHistory(
                peer_id=message['peer_id'],
                count=199
            )['items']
            print(*(), sep='\n')
            answer = get_text_from_history(list(map(lambda msg: msg['text'], history))[::-1])
            vk.messages.send(
                peer_id=message['peer_id'],
                message=answer,#"Спасибо, что написали нам. Мы обязательно ответим",
                random_id=randint(0, 2 ** 32)
            )



if __name__ == "__main__":
    main()
