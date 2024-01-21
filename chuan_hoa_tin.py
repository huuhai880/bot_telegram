import re

async def chuanhoa(current_tin):

    tin = current_tin

    # Chữ thường
    tin = tin.lower()
    
    # Bỏ unicode
   

    tin = tin.replace('đ', 'd')
    tin = tin.replace(
        'aáàảãạăắằẳẵặâấầẩẫậ',
        'a'
    )
    tin = tin.replace(
        'oóòỏõọôốồổỗộơớờởỡợ',
        'o'
    )
    tin = tin.replace(
        'uúùủũụưứừửữự',
        'u'
    )
    tin = tin.replace(
        'eéèẻẽẹêếềểễệ',
        'e'
    )
    tin = tin.replace(
        'dá',
        'da'
    )

    
    tin = tin.replace('đài', 'dai')

    tin = tin.replace('dài', 'dai')

    tin = tin.replace(',2d', '2d')

    tin = tin.replace('đầu', 'dau')

    tin = tin.replace('dàu', 'dau')

    tin = tin.replace('dầu', 'dau')

    tin = tin.replace('đâu', 'dau')

    tin = tin.replace('_',' ')
    tin = tin.replace(' ', "")
    
    tin = tin.replace(',,', " ")
    tin = re.sub(r'\d+\.{3}\d+', lambda match: match.group().replace('...', ' '), tin)
    tin = tin.replace("…", " ")
    # tin = tin.replace(",", " ")
    # tin = tin.replace(".,", " ")

    tin = tin.strip()
    
    return tin
