from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

from datetime import date, timedelta, datetime
from telegram.constants import ParseMode




async def funcHandleHuongDan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = """/mb  - so dai mb
/mt  - so dai mt
/mn  - so dai mt
/mn  - so dai mt
/baocao - lay bao cao
/caidat - cai dat 
/chanso 

- Cách thêm: /chanso [miền] [số]
- Tin VD:
/chanso mn mt 39 79 938 mb 68 86

===========================
/chanloai_mb - chặn số theo loại của miền bác
/chanloai_mt - chặn số theo loại của miền trung
/chanloai_mn - chặn số theo loại của miền nam 

- Tin VD:
/chanloai_[mien]
/chanloai_mb
mb: 00 11 22 33 44 55 66 77 88 99 da0n .
ag bt tp: 39 79 dd500n lo100n 739 938 xc20n .
cm ct: 7777 lo0n .

===============================
/hmmb - chặn điểm của miền băc
/hmmt - chặn điểm của miền trung
/hmmn - chặn điểm của miền nam

- Tin VD:
/hm[miền] [đài] [kiểu] [điểm]
/hmmb vl 12 dd dx 100
/hmmt vl  100
/hmmn 100
===================

===============================
/tdmb - chặn điểm của miền băc
/tdmt - chặn điểm của miền trung
/tdmn - chặn điểm của miền nam

- Tin VD:
/tdmb
mb: 00 11 22 33 44 55 66 77 88 99 da0n .
ag bt tp: 39 79 dd500n lo100n 739 938 xc20n .
cm ct: 7777 lo0n .
===================


/huychan - huy chan so -  /huychan [mã lệnh]"""
            
    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)