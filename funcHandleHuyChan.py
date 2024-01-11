from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import requests
import json
from datetime import date, timedelta, datetime
from telegram.constants import ParseMode
from chuan_hoa_tin import chuanhoa
from supbase_service import callDataSeting, updateTypeMessage, setting
import re
from helper import is_number


API_URL = 'http://159.65.129.60:9000'


async def funcHandleHuyChan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_text = update.message.text

    user = update.message.chat.title
    user = user.replace(" ", "_")

    # Loại bỏ kí tự chặn số

    message_text = message_text.replace("/huychan", '')

    message_text = message_text.strip()

    message_text = await chuanhoa(message_text)

    message_text = re.sub(r'(\d+)([a-zA-z]+)', r'\1', message_text)

    message_text = re.sub(r'([a-zA-z]+)(\d+)', r'\2', message_text)

   #chuyển chuỗi số về mảng
    
    lst_number_limit = message_text.split(" ")

    msg_error = ""

    for number in lst_number_limit:
        if is_number(number) == False:
            msg_error = "Lỗi. không nhận kí tự trong chỗi mã số"

    if msg_error:

        await update.message.reply_text(text=msg_error, parse_mode=ParseMode.HTML)

    else:



        data = {
            'ten_tai_khoan': f'{user}',
            'action': 'huy_chan_tin',
            'tin_huy': f'{",".join(lst_number_limit)}'
        }


        print(data)

        result_limit = requests.post(API_URL+"/huychanso/api_huy_chan_so.php", data=data)

        try:

            result_limit = f"{result_limit.text}"

            print(result_limit)

            if result_limit:

                result_limit = json.loads(result_limit)

                if result_limit['success'] == 1:

                    await context.bot.send_message(chat_id=update.message.chat_id, text="Huỷ tin thành công", parse_mode=ParseMode.HTML)

                else:

                    await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi. Huỷ tin không thành công", parse_mode=ParseMode.HTML)

        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")


        await update.message.reply_text(text="Huỷ chặn lệnh thành công", parse_mode=ParseMode.HTML)