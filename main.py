from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import json
from datetime import date
from telegram.constants import ParseMode

# Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
TOKEN = '6971027835:AAEM-raPv8-lStXEJpUe9TrIJu6apjUZp3M'
API_URL = 'http://localhost:9000'

today = date.today()


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
        return '0.0'
    else :
        return val


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f"Hello {user.first_name}! I'm your bot. How can I help you?")

async def create_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    day = today.strftime("%d-%m-%Y")
    
    #replace message 
    message_text = update.message.text
    user = update.message.from_user

    message_text = message_text.replace('/','')
    message_text = message_text.strip()
    
    if message_text:

        try:

            data = {
                'thoi_gian_danh': ''+day+'',
                'tai_khoan_danh': 'admin',
                'noi_dung': ''+message_text+'',
                'action': 'luu',
                'account_create': ''+str(user.id)+''
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

                    result_string += f"""<code>{splitString('',8,' ')}{splitString(formatMoney(total_xac) ,8,' ')}{splitString(formatMoney(total_thuc_thu),12,' ')}{splitString(formatMoney(total_trung),8,' ')}</code>\n"""

                    
                    await update.message.reply_text(result_string,ParseMode.HTML)


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
                'account_create': ''+str(user.id)+''
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

    
def main():

    app = Application.builder().token(TOKEN).build()

    # command
    app.add_handler(CommandHandler('start', start))

    app.add_handler(CommandHandler('mb', create_number))

    app.add_handler(CommandHandler('mn', create_number))

    app.add_handler(CommandHandler('kt', check_number))

    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()  
