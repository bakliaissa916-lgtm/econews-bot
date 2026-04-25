import os,json,threading,random
from datetime import datetime
from flask import Flask
import telebot
from telebot import types

from config import TOKEN

from modules.plans import *
from modules.progress import *
from modules.danger import *
from modules.stories import *
from modules.resources import *
from modules.medals import *

bot=telebot.TeleBot(TOKEN)

app=Flask(__name__)

DATA="data.json"

def load():
 try:
   with open(DATA,"r",encoding="utf8") as f:
      return json.load(f)
 except:
      return {}

db=load()

def save():
 with open(DATA,"w",encoding="utf8") as f:
   json.dump(db,f)

def user(uid):
 uid=str(uid)

 if uid not in db:
   db[uid]={
   "start_date":str(datetime.now().date()),
   "relapses":0
   }
 save()
 return db[uid]

def menu():
 kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
 kb.row("📅 خطتي","📊 تقدمي")
 kb.row("🏆 الإنجازات","🪜 الترتيب")
 kb.row("🆘 أنا في خطر","📖 قصص التعافي")
 kb.row("💡 الموارد","❌ انتكاسة")
 return kb

@app.route("/")
def home():
 return "alive"

@bot.message_handler(commands=["start"])
def start(m):
 user(m.chat.id)
 bot.send_message(
 m.chat.id,
 "🌱 مرحبا بك في نقاء",
 reply_markup=menu()
 )

@bot.message_handler(func=lambda m:True)
def msg(m):

 u=user(m.chat.id)

 t=m.text

 if t=="📅 خطتي":
   bot.send_message(m.chat.id,daily_plan())

 elif t=="📊 تقدمي":
   d=streak_days(u["start_date"])
   bot.send_message(m.chat.id,f"سلسلتك: {d} يوم")

 elif t=="🏆 الإنجازات":
   d=streak_days(u["start_date"])
   bot.send_message(m.chat.id,achievements(d))

 elif t=="🪜 الترتيب":
   d=streak_days(u["start_date"])
   bot.send_message(m.chat.id,leaderboard(d))

 elif t=="🆘 أنا في خطر":
   kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
   kb.row("🛏 في السرير")
   kb.row("🏠 وحدي")
   kb.row("📱 أتصفح")
   bot.send_message(
   m.chat.id,
   "أين أنت الآن؟",
   reply_markup=kb
   )

 elif t in danger_actions:
   bot.send_message(
   m.chat.id,
   emergency(t),
   reply_markup=menu()
   )

 elif t=="📖 قصص التعافي":
   bot.send_message(
   m.chat.id,
   random.choice(stories)
   )

 elif t=="💡 الموارد":
   bot.send_message(
   m.chat.id,
   "\n".join(tips+books+sites)
   )

 elif t=="❌ انتكاسة":
   u["relapses"]+=1
   u["start_date"]=str(datetime.now().date())
   save()
   bot.send_message(
   m.chat.id,
   "تم تسجيل الانتكاسة",
   reply_markup=menu()
   )

def flask_run():
 port=int(os.getenv("PORT",10000))
 app.run(host="0.0.0.0",port=port)

if __name__=="__main__":
 threading.Thread(
 target=flask_run,
 daemon=True
 ).start()

 bot.infinity_polling()
