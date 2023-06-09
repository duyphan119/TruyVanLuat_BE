import requests
from bs4 import BeautifulSoup


def roman_to_int(roman):
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for i in range(len(roman) - 1, -1, -1):
        current_value = roman_dict[roman[i]]
        if current_value >= prev_value:
            total += current_value
        else:
            total -= current_value
        prev_value = current_value
    return total


def crawl_text():
    url = 'https://luatvietnam.vn/vi-pham-hanh-chinh/nghi-dinh-100-2019-nd-cp-xu-phat-vi-pham-giao-thong-179619-d1.html'
    response = requests.get(url)

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    elements = soup.select("div[class^='docitem-']")

    chuongs = []
    khoans = []

    for element in elements:
        text = element.text
        classes = element['class']
        for class_el in classes:
            if class_el == 'docitem-2':
                split_text = text.split("\n")

                roman = split_text[0].split(" ")[1]

                id_attr = f'ND100{roman_to_int(roman)}'

                element['id'] = id_attr

                chuong = {
                    "id": id_attr,
                    "content": split_text[1].capitalize(),
                    # "legal": f'Chương {id_attr} Nghị định 100/2019/NĐ-CP',
                    "dieus": []
                }

                chuongs.append(chuong)
            elif class_el == 'docitem-5':
                id_attr = text.split(". ")[0].split(" ")[1]

                chuong = chuongs[len(chuongs) - 1]

                element['id'] = f'{chuong["id"]}{id_attr}'

                leng = len(text)
                index = text.index(". ") + 2

                dieu = {
                    "id": f'{chuong["id"]}{id_attr}',
                    "content": text.replace("\n", " ")[index:leng],
                    "chuong_id": chuong['id'],
                    # "legal": f'Điều {id_attr} {chuong["legal"]}',
                    "khoans": []
                }

                chuong['dieus'].append(dieu)
            elif class_el == 'docitem-11':
                id_attr = text.split(". ")[0]

                chuong = chuongs[len(chuongs) - 1]
                dieu = chuong['dieus'][len(chuong['dieus']) - 1]

                element['id'] = f'{dieu["id"]}{id_attr}'

                leng = len(text)
                index = text.index(" ") + 1

                content = text.replace("\n", " ")[index:leng]
                dieu_id = dieu["id"].replace(content, "")
                khoan = {
                    "id": f'{dieu["id"]}{id_attr}',
                    "content": content,
                    "dieu_id": dieu_id,
                    # "legal": f'Khoản {id_attr} {dieu["legal"]}',
                    "diems": []
                }
                khoans.append(khoan["content"])

                dieu['khoans'].append(khoan)
            elif class_el == 'docitem-12':
                split_text = text.split(") ")
                id_attr = split_text[0] if split_text[0] != "đ" else "dd"

                chuong = chuongs[len(chuongs) - 1]
                dieu = chuong['dieus'][len(chuong['dieus']) - 1]
                khoan = dieu['khoans'][len(dieu['khoans']) - 1]

                element['id'] = f'{khoan["id"]}{id_attr}'

                diem = {
                    "id": f'{khoan["id"]}{id_attr}',
                    "content": text[3:len(text)],
                    "khoan_id": khoan['id'],
                    # "legal": f'Điểm {id_attr} {khoan["legal"]}'
                }

                khoan['diems'].append(diem)

    return chuongs
