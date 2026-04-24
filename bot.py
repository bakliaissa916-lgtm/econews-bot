import telebot
from telebot import types
import os, json, random
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

DATA_FILE="data.json"

# --------------------------------
# DATA
# --------------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f)

data=load_data()

def get_user(uid):
    uid=str(uid)
    if uid not in data:
        data[uid]={
            "start_date":str(datetime.now().date()),
            "best_streak":0,
            "relapses":0,
            "triggers":[]
        }
        save_data()
    return data[uid]

def streak_days(start):
    s=datetime.strptime(start,"%Y-%m-%d")
    return (datetime.now()-s).days

# ----------------------------
# CONTENT
# ----------------------------
tips=[
"غير المكان فورًا عند الخطر",
"الفراغ أخطر من الرغبة",
"ابدأ بخطوة صغيرة",
"لا تبق وحدك",
"الهاتف في السرير خطر",
"التعافي بناء حياة"
]

books=[
"Atomic Habits",
"Deep Work",
"The Power of Habit",
"Can't Hurt Me",
"Your Brain On Porn"
]

podcasts=[
"Huberman Lab",
"Diary of a CEO",
"بودكاست تطوير ذات عربي"
]

articles=[
"FightTheNewDrug.org",
"YourBrainOnPorn.com",
"IslamWeb.net",
"مشروع واعي"
]

stories = [
"""📖 قصة 1
بدأت المشكلة مع الفراغ.
كل محاولة كانت منعًا فقط.
التحول بدأ حين تغيّر أسلوب الحياة:
رياضة
انشغال
تقليل عزلة
وبعد انتكاسات كثيرة وصل 90 يوم.
الدرس:
التعافي ليس مقاومة فقط… بناء حياة.""",

"""📖 قصة 2
كان يسقط بعد الفجر دائمًا.
بدل التركيز على السقوط،
غيّر الروتين:
لا رجوع للنوم
مشي بعد الصلاة
خطة للصباح
وبدأت السلسلة تستقر."""
]

danger_actions={
"🛏 في السرير":[
"قم الآن فورًا.",
"ضع الهاتف بعيدًا.",
"اذهب اغسل وجهك."
],
"🏠 وحدي":[
"اخرج 10 دقائق.",
"اتصل بأحد.",
"ابدأ نشاطًا جسديًا."
],
"📱 أتصفح الهاتف":[
"أغلق الهاتف 15 دقيقة.",
"ضعه خارج الغرفة.",
"ابدأ قراءة صفحة كتاب."
]
}

# ----------------------------
# MENUS
# ----------------------------
def main_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📅 خطتي","📊 إحصائياتي")
    kb.row("🏆 الإنجازات","🪜 الترتيب")
    kb.row("🧠 محفزاتي","🆘 أنا في خطر")
    kb.row("💡 موارد التعافي","📖 قصص التعافي")
    kb.row("❌ سجل انتكاسة")
    return kb

def resources_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🎯 نصائح","📚 كتب")
    kb.row("🎧 بودكاست","🌐 مواقع")
    kb.row("⬅ رجوع")
    return kb

def plan_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🤖 أنشئ لي جدول")
    kb.row("📄 دفتر نقاء PDF")
    kb.row("⬅ رجوع")
    return kb

def danger_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🛏 في السرير")
    kb.row("🏠 وحدي")
    kb.row("📱 أتصفح الهاتف")
    kb.row("⬅ رجوع")
    return kb

def trigger_menu():
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("الوحدة","الهاتف")
    kb.row("بعد الفجر","محتوى بصري")
    kb.row("⬅ رجوع")
    return kb

# ----------------------------
# HELPERS
# ----------------------------
def schedule():
    return """
📅 خطة اليوم

06:30 بداية قوية
08:00 دراسة/عمل
13:00 حركة
17:00 تعلم
21:00 بدون هاتف

⚠ وقت الخطر:
غير المكان فورًا
"""

def achievements(days):
    levels=[
(3,"✅ بداية"),
(7,"💪 انضباط"),
(14,"🥉 برونزي"),
(28,"🥈 فضي"),
(42,"🥇 ذهبي"),
(90,"💎 ماسي")
]
    msg="🏆 الإنجازات:\n\n"
    for need,name in levels:
        if days>=need:
            msg+=f"{name} مفتوح\n"
        else:
            remain=need-days
            msg+=f"{name} مقفل (باقي {remain} يوم)\n"
    return msg

