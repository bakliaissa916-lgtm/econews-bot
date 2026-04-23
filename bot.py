import telebot
from telebot import types
import os, json, random
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

DATA_FILE="data.json"

# =========================
# Storage
# =========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(d,f)

data=load_data()

def user(uid):
    uid=str(uid)
    if uid not in data:
        data[uid]={
            "start_date":str(datetime.now().date()),
            "relapses":0
        }
        save_data(data)
    return data[uid]

def days_clean(start):
    s=datetime.strptime(start,"%Y-%m-%d")
    return (datetime.now()-s).days


# =========================
# Content
# =========================

tips=[
"غير مكانك فورًا عند الشعور بالخطر.",
"لا تبق وحدك وقت طويل.",
"اشغل الفراغ قبل أن يشغلك.",
"ابدأ بخطوة صغيرة لا بالكمال.",
"الانتكاس لا يلغي تقدمك.",
"تعب الجسد يخفف الاندفاع.",
"غيّر البيئة عند المحفز.",
"الهاتف في السرير خطر.",
"التعافي بناء حياة لا مقاومة فقط.",
"تذكر لماذا بدأت."
]

books=[
"Atomic Habits",
"The Power of Habit",
"Deep Work",
"Can't Hurt Me",
"The Slight Edge",
"Essentialism",
"The One Thing",
"Your Brain On Porn"
]

podcasts=[
"Huberman Lab",
"The Diary Of A CEO",
"بودكاست تطوير ذات عربي"
]

articles=[
"FightTheNewDrug.org",
"YourBrainOnPorn.com",
"IslamWeb.net",
"مشروع واعي"
]

stories=[
"قصة: شخص بدأ بتحسين يومه بدل محاربة الانتكاس فقط فنجح تدريجيًا.",
"قصة: التعافي بدأ عند أحدهم حين ملأ الفراغ لا حين ركز على المنع فقط."
]


# =========================
# Menus
# =========================

def main_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📅 خطتي","📊 تقدمي")
    kb.row("🏆 الإنجازات","🔥 التحديات")
    kb.row("🆘 أنا في خطر","💡 موارد التعافي")
    kb.row("📖 قصص متعافين","❌ سجل انتكاسة")
    return kb

def plan_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🤖 أنشئ لي جدول")
    kb.row("📝 أعمل جدولي بنفسي")
    kb.row("📄 دفتر نقاء PDF")
    kb.row("⬅ رجوع")
    return kb

def resources_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🎯 نصائح")
    kb.row("📚 كتب")
    kb.row("🎧 بودكاست")
    kb.row("🌐 مواقع ومقالات")
    kb.row("⬅ رجوع")
    return kb

def progress_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🔄 إعادة العداد")
    kb.row("⬅ رجوع")
    return kb


# =========================
# Features
# =========================

def schedule():
    return """
📅 جدول اليوم

06:30 صلاة وبداية قوية
08:00 دراسة / عمل
13:00 خروج أو حركة
17:00 تعلم مهارة
21:00 بدون هاتف
22:30 نوم

⚠ وقت الخطر:
غيّر مكانك فورًا
"""

def challenge_ladder(u):
    d=days_clean(u["start_date"])
    txt="🪜 سلم التعافي:\n\n"
    for i in range(1,15):
        if i<=d:
            txt+="🟩 "
        else:
            txt+="⬜ "
    txt+=f"\n\nعدد الانتكاسات: {u['relapses']}"
    return txt

def achievements(d):
    unlocked=[]

    if d>=3:
        unlocked.append("✅ إنجاز البداية")
    if d>=7:
        unlocked.append("✅ إنجاز الانضباط")
    if d>=14:
        unlocked.append("🥉 برونزي")
    if d>=28:
        unlocked.append("🥈 فضي")
    if d>=42:
        unlocked.append("🥇 ذهبي")
    if d>=90:
        unlocked.append("💎 ماسي")

    behavioral=[
    "📵 بدون هاتف ليلًا (سلوكي)",
    "🌅 مقاومة محفز الفجر",
    "📚 جلسات تركيز",
    "🔥 تحديات مكتملة"
    ]

    if not unlocked:
        unlocked=["ابدأ نحو أول إنجاز"]

    msg="🏆 الإنجازات المفتوحة:\n\n"
    msg+="\n".join(unlocked)

    msg+="\n\n🎯 إنجازات سلوكية قادمة:\n"
    msg+="\n".join(behavioral)

    return msg


