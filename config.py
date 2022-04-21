from json import load
# загружать данные будет из жсон'а

from typing import Optional
# ещё немного типизации


class __Config:
    # класс скрыт ради отсутствия двойников экземпляров
    __token: Optional[str] = None
    __RESPONSE_CHANCE: Optional[float] = None
    __RESPONSE_DELAY: Optional[float] = None
    __ID: Optional[int] = None
    # резервироавние полей с учетом типизации

    def __init__(self) -> None:
        with open('./config.json', 'r', encoding='utf-8') as file:
            params: dict = load(file)
            # выгрузка конфига в жсоне

        if len(params) == 2:
            if 'token' not in params.keys() or 'ID' not in params.keys():
                raise TypeError("Token-key must be in params argument if params key is alone")
            self.__token = params['token']
            self.__ID = params['ID']
        
        elif len(params) == 4:
            if ('RESPONSE_CHANCE' not in params.keys() or
                'RESPONSE_DELAY' not in params.keys() or
                'token' not in params.keys() or
                'ID' not in params.keys()):
                raise TypeError("Incorrect keys at params agrument")
            self.__RESPONSE_CHANCE = params['RESPONSE_CHANCE']
            self.__RESPONSE_DELAY = params['RESPONSE_DELAY']
            self.__token = params['token']
            self.__ID = params['ID']

        # немного проверок на аргументы
        
        else:
            raise TypeError(f"Must be 2 or 4 keys in config.json, not {len(params.keys())}")
    
    # геттер токена
    @property
    def token(self) -> str:
        # всё как в классике ООП
        if self.__token is not None:
            return self.__token
        # с проверками на тип
        # достаточно типобезопасно
        raise TypeError("The token property is None")
    
    # и шанса ответа
    @property
    def RESPONSE_CHANCE(self) -> float:
        if self.__RESPONSE_CHANCE is not None:
            return self.__RESPONSE_CHANCE
        raise TypeError("The RESPONSE_CHANCE property is None")
    
    # и задержки
    @property
    def RESPONSE_DELAY(self) -> float:
        if self.__RESPONSE_DELAY is not None:
            return self.__RESPONSE_DELAY
        raise TypeError("The RESPONSE_DELAY property is None")
    
    # и ID
    @property
    def ID(self) -> int:
        if self.__ID is not None:
            return self.__ID
        raise TypeError("The ID property is None")


# инициализация единственного экземпляра
config = __Config()
