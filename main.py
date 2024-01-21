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
from funcHandleHuyChan import funcHandleHuyChan
from handleLimitTypeStationNumber import handleLimitTypeStationNumberMB,handleLimitTypeStationNumberMN, handleLimitTypeStationNumberMT

from handleUpPrice import handleUpPriceMB, handleUpPriceMT, handleUpPriceMN

from huong_dan import funcHandleHuongDan


# Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
TOKEN = '6705356232:AAErmh47SQeDeuBsRrSJuMBR6oRdQsqOmQ8'
API_URL = 'http://159.65.129.60:9000'
# API_URL = 'http://localhost:9000'

today = date.today()


type_message = 'MB'

file_path = 'Ket_qua.html'

file_path_report = 'Bao_cao.html'

count = 0

FIRST, SECOND = range(2)


def addChar(char, count):
    text = ''

    for j in range(count):

        text += f'{char}'

    return text


def splitString(val, number, char):
    if not val:
        return addChar(char, number)

    if len(str(val)) > number:
        return f"{str(val)}"[:number - 1] + char

    else:
        return f"{str(val)}{addChar(char, number - len(str(val)))}"


def formatMoney(val):

    if not val:
        return '0'
    else:

        formatted_number = f"{val:,.0f}"

        return formatted_number


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # await callDataSeting(update.message.chat.title)

    await update.message.reply_text(f"Hello {user.first_name}! I'm your bot. How can I help you?")


