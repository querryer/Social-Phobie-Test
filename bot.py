import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# База вопросов и правильных ответов
questions = [
    {
        "question": "Как вы себя чувствуете в больших толпах людей?",
        "options": [
            ("Спокойно", "0"),
            ("Немного нервничаю", "1"),
            ("Испытываю сильный дискомфорт", "2"),
        ],
    },
    {
        "question": "Легко ли вы сначала общаетесь с новыми людьми?",
        "options": [
            ("Да, очень", "0"),
            ("Не всегда", "1"),
            ("Практически нет", "2"),
        ],
    },
    {
        "question": "Как реагируете на критику окружающих?",
        "options": [
            ("Игнорирую", "0"),
            ("Необходимо обдумать", "1"),
            ("Сильно переживаю", "2"),
        ],
    },
    {
        "question": "Сильно ли вы переживаете, когда нужно выступать на публике?",
        "options": [
            ("Нет, это легко", "0"),
            ("Немного волнуюсь", "1"),
            ("Это ужасно!", "2"),
        ],
    },
    {
        "question": "Как часто вы избегаете общения?",
        "options": [
            ("Никогда", "0"),
            ("Иногда", "1"),
            ("Часто", "2"),
        ],
    },
]

user_scores = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Привет! Нажми /test, чтобы пройти тест на социофобию.")

@bot.message_handler(commands=['test'])
def start_test(message):
    user_scores[message.chat.id] = 0
    ask_question(message.chat.id, 0)

def ask_question(chat_id, question_index):
    if question_index < len(questions):
        kb = types.InlineKeyboardMarkup()
        for option_text, value in questions[question_index]["options"]:
            kb.add(types.InlineKeyboardButton(option_text, callback_data=f"{question_index}:{value}"))
        bot.send_message(chat_id, questions[question_index]["question"], reply_markup=kb)
    else:
        show_scores(chat_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    question_index, value = map(int, call.data.split(':'))
    user_scores[call.message.chat.id] += value
    bot.answer_callback_query(call.id)
    ask_question(call.message.chat.id, question_index + 1)

def show_scores(chat_id):
    score = user_scores[chat_id]
    bot.send_message(chat_id, f"Ваши очки: {score}/10")
    if score <= 5:
        bot.send_message(chat_id, "Вы успешно прошли тест! По результам выянилось что вы не Социофоб! Вам легко общаться с незнакомыми людьми и также начинать разговор!.")
    elif score <= 8:
        bot.send_message(chat_id, "По результатам теста мы узнали что у вас есть склонность к социофобии! Советуем больше развиваться в обществе!.")
    else:
        bot.send_message(chat_id, "Вы заядлый социофоб :( ! Вам Следует больше общаться с людьми и развивать в себе умение контактировать с людьми!.")

# Запуск бота
bot.polling()
