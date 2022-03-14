import telegram_send

conf=""
text={'Någon ringer på dörren!'}

def toTelegram(): 
    telegram_send.send(messages=text, conf=conf)
    
