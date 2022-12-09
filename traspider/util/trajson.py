import json


class TraJson(json):
    def __init__(self):
        self.__json = json

    def get(self, key, value):
        return self.__json.get(key, value)


