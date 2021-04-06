from datetime import datetime

def format_date(date):
    if date == None:
        return None

    return date.strftime('%Y-%m-%d')

def parse_date(date_str):
    if date_str == "":
        return None

    datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')

    return datetime_obj.date()

def parse_str(val_str):
    if val_str == "":
        return None

    return val_str

def parse_int(int_str):
    if int_str == "":
        return None

    return int(int_str)

def parse_float(float_str):
    if float_str == "":
        return None

    return float(float_str)
