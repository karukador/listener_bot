URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?"
LANGUAGE = "ru-RU"  # распознаём голосовое сообщение на русском языке
model_version = "general"  # используем основную версию модели

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice"]
ADMIN_ID: int = 1234  # сюда введите ваш telegram_id
MAX_USER_STT_BLOCKS = 12  # выделяем на каждого пользователя по 12 аудиоблоков

DB_NAME = "speech_kit.db"
