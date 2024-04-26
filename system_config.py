URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?"
LANGUAGE = "ru-RU" # ��������� ��������� ��������� �� ������� �����
model_version = "general" # ���������� �������� ������ ������

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice"]
ADMIN_ID: int = 1234 # ���� ������� ��� telegram_id
MAX_USER_STT_BLOCKS = 12  # �������� �� ������� ������������ �� 12 �����������

DB_NAME = "speech_kit.db"