# =========================
# START
# =========================
@bot.message_handler(commands=['start'])
def start(m):
    user(m.chat.id)
    bot.send_message(
        m.chat.id,
        "🌱 مرحبًا بك في نقاء",
        reply_markup=main_menu()
    )


# =========================
# Messages
# =========================
@bot.message_handler(func=lambda m:True)
def handle(m):

    u=user(m.chat.id)
    text=m.text

    if text=="📅 خطتي":
        bot.send_message(
            m.chat.id,
            "اختر:",
            reply_markup=plan_menu()
        )

    elif text=="🤖 أنشئ لي جدول":
        bot.send_message(m.chat.id,schedule())

    elif text=="📝 أعمل جدولي بنفسي":
        bot.send_message(
            m.chat.id,
"""قالب سريع:

هدف اليوم:
____

وقت الخطر:
____

بديل صحي:
____
"""
        )

    elif text=="📄 دفتر نقاء PDF":
        try:
            with open("weekly_plan.pdf","rb") as f:
                bot.send_document(
                    m.chat.id,
                    f,
                    caption="دفتر نقاء الأسبوعي"
                )
        except:
            bot.send_message(
                m.chat.id,
                "ضع ملف weekly_plan.pdf داخل المشروع."
            )

    elif text=="📊 تقدمي":
        d=days_clean(u["start_date"])
        msg=f"""
📊 تقدمك

الأيام النظيفة: {d}
عدد الانتكاسات: {u["relapses"]}
"""
        bot.send_message(
            m.chat.id,
            msg,
            reply_markup=progress_menu()
        )

    elif text=="🔄 إعادة العداد":
        u["start_date"]=str(datetime.now().date())
        save_data(data)
        bot.send_message(
            m.chat.id,
            "تم تصفير العداد."
        )

    elif text=="🏆 الإنجازات":
        d=days_clean(u["start_date"])
        bot.send_message(
            m.chat.id,
            achievements(d)
        )

    elif text=="🔥 التحديات":
        bot.send_message(
            m.chat.id,
            challenge_ladder(u)
        )

    elif text=="🆘 أنا في خطر":
        emergency="""
🚨 افعل الآن:

1- انهض فورًا
2- غيّر الغرفة
3- اخرج 5 دقائق
4- اغلق الهاتف
5- تنفس ببطء

الرغبة موجة وستمر.
"""
        bot.send_message(
            m.chat.id,
            emergency
        )

    elif text=="💡 موارد التعافي":
        bot.send_message(
            m.chat.id,
            "اختر موردا:",
            reply_markup=resources_menu()
        )

    elif text=="🎯 نصائح":
        bot.send_message(
            m.chat.id,
            "\n\n".join(random.sample(tips,3))
        )

    elif text=="📚 كتب":
        bot.send_message(
            m.chat.id,
            "📚 كتب مقترحة:\n\n"+
            "\n".join(books)
        )

    elif text=="🎧 بودكاست":
        bot.send_message(
            m.chat.id,
            "🎧 اقتراحات:\n\n"+
            "\n".join(podcasts)
        )

    elif text=="🌐 مواقع ومقالات":
        bot.send_message(
            m.chat.id,
            "🌐 موارد:\n\n"+
            "\n".join(articles)
        )

    elif text=="📖 قصص متعافين":
        bot.send_message(
            m.chat.id,
            random.choice(stories)
        )

    elif text=="❌ سجل انتكاسة":
        u["start_date"]=str(datetime.now().date())
        u["relapses"]+=1
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

print("Running...")
bot.infinity_polling()        
