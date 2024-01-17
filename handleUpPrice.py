from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import requests
import json
from datetime import date, timedelta, datetime
from telegram.constants import ParseMode
from chuan_hoa_tin import chuanhoa

import re
from helper import is_number


API_URL = 'http://localhost:9000'


async def handleUpPriceMB(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.chat.title

    user = user.replace(" ", "_")

    # Loại bỏ kí tự chặn số

    message_text = update.message.text

    message_text = message_text.replace("/tdmb", '')

    message_text = await chuanhoa(message_text)

    message_text = re.sub(
        r'(da|b|x|dx|dd|lo+)(da|b|x|dx|dd|lo+)', r'\1 \2', message_text)
    
    message_text = re.sub(r'(\d+)(n+)', r'\1', message_text)

    message_text = re.sub(r'(\d+)([a-zA-z]+)', r'\1 \2', message_text)

    message_text = re.sub(r'([a-zA-z]+)(\d+)', r'\1 \2', message_text)

    message_text = message_text.replace(".",'')
    # cắt chuỗi thành những mảng đã cho theo dấu chấm cuối
    message_text = message_text.split("\n")

    

    message_out_put = []
    
    for message in message_text:

        #cắt chuỗi message thành 2 mảng theo dấu ":"

        _lst_message = message.split(":")

        #kiểm tra xem chỗi message có 2 mảng hay không nếu không báo lỗi không đúng định dạng
        if len(_lst_message) ==2:

            list_dai = _lst_message[0].split(" ")

            list_so_and_kieu = _lst_message[1]

            list_dai = list(filter(lambda x: x != "", list_dai))

            for item_dai in list_dai :

                item_out_put = f"{item_dai} {list_so_and_kieu}"

                message_out_put.append(item_out_put)
                
        else:

            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Lỗi \n Tin của bạn không đúng định dạng đã có. {message}", parse_mode=ParseMode.HTML)

            return
        

    
    print(message_out_put)

    data = {

        'ten_tai_khoan': f'{user}',
        'action': 'tang_diem_han_muc',
        'lst_so_chan': f'{message_out_put}',
        'vung_mien': 'mb'
    }

    await context.bot.send_message(chat_id=update.message.chat_id, text="Đang lưu tăng điểm", parse_mode=ParseMode.HTML)

    try:

        result_limit = requests.post(API_URL+"/cai_tang_diem/api_tang_diem_theo_loai.php", data=data)

        print(result_limit.text)

        result_limit = f"{result_limit.text}"

        if result_limit:

            result_limit = json.loads(result_limit)

            if result_limit['success'] == 1:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Lưu số tăng tiền thành công", parse_mode=ParseMode.HTML)

    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi \n Tin của bạn không đúng định dạng đã có.", parse_mode=ParseMode.HTML)


        

async def handleUpPriceMN(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.chat.title

    user = user.replace(" ", "_")

    # Loại bỏ kí tự chặn số

    message_text = update.message.text

    message_text = message_text.replace("/tdmn", '')

    message_text = await chuanhoa(message_text)

    message_text = re.sub(
        r'(da|b|x|dx|dd|lo+)(da|b|x|dx|dd|lo+)', r'\1 \2', message_text)
    
    message_text = re.sub(r'(\d+)(n+)', r'\1', message_text)

    message_text = re.sub(r'(\d+)([a-zA-z]+)', r'\1 \2', message_text)

    message_text = re.sub(r'([a-zA-z]+)(\d+)', r'\1 \2', message_text)

    message_text = message_text.replace(".",'')
    # cắt chuỗi thành những mảng đã cho theo dấu chấm cuối
    message_text = message_text.split("\n")

    

    message_out_put = []
    
    for message in message_text:

        #cắt chuỗi message thành 2 mảng theo dấu ":"

        _lst_message = message.split(":")

        #kiểm tra xem chỗi message có 2 mảng hay không nếu không báo lỗi không đúng định dạng
        if len(_lst_message) ==2:

            list_dai = _lst_message[0].split(" ")

            list_so_and_kieu = _lst_message[1]

            list_dai = list(filter(lambda x: x != "", list_dai))

            for item_dai in list_dai :

                item_out_put = f"{item_dai} {list_so_and_kieu}"

                message_out_put.append(item_out_put)
                
        else:

            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Lỗi \n Tin của bạn không đúng định dạng đã có. {message}", parse_mode=ParseMode.HTML)

            return
        

    
    print(message_out_put)

    data = {

        'ten_tai_khoan': f'{user}',
        'action': 'tang_diem_han_muc',
        'lst_so_chan': f'{message_out_put}',
        'vung_mien': 'mb'
    }

    await context.bot.send_message(chat_id=update.message.chat_id, text="Đang lưu tăng điểm", parse_mode=ParseMode.HTML)

    try:

        result_limit = requests.post(API_URL+"/cai_tang_diem/api_tang_diem_theo_loai.php", data=data)

        print(result_limit.text)

        result_limit = f"{result_limit.text}"

        if result_limit:

            result_limit = json.loads(result_limit)

            if result_limit['success'] == 1:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Lưu số tăng tiền thành công", parse_mode=ParseMode.HTML)

    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi \n Tin của bạn không đúng định dạng đã có.", parse_mode=ParseMode.HTML)




async def handleUpPriceMT(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.chat.title

    user = user.replace(" ", "_")

    # Loại bỏ kí tự chặn số

    message_text = update.message.text

    message_text = message_text.replace("/tdmt", '')

    message_text = await chuanhoa(message_text)

    message_text = re.sub(
        r'(da|b|x|dx|dd|lo+)(da|b|x|dx|dd|lo+)', r'\1 \2', message_text)
    
    message_text = re.sub(r'(\d+)(n+)', r'\1', message_text)

    message_text = re.sub(r'(\d+)([a-zA-z]+)', r'\1 \2', message_text)

    message_text = re.sub(r'([a-zA-z]+)(\d+)', r'\1 \2', message_text)

    message_text = message_text.replace(".",'')
    # cắt chuỗi thành những mảng đã cho theo dấu chấm cuối
    message_text = message_text.split("\n")

    

    message_out_put = []
    
    for message in message_text:

        #cắt chuỗi message thành 2 mảng theo dấu ":"

        _lst_message = message.split(":")

        #kiểm tra xem chỗi message có 2 mảng hay không nếu không báo lỗi không đúng định dạng
        if len(_lst_message) ==2:

            list_dai = _lst_message[0].split(" ")

            list_so_and_kieu = _lst_message[1]

            list_dai = list(filter(lambda x: x != "", list_dai))

            for item_dai in list_dai :

                item_out_put = f"{item_dai} {list_so_and_kieu}"

                message_out_put.append(item_out_put)
                
        else:

            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Lỗi \n Tin của bạn không đúng định dạng đã có. {message}", parse_mode=ParseMode.HTML)

            return
        

    
    print(message_out_put)

    data = {

        'ten_tai_khoan': f'{user}',
        'action': 'tang_diem_han_muc',
        'lst_so_chan': f'{message_out_put}',
        'vung_mien': 'mb'
    }

    await context.bot.send_message(chat_id=update.message.chat_id, text="Đang lưu tăng điểm", parse_mode=ParseMode.HTML)

    try:

        result_limit = requests.post(API_URL+"/cai_tang_diem/api_tang_diem_theo_loai.php", data=data)

        print(result_limit.text)

        result_limit = f"{result_limit.text}"

        if result_limit:

            result_limit = json.loads(result_limit)

            if result_limit['success'] == 1:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Lưu số tăng tiền thành công", parse_mode=ParseMode.HTML)

    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi \n Tin của bạn không đúng định dạng đã có.", parse_mode=ParseMode.HTML)