from supabase import create_client, Client

url: str = "https://arcqzcecekxwhwrlccpz.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyY3F6Y2VjZWt4d2h3cmxjY3B6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDMwNjQwODgsImV4cCI6MjAxODY0MDA4OH0.HcI01HT5QTOsI1rkHmW3W2UL2wh2ggz9fIiHIsuX1xE"
supabase: Client = create_client(url, key)


setting = {}


async def checkExistsAccount(_user):
    print("Kiểm tra xem có account setting chưa")
    reslut_setting = supabase.table('setting').select('key_setting,value').eq('account', _user).execute()

    if len(reslut_setting.data) == 0:

        supabase.table('setting')\
            .insert([
                {"value": '16:10:00', "account": _user,"key_setting":"TIME_REPORT_MN"},
                {"value": '18:10:00', "account": _user,"key_setting":"TIME_REPORT_MB"},
                {"value": '17:10:00', "account": _user,"key_setting":"TIME_REPORT_MT"},
                {"value": 'MB', "account": _user,"key_setting":"TYPE_MESSAGE"},
                {"value": '0', "account": _user,"key_setting":"COUNT_MESSAGE"},
            ])\
            .execute()



async def callDataSeting(user):

    global setting

    _user = user.replace(" ","_")

    await checkExistsAccount(_user)

    # lấy thông tin cài đặt
    reslut_setting = supabase.table('setting').select('key_setting,value').eq('account', _user).execute()

    setting = reslut_setting.data

    my_dict = {}  # Initialize the dictionary outside the loop

    if len(reslut_setting.data) > 0:

        for index in range(0, len(reslut_setting.data)):
            print(reslut_setting.data[index])
            my_dict[reslut_setting.data[index]['key_setting']] = reslut_setting.data[index]['value']

        setting = my_dict
    
    return setting
    

async def updateTypeMessage(user,key_setting, value):

    _user = user.replace(" ","_")

    await checkExistsAccount(_user)

    supabase.table('setting').update({"value": value}).eq('account', _user).eq('key_setting', key_setting).execute()
    
