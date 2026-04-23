import telebot
from telebot import types
import os, json, random
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

DATA_FILE="data.json"

# ----------------------
# Data
# ----------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE,"r") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE,"w") as f:
        json.dump(d,f)

data=load_data()

def get_user(uid):
    uid=str(uid)
    if uid not in data:
        data[uid]={
            "start_date":str(datetime.now().date()),
            "relapses":0
        }
        save_data(data)
    return data[uid]

def clean_days(start):
    s=datetime.strptime(start,"%Y-%m-%d")
    return (datetime.now()-s).days

# ----------------------
# Tips
# ----------------------
tips = [
"غير مكانك فورًا عند الشعور بالخطر",
"لا تبق وحدك طويلًا",
"الهاتف في السرير خطر",
"الخروج يكسر الرغبة",
"الانتكاس لا يلغي التقدم",
"ابدأ دقيقة واحدة فقط عند الكسل",
"اشغل الفراغ قبل أن يشغلك",
"التعب الجسدي يقلل الشهوة",
"راقب المحفزات لا النتائج فقط",
"التعافي بناء حياة لا مجرد منع"
]

books = [
"📘 Atomic Habits",
"📗 Deep Work",
"📙 The Power of Habit"
]

articles = [
"https://fightthenewdrug.org/",
"https://www.yourbrainonporn.com/"
]

# ----------------------
# Main Menu
# ----------------------
def main_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📅 خطتي","📊 تقدمي")
    kb.row("🚨 دعم فوري","🔥 التحديات")
    kb.row("🏅 الأوسمة","💡 نصائح")
    kb.row("❌ سجل انتكاسة")
    return kb

# ----------------------
# Start
# ----------------------
@bot.message_handler(commands=['start'])
def start(message):
    get_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        "مرحبا بك في نقاء 🌱",
        reply_markup=main_menu()
    )

# ----------------------
# Plan Menu
# ----------------------
def plan_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🤖 أنشئ لي جدول")
    kb.row("📝 أعمل جدولي بنفسي")
    kb.row("📄 تحميل قالب PDF")
    kb.row("⬅ رجوع")
    return kb

# ----------------------
# Progress Menu
# ----------------------
def progress_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🔄 إعادة العداد")
    kb.row("⬅ رجوع")
    return kb

# ----------------------
# Tips Menu
# ----------------------
def tips_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📚 كتب مقترحة")
    kb.row("🌐 مقالات تعافي")
    kb.row("🎯 أعطني نصائح")
    kb.row("⬅ رجوع")
    return kb

# ----------------------
# Generate sample schedule
# ----------------------
def sample_schedule():
    return """
📅 جدول مقترح

06:30 صلاة وبداية اليوم
08:00 دراسة/عمل
13:00 خروج أو حركة
17:00 تعلم مهارة
21:00 بدون هاتف
22:30 نوم

⚠ وقت الخطر:
غيّر المكان فورًا
"""

# ----------------------
# Challenge ladder
# ----------------------
def challenge_ladder(user):
    days=clean_days(user["start_date"])
    rel=user["relapses"]

    txt="🪜 سلم التقدم:\n\n"

    for i in range(1,15):
        if i<=days:
            txt+="🟩 "
        else:
            txt+="⬜ "

    txt+=f"\n\n❌ الانتكاسات: {rel} (تمثل بالأحمر)"
    return txt

# ----------------------
# Medals
# ----------------------
def medal(days):
    if days>=42:
        return "🥇 وسام ذهبي"
    elif days>=28:
        return "🥈 وسام فضي"
    elif days>=14:
        return "🥉 وسام برونزي"
    else:
        return "ابدأ نحو أول وسام"

# ----------------------
# Messages
# ----------------------
@bot.message_handler(func=lambda m: True)
def handle(m):

    user=get_user(m.chat.id)
    text=m.text

    if text=="📅 خطتي":
        bot.send_message(
            m.chat.id,
            "اختر طريقة التخطيط:",
            reply_markup=plan_menu()
        )

    elif text=="🤖 أنشئ لي جدول":
        bot.send_message(
            m.chat.id,
            sample_schedule()
        )

    elif text=="📝 أعمل جدولي بنفسي":
        bot.send_message(
            m.chat.id,
"""قالب تعبئة سريع:

الهدف اليوم:
_____

أوقات الخطر:
_____

بدائل صحية:
_____"""
        )

    elif text=="📄 تحميل قالب PDF":
        try:
            with open("weekly_plan.pdf","rb") as f:
                bot.send_document(
                    m.chat.id,
                    f,
                    caption="📄 قالب نقاء الأسبوعي"
                )
        except:
            bot.send_message(
                m.chat.id,
                "ضع ملف weekly_plan.pdf داخل المشروع."
            )

    elif text=="📊 تقدمي":
        days=clean_days(user["start_date"])

        msg=f"""
📊 تقدمك

عدد الأيام: {days}
عدد الانتكاسات: {user["relapses"]}
"""
        bot.send_message(
            m.chat.id,
            msg,
            reply_markup=progress_menu()
        )

    elif text=="🔄 إعادة العداد":
        user["start_date"]=str(datetime.now().date())
        save_data(data)
        bot.send_message(
            m.chat.id,
            "تم تصفير العداد."
        )

    elif text=="🚨 دعم فوري":
        emergency="""
🚨 افعل الآن:

1- انهض فورًا
2- غيّر مكانك
3- اغسل وجهك
4- لا تبق وحدك
5- اخرج 5 دقائق

هذه الرغبة مؤقتة.
"""
        bot.send_message(m.chat.id,emergency)

    elif text=="🔥 التحديات":
        bot.send_message(
            m.chat.id,
            challenge_ladder(user)
        )

    elif text=="🏅 الأوسمة":
        days=clean_days(user["start_date"])
        bot.send_message(
            m.chat.id,
            medal(days)
        )

    elif text=="💡 نصائح":
        bot.send_message(
            m.chat.id,
            "اختر:",
            reply_markup=tips_menu()
        )

    elif text=="🎯 أعطني نصائح":
        selected=random.sample(tips,3)
        bot.send_message(
            m.chat.id,
            "\n\n".join(selected)
        )

    elif text=="📚 كتب مقترحة":
        bot.send_message(
            m.chat.id,
            "\n".join(books)
        )

    elif text=="🌐 مقالات تعافي":
        bot.send_message(
            m.chat.id,
            "\n".join(articles)
        )

    elif text=="❌ سجل انتكاسة":
        user["start_date"]=str(datetime.now().date())
        user["relapses"]+=1
        save_data(data)
        bot.send_message(
            m.chat.id,
            "تم تسجيل الانتكاسة. واصل من جديد 💪"
        )

    elif text=="⬅ رجوع":
        bot.send_message(
            m.chat.id,
            "القائمة الرئيسية",
            reply_markup=main_menu()
        )

print("Bot running...")
bot.infinity_polling()
