import os
from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client

def read_sms():
    ip = os.getenv("MODEM_IP", "192.168.110.254")
    user = os.getenv("MODEM_USER", "admin")
    password = os.getenv("MODEM_PASS", "admin")

    # Используем f-строку для формирования URL
    url = f"http://{user}:{password}@{ip}/"

    try:
        with Connection(url) as connection:
            client = Client(connection)
            # Получаем список SMS (BoxType 1 = Входящие)
            sms = client.sms.get_sms_list(1, 1, 10, 0, 0, 1)

            messages = sms.get('Messages', {}).get('Message')
            if not messages:
                print("Сообщений нет.")
                return

            if isinstance(messages, dict): messages = [messages]

            for m in messages:
                print(f"[{m.get('Date')}] {m.get('Phone')}: {m.get('Content')}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    read_sms()
