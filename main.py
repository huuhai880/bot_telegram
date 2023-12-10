from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import requests
import json
from datetime import date, timedelta
from telegram.constants import ParseMode
from prettytable import PrettyTable


# Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
TOKEN = '6971027835:AAEM-raPv8-lStXEJpUe9TrIJu6apjUZp3M'
API_URL = 'http://localhost:9000'

today = date.today()


type_message = 'MB'

file_path = 'Ket_qua.html'

count = 0

def addChar(char, count):
    text = ''

    for j in range(count):

        text += f'{char}'
    
    return text


def splitString (val, number, char) :
    if not val : 
        return addChar(char, number)
    
    if len(str(val)) > number : 
        return f"{str(val)}"[:number - 1] + char
    
    else :
        return f"{str(val)}{addChar(char, number - len(str(val)))}"

def formatMoney(val) :

    if not val : 
        return '0'
    else :

        formatted_number = f"{val:,.0f}"

        return formatted_number


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f"Hello {user.first_name}! I'm your bot. How can I help you?")


async def sendMessageMB(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global type_message, count
    type_message = 'MB'
    message_text = "<code>=== BẮT ĐẦU NHẬP CHO MB ===</code>"
    count = 1
    await context.bot.send_message(chat_id=update.message.chat_id, text=message_text, parse_mode=ParseMode.HTML)


async def sendMessageMN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global type_message, count
    type_message = 'MN'
    message_text = "<code>=== BẮT ĐẦU NHẬP CHO MN ===</code>"
    count = 1
    await context.bot.send_message(chat_id=update.message.chat_id, text=message_text, parse_mode=ParseMode.HTML)


async def sendMessageMT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global type_message, count
    type_message = 'MT'
    message_text = "<code>=== BẮT ĐẦU NHẬP CHO MT ===</code>\n"
    count = 1
    await context.bot.send_message(chat_id=update.message.chat_id, text=message_text, parse_mode=ParseMode.HTML)


# async def writeHTMLFile(ds_chi_tiet=[], ma_lenh='', data_list=[]):

#     with open(file_path, 'r') as file:
#         html_content = file.read()
    
#     item_table =''

#     for tin in ds_chi_tiet:

#         _dai = tin['dai']

#         if type_message == 'MB':
#             _dai = 'mb'

#         item_table += f"""<tr>
#                         <td>{_dai}</td>
#                         <td>{tin['so']}</td>
#                         <td>{tin['kieu']}</td>
#                         <td>{tin['diem']}</td>
#                         <td>{formatMoney(tin['tien'])}</td>
#                     </tr>"""
    
#     item_kieu_danh=''

#     for keu_danh in data_list:

#         if formatMoney(keu_danh['xac']) !='0' or formatMoney(keu_danh['thuc_thu']) != '0' :
#             item_table += f"""<p>Kiểu: {keu_danh['kieu']}</p>
#             <p>Xác: {formatMoney(keu_danh['xac'])}</p>
#             <p>Tổng tiền: {formatMoney(keu_danh['thuc_thu'])}</p>"""

#     new_paragraph = """
#             <!DOCTYPE html>
#             <html lang="en">
#             <head>
#                 <meta charset="UTF-8">
#                 <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                 <title>HTML Table with 5 Columns</title>
#                 <style>
#                     table {
#                         width: 100%;
#                         border-collapse: collapse;
#                         margin-top: 20px;
#                     }

#                     th, td {
#                         border: 1px solid #ddd;
#                         padding: 8px;
#                         text-align: left;
#                     }

#                     th {
#                         background-color: #f2f2f2;
#                     }
#                 </style>
#             </head>
#             <body>

#             <h2>Thông tin chi tiết</h2>
#             <hr>
#             <p>Mã lệnh: """+ma_lenh+"""</p>
#             """+item_kieu_danh+""""

#             <table>
#                 <thead>
#                     <tr>
#                         <th>Đài</th>
#                         <th>Số</th>
#                         <th>Kiểu</th>
#                         <th>Điểm</th>
#                         <th>Tiền</th>
#                     </tr>
#                 </thead>
#                 <tbody>
#                     """+ item_table +"""""
#                 </tbody>
#             </table>
#             </body>
#             </html>
#         """
    

#     html_content = new_paragraph

#     with open(file_path, 'w') as file:
#         file.write(html_content)

async def writeHTMLFile(ds_chi_tiet=[], ma_lenh='', data_list=[]):

    with open(file_path, 'r') as file:
        html_content = file.read()
    
    item_table =''

    for key, value in ds_chi_tiet.items():
        print(f"Key: {key}")
        item_table += f"""<tr>
                    <td col='5'>{key}</td>
                </tr>"""
        
        for tin in value:

            _dai = tin['dai']

            if type_message == 'MB':
                _dai = 'mb'

            item_table += f"""<tr>
                <td>{_dai}</td>
                <td>{tin['so']}</td>
                <td>{tin['kieu']}</td>
                <td>{tin['diem']}</td>
                <td>{formatMoney(tin['tien'])}</td>
            </tr>"""
                
    item_kieu_danh=''

    for keu_danh in data_list:

        if formatMoney(keu_danh['xac']) !='0' or formatMoney(keu_danh['thuc_thu']) != '0' :
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
                        <th>Đài</th>
                        <th>Số</th>
                        <th>Kiểu</th>
                        <th>Điểm</th>
                        <th>Tiền</th>
                    </tr>
                </thead>
                <tbody>
                    """+ item_table +"""""
                </tbody>
            </table>
            </body>
            </html>
        """
    

    html_content = new_paragraph

    with open(file_path, 'w') as file:
        file.write(html_content)


async def create_number_mb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    global count

    day = today.strftime("%d-%m-%Y")
    
    #replace message 
    message_text = update.message.text
    user = update.message.from_user

    message_text = message_text.replace('/','')
    message_text = message_text.replace(' ', "")
    message_text = message_text.strip()

    if message_text:

        try:

            data = {
                'thoi_gian_danh': ''+day+'',
                'tai_khoan_danh': f'{update.message.chat.title}',
                'noi_dung': ''+str(message_text)+'',
                'action': 'luu',
                'account_create': ''+str(update.message.chat.title)+'',
                'vung_mien':'mb'
            }
            
            respone = requests.post(API_URL+"/mb/tin/api_tao_tin.php", data = data)

            
            result_tin = respone.text

            data_list = json.loads(result_tin)

            if data_list['status'] == 200 :
                
                ds_chi_tiet = data_list['ds_chi_tiet']

                data_list = list(data_list['data'].values())


                print(ds_chi_tiet)


                if len(ds_chi_tiet) >0:

                    await writeHTMLFile(ds_chi_tiet, message_text, data_list)
                
                
                total_xac = 0
                total_thuc_thu = 0
                total_trung = 0

                if len(data_list) > 0 :

                    result_string = f"OK MB - T{count}\n"

                    for tin in data_list:
                        if formatMoney(tin['xac']) !='0' or formatMoney(tin['thuc_thu']) != '0' :
                            
                            result_string += f"- {tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"
                            total_xac += tin['xac'] or 0
                            total_thuc_thu += tin['thuc_thu'] or 0
                            total_trung += tin['tien_trung'] or 0

                    result_string += f'TỔNG: {formatMoney(total_xac)}'

                    
                    with open(file_path, 'rb') as file:
                        count +=1
                        await update.message.reply_document(document=InputFile(file), caption=result_string,parse_mode =ParseMode.HTML)
                         
            else:

                await update.message.reply_text(data_list['message'],ParseMode.HTML)

        except Exception as e:
            # Log the exception using the logging module
            await update.message.reply_text(f"{e}")
            # Optionally, re-raise the exception
            raise


async def create_number_mn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global count

    day = today.strftime("%d-%m-%Y")
    
    #replace message 
    message_text = update.message.text
    user = update.message.from_user

    message_text = message_text.replace('/','')
    message_text = message_text.replace(' ', "")
    message_text = message_text.strip()
    
    if message_text:

        try:

            data = {
                'thoi_gian_danh': ''+day+'',
                'tai_khoan_danh': f'{update.message.chat.title}',
                'noi_dung': ''+message_text+'',
                'action': 'luu',
                'account_create': ''+str(update.message.chat.title)+'',
                'vung_mien':'mn'
            }
            
            respone = requests.post(API_URL+"/mn/tin/api_tao_tin.php", data = data)

            result_tin = respone.text

            print(result_tin)
            

            data_list = json.loads(result_tin)

            if data_list['status'] == 200 :
                
                ds_chi_tiet = data_list['ds_chi_tiet']

                data_list = list(data_list['data'].values())

                if len(ds_chi_tiet) >0:

                    await writeHTMLFile(ds_chi_tiet, message_text, data_list)

                total_xac = 0
                total_thuc_thu = 0
                total_trung = 0

                if len(data_list) > 0 :

                    result_string = f"OK MN - T{count}\n"

                    for tin in data_list:
                        if formatMoney(tin['xac']) !='0' or formatMoney(tin['thuc_thu']) != '0' :
                            
                            result_string += f"- {tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"
                            total_xac += tin['xac'] or 0
                            total_thuc_thu += tin['thuc_thu'] or 0
                            total_trung += tin['tien_trung'] or 0

                    result_string += f'TỔNG: {formatMoney(total_xac)}'
                    
                    with open(file_path, 'rb') as file:
                        count +=1
                        await update.message.reply_document(document=InputFile(file), caption=result_string,parse_mode =ParseMode.HTML)


            else:

                await update.message.reply_text(data_list['message'],ParseMode.HTML)

        except Exception as e:
            # Log the exception using the logging module
            await update.message.reply_text(f"{e}")
            # Optionally, re-raise the exception
            raise
    
async def create_number_mt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global count

    day = today.strftime("%d-%m-%Y")
    
    #replace message 
    message_text = update.message.text
    user = update.message.from_user

    message_text = message_text.replace('/','')
    message_text = message_text.replace(' ', "")
    message_text = message_text.strip()
    
    if message_text:

        try:

            data = {
                'thoi_gian_danh': ''+day+'',
                'tai_khoan_danh': f'{update.message.chat.title}',
                'noi_dung': ''+message_text+'',
                'action': 'luu',
                'account_create': ''+str(update.message.chat.title)+'',
                'vung_mien':'mt'
            }
            
            respone = requests.post(API_URL+"/mt/tin/api_tao_tin.php", data = data)

            
            result_tin = respone.text

            data_list = json.loads(result_tin)

            if data_list['status'] == 200 :
                
                ds_chi_tiet = data_list['ds_chi_tiet']

                data_list = list(data_list['data'].values())

                if len(ds_chi_tiet) >0:

                    await writeHTMLFile(ds_chi_tiet, message_text, data_list)

                total_xac = 0
                total_thuc_thu = 0
                total_trung = 0

                if len(data_list) > 0 :

                    result_string = f"OK MT - T{count}\n"

                    for tin in data_list:
                        if formatMoney(tin['xac']) !='0' or formatMoney(tin['thuc_thu']) != '0' :
                            
                            result_string += f"- {tin['kieu'].upper()}: {formatMoney(tin['xac'])}\n"
                            total_xac += tin['xac'] or 0
                            total_thuc_thu += tin['thuc_thu'] or 0
                            total_trung += tin['tien_trung'] or 0

                    result_string += f'TỔNG: {formatMoney(total_xac)}'
                    
                    with open(file_path, 'rb') as file:
                        count +=1
                        await update.message.reply_document(document=InputFile(file), caption=result_string,parse_mode =ParseMode.HTML)
                        
            else:

                await update.message.reply_text(data_list['message'],ParseMode.HTML)

        except Exception as e:
            # Log the exception using the logging module
            await update.message.reply_text(f"{e}")
            # Optionally, re-raise the exception
            raise

async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    day = today.strftime("%d-%m-%Y")
    user = update.message.from_user

    print(update.message.from_user.username)

    #replace message 
    message_text = update.message.text

    message_text = message_text.replace('/kt','')
    message_text = message_text.strip()
    
    if message_text:

        try:

            data = {
                'thoi_gian_danh': ''+day+'',
                'tai_khoan_danh': 'admin',
                'noi_dung': ''+message_text+'',
                'action': 'kiem_tra',
                'account_create': ''+str(user.username)+''
            }

            respone = requests.post(API_URL+"/tin/api_tao_tin.php", data = data)

            result_tin = respone.text
            print(result_tin)

            data_list = json.loads(result_tin)

            if data_list['status'] == 200 :
                
                data_list = list(data_list['data'].values())

                total_xac = 0
                total_thuc_thu = 0
                total_trung = 0

                if len(data_list) > 0 :
                    
                    result_string = f"Đã nghi nhận số của bạn"

                    result_string = f"""<code>{splitString("Kiểu",8,' ')}{splitString("Xác",8,' ')}{splitString("Thực Thu",12,' ')}{splitString("Trúng",8,' ')}</code>\n"""

                    result_string += f"""<code>================================================</code>\n"""
                    
                    for tin in data_list:
                        
                        result_string += f"""<code>{splitString(tin['kieu'] or '--',8,' ')}{splitString(formatMoney(tin['xac']),8,' ')}{splitString(formatMoney(tin['thuc_thu']),12,' ')}{splitString(formatMoney(tin['tien_trung']),8,' ')}</code>\n"""
                        total_xac += tin['xac'] or 0
                        total_thuc_thu += tin['thuc_thu'] or 0
                        total_trung += tin['tien_trung'] or 0

                    result_string += f"""<code>================================================</code>\n"""

                    result_string += f"""<code>{splitString('Tổng',8,' ')}{splitString(formatMoney(total_xac) ,8,' ')}{splitString(formatMoney(total_thuc_thu),12,' ')}{splitString(formatMoney(total_trung),8,' ')}</code>\n"""

                    
                    await update.message.reply_text(result_string,ParseMode.HTML)

            else:

                await update.message.reply_text(data_list['message'],ParseMode.HTML)

        except Exception as e:
            # Log the exception using the logging module
            await update.message.reply_text(f"{e}")
            # Optionally, re-raise the exception
            raise


async def fetchReport(update: Update, context: ContextTypes.DEFAULT_TYPE, date_report):
    
    #replace message 
    query = update.callback_query

    print(update.callback_query.message.chat.title)

    try:

        data = {
            'ngay': ''+date_report+'',
            'ten_tai_khoan': f'{update.callback_query.message.chat.title}',
            'loai_tai_khoan':'admin',
            'action': 'doc',
        }

        respone_mb = requests.post(API_URL+"/mb/thong_ke/api_thong_ke.php", data = data)

        result_report_mb = respone_mb.text
        
        report_mb_format = json.loads(result_report_mb)

        thong_ke_mb = json.loads(report_mb_format['thong_ke'])

        #mn

        respone_mn = requests.post(API_URL+"/mn/thong_ke/api_thong_ke.php", data = data)

        result_report_mn = respone_mn.text
        
        report_mn_format = json.loads(result_report_mn)

        thong_ke_mn = json.loads(report_mn_format['thong_ke'])

        #mt

        respone_mt = requests.post(API_URL+"/mt/thong_ke/api_thong_ke.php", data = data)

        result_report_mt = respone_mt.text
        
        report_mt_format = json.loads(result_report_mt)

        thong_ke_mt = json.loads(report_mt_format['thong_ke'])

        # tin_list_mt = json.loads(report_mt_format['tin_list'])

        # print(tin_list_mt)
        message_text = f"""<b>{splitString(date_report,15,' ')}</b>\n"""
        
        if 'mb' in thong_ke_mb:

            message_text += f"""=============================================\n"""

            message_text += f"""MB\n"""

            data_thong_ke_mb= thong_ke_mb['mb']

            message_text += f"""<code>{splitString("Số tin: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['so_tin']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("hai_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['hai_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("ba_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['ba_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("bon_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['bon_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Đá/ Đá xiên: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['da_daxien']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Tiền xác: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['xac']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Thực thu: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['thuc_thu']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Tiền Trúng: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['tien_trung']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Thắng/ Thua: ",15,' ')}{splitString(formatMoney(data_thong_ke_mb['thang_thua']),8,' ')}</code>\n"""
            message_text += f"""=============================================\n"""
            

        if 'mt' in thong_ke_mt:

            message_text += f"""MT\n"""

            data_thong_ke_mt= thong_ke_mt['mt']

            message_text += f"""<code>{splitString("Số tin :",15,' ')}{splitString(formatMoney(data_thong_ke_mt['so_tin']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("hai_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mt['hai_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("ba_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mt['ba_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("bon_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mt['bon_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Đá/ Đá xiên: ",15,' ')}{splitString(formatMoney(data_thong_ke_mt['da_daxien']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Tiền xác: ",15,' ')}{splitString(formatMoney(data_thong_ke_mt['xac']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Thực thu: ",15,' ')}{splitString(formatMoney(data_thong_ke_mt['thuc_thu']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Tiền Trúng: ",15,' ')}{splitString(formatMoney(data_thong_ke_mt['tien_trung']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Thắng/Thua: ",15,' ')}{splitString(formatMoney(data_thong_ke_mt['thang_thua']),8,' ')}</code>\n"""
            message_text += f"""=============================================\n"""
           
        if 'mn' in thong_ke_mn:

            message_text += f"""MN\n"""

            data_thong_ke_mn= thong_ke_mn['mn']

            message_text += f"""<code>{splitString("Số tin: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['so_tin']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("hai_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['hai_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("ba_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['ba_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("bon_c: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['bon_c']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Đá/ Đá xiên: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['da_daxien']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Tiền xác: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['xac']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Thực thu: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['thuc_thu']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Tiền Trúng: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['tien_trung']),8,' ')}</code>\n"""
            message_text += f"""<code>{splitString("Thắng/ Thua: ",15,' ')}{splitString(formatMoney(data_thong_ke_mn['thang_thua']),8,' ')}</code>\n"""
            

        await query.edit_message_text(text=message_text, parse_mode=ParseMode.HTML)
            
        
        

    except Exception as e:
        # Log the exception using the logging module
       
        await query.edit_message_text(text=f"{str(e)}",parse_mode=ParseMode.HTML)
        # Optionally, re-raise the exception
        raise


async def handlerListenMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):


    if type_message == 'MB':
       
        await create_number_mb(update, context)

    if type_message == 'MN':
       
        await create_number_mn(update, context)

    if type_message == 'MT':
       
        await create_number_mt(update, context)

async def select_report(update, context):


    keyboard = [
        [InlineKeyboardButton(f"{today.strftime('%d-%m')}", callback_data=f'{today.strftime("%d-%m-%Y")}')],
        [InlineKeyboardButton(f"{(today  - timedelta(days=1)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=1)).strftime('%d-%m-%Y')}")],
        
        [InlineKeyboardButton(f"{(today  - timedelta(days=2)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=2)).strftime('%d-%m-%Y')}"), InlineKeyboardButton(f"{(today  - timedelta(days=3)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=3)).strftime('%d-%m-%Y')}")],
       
        [InlineKeyboardButton(f"{(today  - timedelta(days=4)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=4)).strftime('%d-%m-%Y')}"),InlineKeyboardButton(f"{(today  - timedelta(days=5)).strftime('%d-%m')}", callback_data=f"{(today  - timedelta(days=5)).strftime('%d-%m-%Y')}")],
       
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    

    await update.message.reply_text('Chọn thời gian báo cáo:', reply_markup=reply_markup)

async def button_click(update, context):
    query = update.callback_query

    await fetchReport(update, context, query.data)
   


def main():

    app = Application.builder().token(TOKEN).build()

    # command
    app.add_handler(CommandHandler('start', start))

    app.add_handler(CommandHandler('mb', sendMessageMB))

    app.add_handler(CommandHandler('mn', sendMessageMN))

    app.add_handler(CommandHandler('mt', sendMessageMT))

    app.add_handler(CommandHandler('baocao', select_report))

    app.add_handler(MessageHandler(filters.ChatType.GROUP & filters.TEXT, handlerListenMessage))

    app.add_handler(CallbackQueryHandler(button_click))
    

    
    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()  
