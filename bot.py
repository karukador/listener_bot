import math
import telebot
import logging
from database import create_table, insert_row, count_all_blocks
from speechkit import speech_to_text
from telebot.types import BotCommand, BotCommandScope, ReplyKeyboardMarkup
from system_config import ADMIN_ID, CONTENT_TYPES, MAX_USER_STT_BLOCKS
from config import TOKEN

bot = telebot.TeleBot(token=TOKEN)

# при вынесении текста в отдельный файлик, что-то произошло с кодировкой, пусть текст здесь полежит
help_message = ('Так как я использую платные ресурсы для взаимодействия с '
                'нейросетью, то у вас ограниченное количество аудиоблоков '
                'для прослушивания.\n\n'
                '<b>Что такое SpeechKit?</b>\n'
                '<b>SpeechKit</b> - это набор инструментов для работы с '
                'естественным языком, разработанный компанией Яндекс. Он '
                'включает в себя распознавание речи, синтез речи, а также '
                'API для управления устройствами через голосовые команды.\n\n'
                'Информацию о том, сколько ресурсов вы уже потратили, вы сможете '
                'найти, нажав на кнопку <b>"Статистика"</b>.\n'
                '<b>"Озвучить"</b> - начните озвучивать текст.')

manual_message = "Отправляйте аудио. Говорите внятно и чётко для лучшего распознания."


# Команда /debug с доступом только для админов
@bot.message_handler(commands=["debug"])
def send_logs(message):
    user_id = message.chat.id

    if user_id == ADMIN_ID:
        try:

            with open("log_file.txt", "rb") as f:
                bot.send_document(message.chat.id, f)
                logging.info("логи отправлены")
        except telebot.apihelper.ApiTelegramException:

            bot.send_message(message.chat.id, "Логов пока нет.")

    else:
        bot.send_message(message.chat.id, "У Вас недостаточно прав для использования этой команды.")
        logging.info(f"{user_id} пытался получить доступ к логам, не являясь админом")


# клавиатура
main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("🗣️ Прослушать")


def register_comands(message):
    commands = [  # Установка списка команд с областью видимости и описанием
        BotCommand('start', 'запуск бота'),
        BotCommand('help', 'основная информация о боте'),
        BotCommand('stt', 'прослушать текст')]
    bot.set_my_commands(commands)
    BotCommandScope('private', chat_id=message.chat.id)


# Команда /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    logging.info("Отправка приветственного сообщения")
    bot.reply_to(
        message,
        'Привет! Я бот прослушивания текста с помощью SpeechKit. Нажми на кнопку "🗣️ Прослушать" и запишите аудио '
        'для прослушивания.',
        reply_markup=main_menu_keyboard)
    register_comands(message)


# команда /help
@bot.message_handler(commands=["help"])
def about_bot(message):
    bot.send_message(message.chat.id, help_message,
                     reply_markup=main_menu_keyboard, parse_mode="html")


@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "🗣️ прослушать")
# функция, направляющая аудио от speechkit
# Обрабатываем команду /stt
@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь голосовое сообщение, чтобы я его распознал!')
    bot.register_next_step_handler(message, stt)


# Переводим голосовое сообщение в текст после команды stt
def stt(message):
    user_id = message.from_user.id

    # Проверка, что сообщение действительно голосовое
    if not message.voice:
        bot.send_message(user_id, "Отправьте голосовое сообщение.")
        return

    # Считаем аудиоблоки и проверяем сумму потраченных аудиоблоков
    stt_blocks = is_stt_block_limit(message, message.voice.duration)
    if not stt_blocks:
        return

    file_id = message.voice.file_id  # получаем id голосового сообщения
    file_info = bot.get_file(file_id)  # получаем информацию о голосовом сообщении
    file = bot.download_file(file_info.file_path)  # скачиваем голосовое сообщение

    status, text = speech_to_text(file)
    if status:
        logging.info(f"Распознанный текст: {user_id}: {text}")
        bot.send_message(user_id, text, reply_to_message_id=message.id)

    else:
        logging.debug("Ошибка при распознавании речи: ", text)
    if status:
        # Записываем сообщение и кол-во аудиоблоков в БД
        insert_row(user_id, text, 'stt_blocks', stt_blocks)


def is_stt_block_limit(message, duration):
    user_id = message.from_user.id

    # Переводим секунды в аудиоблоки
    audio_blocks = math.ceil(duration / 15)  # округляем в большую сторону
    # Функция из БД для подсчёта всех потраченных пользователем аудиоблоков
    all_blocks = int(count_all_blocks(user_id) or 0) + int(audio_blocks)

    # Проверяем, что аудио длится меньше 30 секунд
    if duration >= 30:
        msg = "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"
        bot.send_message(user_id, msg)
        return None

    # Сравниваем all_blocks с количеством доступных пользователю аудиоблоков
    if all_blocks >= MAX_USER_STT_BLOCKS:
        msg = (f"Превышен общий лимит SpeechKit STT {MAX_USER_STT_BLOCKS}. Использовано {all_blocks} блоков. Доступно: "
               f"{MAX_USER_STT_BLOCKS - all_blocks}")
        bot.send_message(user_id, msg)
        return None

    return audio_blocks


@bot.message_handler(content_types=CONTENT_TYPES)
def any_msg(message):
    bot.send_message(message.chat.id, 'Если хотите озвучить текст, то сначала нажмите на кнопку "🗣️ Прослушать"',
                     reply_markup=main_menu_keyboard)


if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H",
        filename="log_file.log",
        filemode="w",
        force=True)
    create_table()  # Создание таблицы в БД
    bot.infinity_polling()  # запуск бота 🎉
    logging.info("Бот запущен")
