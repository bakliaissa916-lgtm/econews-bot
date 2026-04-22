import telebot
from telebot import types
import os

# ضع التوكن الخاص بك هنا أو استخرجه من بيئة العمل
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

# قاموس بسيط لتخزين بيانات المستخدمين (للتطوير المستقبلي يفضل استخدام قاعدة بيانات)
user_data = {}

def get_user_stats(user_id):
    if user_id not in user_data:
        user_data[user_id] = {'days': 0, 'relapses': 0, 'history': []}
    return user_data[user_id]

# --- لوحة التحكم الرئيسية ---
def main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🗓️ الخطة اليومية')
    btn2 = types.KeyboardButton('🔥 التحديات')
    btn3 = types.KeyboardButton('📊 تقدمي')
    btn4 = types.KeyboardButton('🏆 الأوسمة')
    btn5 = types.KeyboardButton('🚨 دعم فوري')
    btn6 = types.KeyboardButton('💡 نصائح ومقالات')
    btn7 = types.KeyboardButton('❌ سجل انتكاسة')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "<b>مرحباً بك في بوت نقاء ✨</b>\nرحلة التعافي تبدأ بخطوة، أنا هنا لدعمك.", 
                     parse_mode='HTML', reply_markup=main_markup())

# --- 1. الخطة اليومية ---
@bot.message_handler(func=lambda message: message.text == '🗓️ الخطة اليومية')
def daily_plan(message):
    markup = types.InlineKeyboardMarkup()
    btn_pdf = types.InlineKeyboardButton("📥 تحميل جدول PDF فارغ", callback_data="get_pdf")
    markup.add(btn_pdf)
    
    text = (
        "<b>🗓️ خطتك اليومية المقترحة:</b>\n\n"
        "1️⃣ <b>الفجر:</b> صلاة ورياضة صباحية 🏃‍♂️\n"
        "2️⃣ <b>الظهر:</b> عمل/دراسة مركزة 📚\n"
        "3️⃣ <b>المساء:</b> قراءة أو تطوير مهارة 🧠\n"
        "4️⃣ <b>قبل النوم:</b> ابعد الهاتف عن السرير 🚫📱"
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- 2. تقدمي (العداد) ---
@bot.message_handler(func=lambda message: message.text == '📊 تقدمي')
def my_progress(message):
    stats = get_user_stats(message.from_user.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 تصفير العداد (إعادة)", callback_data="reset_days"))
    
    text = (
        f"<b>📊 تقرير الأداء:</b>\n\n"
        f"⏳ عدد الأيام الصافية: <code>{stats['days']}</code> يوم\n"
        f"⚠️ عدد الانتكاسات: <code>{stats['relapses']}</code>\n"
        f"🏁 استمر، أنت أقوى من مجرد رقم!"
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- 3. الأوسمة (نظام النقاط) ---
@bot.message_handler(func=lambda message: message.text == '🏆 الأوسمة')
def medals(message):
    days = get_user_stats(message.from_user.id)['days']
    
    def get_status(target):
        return "✅ تم الحصول عليه" if days >= target else f"🔒 متبقي {target - days} يوم"

    text = (
        "<b>🏆 لوحة الشرف الخاصة بك:</b>\n\n"
        f"🥉 <b>الوسام البرونزي (14 يوم):</b> {get_status(14)}\n"
        f"🥈 <b>الوسام الفضي (30 يوم):</b> {get_status(30)}\n"
        f"🥇 <b>الوسام الذهبي (90 يوم):</b> {get_status(90)}\n"
        f"👑 <b>وسام الحرية (180 يوم):</b> {get_status(180)}"
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML')

# --- 4. التحديات (سجل الألوان) ---
@bot.message_handler(func=lambda message: message.text == '🔥 التحديات')
def challenges(message):
    stats = get_user_stats(message.from_user.id)
    # محاكاة للسلم بالألوان
    history = "🟩" * stats['days'] + "🟥" * stats['relapses']
    if not history: history = "لا يوجد سجل بعد، ابدأ اليوم!"
    
    bot.send_message(message.chat.id, f"<b>🔥 سلم التحدي الخاص بك:</b>\n\n{history}\n\n🟩 = يوم نجاح\n🟥 = انتكاسة", parse_mode='HTML')

# --- 5. دعم فوري ---
@bot.message_handler(func=lambda message: message.text == '🚨 دعم فوري')
def quick_support(message):
    tips = [
        "⚠️ <b>خطر!</b> اترك المكان الذي أنت فيه فوراً واذهب لمكان عام.",
        "🚶‍♂️ <b>تحرك:</b> قم بممارسة تمارين الضغط (15 مرة) الآن.",
        "🚿 <b>تحدي:</b> خذ حماماً بارداً فوراً لتهدئة الأعصاب.",
        "📱 <b>أغلق الشاشة:</b> ارمِ الهاتف بعيداً واقرأ صفحتين من كتاب."
    ]
    bot.send_message(message.chat.id, "\n\n".join(tips), parse_mode='HTML')

# --- 6. نصائح ومقالات ---
@bot.message_handler(func=lambda message: message.text == '💡 نصائح ومقالات')
def tips_and_articles(message):
    text = (
        "<b>📚 مكتبة التعافي:</b>\n\n"
        "1. <b>كتاب:</b> 'سماح بالرحيل' - لتنظيف المشاعر.\n"
        "2. <b>كتاب:</b> 'العادات الذرية' - لبناء حياة جديدة.\n\n"
        "🔗 <b>مقالات مختارة:</b>\n"
        "<a href='https://example.com'>كيف يعيد الدماغ ترميم نفسه بعد التعافي؟</a>\n"
        "<a href='https://example.com'>خطوات عملية لتجاوز المحفزات.</a>"
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML', disable_web_page_preview=False)

# --- معالجة الضغط على الأزرار (Callback) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_pdf":
        try:
            with open('schedule.pdf', 'rb') as f:
                bot.send_document(call.message.chat.id, f, caption="إليك الجدول الفارغ، قم بطباعته والالتزام به!")
        except FileNotFoundError:
            bot.answer_callback_query(call.id, "عذراً، ملف PDF غير موجود حالياً.")
            
    elif call.data == "reset_days":
        user_data[call.from_user.id]['days'] = 0
        bot.answer_callback_query(call.id, "تم تصفير العداد. بداية جديدة قوية!")
        bot.edit_message_text("تم تصفير العداد بنجاح. عد للوحة التحكم وابدأ من جديد.", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: message.text == '❌ سجل انتكاسة')
def record_relapse(message):
    stats = get_user_stats(message.from_user.id)
    stats['relapses'] += 1
    stats['days'] = 0
    bot.send_message(message.chat.id, "آسف لسماع ذلك، لكن تذكر: <b>الانتكاسة ليست النهاية، بل درس.</b> ارفع رأسك وابدأ من جديد الآن!", parse_mode='HTML')

# إضافة ميزة زيادة الأيام (للتجربة)
@bot.message_handler(commands=['add_day'])
def add_day(message):
    stats = get_user_stats(message.from_user.id)
    stats['days'] += 1
    bot.send_message(message.chat.id, f"أحسنت! أضفت يوماً جديداً. مجموعك الآن: {stats['days']}")

bot.infinity_polling()


