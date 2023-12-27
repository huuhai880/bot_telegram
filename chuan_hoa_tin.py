import re

async def chuanhoa(tin):
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

    tin = tin.replace('/',' ')
    tin = tin.replace('_',' ')
    tin = tin.replace(' ', "")
    tin = tin.replace(',,', " ")
    tin = re.sub(r'\d+\.{3}\d+', lambda match: match.group().replace('...', ' '), tin)
    tin = tin.replace("…", " ")
    # tin = tin.replace(",", " ")
    # tin = tin.replace(".,", " ")


    tin = tin.strip()
    
    return tin
