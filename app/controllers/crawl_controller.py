import requests
from bs4 import BeautifulSoup
from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL, RDFS


def add_to_ontology(chapters):
    g = Graph()
    g.parse('./app/ontology/luatgt copy 3.rdf', format="application/rdf+xml")

    name_space = "http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#"

    # Định nghĩa các namespace
    ns = Namespace(name_space)
    uri_name = URIRef(f'{name_space}Ten')
    uri_so = URIRef(f'{name_space}So')
    uri_thuoc_chuong = URIRef(f'{name_space}ThuocChuong')
    uri_thuoc_dieu = URIRef(f'{name_space}ThuocDieu')
    uri_thuoc_khoan = URIRef(f'{name_space}ThuocKhoan')
    
    for chapter in chapters:
        chapter_content = chapter["content"]
        chapter_code = chapter["id"]
        chapter_num = chapter["so"]

        uri_chapter = URIRef(f'{name_space}ND_Chuong{chapter_num}')
        uri_super = URIRef(f'{name_space}NghiDinh')
        uri_chapter_content = URIRef(f'{name_space}Ten')
        uri_chapter_num = URIRef(f'{name_space}So')

        g.add((ns[f'ND_Chuong{chapter_num}'], RDFS.subClassOf, uri_super))
        g.add((ns[chapter_code], RDF.type, uri_chapter))
        g.add((ns[chapter_code], uri_chapter_content, Literal(chapter_content)))
        g.add((ns[chapter_code], uri_chapter_num, Literal(chapter_num)))

        for article in chapter["dieus"]:
            article_content = article["content"]
            article_code = article["id"]
            article_num = article["so"]


            uri_article = URIRef(f'{name_space}ND_Chuong{chapter_num}Dieu{article_num}')
            g.add((ns[f'ND_Chuong{chapter_num}Dieu{article_num}'], RDFS.subClassOf, uri_chapter))
            g.add((ns[article_code],  RDF.type, uri_article))
            g.add((ns[article_code], uri_thuoc_chuong, URIRef(f'{name_space}{chapter_code}')))
            g.add((ns[article_code], uri_name, Literal(article_content)))
            g.add((ns[article_code], uri_so, Literal(article_num)))
            for clause in article["khoans"]:
                clause_content = clause["content"]
                clause_code = clause["id"]
                clause_num = clause["so"]
            
                uri_clause = URIRef(f'{name_space}ND_Chuong{chapter_num}Dieu{article_num}Khoan{clause_num}')
                g.add((ns[f'ND_Chuong{chapter_num}Dieu{article_num}Khoan{clause_num}'], RDFS.subClassOf, uri_article))
                g.add((ns[clause_code], RDF.type, uri_clause))
                g.add((ns[clause_code], uri_name, Literal(clause_content)))
                g.add((ns[clause_code], uri_so, Literal(clause_num)))
                g.add((ns[clause_code], uri_thuoc_dieu, URIRef(f'{name_space}{article_code}')))
                for point in clause["diems"]:
                    point_content = point["content"]
                    point_code = point["id"]
                    point_num = point["so"]

                    uri_point = URIRef(f'{name_space}ND_Chuong{chapter_num}Dieu{article_num}Khoan{clause_num}Diem{point_num}')
                    g.add((ns[f'ND_Chuong{chapter_num}Dieu{article_num}Khoan{clause_num}Diem{point_num}'], RDFS.subClassOf, uri_clause))
                    g.add((ns[point_code],  RDF.type, uri_point))
                    g.add((ns[point_code], uri_name, Literal(point_content)))
                    g.add((ns[point_code], uri_so, Literal(point_num)))
                    g.add((ns[point_code], uri_thuoc_khoan, URIRef(f'{name_space}{clause_code}')))




    g.serialize('./app/ontology/luatgt copy 3.rdf', format="application/rdf+xml")



    print("add_to_ontology OK")


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
        text = element.text.replace(" ", "")
        classes = element['class']
        for class_el in classes:
            if class_el == 'docitem-2':
                split_text = text.split("\n")

                roman = split_text[0].split(" ")[1]

                chuong_so = roman_to_int(roman)

                id_attr = f'ND100{chuong_so}'

                element['id'] = id_attr

                chuong = {
                    "id": id_attr,
                    "content": split_text[1].capitalize(),
                    # "legal": f'Chương {id_attr} Nghị định 100/2019/NĐ-CP',
                    "dieus": [],
                    "so": chuong_so
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
                    "khoans": [],
                    "so": id_attr
                }

                chuong['dieus'].append(dieu)
            elif class_el == 'docitem-11':
                id_attr = text.split(".")[0]

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
                    "diems": [],
                    "so": id_attr
                }
                khoans.append(khoan["content"])

                dieu['khoans'].append(khoan)
            elif class_el == 'docitem-12':
                split_text = text.split(".")[0].split(")")
                id_attr = split_text[0] if split_text[0] != "đ" else "dd"

                chuong = chuongs[len(chuongs) - 1]
                dieu = chuong['dieus'][len(chuong['dieus']) - 1]
                khoan = dieu['khoans'][len(dieu['khoans']) - 1]

                element['id'] = f'{khoan["id"]}{id_attr}'

                diem = {
                    "id": f'{khoan["id"]}{id_attr}',
                    "content": text[3:len(text)],
                    "khoan_id": khoan['id'],
                    # "legal": f'Điểm {id_attr} {khoan["legal"]}',
                    "so":id_attr
                }

                khoan['diems'].append(diem)

    add_to_ontology(chuongs)

    return chuongs
