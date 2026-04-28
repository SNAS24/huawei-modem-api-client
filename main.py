import requests
import datetime
import re
from bs4 import BeautifulSoup
import os

ip = os.getenv("MODEM_IP", "192.168.110.254")
user = os.getenv("MODEM_USER", "admin")
password = os.getenv("MODEM_PASS", "admin")
MODEM_LINK = "http://192.168.110.254/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
LOGIN_DATA = {'Username': {user}, 'Password': {password}}

def get_session():
    """Создает авторизованную сессию"""
    s = requests.Session()
    # 1. Заходим на главную для получения кук
    s.get(MODEM_LINK, headers=HEADERS)
    # 2. Логинимся
    s.post(f'{MODEM_LINK}index/login.cgi', data=LOGIN_DATA, headers=HEADERS)
    return s

# def read_inbox(session):
#     """Читает список SMS и возвращает список словарей"""
#     response = session.get(f'{MODEM_LINK}html/sms/inbox.asp', headers=HEADERS)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     messages = []
#     # Ищем строки таблицы с SMS
#     rows = soup.find_all('tr', id=re.compile(r'^inbox_record_'))
    
#     for row in rows:
#         cells = row.find_all('td')
#         if len(cells) < 6: continue
        
#         # Извлекаем ID для удаления из функции onclick="deleteItem('9')"
#         del_onclick = row.find('a', onclick=re.compile(r'deleteItem'))['onclick']
#         sms_id = re.search(r"deleteItem\('(\d+)'\)", del_onclick).group(1)
        
#         messages.append({
#             'id': sms_id,
#             'sender': cells[2].get_text(strip=True),
#             'text': cells[3].get_text(strip=True),
#             'date': cells[4].get_text(strip=True)
#         })
#     return messages

def read_inbox(session):
    response = session.get(f'{MODEM_LINK}html/sms/inbox.asp', headers=HEADERS)
    # Если модем отдает кодировку некорректно, раскомментируйте строку ниже:
    # response.encoding = 'utf-8' 
    
    soup = BeautifulSoup(response.text, 'html.parser')
    messages = []
    
    # Находим все строки TR, которые начинаются на inbox_record_
    rows = soup.find_all('tr', id=re.compile(r'^inbox_record_\d+$'))
    
    if not rows:
        print("DEBUG: Строки в таблице не найдены. Проверьте авторизацию.")
        return []

    for row in rows:
        # Получаем порядковый номер строки из id (например, '1' из 'inbox_record_1')
        row_num = row['id'].split('_')[-1]
        
        # 1. Отправитель (id заканчивается на _2)
        sender_div = row.find(id=f'inbox_record_{row_num}_2')
        sender = sender_div.get_text(strip=True) if sender_div else "Неизвестен"
        
        # 2. Текст сообщения (div с name="divContentName")
        content_div = row.find('div', {'name': 'divContentName'})
        content = content_div.get_text(strip=True) if content_div else "Пусто"
        
        # 3. Дата (обычно это 5-й по счету TD)
        cells = row.find_all('td')
        date = cells[4].get_text(strip=True) if len(cells) > 4 else "Нет даты"
        
        # 4. ID для удаления из ссылки onclick
        del_link = row.find('a', onclick=re.compile(r'deleteItem'))
        sms_id = re.search(r"deleteItem\('(\d+)'\)", del_link['onclick']).group(1) if del_link else None

        messages.append({
            'id': sms_id,
            'sender': sender,
            'text': content,
            'date': date
        })
        
    return messages



def delete_sms(session, sms_id):
    """Удаляет SMS по его ID"""
    url = f'{MODEM_LINK}html/sms/deleteSms.cgi?RequestFile=/html/sms/message.asp'
    session.post(url, data={'Index': sms_id}, headers=HEADERS)

# --- ГЛАВНЫЙ ЦИКЛ ПРИЛОЖЕНИЯ ---
if __name__ == "__main__":
    with get_session() as s:
        # 1. Читаем сообщения
        inbox = read_inbox(s)
        
        for sms in inbox:
            print(f"Новое сообщение от {sms['sender']}: {sms['text']}")
            
            # 2. Пример логики: если в тексте есть ссылка, удаляем SMS
            if "http" in sms['text']:
                print(f"Удаляем сервисное сообщение {sms['id']}...")
                #delete_sms(s, sms['id'])

        # 3. Ваша существующая функция отправки (теперь может использовать ту же сессию s)
        # sendSms("Проверка связи", session=s) 
