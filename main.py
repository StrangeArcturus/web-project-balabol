from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from random import randint
from pprint import pprint

from config import config
from generate_text import get_text_from_history


def auth_handler():
    """
    При двухфакторной аутентификации вызывается эта функция.
    """
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


inv_message = """
Всем привет! Я Балабол, я учусь человеческой речи, и для каждого чата
"обучен" я буду в зависимости от ваших сообщений)
А для работы мне нужно выдать доступ к переписке или права администратора.
Для сброса базы данных этого чата используйте команды /сброс или /reset
""".strip(' ').strip('\n').strip(' ')


def main():
    vk_session = VkApi(
        token=config.token
    )
    longpoll = VkBotLongPoll(vk_session, config.ID)
    print("бот начал слушать сообщения")
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            pprint(event.obj.message, depth=7)
            if 'action' in event.obj.message:
                if event.obj.message['action']['type'] == 'chat_invite_user':
                    if event.group_id == -event.obj.message['action']['member_id']:
                        print("пригласили в новый чат")
                        try:
                            vk.messages.send(
                                peer_id=event.obj.message['peer_id'],
                                massage="inv_message",
                                random_id=randint(0, 2 ** 32)
                            )
                        except Exception as e:
                            print(e, e.args)
                        finally:
                            continue


            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk.messages.getHistory()
            vk.messages.send(user_id=event.obj.message['from_id'],
                            message="Спасибо, что написали нам. Мы обязательно ответим",
                            random_id=randint(0, 2 ** 64))



if __name__ == "__main__":
    main()
