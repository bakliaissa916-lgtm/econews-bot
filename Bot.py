import telebot
import json
import os
import random
from datetime import datetime
import threading
import time

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"

# تحميل البيانات
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# حفظ
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# مستخدم
def get_user(user_id):
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "start_date": str(datetime.now().date()),
            "relapses": 0
        }
        save_data(data)
    return data[user_id]

# الأيام
def get_days(start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    return (datetime.now() - start).days

# نصائح
tips = [
"💡 لا تبق وحدك",
"💡 الهاتف في السرير خطر",
"💡 غير مكانك فورًا",
"💡 كل مقاومة تقويك",
"💡 الانتكاس ليس النهاية",
"💡 اخرج وتمشى",
"💡 اشغل نفسك بشيء مفيد"
]

# القائمة
def menu():
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📅 الخطة اليومية", "🔥 التحديات")
    kb.add("📊 تقدمي", "🏆 الترتيب")
    kb.add("🚨 دعم فوري", "💡 نصيحة")
    kb.add("❌ سجل انتكاسة")
    return kb

@bot.message_handler(commands=['start'])
def start(message):
    get_user(message.chat.id)
    bot.send_message(message.chat.id, "👋 مرحبًا بك", reply_markup=menu())

@bot.message_handler(func=lambda m: True)
def handle(message):
    user = get_user(message.chat.id)

    if message.text == "📅 الخطة اليومية":
        bot.send_message(message.chat.id,
        """📅 خطة اليوم:

🚶‍♂️ نشاط
📚 دراسة
🕌 صلاة
📵 لا هاتف في السرير

🔥 لا انتكاس اليوم""")

    elif message.text == "🔥 التحديات":
        tip = random.choice(tips)
        bot.send_message(message.chat.id, f"🔥 تحدي:\n✔ لا عزلة\n✔ خروج\n\n{tip}")

    elif message.text == "📊 تقدمي":
        days = get_days(user["start_date"])
        relapses = user["relapses"]

        badge = "😅 مبتدئ"
        if days >= 3: badge = "💪 جيد"
        if days >= 7: badge = "🔥 أسبوع"
        if days >= 30: badge = "🏆 بطل"

        bot.send_message(message.chat.id,
        f"📊 الأيام: {days}\n❌ الانتكاسات: {relapses}\n🏅 {badge}")

    elif message.text == "❌ سجل انتكاسة":
        user["start_date"] = str(datetime.now().date())
        user["relapses"] += 1
        save_data(data)
        bot.send_message(message.chat.id, "❌ تم التسجيل… ابدأ من جديد")

    elif message.text == "🚨 دعم فوري":
        bot.send_message(message.chat.id,
        "🚨 غيّر مكانك فورًا\nلا تبق وحدك\nتنفس")

    elif message.text == "💡 نصيحة":
        bot.send_message(message.chat.id, random.choice(tips))

    elif message.text == "🏆 الترتيب":
        leaderboard = []
        for uid, u in data.items():
            days = get_days(u["start_date"])
            leaderboard.append((uid, days))

        leaderboard.sort(key=lambda x: x[1], reverse=True)

        msg = "🏆 أفضل المستخدمين:\n\n"
        for i, (uid, d) in enumerate(leaderboard[:5], 1):
            msg += f"{i}. {d} يوم\n"

        bot.send_message(message.chat.id, msg)

# ⏰ تذكير يومي
def reminder():
    while True:
        for uid in data:
            try:
                bot.send_message(uid, "⏰ تذكير: لا تستسلم اليوم 💪")
            except:
                pass
        time.sleep(86400)  # كل 24 ساعة

threading.Thread(target=reminder).start()

print("Bot running...")
bot.polling()
