from bs4 import BeautifulSoup
import requests
import time
import send_mail

seconds = 3600.0
start_time = time.time()

page_link = 'https://www.iski.istanbul/web/tr-TR/ariza-kesinti'

semt = 'Fatih'
mah = 'Aksaray'
is_there_semt = False
is_there_mah = False

first_line = ''
second_line = ''

excluded_texts = ['', ':', 'Açıklama', 'İlçe', 'Etkilenen Mahalleler', 'Başlama Tarihi', 'Bitiş Tarihi']


def indexes(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset)


def time_stamp():
    print(time.strftime('%d %b %Y - %H:%M:%S'))


while True:
    clean_page_txt = []

    # fetch the content from url
    page_response = requests.get(page_link, timeout=5)
    # parse html
    page_content = BeautifulSoup(page_response.text, 'html.parser')

    targeted_class = page_content.find(class_='col-xs-12 col-sm-12 col-md-9 col-lg-9 sp-rightcol')
    targeted_class_items = targeted_class.find_all('td')

    for line in targeted_class_items:
        txt = line.get_text().strip()
        if txt in excluded_texts:
            continue
        else:
            clean_page_txt.append(txt.translate(str.maketrans({',': ' '})))

    for value in clean_page_txt:
        if (semt and mah) in value:
            is_there_semt = True
            is_there_mah = True
            break

    if is_there_semt and is_there_mah:
        index_list = indexes(clean_page_txt, semt)
        for i in index_list:
            if mah in clean_page_txt[i + 1]:
                extracted_info = clean_page_txt[i + 4][0:11] + clean_page_txt[i + 4][26:]
                time_stamp()
                print(semt + ', ' + mah + ' Mah: ')
                print(extracted_info)
                # send_mail.send(str(semt + ', ' + mah + ' Mah: ' + extracted_info))

    else:
        time_stamp()
        print(semt + ', ' + mah + ' bolgesine ait veri bulunmamakta!')

    time.sleep(seconds - ((time.time() - start_time) % seconds))  # seconds later run the program again
    print()