def leaderboard(uid):
    board=[]
    for k,v in data.items():
        d=streak_days(v["start_date"])
        board.append((k,d))
    board.sort(key=lambda x:x[1], reverse=True)

    txt="🪜 الترتيب:\n\n"
    rank=1
    mine=None
    for k,d in board[:5]:
        txt+=f"{rank}- {d} يوم\n"
        if k==str(uid):
            mine=rank
        rank+=1
    if mine:
        txt+=f"\nرتبتك: #{mine}"
    return txt

# ----------------------------
# START
# ----------------------------
@bot.message_handler(commands=['start'])
def start(m):
    get_user(m.chat.id)
    bot.send_message(
        m.chat.id,
        "🌱 مرحبًا بك في نقاء",
        reply_markup=main_menu()
    )

# ----------------------------
# MAIN HANDLER
# ----------------------------
@bot.message_handler(func=lambda m:True)
def handle(m):
    u=get_user(m.chat.id)
    text=m.text

    # خطتي
    if text=="📅 خطتي":
        bot.send_message(
            m.chat.id,
            "اختر:",
            reply_markup=plan_menu()
        )

    elif text=="🤖 أنشئ لي جدول":
        bot.send_message(
            m.chat.id,
            schedule()
        )

    elif text=="📄 دفتر نقاء PDF":
        try:
            with open("weekly_plan.pdf","rb") as f:
                bot.send_document(m.chat.id,f)
        except:
            bot.send_message(
                m.chat.id,
                "أضف ملف weekly_plan.pdf"
            )

    # احصائياتي
    elif text=="📊 إحصائياتي":
        current=streak_days(u["start_date"])
        if current>u["best_streak"]:
            u["best_streak"]=current
            save_data()

        msg=f"""
📊 إحصائياتك

السلسلة الحالية: {current}
أفضل سلسلة: {u['best_streak']}
عدد الانتكاسات: {u['relapses']}
"""
        bot.send_message(m.chat.id,msg)

    # الإنجازات
    elif text=="🏆 الإنجازات":
        d=streak_days(u["start_date"])
        bot.send_message(
            m.chat.id,
            achievements(d)
        )

    # الترتيب
    elif text=="🪜 الترتيب":
        bot.send_message(
            m.chat.id,
            leaderboard(m.chat.id)
        )

    # محفزاتي
    elif text=="🧠 محفزاتي":
        bot.send_message(
            m.chat.id,
            "اختر محفزًا لديك:",
            reply_markup=trigger_menu()
        )

    elif text in ["الوحدة","الهاتف","بعد الفجر","محتوى بصري"]:
        if text not in u["triggers"]:
            u["triggers"].append(text)
            save_data()

        bot.send_message(
            m.chat.id,
            f"تم حفظ المحفز: {text}\n"
            "خطة المواجهة:\n"
            "- غيّر البيئة\n- بديل صحي\n- راقب التوقيت"
        )

    # أنا في خطر
    elif text=="🆘 أنا في خطر":
        bot.send_message(
            m.chat.id,
            "أين أنت الآن؟",
            reply_markup=danger_menu()
        )

    elif text in danger_actions:
        solution=random.choice(danger_actions[text])
        bot.send_message(
            m.chat.id,
            "🚨 افعل الآن:\n\n"+solution
        )

    # الموارد
    elif text=="💡 موارد التعافي":
        bot.send_message(
            m.chat.id,
            "اختر:",
            reply_markup=resources_menu()
        )

    elif text=="🎯 نصائح":
        bot.send_message(
            m.chat.id,
            "\n".join(random.sample(tips,3))
        )

    elif text=="📚 كتب":
        bot.send_message(
            m.chat.id,
            "\n".join(books)
        )

    elif text=="🎧 بودكاست":
        bot.send_message(
            m.chat.id,
            "\n".join(podcasts)
        )

    elif text=="🌐 مواقع":
        bot.send_message(
            m.chat.id,
            "\n".join(articles)
        )

    # قصص
    elif text=="📖 قصص التعافي":
        bot.send_message(
            m.chat.id,
            random.choice(stories)
        )

    # انتكاسة
    elif text=="❌ سجل انتكاسة":
        current=streak_days(u["start_date"])
        if current>u["best_streak"]:
            u["best_streak"]=current

        u["relapses"]+=1
        u["start_date"]=str(datetime.now().date())
        save_data()

        bot.send_message(
            m.chat.id,
            "تم تسجيل الانتكاسة. ابدأ من جديد 💪"
        )

    elif text=="⬅ رجوع":
        bot.send_message(
            m.chat.id,
            "القائمة الرئيسية",
            reply_markup=main_menu()
        )


print("Running...")
bot.infinity_polling() 
while True:
    try:
        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=60
        )
    except Exception as e:
        print(e)
        
        from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot alive"

def run_web():
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)

threading.Thread(target=run_web).start()
