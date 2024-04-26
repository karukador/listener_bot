import requests
from system_config import URL, LANGUAGE, model_version
from config import FOLDER_ID, IAM_TOKEN
import logging

import requests


def speech_to_text(data):
    # Указываем параметры запроса
    params = "&".join([
        f"topic={model_version}",
        f"folderId={FOLDER_ID}",
        f"lang={LANGUAGE}"
    ])

    # Аутентификация через IAM-токен
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
    }

    # Выполняем запрос
    response = requests.post(URL + params, headers=headers, data=data)

    # Читаем json в словарь
    decoded_data = response.json()
    # Проверяем, не произошла ли ошибка при запросе
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")  # Возвращаем статус и текст из аудио
    else:
        return False, logging.debug("При запросе в SpeechKit возникла ошибка")
