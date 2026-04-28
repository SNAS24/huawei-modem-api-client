from bs4 import BeautifulSoup
import re
MODEM_LINK = 'http://192.168.110.254/'
HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://homerouter.cpe/',
    'Host': 'homerouter.cpe',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer': 'http://homerouter.cpe/html/sms/message.asp',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

def get_and_clean_sms(session):
    # 1. Загружаем страницу входящих
    resp = session.get(f'{MODEM_LINK}html/sms/inbox.asp', headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    messages = []
    # Ищем все строки таблицы с ID, начинающимся на inbox_record
    rows = soup.find_all('tr', id=re.compile(r'^inbox_record_'))
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 5: continue
        
        # Извлекаем ID для удаления из функции onclick="deleteItem('9')"
        delete_link = row.find('a', onclick=re.compile(r'deleteItem'))
        sms_id = re.search(r"deleteItem\('(\d+)'\)", delete_link['onclick']).group(1)
        
        msg = {
            'id': sms_id,
            'sender': cells[2].get_text(strip=True),
            'content': cells[3].get_text(strip=True),
            'date': cells[4].get_text(strip=True)
        }
        messages.append(msg)
        print(f"Найдено SMS от {msg['sender']}: {msg['content'][:30]}...")

    return messages

def delete_sms(session, sms_id):
    # Тот самый запрос для удаления
    url = f'{MODEM_LINK}html/sms/deleteSms.cgi?RequestFile=/html/sms/message.asp'
    data = {'Index': sms_id}
    try:
        r = session.post(url, data=data, headers=HEADERS)
        if r.status_code == 200:
            print(f"SMS ID {sms_id} удалено.")
            return True
    except Exception as e:
        print(f"Ошибка при удалении {sms_id}: {e}")
    return False

# ПРИМЕР ИСПОЛЬЗОВАНИЯ В ВАШЕМ ЦИКЛЕ:
# with requests.Session() as s:
#     # ... ваша авторизация ...
#     inbox = get_and_clean_sms(s)
#     for sms in inbox:
#         # Если нужно удалить после прочтения:
#         delete_sms(s, sms['id'])
