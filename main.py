import os
import huaweisms.api.user
import huaweisms.api.sms

def read_modem_sms():
    # Берем настройки из переменных окружения Docker
    ip = os.getenv("MODEM_IP", "192.168.1.1")
    user = os.getenv("MODEM_USER", "admin")
    password = os.getenv("MODEM_PASS", "admin")

    try:
        ctx = huaweisms.api.user.quick_login(user, password, modem_host=ip)
        sms_list = huaweisms.api.sms.get_sms(ctx, box_type=1, qty=10)
        
        if sms_list and 'response' in sms_list and 'Messages' in sms_list['response']:
            msg_data = sms_list['response']['Messages']['Message']
            if isinstance(msg_data, dict): msg_data = [msg_data]
            for msg in msg_data:
                print(f"[{msg.get('Date')}] {msg.get('Phone')}: {msg.get('Content')}")
        else:
            print("Входящих сообщений нет.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    read_modem_sms()
