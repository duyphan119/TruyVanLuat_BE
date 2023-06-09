import math
from rdflib import Graph, Namespace, RDF, URIRef, Literal
import json
import requests
from bs4 import BeautifulSoup
import os

current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)

g = Graph()
g.parse(current_folder_path + '/luatgt.rdf', format="application/rdf+xml")

url = 'https://luatvietnam.vn/vi-pham-hanh-chinh/nghi-dinh-100-2019-nd-cp-xu-phat-vi-pham-giao-thong-179619-d1.html'
response = requests.get(url)

html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

elements = soup.select("div[class^='docitem-']")

chuongs = []

for element in elements:
    text = element.text
    classes = element['class']
    for class_el in classes:
        if class_el == 'docitem-2':
            split_text = text.split("\n")

            id_attr = split_text[0].split(" ")[1]

            element['id'] = f'chuong_{id_attr.lower()}'

            chuong = {
                "id": f'chuong_{id_attr.lower()}',
                "content": f'{split_text[0]} {split_text[1].capitalize()}',
                "legal": f'Chương {id_attr} Nghị định 100/2019/NĐ-CP',
                "dieus": []
            }

            chuongs.append(chuong)
        elif class_el == 'docitem-5':
            id_attr = text.split(". ")[0].split(" ")[1]

            element['id'] = f'dieu_{id_attr}_{chuong["id"]}'

            chuong = chuongs[len(chuongs) - 1]

            leng = len(text)
            index = text.index(". ") + 2

            dieu = {
                "id": f'dieu_{id_attr}_{chuong["id"]}',
                "content": text.replace("\n", " ")[index:leng],
                "chuong_id": chuong['id'],
                "legal": f'Điều {id_attr} {chuong["legal"]}',
                "khoans": []
            }

            chuong['dieus'].append(dieu)
        elif class_el == 'docitem-11':
            id_attr = text.split(". ")[0]

            chuong = chuongs[len(chuongs) - 1]
            dieu = chuong['dieus'][len(chuong['dieus']) - 1]

            element['id'] = f'khoan_{id_attr}_{dieu["id"]}'

            leng = len(text)
            index = text.index(" ") + 1

            content = text.replace("\n", " ")[index:leng]
            dieu_id = dieu["id"].replace(content, "")
            khoan = {
                "id": f'khoan_{id_attr}_{dieu_id}',
                "content": content,
                "dieu_id": dieu_id,
                "legal": f'Khoản {id_attr} {dieu["legal"]}',
                "diems": []
            }
            print(khoan["dieu_id"])

            dieu['khoans'].append(khoan)
        elif class_el == 'docitem-12':
            id_attr = text.split(") ")[0]

            chuong = chuongs[len(chuongs) - 1]
            dieu = chuong['dieus'][len(chuong['dieus']) - 1]
            khoan = dieu['khoans'][len(dieu['khoans']) - 1]

            element['id'] = f'diem_{id_attr}_{khoan["id"]}'

            diem = {
                "id": f'diem_{id_attr}_{khoan["id"]}',
                "content": text[3:len(text)],
                "khoan_id": khoan['id'],
                "legal": f'Điểm {id_attr} {khoan["legal"]}'
            }

            khoan['diems'].append(diem)

print(chuongs)
