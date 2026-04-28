import huaweisms.api.user
import huaweisms.api.sms

def read_modem_sms(ip, username, password):
    # 1. Авторизация и получение контекста сессии
    try:
        ctx = huaweisms.api.user.quick_login(username, password, modem_host=ip)
        print(f"Статус подключения: {ctx}")
    except Exception as e:
        return f"Ошибка входа: {e}"

    # 2. Получение списка SMS
    # box_type=1 — входящие (inbox), qty=10 — количество сообщений
    try:
        sms_list = huaweisms.api.sms.get_sms(ctx, box_type=1, qty=10)
        
        messages = []
        if sms_list and 'response' in sms_list and 'Messages' in sms_list['response']:
            msg_data = sms_list['response']['Messages']['Message']
            
            # Если сообщение одно, API возвращает словарь, если много — список
            if isinstance(msg_data, dict):
                msg_data = [msg_data]
                
            for msg in msg_data:
                messages.append({
                    "от": msg.get('Phone'),
                    "текст": msg.get('Content'),
                    "дата": msg.get('Date')
                })
        return messages
    except Exception as e:
        return f"Ошибка при чтении: {e}"

# Пример использования
MODEM_IP = "192.168.1.1"  # Проверьте IP вашего модема (обычно 192.168.1.1 или 192.168.8.1)
USER = "admin"
PASSWORD = "your_password"

sms_inbox = read_modem_sms(MODEM_IP, USER, PASSWORD)

if isinstance(sms_inbox, list):
    for s in sms_inbox:
        print(f"[{s['дата']}] {s['от']}: {s['текст']}")
else:
    print(sms_inbox)
