from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

products = {
    "Kinkou Balance": "https://www.marinehealth.asia/kk/products/kinkou-balance",
    "MH Collagen": "https://www.marinehealth.asia/kk/products/collagen",
    "Cardio Marine": "https://www.marinehealth.asia/kk/products/cardio-marine",
    "Indium kelp": "https://www.marinehealth.asia/kk/products/iodium-kelp",
    "Premium Squalene": "https://www.marinehealth.asia/kk/products/premium-squalene",
    "Artromarine": "https://www.marinehealth.asia/kk/products/artro-marine-msm",
    "Ashitaba": "https://www.marinehealth.asia/kk/products/ashitaba",
    "Spirulina-jar": "https://www.marinehealth.asia/kk/products/spirulina-jar",
    "Zostera": "https://www.marinehealth.asia/kk/products/zostera",
    "Vita Marine B": "https://www.marinehealth.asia/kk/products/vita-marine-b",
    "Vita Marine A": "https://www.marinehealth.asia/kk/products/vita-marine-a"
}

quiz_questions = [
    {"question": "1. Саған командада жұмыс істеген ұнай ма?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "2. Өз бизнесің болғанын қалайсың ба?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "3. Жаңа нәрселерді үйренуге дайынсың ба?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "4. Адамдармен сөйлескенде өзіңді сенімді сезінесің бе?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "5. Қиындықтардан қорықпайсың ба?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "6. Сетевойға көзқарасың қандай?", "options": ["Жақсы", "Жаман"], "scores": [1, 0]},
    {"question": "7. Қосымша табыс көзін іздеп жүрсің бе?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "8. Көшбасшы болуды қалайсың ба?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "9. Уақытыңды өзің басқарғың келе ме?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "10. Әлеуметтік желіде белсендісің бе?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "11. Қиындықтарға қарамастан әрекет етесің бе?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "12. Өміріңді өзгерткің келе ме?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "13. Адамдарға көмектескенді ұнатасың ба?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "14. Бос уақытыңда ақша тапқың келе ме?", "options": ["Иә", "Жоқ"], "scores": [1, 0]},
    {"question": "15. Табысты адамдармен бірге болғың келе ме?", "options": ["Иә", "Жоқ"], "scores": [1, 0]}
]

user_data = {}

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌿 Өнімдер туралы ақпарат", callback_data='products')],
        [InlineKeyboardButton("❓ Сетевой викторинасы", callback_data='quiz')],
        [InlineKeyboardButton("📲 Менеджермен байланысу", url='wa.me/77084828209')],
        [InlineKeyboardButton(" 🗣 Өнім отзывтары", url='https://t.me/OtzivMarineHealth')],
    ])

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Қош келдің, Marine Health ботына!\n\nМына бөлімдерден таңда:",
        reply_markup=main_menu_keyboard()
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id

    if query.data == 'products':
        buttons = [[InlineKeyboardButton(name, url=link)] for name, link in products.items()]
        buttons.append([InlineKeyboardButton("🔙 Артқа", callback_data='back_to_main')])
        query.edit_message_text("Өнімдер тізімі:", reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data == 'quiz':
        user_data[chat_id] = {'score': 0, 'q_index': 0}
        send_quiz_question(update, context)

    elif query.data.startswith('answer_'):
        index = int(query.data.split('_')[1])
        current_q = user_data[chat_id]['q_index']
        user_data[chat_id]['score'] += quiz_questions[current_q]['scores'][index]
        user_data[chat_id]['q_index'] += 1

        if user_data[chat_id]['q_index'] < len(quiz_questions):
            send_quiz_question(update, context)
        else:
            total = user_data[chat_id]['score']
            if total >= 12:
                result = "Сен керемет көшбасшысың! Сетевой бизнеске дайынсың! 💪"
            elif total >= 6:
                result = "Сенің әлеуетің бар! Барлығы үйренуге болады. ✨"
            else:
                result = "Сенің қызығушылығың төмен сияқты. Бірақ мүмкіндіктер шексіз! 🌱"
            query.edit_message_text(
                f"✅ Викторина аяқталды!\nСіздің ұпайыңыз: {total}/15\n\n{result}",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Басты бет", callback_data='back_to_main')]])
            )

    elif query.data == 'back_to_main':
        query.edit_message_text(
            "Қош келдің, Marine Health ботына!\n\nМына бөлімдерден таңда:",
            reply_markup=main_menu_keyboard()
        )

def send_quiz_question(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    q_index = user_data[chat_id]['q_index']
    question = quiz_questions[q_index]['question']
    options = quiz_questions[q_index]['options']
    buttons = [[InlineKeyboardButton(opt, callback_data=f"answer_{i}")] for i, opt in enumerate(options)]
    query.edit_message_text(question, reply_markup=InlineKeyboardMarkup(buttons))

def main():
    TOKEN = "7602120627:AAEkBULB7fVvBNF1QzoWjKqYBmFiADPAdfk"  # ← Өз токеніңізді осында қойыңыз
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