async def sendMessageMB(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global type_message, count
    type_message = 'MB'
    message_text = "=== BẮT ĐẦU NHẬP CHO MB ==="
    count = 1

    await updateTypeMessage(update.message.chat.title, 'TYPE_MESSAGE', "MB")
    await updateTypeMessage(update.message.chat.title, 'COUNT_MESSAGE', "0")

    # await callDataSeting(update.message.chat.title)

    await context.bot.send_message(chat_id=update.message.chat_id, text=message_text, parse_mode=ParseMode.HTML)


async def sendMessageMN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global type_message, count
    type_message = 'MN'
    message_text = "=== BẮT ĐẦU NHẬP CHO MN ==="
    count = 1

    await updateTypeMessage(update.message.chat.title, 'TYPE_MESSAGE', "MN")
    await updateTypeMessage(update.message.chat.title, 'COUNT_MESSAGE', "0")

    # await callDataSeting(update.message.chat.title)

    await context.bot.send_message(chat_id=update.message.chat_id, text=message_text, parse_mode=ParseMode.HTML)


async def sendMessageMT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global type_message, count
    type_message = 'MT'
    message_text = "=== BẮT ĐẦU NHẬP CHO MT ===\n"
    count = 1

    await updateTypeMessage(update.message.chat.title, 'TYPE_MESSAGE', "MT")
    await updateTypeMessage(update.message.chat.title, 'COUNT_MESSAGE', "0")

    # await callDataSeting(update.message.chat.title)

    await context.bot.send_message(chat_id=update.message.chat_id, text=message_text, parse_mode=ParseMode.HTML)


async def writeHTMLFile(ds_chi_tiet=[], ma_lenh='', data_list=[]):

    with open(file_path, 'r') as file:
        html_content = file.read()

    item_table = ''

    for key, value in ds_chi_tiet.items():
        print(f"Key: {key}")
        item_table += f"""<tr>
                    <td colspan='6' style='background: #DDDDDD;'>{key}</td>
                </tr>"""

        for index, tin in enumerate(value):

            _dai = tin['dai']

            if setting['TYPE_MESSAGE'] == 'MB':
                _dai = 'mb'

            item_table += f"""<tr>
                <td>{index+1}</td>
                <td>{_dai}</td>
                <td>{tin['so']}</td>
                <td>{tin['kieu']}</td>
                <td>{tin['diem']}</td>
                <td>{formatMoney(tin['xac'])}</td>
            </tr>"""

    item_kieu_danh = ''

    for keu_danh in data_list:

        if formatMoney(keu_danh['xac']) != '0' or formatMoney(keu_danh['thuc_thu']) != '0':
            item_table += f"""<p>Kiểu: {keu_danh['kieu']}</p>
            <p>Xác: {formatMoney(keu_danh['xac'])}</p>
            <p>Tổng tiền: {formatMoney(keu_danh['thuc_thu'])}</p>"""

    new_paragraph = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>HTML Table with 5 Columns</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }

                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>

            <h2>Thông tin chi tiết</h2>
            <hr>
            <p>Mã lệnh: """+ma_lenh+"""</p>
            """+item_kieu_danh+""""

            <table>
                <thead>
                    <tr>
                        <th>STT</th>
                        <th>Đài</th>
                        <th>Số</th>
                        <th>Kiểu</th>
                        <th>Điểm</th>
                        <th>Tiền</th>
                    </tr>
                </thead>
                <tbody>
                    """ + item_table + """""
                </tbody>
            </table>
            </body>
            </html>
        """

    html_content = new_paragraph

    with open(file_path, 'w') as file:
        file.write(html_content)


async def writeHTMLFileReport(ds_chi_tiet_mb={}, ds_chi_tiet_mn={}, ds_chi_tiet_mt={}):

    with open(file_path_report, 'r') as file:
        html_content = file.read()

    item_table_mn = ''

    for value in ds_chi_tiet_mn:

        for detail_tin in ds_chi_tiet_mn[value]:
            item_table_mn += f"""<tr>
                    <td>{int(value)}</td>
                    <td>MN</td>
                    <td>{detail_tin['dai']}</td>
                    <td>{detail_tin['so_trung']}</td>
                    <td>{detail_tin['kieu']}</td>
                    <td>{detail_tin['diem']}</td>
                    <td  class="colorBlue">{detail_tin['tien_trung']}</td>
                </tr>"""

    item_table_mb = ''

    for value in ds_chi_tiet_mb:

        for detail_tin in ds_chi_tiet_mb[value]:
            item_table_mb += f"""<tr>
                    <td>{int(value)}</td>
                    <td>MB</td>
                    <td>mb</td>
                    <td>{detail_tin['so_trung']}</td>
                    <td>{detail_tin['kieu']}</td>
                    <td>{detail_tin['diem']}</td>
                    <td  class="colorBlue">{detail_tin['tien_trung']}</td>
                </tr>"""

    item_table_mt = ''

    for value in ds_chi_tiet_mt:

        for detail_tin in ds_chi_tiet_mt[value]:
            item_table_mt += f"""<tr>
                    <td>{int(value)}</td>
                    <td>MT</td>
                    <td>{detail_tin['dai']}</td>
                    <td>{detail_tin['so_trung']}</td>
                    <td>{detail_tin['kieu']}</td>
                    <td>{detail_tin['diem']}</td>
                    <td  class="colorBlue">{detail_tin['tien_trung']}</td>
                </tr>"""

    new_paragraph = """
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <style>
            table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            }

            td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
            font-size: 32px;
            }
            p {
            font-weight: bold
            }

            .colorRed {
            font-weight: bold;
            color: red;
            }

            .colorBlue {
            font-weight: bold;
            color: #3d73dd;
            }

            .footer {
            font-weight: bold;
            font-size: 150%;
            }
            </style>
            </head>
            <body>

            <table>
            <tr style="background-color: #66ffcc">
                <th>STT</th>
                <th>Miền</th>
                <th>Đài</th>
                <th>Số</th>
                <th>CChơi</th>
                <th>Tiền</th>
                <th>Thắng</th>
            </tr>

            <tr style="background-color: #66ffcc">
                <td colspan='7' style='background: #DDDDDD;'>MB</td>
            </tr>
            """+item_table_mb+"""""
            <tr style="background-color: #66ffcc">
                <td colspan='7' style='background: #DDDDDD;'>MN</td>
            </tr>
            """+item_table_mn+"""""

            <tr style="background-color: #66ffcc">
                <td colspan='7' style='background: #DDDDDD;'>MT</td>
            </tr>
            """+item_table_mt+"""""

            </table>
            </body>
            </html>
        """

    html_content = new_paragraph

    with open(file_path_report, 'w') as file:
        file.write(html_content)


async def create_number_mb(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global count

    today = date.today()

    day = today.strftime("%d-%m-%Y")

    # replace message
    message_text = update.message.text
    message_text = await chuanhoa(message_text)

    user = update.message.chat.title

    user = user.replace(" ", "_")

   

    if message_text:

        try:

            data = {
                'thoi_gian_danh': ''+day+'',
                'tai_khoan_danh': f'{user}',
                'noi_dung': ''+str(message_text)+'',
                'action': 'luu',
                'account_create': ''+str(user)+'',
                'vung_mien': 'mb',
                'message_id': f'{update.message.message_id}',
            }

            respone = requests.post(
                API_URL+"/mb/tin/api_tao_tin.php", data=data)

            result_tin = respone.text

            print(result_tin)

            data_list = json.loads(result_tin)

            if data_list['status'] == 200:

                ds_chi_tiet = data_list['ds_chi_tiet']

                msg_tang_diem = data_list['diem_tang']

                data_list = list(data_list['data'].values())

                if len(ds_chi_tiet) > 0:

                    await writeHTMLFile(ds_chi_tiet, message_text, data_list)

                total_xac = 0
                total_thuc_thu = 0
                total_trung = 0

                if len(data_list) > 0:

                    result_string = f"OK MB - T{int(setting['COUNT_MESSAGE']) + 1}\n"

                    for tin in data_list:
                        if formatMoney(tin['xac']) != '0' or formatMoney(tin['thuc_thu']) != '0':

                            result_string += f"- {tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"
                            total_xac += tin['xac'] or 0
                            total_thuc_thu += tin['thuc_thu'] or 0
                            total_trung += tin['tien_trung'] or 0

                    result_string += f'TỔNG: {formatMoney(total_xac)}'

                    if msg_tang_diem :
                        result_string += '\n'+msg_tang_diem


                    with open(file_path, 'rb') as file:
                        count += 1
                        await update.message.reply_document(document=InputFile(file), caption=result_string, parse_mode=ParseMode.HTML)
                       
                        await updateTypeMessage(update.message.chat.title, 'COUNT_MESSAGE', int(setting['COUNT_MESSAGE']) + 1)

            else:

                await update.message.reply_text(data_list['message'], ParseMode.HTML)

        except Exception as e:
            # Log the exception using the logging module
            await update.message.reply_text(f"{e}")
            # Optionally, re-raise the exception
            raise


async def create_number_mn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global count

    today = date.today()

    day = today.strftime("%d-%m-%Y")

    # replace message
    message_text = update.message.text

    message_text = await chuanhoa(message_text)

    user = update.message.chat.title

    user = user.replace(" ", "_")



   
    if message_text:

        try:

            data = {
                'thoi_gian_danh': ''+day+'',
                'tai_khoan_danh': f'{user}',
                'noi_dung': ''+message_text+'',
                'action': 'luu',
                'account_create': ''+str(user)+'',
                'vung_mien': 'mn',
                'message_id': f'{update.message.message_id}',
            }

            respone = requests.post(
                API_URL+"/mn/tin/api_tao_tin.php", data=data)

            result_tin = respone.text

            print(result_tin)

            data_list = json.loads(result_tin)

            if data_list['status'] == 200:

                ds_chi_tiet = data_list['ds_chi_tiet']

                msg_tang_diem = data_list['diem_tang']

                data_list = list(data_list['data'].values())

                if len(ds_chi_tiet) > 0:

                    await writeHTMLFile(ds_chi_tiet, message_text, data_list)

                total_xac = 0
                total_thuc_thu = 0
                total_trung = 0

                print(data_list)

                if len(data_list) > 0:

                    result_string = f"OK MN - T{int(setting['COUNT_MESSAGE']) + 1}\n"

                    for tin in data_list:
                        if formatMoney(tin['xac']) != '0' or formatMoney(tin['thuc_thu']) != '0':

                            result_string += f"- {tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"
                            total_xac += tin['xac'] or 0
                            total_thuc_thu += tin['thuc_thu'] or 0
                            total_trung += tin['tien_trung'] or 0

                    result_string += f'TỔNG: {formatMoney(total_xac)}'

                    if msg_tang_diem :
                        result_string += '\n'+msg_tang_diem

                    with open(file_path, 'rb') as file:
                        count += 1
                        await update.message.reply_document(document=InputFile(file), caption=result_string, parse_mode=ParseMode.HTML)

                        await updateTypeMessage(update.message.chat.title, 'COUNT_MESSAGE', int(setting['COUNT_MESSAGE']) + 1)

            else:

                await update.message.reply_text(data_list['message'], ParseMode.HTML)

        except Exception as e:
            # Log the exception using the logging module
            await update.message.reply_text(f"{e}")
            # Optionally, re-raise the exception
            raise


async def create_number_mt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global count

    today = date.today()

    day = today.strftime("%d-%m-%Y")

    # replace message
    message_text = update.message.text
    message_text = await chuanhoa(message_text)

    user = update.message.chat.title

    user = user.replace(" ", "_")

    if message_text:

        try:

            data = {
                'thoi_gian_danh': ''+day+'',
                'tai_khoan_danh': f'{user}',
                'noi_dung': ''+message_text+'',
                'action': 'luu',
                'account_create': ''+str(user)+'',
                'vung_mien': 'mt',
                'message_id': f'{update.message.message_id}',
            }

          
            respone = requests.post(
                API_URL+"/mt/tin/api_tao_tin.php", data=data)

            result_tin = respone.text


            data_list = json.loads(result_tin)

            if data_list['status'] == 200:

                ds_chi_tiet = data_list['ds_chi_tiet']
                msg_tang_diem = data_list['diem_tang']
                data_list = list(data_list['data'].values())

                if len(ds_chi_tiet) > 0:

                    await writeHTMLFile(ds_chi_tiet, message_text, data_list)

                total_xac = 0
                total_thuc_thu = 0
                total_trung = 0

                if len(data_list) > 0:

                    result_string = f"OK MT - T{int(setting['COUNT_MESSAGE']) + 1}\n"

                    for tin in data_list:
                        if formatMoney(tin['xac']) != '0' or formatMoney(tin['thuc_thu']) != '0':

                            result_string += f"- {tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"
                            total_xac += tin['xac'] or 0
                            total_thuc_thu += tin['thuc_thu'] or 0
                            total_trung += tin['tien_trung'] or 0

                    result_string += f'TỔNG: {formatMoney(total_xac)}'

                    if msg_tang_diem :
                        result_string += '\n'+msg_tang_diem

                    with open(file_path, 'rb') as file:
                        count += 1
                        await update.message.reply_document(document=InputFile(file), caption=result_string, parse_mode=ParseMode.HTML)
                        await updateTypeMessage(update.message.chat.title, 'COUNT_MESSAGE', int(setting['COUNT_MESSAGE']) + 1)

            else:

                await update.message.reply_text(data_list['message'], ParseMode.HTML)

        except Exception as e:
            # Log the exception using the logging module
            await update.message.reply_text(f"{e}")
            # Optionally, re-raise the exception
            raise


async def fetchReport(update: Update, context: ContextTypes.DEFAULT_TYPE, date_report):

    # replace message
    query = update.callback_query

    user = update.callback_query.message.chat.title

    user = user.replace(" ", "_")

    try:

        data = {
            'ngay': ''+date_report+'',
            'ten_tai_khoan': f'{user}',
            # 'ten_tai_khoan': f'Group_ChatBot',
            'loai_tai_khoan': 'admin',
            'action': 'doc',
        }

        # print(tin_list_mt)
        message_text = f"""<b>{splitString(date_report,15,' ')}</b>\n"""

        total_money = 0

        ds_chi_tiet_mb = []
        ds_chi_tiet_mt = []
        ds_chi_tiet_mn = []

        # if  specific_date <= current_date and datetime.strptime(setting["TIME_REPORT_MB"], "%H:%M:%S").time() <= current_time  :

        respone_mb = requests.post(
            API_URL+"/mb/thong_ke/api_thong_ke.php", data=data)

        result_report_mb = respone_mb.text

        report_mb_format = json.loads(result_report_mb)

        thong_ke_mb = json.loads(report_mb_format['thong_ke'])

        ds_chi_tiet_mb = json.loads(report_mb_format['ds_chi_tiet'])

        result_thong_ke_mb = json.loads(report_mb_format['result_thong_ke'])

        if len(result_thong_ke_mb) > 0:
            result_thong_ke_mb = list(result_thong_ke_mb.values())

        if 'mb' in thong_ke_mb and len(result_thong_ke_mb) > 0:

            message_text += f"""=============================================\n"""

            message_text += f"""MB\n"""

            data_thong_ke_mb = thong_ke_mb['mb']

            message_text += f"""Số tin: {formatMoney(data_thong_ke_mb['so_tin'])}\n"""

            type_money_mb = 'bu'

            if int(data_thong_ke_mb['thang_thua']) < 0:
                type_money_mb = 'thu'

            total_tr_mb = ''

            for tin in result_thong_ke_mb:
                if int(tin['xac']) > 0 or int(tin['thuc_thu']) > 0:
                    message_text += f"{tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"

                    if int(tin['diem_trung']) > 0:
                        total_tr_mb += f"{tin['kieu']}_{tin['diem_trung']}n; "

            if total_tr_mb == '':
                total_tr_mb = '0.0'

            message_text += f"""Tr: {total_tr_mb} \n"""
            message_text += f"""Tổng: <b>{formatMoney(data_thong_ke_mb['thang_thua'])} {type_money_mb} </b> \n"""
            message_text += f"""=============================================\n"""

            total_money += int(data_thong_ke_mb['thang_thua'])

        # mn

        # if datetime.strptime(setting["TIME_REPORT_MN"], "%H:%M:%S").time() <= current_time and specific_date <= current_date:

        respone_mn = requests.post(
            API_URL+"/mn/thong_ke/api_thong_ke.php", data=data)

        result_report_mn = respone_mn.text

        print(result_report_mn)

        report_mn_format = json.loads(result_report_mn)

        thong_ke_mn = json.loads(report_mn_format['thong_ke'])

        ds_chi_tiet_mn = json.loads(report_mn_format['ds_chi_tiet'])

        result_thong_ke_mn = json.loads(report_mn_format['result_thong_ke'])

        if len(result_thong_ke_mn) > 0:
            result_thong_ke_mn = list(result_thong_ke_mn.values())

        if 'mn' in thong_ke_mn and len(result_thong_ke_mn) > 0:

            message_text += f"""MN\n"""

            data_thong_ke_mn = thong_ke_mn['mn']

            message_text += f"""Số tin: {formatMoney(data_thong_ke_mn['so_tin'])}\n"""

            type_money_mn = 'bu'

            if int(data_thong_ke_mn['thang_thua']) < 0:
                type_money_mn = 'thu'

            total_tr_mn = ''

            for tin in result_thong_ke_mn:
                if int(tin['xac']) > 0 or int(tin['thuc_thu']) > 0:
                    message_text += f"{tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"

                    if int(tin['diem_trung']) > 0:
                        total_tr_mn += f"{tin['kieu']}_{tin['diem_trung']}n; "

            if total_tr_mn == '':
                total_tr_mn = '0.0'

            message_text += f"""Tr: {total_tr_mn}  \n"""
            message_text += f"""Tổng: <b>{formatMoney(data_thong_ke_mn['thang_thua'])} {type_money_mn} </b> \n"""
            message_text += f"""=============================================\n"""
            total_money += int(data_thong_ke_mn['thang_thua'])

        # mt

        respone_mt = requests.post(
            API_URL+"/mt/thong_ke/api_thong_ke.php", data=data)

        result_report_mt = respone_mt.text

        report_mt_format = json.loads(result_report_mt)

        thong_ke_mt = json.loads(report_mt_format['thong_ke'])

        ds_chi_tiet_mt = json.loads(report_mt_format['ds_chi_tiet'])

        result_thong_ke_mt = json.loads(report_mt_format['result_thong_ke'])

        if len(result_thong_ke_mt) > 0:
            result_thong_ke_mt = list(result_thong_ke_mt.values())

        if 'mt' in thong_ke_mt and len(result_thong_ke_mt) > 0:

            message_text += f"""MT\n"""

            data_thong_ke_mt = thong_ke_mt['mt']

            message_text += f"""Số tin: {formatMoney(data_thong_ke_mt['so_tin'])}\n"""

            type_money_mt = 'bu'

            if int(data_thong_ke_mt['thang_thua']) < 0:
                type_money_mt = 'thu'

            total_tr_mt = ''

            for tin in result_thong_ke_mt:
                if int(tin['xac']) > 0 or int(tin['thuc_thu']) > 0:
                    message_text += f"{tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"

                    if int(tin['diem_trung']) > 0:
                        total_tr_mt += f"{tin['kieu']}_{tin['diem_trung']}n; "

            if total_tr_mt == '':
                total_tr_mt = '0.0'

            message_text += f"""Tr: {total_tr_mt} \n"""
            message_text += f"""Tổng: <b>{formatMoney(data_thong_ke_mt['thang_thua'])} {type_money_mt} </b> \n"""
            message_text += f"""=============================================\n"""
            total_money += int(data_thong_ke_mt['thang_thua'])

        typt_TC = 'bu'

        if int(total_money) < 0:
            typt_TC = 'thu'

        message_text += f"""<b>TC: {formatMoney(total_money)} {typt_TC} </b>\n"""

        await writeHTMLFileReport(ds_chi_tiet_mb, ds_chi_tiet_mn, ds_chi_tiet_mt)

        await update.callback_query.message.reply_text(text=message_text, parse_mode=ParseMode.HTML)

        with open(file_path_report, 'rb') as file:

            await context.bot.send_document(chat_id=update.callback_query.message.chat.id, document=InputFile(file), parse_mode=ParseMode.HTML)

    except Exception as e:
        # Log the exception using the logging module

        await query.edit_message_text(text=f"{str(e)}", parse_mode=ParseMode.HTML)
        # Optionally, re-raise the exception
        raise


async def select_report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    today = date.today()

    await callDataSeting(update.message.chat.title)

    keyboard = [
        [InlineKeyboardButton(f"{today.strftime('%d-%m')}",
                              callback_data=f'{today.strftime("%d-%m-%Y")}')],
        [InlineKeyboardButton(f"{(today  - timedelta(days=1)).strftime('%d-%m')}",
                              callback_data=f"{(today  - timedelta(days=1)).strftime('%d-%m-%Y')}")],

        [InlineKeyboardButton(f"{(today  - timedelta(days=2)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=2)).strftime('%d-%m-%Y')}"),
         InlineKeyboardButton(f"{(today  - timedelta(days=3)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=3)).strftime('%d-%m-%Y')}")],

        [InlineKeyboardButton(f"{(today  - timedelta(days=4)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=4)).strftime('%d-%m-%Y')}"),
         InlineKeyboardButton(f"{(today  - timedelta(days=5)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=5)).strftime('%d-%m-%Y')}")],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Chọn thời gian báo cáo:', reply_markup=reply_markup)


async def select_setting(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("chọn cài đặt")

    keyboard = [
        [
            InlineKeyboardButton(f"Chặn", callback_data="LIMIT_NUMBER"),
            InlineKeyboardButton(f"Giá", callback_data="CONFIG_PRICE"),
            InlineKeyboardButton(f"Hạn mức", callback_data="MAX_PRICE"),
            
        ],
        [
            InlineKeyboardButton(f"Tăng Giá", callback_data="UP_PRICE")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text='Chọn loại cài đặt', reply_markup=reply_markup)


async def fetch_config_price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="Cài đặt giá", parse_mode=ParseMode.HTML)

    user = update.callback_query.message.chat.title

    user = user.replace(" ", "_")

    data = {

        'ten_tai_khoan': f'{user}',
        'loai_tai_khoan': 'admin',
        'action': 'doc',
    }

    price_config = requests.post(
        API_URL+"/cau_hinh/api_cau_hinh.php", data=data)

    price_config = price_config.text

    price_config = json.loads(price_config)

    ds_chi_tiet_cau_hinh = price_config["ds_chi_tiet_cau_hinh"]

    ds_chi_tiet_cau_hinh = json.loads(ds_chi_tiet_cau_hinh)

    grouped_data = {}

    text_message = ""

    if len(ds_chi_tiet_cau_hinh) > 0:

        for entry in ds_chi_tiet_cau_hinh:

            region = entry['vung_mien']

            # If the region is not in the dictionary, add it with an empty list
            grouped_data.setdefault(region, []).append(entry)

        for region, entries in grouped_data.items():

            text_message += f"========={region}=========\n"

            for entry in entries:

                text_message += f"{entry['kieu_danh']}  {entry['co']} {entry['trung']} \n"

    await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=text_message, parse_mode=ParseMode.HTML)


async def update_config_price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("Update cài đặt giá")

    message_text = update.message.text

    # Split the data by lines
    lines = message_text.strip().split('\n')

    # Initialize an empty list to store the result
    result = []

    # Iterate through lines and extract relevant information
    current_region = None
    for line in lines:
        if line.startswith("========="):
            current_region = line.strip("=")
        else:
            parts = line.split()
            if len(parts) >= 3:
                name = ' '.join(parts[:-2])
                values = list(map(float, parts[-2:]))
                result.append([current_region, name] + values)

    config_price = []

    # Print the result
    for entry in result:

        config_price.append(
            {'vung_mien': entry[0], 'kieu': entry[1], 'co': int(entry[2]), 'trung': entry[3]})

    if len(config_price) > 0:

        await context.bot.send_message(chat_id=update.message.chat_id, text="Đang lưu cài đặt", parse_mode=ParseMode.HTML)

        user = update.message.chat.title

        user = user.replace(" ", "_")

        data = {

            'ten_tai_khoan': f'{user}',
            'action': 'cap_nhat_chi_tiet',
            'config_price': f'{config_price}'
        }

        result_price_config = requests.post(
            API_URL+"/cau_hinh/api_cau_hinh.php", data=data)

        try:

            price_config = f"{result_price_config.text}"

            if price_config:

                price_config = json.loads(price_config)

                if price_config['success'] == 1:
                    await context.bot.send_message(chat_id=update.message.chat_id, text="Lưu cài đặt thành công", parse_mode=ParseMode.HTML)

        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")


async def handleLimitStationNumber(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_text = update.message.text

    # Loại bỏ kí tự chặn số

    message_text = message_text.replace("/chanso", '')

    message_text = message_text.strip()

    # kiểm tra xem tin có bắt đầu bằng tên đài hay không

    if message_text.startswith(("mb", "mn", "mt")) and not message_text.endswith(("mb", "mn", "mt")):

        i = 0

        message_text_format = ""

        while i < len(message_text):

            if i + 2 < len(message_text) and message_text[i:i+2] in ["mb", "mt", "mn"]:
                message_text_format += message_text[i:i+2]+" "
                i += 2
            else:
                message_text_format += message_text[i]
                i += 1

        # Chuyển chuỗi thành mảng
        message_text_format = message_text_format.split(" ")

        message_text_format = list(filter(lambda x: x != "", message_text_format))

        current_item = {}

        for i in range(0, len(message_text_format)):

            # kiểm tra nếu là đài thì tạo 1 mảng
            if message_text_format[i] in ["mb", "mt", "mn"]:

                _number = []

                if len(current_item) > 0 and message_text_format[i] in current_item:
                    _number = current_item[message_text_format[i]]["so"]

                isNumber = False
                # chạy từ vị trí hiện tại đến hết lấy những kí tự là số
                for key in range(i, len(message_text_format)):

                    if message_text_format[key].isdigit() and isNumber == True:

                        _number.append(message_text_format[key])

                        if (key+1) < len(message_text_format) and message_text_format[key+1].isalpha() and isNumber == True:
                            isNumber = False
                            break

                    # kiểm tra xem kí tự hiện tại nếu là chữ mà kí tự sau là số thì chuyển trạng thái về True
                    if message_text_format[key].isalpha() and (key+1) < len(message_text_format) and message_text_format[key+1].isdigit():
                        isNumber = True

                _lst_number = {"dai": message_text_format[i], "so": _number}

                current_item[message_text_format[i]] = _lst_number

        list_of_dicts = list(current_item.values())

        if len(list_of_dicts) > 0:

            user = update.message.chat.title

            user = user.replace(" ", "_")

            data = {

                'ten_tai_khoan': f'{user}',
                'action': 'chan_so_theo_mien',
                'so_chan': f'{list_of_dicts}'
            }

            result_limit = requests.post(
                API_URL+"/chan_so/api_chan_so.php", data=data)

            try:

                result_limit = f"{result_limit.text}"

                if result_limit:

                    result_limit = json.loads(result_limit)

                    if result_limit['success'] == 1:
                        await context.bot.send_message(chat_id=update.message.chat_id, text="Lưu chặn số thành công", parse_mode=ParseMode.HTML)

            except json.decoder.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")

    else:

        await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi \n Tin của bạn không đúng định dạng đã có.", parse_mode=ParseMode.HTML)




async def handleLimitMaxPriceMB(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_text = update.message.text

    # Loại bỏ kí tự chặn số

    message_text = message_text.replace("/hmmb", '')

    message_text = message_text.strip()

    message_text = await chuanhoa(message_text)

    message_text = re.sub(
        r'(da|b|x|dx|dd|lo+)(da|b|x|dx|dd|lo+)', r'\1 \2', message_text)

    message_text = re.sub(r'(\d+)([a-zA-z]+)', r'\1 \2', message_text)

    message_text = re.sub(r'([a-zA-z]+)(\d+)', r'\1 \2', message_text)

    user = update.message.chat.title

    user = user.replace(" ", "_")

    data = {

        'ten_tai_khoan': f'{user}',
        'action': 'cai_dat_han_muc',
        'so_chan': f'{message_text}',
        'vung_mien': 'mb'
    }

    

    try:

        result_limit = requests.post(API_URL+"/chan_so/api_chan_so.php", data=data)

        result_limit = f"{result_limit.text}"

        if result_limit:

            result_limit = json.loads(result_limit)

            if result_limit['success'] == 1:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Lưu hạn mức thành công", parse_mode=ParseMode.HTML)

    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi \n Tin của bạn không đúng định dạng đã có.", parse_mode=ParseMode.HTML)


async def handleLimitMaxPriceMN(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_text = update.message.text

    # Loại bỏ kí tự chặn số

    message_text = message_text.replace("/hmmn", '')

    message_text = message_text.strip()

    message_text = await chuanhoa(message_text)

    message_text = re.sub(
        r'(da|b|x|dx|dd|lo+)(da|b|x|dx|dd|lo+)', r'\1 \2', message_text)

    message_text = re.sub(r'(\d+)([a-zA-z]+)', r'\1 \2', message_text)

    message_text = re.sub(r'([a-zA-z]+)(\d+)', r'\1 \2', message_text)

    user = update.message.chat.title

    user = user.replace(" ", "_")

    type_tin = 'current'

    # kiểm tra message nếu chỉ có đài và điểm hoặc chỉ có điểm ==> lưu lại theo cách tính khác
    temp_message_text = message_text.split(" ")

    temp_message_text = list(filter(lambda x: x != "", temp_message_text))

    if len(temp_message_text) <= 2 and len(temp_message_text) > 0:
        print("tin chỉ có đài và điểm hoặc chỉ có điểm")
        # kiểm tra vị trí thứ nhất nếu là số thì đó là điểm chặn
        if is_number(temp_message_text[0]):
            type_tin = 'only_diem'
        else:
            type_tin = 'dai_and_diem'

    data = {

        'ten_tai_khoan': f'{user}',
        'action': 'cai_dat_han_muc',
        'so_chan': f'{message_text}',
        'vung_mien': 'mn',
        'type_tin': f'{type_tin}'
    }

    result_limit = requests.post(API_URL+"/chan_so/api_chan_so.php", data=data)

    try:

        result_limit = f"{result_limit.text}"

        if result_limit:

            result_limit = json.loads(result_limit)

            if result_limit['success'] == 1:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Lưu hạn mức thành công", parse_mode=ParseMode.HTML)

    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi \n Tin của bạn không đúng định dạng đã có.", parse_mode=ParseMode.HTML)


async def handleLimitMaxPriceMT(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_text = update.message.text

    # Loại bỏ kí tự chặn số

    message_text = message_text.replace("/hmmt", '')

    message_text = message_text.strip()

    message_text = await chuanhoa(message_text)

    message_text = re.sub(
        r'(da|b|x|dx|dd|lo+)(da|b|x|dx|dd|lo+)', r'\1 \2', message_text)

    message_text = re.sub(r'(\d+)([a-zA-z]+)', r'\1 \2', message_text)

    message_text = re.sub(r'([a-zA-z]+)(\d+)', r'\1 \2', message_text)

    user = update.message.chat.title

    user = user.replace(" ", "_")

    data = {

        'ten_tai_khoan': f'{user}',
        'action': 'cai_dat_han_muc',
        'so_chan': f'{message_text}',
        'vung_mien': 'mt'
    }

    result_limit = requests.post(API_URL+"/chan_so/api_chan_so.php", data=data)

    try:

        result_limit = f"{result_limit.text}"

        if result_limit:

            result_limit = json.loads(result_limit)

            if result_limit['success'] == 1:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Lưu hạn mức thành công", parse_mode=ParseMode.HTML)

    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")

        await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi \n Tin của bạn không đúng định dạng đã có.", parse_mode=ParseMode.HTML)


async def handleLimitStation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_text = update.callback_query.data

    # kiểm tra xem tin có bắt đầu bằng tên đài hay không

    if message_text:

        # xoá kí tự mẫu
        message_text = message_text.replace("STATION_", '')

        message_text = message_text.strip()

        # cắt chuỗi đã có thành mảng với giá trị đài và vung miền

        message_text = message_text.split("-")

        user = update.callback_query.message.chat.title

        user = user.replace(" ", "_")

        data = {

            'ten_tai_khoan': f'{user}',
            'action': 'chan_dai',
            'dai_chan': f'{message_text[0].lower()}',
            'vung_mien': f'{message_text[1].lower()}'
        }

        result_limit = requests.post(
            API_URL+"/chan_so/api_chan_so.php", data=data)

        try:

            result_limit = f"{result_limit.text}"

            if result_limit:

                result_limit = json.loads(result_limit)

                if result_limit['success'] == 1:
                    await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="Lưu chặn đài thành công", parse_mode=ParseMode.HTML)

        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")

    else:

        await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi \n Tin của bạn không đúng định dạng đã có.", parse_mode=ParseMode.HTML)


async def config_limit_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton(f"Chặn đài", callback_data="LIMIT_NUMBER_STATION"), InlineKeyboardButton(f"Huỷ chặn đài", callback_data="CANCEL_LIMIT_STATION")],
        # [InlineKeyboardButton(
        #     f"Chặn đài", callback_data="LIMIT_NUMBER_STATION")],
        [InlineKeyboardButton(f"Chặn số theo miền",
                              callback_data="LIMIT_NUMBER_AREA")],
        [InlineKeyboardButton(f"Chặn theo đài và loại", callback_data="LIMIT_NUMBER_WITH_STATION_AND_TYPE")],
        [InlineKeyboardButton(f"<<< Quay lại", callback_data="BACK_STEP")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text='Chọn loại cài đặt', reply_markup=reply_markup)


async def pick_limit_station(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    query.answer()

    keyboard_mn = [
        [InlineKeyboardButton(
            f"==Miền Bắc==", callback_data="LIMIT_NUMBER_STATION")],

        [InlineKeyboardButton(f"MB", callback_data="STATION_MB-MB")],

        [InlineKeyboardButton(
            f"==Miền Nam==", callback_data="LIMIT_NUMBER_STATION")],

        [InlineKeyboardButton(f"AG", callback_data="STATION_AG-MN"),
         InlineKeyboardButton(f"BD", callback_data="STATION_BD-MN"),
         InlineKeyboardButton(f"BL", callback_data="STATION_BL-MN"),
         InlineKeyboardButton(f"BT", callback_data="STATION_BT-MN"),
         InlineKeyboardButton(f"BTH", callback_data="STATION_BTH-MN"),
         InlineKeyboardButton(f"BP", callback_data="STATION_BP-MN"),
         InlineKeyboardButton(f"CM", callback_data="STATION_CM-MN")],

        [InlineKeyboardButton(f"CT", callback_data="STATION_CT-MN"),
         InlineKeyboardButton(f"ĐL", callback_data="STATION_DL-MN"),
         InlineKeyboardButton(f"ĐN", callback_data="STATION_DN-MN"),
         InlineKeyboardButton(f"ĐT", callback_data="STATION_DT-MN"),
         InlineKeyboardButton(f"HG", callback_data="STATION_HG-MN"),
         InlineKeyboardButton(f"KG", callback_data="STATION_KG-MN"),
         InlineKeyboardButton(f"LA", callback_data="STATION_LA-MN")],

        [InlineKeyboardButton(f"ST", callback_data="STATION_ST-MN"),
         InlineKeyboardButton(f"TG", callback_data="STATION_TG-MN"),
         InlineKeyboardButton(f"TN", callback_data="STATION_TN-MN"),
         InlineKeyboardButton(f"TP", callback_data="STATION_TP-MN"),
         InlineKeyboardButton(f"TV", callback_data="STATION_TV-MN"),
         InlineKeyboardButton(f"VT", callback_data="STATION_VT-MN"),
         InlineKeyboardButton(f"VL", callback_data="STATION_VL-MN")],


        [InlineKeyboardButton(
            f"==Miền Trung==", callback_data="LIMIT_NUMBER_STATION")],

        [InlineKeyboardButton(f"PY", callback_data="STATION_PY-MT"),
         InlineKeyboardButton(f"HUE", callback_data="STATION_HUE-MT"),
         InlineKeyboardButton(f"DL", callback_data="STATION_DL-MT"),
         InlineKeyboardButton(f"QN", callback_data="STATION_QN-MT"),
         InlineKeyboardButton(f"DN", callback_data="STATION_DN-MT"),
         InlineKeyboardButton(f"KH", callback_data="STATION_KH-MT"),
         InlineKeyboardButton(f"BD", callback_data="STATION_BD-MT")],

        [InlineKeyboardButton(f"QT", callback_data="STATION_QT-MT"),
         InlineKeyboardButton(f"QB", callback_data="STATION_QB-MT"),
         InlineKeyboardButton(f"GL", callback_data="STATION_GL-MT"),
         InlineKeyboardButton(f"NTH", callback_data="STATION_NTH-MT"),
         InlineKeyboardButton(f"QNG", callback_data="STATION_QNG-MT"),
         InlineKeyboardButton(f"DNO", callback_data="STATION_DNO-MT"),
         InlineKeyboardButton(f"KT", callback_data="STATION_KT-MT")],

        [InlineKeyboardButton(f"<<< Quay lại", callback_data="BACK_STEP")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard_mn)

    await query.edit_message_text(text='Chọn đài', reply_markup=reply_markup)


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    user = update.callback_query.message.chat.title

    user = user.replace(" ", "_")

    if query.data == "LIMIT_NUMBER":

        await config_limit_number(update, context)
        await updateTypeMessage(user, 'TYPE_MESSAGE', "LIMIT_NUMBER")

    elif query.data == "CONFIG_PRICE":

        await updateTypeMessage(user, 'TYPE_MESSAGE', "CONFIG_PRICE")

        await fetch_config_price(update, context)

    elif query.data == 'LIMIT_NUMBER_STATION':

        await pick_limit_station(update, context)

    elif query.data == 'LIMIT_NUMBER_AREA':

        await query.edit_message_text(text="- Cách thêm: /chanso [miền] [đài] [số]\n" +
                                    #   "- Cách hủy: gởi một lệnh trống để hủy chặn (/chanso)\n" +
                                      "- Tin VD:\n" +
                                      "/chanso mn mt 39 79 938 mb 68 86\n"+
                                      "/chanso vl 39 79 938 mb 68 86")

    elif query.data == 'LIMIT_NUMBER_WITH_STATION_AND_TYPE':

        await query.edit_message_text(text="/chanloai_[mien]\n" +
                                      "/chanloai_mb\n" +
                                      "mb: 00 11 22 33 44 55 66 77 88 99 da0n .\n" +
                                      "ag bt tp: 39 79 dd500n lo100n 739 938 xc20n .\n" +
                                      "cm ct: 7777 lo0n .")

    elif query.data.startswith('STATION_'):

        await handleLimitStation(update, context)

    elif query.data == 'BACK_STEP':

        keyboard = [
            [InlineKeyboardButton(f"Chặn", callback_data="LIMIT_NUMBER"), InlineKeyboardButton(
                f"Giá", callback_data="CONFIG_PRICE"), InlineKeyboardButton(f"Hạn mức", callback_data="MAX_PRICE")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text='Chọn loại cài đặt', reply_markup=reply_markup)

    elif query.data == 'MAX_PRICE':

        await query.edit_message_text(text="/hm[miền] [đài] [kiểu] [điểm]\n" +
                                      "/hmmb vl 12 dd dx 100\n" +
                                      "/hmmt vl  100\n" +
                                      "/hmmn 100\n")

    elif query.data == 'UP_PRICE':

        await query.edit_message_text(text="/td[miền]\n"+
                                      "/tdmb\n" +
                                      '[đài]: [so] [kieu] [tien]'
                                      "vl tp ag: dd bl dx 100 - 20/01/2023 .\n")
    
    
    elif query.data == 'CANCEL_LIMIT_STATION':

        data = {

            'ten_tai_khoan': f'{user}',
            'action': 'list_tin_huy',
            
        }

        try:

            result_limit = requests.post(API_URL+"/huychanso/api_huy_chan_so.php", data=data)

            result_limit = f"{result_limit.text}"

            if result_limit:

                result_limit = json.loads(result_limit)

                if result_limit['success'] == 1 and len(result_limit['lst_number_limit']) > 0:


                    lst_number_limit = result_limit['lst_number_limit']
                    
                    str_list_number = ""

                    for number_limit in lst_number_limit:
                        
                        str_list_number += f"Mã: {number_limit['id_limit']} - {number_limit['vung_mien']} {number_limit['number_limit']} {number_limit['dai_limit'] or ''} {number_limit['kieu_so'] or ''}\n"


                    await query.edit_message_text(text="/huychan [mã lệnh] \n "+ str_list_number)

        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")


    else:

        await query.edit_message_text(text=f"Đang tổng hợp báo cáo chờ giây lát ....", parse_mode=ParseMode.HTML)

        await fetchReport(update, context, query.data)


async def funcHandleDeleteTin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.chat.title

    user = user.replace(" ", "_")

    data = {

        'ten_tai_khoan': f'{user}',
        'action': 'xoa_tin',
        'message_id': f'{update.message.reply_to_message.message_id}'
    }

    result_limit = requests.post(API_URL+"/chan_so/api_chan_so.php", data=data)

    try:

        result_limit = f"{result_limit.text}"

        if result_limit:

            result_limit = json.loads(result_limit)

            if result_limit['success'] == 1:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Xoá tin thành công", parse_mode=ParseMode.HTML)
            else:
                await context.bot.send_message(chat_id=update.message.chat_id, text="Lỗi. Xoá tin", parse_mode=ParseMode.HTML)

    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")


async def handlerListenMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global setting
    setting = await callDataSeting(update.message.chat.title)

    current_time = datetime.now().time()

    if update.message.reply_to_message and update.message.text == 'huy':
        print("huy")
        await funcHandleDeleteTin(update, context)

    else:

        if setting['TYPE_MESSAGE'] == 'MB':

            if datetime.strptime(setting["TIME_REPORT_MB"], "%H:%M:%S").time() >= current_time:
                await create_number_mb(update, context)
            else:
                await update.message.reply_text(text="Lỗi. Không trong thời gian nhận tin", parse_mode=ParseMode.HTML)

        if setting['TYPE_MESSAGE'] == 'MN':

            if datetime.strptime(setting["TIME_REPORT_MN"], "%H:%M:%S").time() >= current_time:
                await create_number_mn(update, context)
            else:
                await update.message.reply_text(text="Lỗi. Không trong thời gian nhận tin", parse_mode=ParseMode.HTML)

        if setting['TYPE_MESSAGE'] == 'MT':

            if datetime.strptime(setting["TIME_REPORT_MT"], "%H:%M:%S").time() >= current_time:
                await create_number_mt(update, context)
            else:
                await update.message.reply_text(text="Lỗi. Không trong thời gian nhận tin", parse_mode=ParseMode.HTML)

        if setting['TYPE_MESSAGE'] == "CONFIG_PRICE":

            await update_config_price(update, context)


        if setting['TYPE_MESSAGE'] == "LIMIT_NUMBER":

            await config_limit_number(update, context)



def main():

    global setting

    app = Application.builder().token(TOKEN).build()

    # command
    app.add_handler(CommandHandler('start', start))

    app.add_handler(CommandHandler('mb', sendMessageMB))

    app.add_handler(CommandHandler('mn', sendMessageMN))

    app.add_handler(CommandHandler('mt', sendMessageMT))

    app.add_handler(CommandHandler('baocao', select_report))

    app.add_handler(CommandHandler('caidat', select_setting))

    app.add_handler(CommandHandler('chanso', handleLimitStationNumber))

    app.add_handler(CommandHandler('chanloai_mb', handleLimitTypeStationNumberMB))

    app.add_handler(CommandHandler('chanloai_mn', handleLimitTypeStationNumberMN))

    app.add_handler(CommandHandler('chanloai_mt', handleLimitTypeStationNumberMT))

    app.add_handler(CommandHandler('hmmb', handleLimitMaxPriceMB))

    app.add_handler(CommandHandler('hmmt', handleLimitMaxPriceMT))

    app.add_handler(CommandHandler('hmmn', handleLimitMaxPriceMN))

    app.add_handler(CommandHandler('tdmb', handleUpPriceMB))
    app.add_handler(CommandHandler('tdmt', handleUpPriceMT))
    app.add_handler(CommandHandler('tdmn', handleUpPriceMN))

    app.add_handler(CommandHandler('huongdan', funcHandleHuongDan))

    app.add_handler(CommandHandler('huychan', funcHandleHuyChan))

    app.add_handler(MessageHandler(filters.ChatType.GROUP &
                    filters.TEXT, handlerListenMessage))

    app.add_handler(CallbackQueryHandler(button_click))

    app.run_polling(poll_interval=5)


if __name__ == '__main__':
    main()
