from bs4 import BeautifulSoup
import requests
import time
import send_mail

# seconds = 30.0
seconds = 3600.0
start_time = time.time()

semt = 'Fatih'
mah = 'Cerrahpaşa'
is_there_semt = False
is_there_mah = False

first_line = ''
second_line = ''


def indexes(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset)


def report():
    print(time.strftime('%d %b %Y - %H:%M:%S'))


while True:
    clean_page_txt = []

    page_link = 'https://www.iski.istanbul/web/tr-TR/ariza-kesinti'
    # fetch the content from url
    page_response = requests.get(page_link, timeout=5)
    # parse html
    page_content = BeautifulSoup(page_response.text, 'html.parser')

    for lnk in page_content.find_all('a'):
        lnk.decompose()

    targeted_class = page_content.find(class_='col-xs-12 col-sm-12 col-md-9 col-lg-9 sp-rightcol')
    targeted_class_items = targeted_class.find_all('td')

    for line in targeted_class_items:
        clean_page_txt.append(line.get_text().strip())

    for value in clean_page_txt:
        if (semt and mah) in value:
            is_there_semt = True
            is_there_mah = True
            break

    if is_there_semt and is_there_mah:
        index_list = indexes(clean_page_txt, semt)
        for i in index_list:
            extracted_info = clean_page_txt[i + 12][0:11] + clean_page_txt[i + 12][26:]
            report()
            print(semt + ', ' + mah + ' Mah: ')
            print(extracted_info)
            send_mail.send(str(semt + ', ' + mah + ' Mah: ' + extracted_info))

    else:
        report()
        print(semt + ', ' + mah + ' bölgesine ait veri bulunmamakta!')

    time.sleep(seconds - ((time.time() - start_time) % seconds))  # seconds later run the program again
    print()
