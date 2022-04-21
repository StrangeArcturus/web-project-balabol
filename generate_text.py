import re
# регулярные выражения это лучшее, что изобрели программисты
# (и лисп)
from typing import List
# типизация подсказок
from random import choice

from markovify import NewlineText
# весь секрет успеха генерации


pattern = re.compile(r"\[id(\d*?)\|.*?]")
# паттерн регулярного выражения на id


def get_text_from_history(messages: List[str]) -> str:
    """
    Получает на вход список строк из фраз, разделённых переносом строки
    Составляет в итоге новую фразу на их основе
    :message: `List[str]`
    :return `str`
    """
    while any({
        "\n\n" in message for message in messages
        }):
        messages = list(map(
            lambda message: message.replace("\n\n", "\n"), messages
        ))
        # маппинг всех сообщений на пустые строки
    messages = list(filter(
        lambda message: not (re.fullmatch(r'(https?://[\w.-]+)', message)), messages
    ))
    # фильтрация сообщений, чтобы не допустить ссылок в них
    messages_as_string = '\n'.join(messages)
    user__IDs = tuple(set(
        pattern.findall(messages_as_string)
    ))
    for user__ID in user__IDs:
        messages_as_string = re.sub(rf"\[id{user__ID}\|.*?]", f"@id{user__ID}", messages_as_string)
        # замена всех id в простые id, 
        # которые мы обычно пишем при упоминании

    for state in range(1, 100):
        # пока не добьёмся результата -- всё одно и то же
        text_model = NewlineText(input_text=messages_as_string, well_formed=False, state_size=state)
        sentence = text_model.make_sentence(tries=1000)
        if sentence:
            # если результат -- не None
            return sentence
    # спасение рандомизации в обртном случае
    return choice(messages_as_string.split('\n'))