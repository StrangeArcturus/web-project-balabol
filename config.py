from json import load

from typing import Optional


class __Config:
    token: Optional[str] = None
    RESPONSE_CHANCE: Optional[float] = None
    RESPONSE_DELAY: Optional[float] = None
    ID: Optional[int] = None

    def __init__(self) -> None:
        with open('./config.json', 'r', encoding='utf-8') as file:
            params: dict = load(file)

        if len(params) == 2:
            if 'token' not in params.keys() or 'ID' not in params.keys():
                raise TypeError("Token-key must be in params argument if params key is alone")
            self.token = params['token']
            self.ID = params['ID']
        
        elif len(params) == 4:
            if ('RESPONSE_CHANCE' not in params.keys() or
                'RESPONSE_DELAY' not in params.keys() or
                'token' not in params.keys() or
                'ID' not in params.keys()):
                raise TypeError("Incorrect keys at params agrument")
            self.RESPONSE_CHANCE = params['RESPONSE_CHANCE']
            self.RESPONSE_DELAY = params['RESPONSE_DELAY']
            self.token = params['token']
            self.ID = params['ID']
        
        else:
            raise TypeError(f"Must be 2 or 4 keys in config.json, not {len(params.keys())}")


config = __Config()
