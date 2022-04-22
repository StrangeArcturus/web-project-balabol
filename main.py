from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.vk_api import VkApiMethod
# всякая всячина api

from random import randint
# для случайного id
# так как так требует api vk
from typing import List, NoReturn, Optional
# немного подсказок типов

from config import config
# самописный конфиг
from generate_text import get_text_from_history
# обёртка над чудо-библиотекой
from data import db_session
from data.messages import Message
# базы данных


inv_message = """
Всем привет! Я Балабол, я учусь человеческой речи, и для каждого чата
"обучен" я буду в зависимости от ваших сообщений)
А для работы мне нужно выдать доступ к переписке или права администратора.
Для сброса базы данных этого чата используйте команды /сброс или /reset
""".strip(' ').strip('\n').strip(' ').replace('\n', '. ')
# сообщение при приглашении
# временно не будет использоваться
db_session.global_init("db/messages.db")
print("база данных успешно подключена")
db_sess = db_session.create_session()
# суета с базами данных


def send_on_invite(vk: VkApiMethod, peer_id: int) -> None:
    """
    обёртка на приглашение бота в беседу
    :vk `VkApiMethod`
    :peer_id `int`
    return `None`
    """
    vk.messages.send(
        peer_id=peer_id,
        massage=inv_message,
        random_id=randint(0, 2 ** 32)
    )


def add_history_to_db(history: List[str]) -> None:
    for message in history:
        msg = Message()
        msg.text = message
        db_sess.add(msg)
        db_sess.commit()


def get_and_generate_message_from_db() -> str:
    messages: List[str] = db_sess.query(Message).all()
    return get_text_from_history(messages)


def main() -> Optional[NoReturn]:
    vk_session = VkApi(
        token=config.token
    )
    longpoll = VkBotLongPoll(vk_session, config.ID)
    print("бот начал слушать сообщения")
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message: dict = dict(event.obj.message)
            if 'action' in message:
                if message['action']['type'] == 'chat_invite_user':
                    # проверка на приглашение в чат
                    if event.group_id == -message['action']['member_id']:
                        print("пригласили в новый чат")
                        try:
                            # send_on_invite(vk, message['peer_id'])
                            # по какой-то причине вылетает ошибка api с кодом 100
                            ...
                        except Exception as e:
                            print(e)
                        finally:
                            # следующий круг -- всё по новой
                            continue


            print('Новое сообщение:')
            print('Для меня от:', message['from_id'])
            print('Текст:', message['text'])
            # информирование
            history = vk.messages.getHistory(
                peer_id=message['peer_id'],
                count=199
            )['items']
            history = list(
                map(
                    lambda msg: msg["text"],
                    filter(
                        lambda msg: msg["from_id"] != -config.ID,
                        history
                    )
                )
            )
            add_history_to_db(history)
            # получение истории чата для обучения на лету позже
            answer = get_and_generate_message_from_db()
            print("мой ответ: ", answer)
            # полученный сгенерированный ответ бота
            vk.messages.send(
                peer_id=message['peer_id'],
                message=answer,
                random_id=randint(0, 2 ** 32)
            )



if __name__ == "__main__":
    main()
