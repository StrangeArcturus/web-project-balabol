import re
from typing import List
from random import choice

from markovify import NewlineText


pattern = re.compile(r"\[id(\d*?)\|.*?]")


def get_text_from_history(messages: List[str]) -> str:
    """
    Получает на вход список строк из фраз, разделённых переносом строки
    Составляет в итоге новую фразу на их основе
    """
    while any({"\n\n" in message for message in messages}):
        messages = list(map(
            lambda message: message.replace("\n\n", "\n"), messages
        ))
    messages = list(filter(
        lambda message: not (re.fullmatch(r'(https?://[\w.-]+)', message)), messages
    ))
    messages_as_string = '\n'.join(messages)
    user_ids = tuple(set(pattern.findall(messages_as_string)))
    for user_id in user_ids:
        messages_as_string = re.sub(rf"\[id{user_id}\|.*?]", f"@id{user_id}", messages_as_string)

    for state in range(1, 100):
        text_model = NewlineText(input_text=messages_as_string, well_formed=False, state_size=state)
        sentence = text_model.make_sentence(tries=1000)
        if sentence:
            return sentence
    return choice(messages_as_string.split('\n'))