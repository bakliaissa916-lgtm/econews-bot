from datetime import datetime

def streak_days(start):
    s = datetime.strptime(start,"%Y-%m-%d")
    return (datetime.now()-s).days

def achievements(days):

    levels = [
      (7,"🥉 برونزي"),
      (14,"🥈 فضي"),
      (30,"🥇 ذهبي"),
      (90,"💎 ماسي")
    ]

    msg="🏆 الإنجازات\n\n"

    for need,name in levels:
        if days>=need:
            msg+=f"✅ {name}\n"
        else:
            msg+=f"🔒 {name} (باقي {need-days})\n"

    return msg
