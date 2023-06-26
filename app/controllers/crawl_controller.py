import requests
from bs4 import BeautifulSoup
from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL, RDFS, XSD
from app.helpers.count_substring_occurrences import count_substring_occurrences
from app.helpers.to_code import to_code
from app.helpers.tokenize_sentence import tokenize_sentence

def add_to_ontology(chapters, json_data):
    g = Graph()
    g.parse('./app/ontology/trafficlaws.rdf', format="application/rdf+xml")

    name_space = "http://www.semanticweb.org/duyphan/ontologies/2023/5/trafficlaws#"
    # Định nghĩa các namespace
    ns = Namespace(name_space)
    # uri_name = URIRef(f'{name_space}Ten')
    # uri_so = URIRef(f'{name_space}So')
    # uri_thuoc_chuong = URIRef(f'{name_space}ThuocChuong')
    # uri_thuoc_dieu = URIRef(f'{name_space}ThuocDieu')
    # uri_thuoc_khoan = URIRef(f'{name_space}ThuocKhoan')
    
    # for chapter in chapters:
    #     chapter_content = chapter["content"]
    #     chapter_code = chapter["id"]
    #     chapter_num = chapter["so"]

    #     uri_chapter = URIRef(f'{name_space}ND_Chuong{chapter_num}')
    #     uri_super = URIRef(f'{name_space}NghiDinh')
    #     uri_chapter_content = URIRef(f'{name_space}Ten')
    #     uri_chapter_num = URIRef(f'{name_space}So')

    #     g.add((ns[f'ND_Chuong{chapter_num}'], RDFS.subClassOf, uri_super))
    #     g.add((ns[chapter_code], RDF.type, uri_chapter))
    #     g.add((ns[chapter_code], uri_chapter_content, Literal(chapter_content)))
    #     g.add((ns[chapter_code], uri_chapter_num, Literal(chapter_num)))

    #     for article in chapter["dieus"]:
    #         article_content = article["content"]
    #         article_code = article["id"]
    #         article_num = article["so"]


    #         uri_article = URIRef(f'{name_space}ND_Chuong{chapter_num}Dieu{article_num}')
    #         g.add((ns[f'ND_Chuong{chapter_num}Dieu{article_num}'], RDFS.subClassOf, uri_chapter))
    #         g.add((ns[article_code],  RDF.type, uri_article))
    #         g.add((ns[article_code], uri_thuoc_chuong, URIRef(f'{name_space}{chapter_code}')))
    #         g.add((ns[article_code], uri_name, Literal(article_content)))
    #         g.add((ns[article_code], uri_so, Literal(article_num)))
    #         for clause in article["khoans"]:
    #             clause_content = clause["content"]
    #             clause_code = clause["id"]
    #             clause_num = clause["so"]
            
    #             uri_clause = URIRef(f'{name_space}ND_Chuong{chapter_num}Dieu{article_num}Khoan{clause_num}')
    #             g.add((ns[f'ND_Chuong{chapter_num}Dieu{article_num}Khoan{clause_num}'], RDFS.subClassOf, uri_article))
    #             g.add((ns[clause_code], RDF.type, uri_clause))
    #             g.add((ns[clause_code], uri_name, Literal(clause_content)))
    #             g.add((ns[clause_code], uri_so, Literal(clause_num)))
    #             g.add((ns[clause_code], uri_thuoc_dieu, URIRef(f'{name_space}{article_code}')))
    #             for point in clause["diems"]:
    #                 point_content = point["content"]
    #                 point_code = point["id"]
    #                 point_num = point["so"]

    #                 uri_point = URIRef(f'{name_space}ND_Chuong{chapter_num}Dieu{article_num}Khoan{clause_num}Diem{point_num}')
    #                 g.add((ns[f'ND_Chuong{chapter_num}Dieu{article_num}Khoan{clause_num}Diem{point_num}'], RDFS.subClassOf, uri_clause))
    #                 g.add((ns[point_code],  RDF.type, uri_point))
    #                 g.add((ns[point_code], uri_name, Literal(point_content)))
    #                 g.add((ns[point_code], uri_so, Literal(point_num)))
    #                 g.add((ns[point_code], uri_thuoc_khoan, URIRef(f'{name_space}{clause_code}')))


    for violation in json_data["violations"]:
        fine = violation["fine"]
        content = violation["content"]
        legal = violation["legal"]
        violation_id = violation["id"]
        violator = violation["violator"]
        note = violation["note"]
        violation_code = to_code(legal.replace("đ","dd"))
        # violator_code = to_code(violator)
        # clause = violation["clause"]
        # clause_legal = clause["legal"]
        # clause_code = to_code(clause_legal)

        # Thêm điều
        g.add((ns[violation_code], RDF.type, URIRef(f'{name_space}ViPham')))
        g.add((ns[violation_code], URIRef(f'{name_space}HinhPhat'), Literal(fine)))
        g.add((ns[violation_code], URIRef(f'{name_space}NoiDung'), Literal(content)))
        g.add((ns[violation_code], URIRef(f'{name_space}DoiTuongXuPhat'), Literal(violator)))
        g.add((ns[violation_code], URIRef(f'{name_space}Luat'), Literal(legal)))
        g.add((ns[violation_code], URIRef(f'{name_space}MaViPham'), Literal(violation_id)))
        g.add((ns[violation_code], URIRef(f'{name_space}TuKhoa'), Literal("")))
        g.add((ns[violation_code], URIRef(f'{name_space}GhiChu'), Literal(note)))

    for pbs in json_data["addition_punishments"]:
        pbs_content = pbs["addition_punishment"]
        pbs_legal = pbs["main_legal"]
        violation_legal = pbs["legal"]
        pbs_code = to_code(pbs_legal)+to_code(content)
        violation_code = to_code(violation_legal.replace("đ","dd"))
        g.add((ns[pbs_code], RDF.type, URIRef(f'{name_space}HinhPhatBoSung')))
        g.add((ns[pbs_code], URIRef(f'{name_space}MaPhatBoSung'), Literal(to_code(pbs_legal))))
        g.add((ns[pbs_code], URIRef(f'{name_space}NoiDung'), Literal(pbs_content)))
        g.add((ns[pbs_code], URIRef(f'{name_space}Luat'), Literal(pbs_legal)))
        g.add((ns[violation_code], URIRef(f'{name_space}PhatBoSung'), URIRef(f'{name_space}{pbs_code}')))

    for gp in json_data["solutions"]:
        gp_content = gp["solution"]
        gp_legal = gp["main_legal"]
        violation_legal = gp["legal"]
        gp_code = to_code(gp_legal)+to_code(content)
        violation_code = to_code(violation_legal.replace("đ","dd"))
        g.add((ns[gp_code], RDF.type, URIRef(f'{name_space}BienPhapKhacPhuc')))
        g.add((ns[gp_code], URIRef(f'{name_space}MaBienPhap'), Literal(to_code(gp_legal))))
        g.add((ns[gp_code], URIRef(f'{name_space}NoiDung'), Literal(gp_content)))
        g.add((ns[gp_code], URIRef(f'{name_space}Luat'), Literal(gp_legal)))
        g.add((ns[violation_code], URIRef(f'{name_space}KhacPhuc'), URIRef(f'{name_space}{gp_code}')))


    g.serialize('./app/ontology/trafficlaws.rdf', format="application/rdf+xml")



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


def crawl_text(args):
    q = args.get("q") or ""
    p = args.get("p") or 1
    url = f'https://thuvienphapluat.vn/iThong/tra-cuu-xu-phat-giao-thong.aspx?k={q}&type=0&group=0&page={p}'
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    elements = soup.select(".tbViolation tbody tr")
    rows = []

    def crawl_by_id(slug):

        return {}

    for element in elements:
        violator = element.select_one(".ViolationObject").text
        name = element.select_one(".ViolationName").text
        fine = element.select_one(".ViolationFines").text
        slug = element.select_one(".ViolationDetail a")["href"]
        code = slug.split("id=")[1]
        

        rows.append({
            "violator": violator,
            "name": name,
            "fine": fine,
            "slug": slug,
            "id": code
        })

    return rows








    # url = 'https://luatvietnam.vn/giao-thong/luat-giao-thong-duong-bo-2008-39051-d1.html'
    url = 'https://luatvietnam.vn/vi-pham-hanh-chinh/nghi-dinh-100-2019-nd-cp-xu-phat-vi-pham-giao-thong-179619-d1.html'
    response = requests.get(url)

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    elements = soup.select("div[class^='docitem-']")
    data = []
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
                    # "id": id_attr,
                    "id": f"chuong_{chuong_so}",
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
                    # "id": f'{chuong["id"]}{id_attr}',
                    "id": f"dieu_{id_attr}",
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
                    # "id": f'{dieu["id"]}{id_attr}',
                    "id": f"khoan_{dieu['so']}_{id_attr}",
                    "content": content,
                    "dieu_id": dieu_id,
                    # "legal": f'Khoản {id_attr} {dieu["legal"]}',
                    "diems": [],
                    "so": id_attr
                }
                khoans.append(khoan["content"])

                # count_gom = count_substring_occurrences(content, " gồm ")
                # count_la = count_substring_occurrences(content, " là ")
                # count_la_1 = count_substring_occurrences(content, ") là ")
                # count_sau_day = count_substring_occurrences(content, "sau đây gọi là ")
                # try:
                #     if count_la_1 > 0 and count_la > 0:
                #         index = content.rindex(" là ")
                #         if count_sau_day == 0:
                #             data.append({
                #                 "name": content[0:index],
                #                 "meaning": content[index+1:len(content)],
                #                 "content":content
                #             })
                #     if count_gom > 0:
                #         index = content.rindex(" gồm ")
                #         data.append({
                #             "name": content[0:index],
                #             "meaning": content[index+1:len(content)],
                #                 "content":content
                #         })
                # except:
                #     True
                # if count_la > 0:
                #     if count_sau_day > 0:
                #         count_la_1 = count_substring_occurrences(content, ") là ")
                #         if count_la_1 > 0:
                #             content = content.replace(") là ", ");;")
                #             data.append(content.split(";;")[0])
                #     else:
                #         content = content.replace(" là ", ";;")
                #         data.append(content.split(";;")[0])
                # if count_gom > 0:
                #     content = content.replace(" gồm ", ";;")
                #     data.append(content.split(";;")[0])

                dieu['khoans'].append(khoan)
            elif class_el == 'docitem-12':
                split_text = text.split(".")[0].split(")")
                id_attr = split_text[0] if split_text[0] != "đ" else "dd"

                chuong = chuongs[len(chuongs) - 1]
                dieu = chuong['dieus'][len(chuong['dieus']) - 1]
                khoan = dieu['khoans'][len(dieu['khoans']) - 1]

                element['id'] = f'{khoan["id"]}{id_attr}'
                content = text[3:len(text)]
                diem = {
                    # "id": f'{khoan["id"]}{id_attr}',
                    "id": f'diem_{dieu["so"]}_{khoan["so"]}_{id_attr}',
                    "content": content,
                    "khoan_id": khoan['id'],
                    # "legal": f'Điểm {id_attr} {khoan["legal"]}',
                    "so":id_attr
                }

                # count_gom = count_substring_occurrences(content, " gồm ")
                # count_la = count_substring_occurrences(content, " là ")
                # count_sau_day = count_substring_occurrences(content, "sau đây gọi là ")

                # if count_la > 0:
                #     index = content.rindex(" là ")
                #     if count_sau_day == 0:
                #         data.append({
                #             "name": content[0:index],
                #             "meaning": content[index+1:len(content)],
                #                 "content":content
                #         })
                # if count_gom > 0:
                #     index = content.rindex(" gồm ")
                #     data.append({
                #         "name": content[0:index],
                #         "meaning": content[index+1:len(content)],
                #                 "content":content
                #     })

                khoan['diems'].append(diem)

    # add_to_ontology(chuongs)
   
    for chuong in chuongs:
        if f'{chuong["so"]}' != "4":
            for dieu in chuong["dieus"]:
                item = xldl(dieu, chuong)
                # add_to_ontology(chuongs, item)

                if len(item["violations"]) > 0:
                    data.append( item) 
    return data
    # return chuongs

def xldl(article, chapter):
    violations = []
    solutions = []
    addition_punishments = []
    count_violator = count_substring_occurrences(article["content"],"Xử phạt người ")
    count_hv = count_substring_occurrences(article["content"],"Xử phạt các hành vi ")
    if count_violator > 0:
        violator = article["content"].split("Xử phạt ")[1].split(" vi phạm")[0]
      
        for clause in article["khoans"]:
            fine = clause["content"]
            # fine.startswith("Ngoài việc bị áp dụng hình thức xử phạt")
            if count_substring_occurrences(fine, "Ngoài việc bị phạt tiền") > 0:
                count_sau_day = count_substring_occurrences(fine, "sau đây:")
                if count_sau_day > 0:
                    for point in clause["diems"]:
                        filtered_result = filter_addition(point["content"])
                        for result in filtered_result:
                            addition_punishment = result["value"]
                            text = result["key"]
                            split_text = text.split("; ")
                            for legal in split_text:
                                split_legal = legal.split(", ")
                                if len(split_legal) > 1:
                                    clause_num = split_legal[len(split_legal) - 1].split("khoản ")[1]
                                    
                                    for _legal in split_legal:
                                        if _legal.startswith("điểm"):
                                            addition_punishments.append({
                                                # "legals": point_legal + " khoản " + last_clause_legals,
                                                "addition_punishment":addition_punishment,
                                                "legal":(_legal if split_legal[len(split_legal) - 1] == _legal else f'{_legal} khoản {clause_num}') + f" Điều {article['so']} Nghị định 100",
                                                "main_legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100",
                                                # "fine": result["fine"]
                                            })
                                else:
                                    if legal.startswith("điểm"):
                                        addition_punishments.append({
                                            # "legals": point_legal + " khoản " + last_clause_legals,
                                            "addition_punishment":addition_punishment,
                                            "legal":f"{legal} Điều {article['so']} Nghị định 100",
                                            "main_legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100",
                                            # "fine": result["fine"]
                                        })
                    
                # else:
                #     split_tai = fine.split(" tại ")
                #     if len(split_tai) > 1:
                #         split_dieu_nay = split_tai[1].split(" Điều này còn bị áp dụng hình thức xử phạt bổ sung ")
                #         if len(split_dieu_nay) > 1:
                #             addition_punishments.append({
                #                 # "legals": point_legal + " khoản " + last_clause_legals,
                #                 "addition_punishment":split_dieu_nay[1],
                #                 "legal":split_dieu_nay[0],
                #                 "main_legal": f"Điểm {point['so']} Khoản {clause['so']} Điều {article['so']}",
                #                 # "fine": result["fine"]
                #             })
            if fine.startswith("Ngoài việc bị áp dụng hình thức xử phạt"):
                count_sau_day = count_substring_occurrences(fine, "sau đây:")
                if count_sau_day > 0:
                    for point in clause["diems"]:
                        solution = point["content"].replace("Thực hiện hành vi quy định tại ", "")
                        split_solution = solution.split(" Điều này ")
                        if len(split_solution) > 1:
                            split_solution_2 = split_solution[0].split(";")
                            for legal_clause in split_solution_2:
                                count_khoan = count_substring_occurrences(legal_clause, ",")
                                if count_khoan == 0:
                                    if legal_clause.startswith("điểm"):
                                        solutions.append({
                                            "solution": split_solution[1],
                                            "legal": legal_clause+f" Điều {article['so']} Nghị định 100",
                                            "main_legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100"
                                        })
                                else:
                                    split_legal_dp = legal_clause.split(", ")
                                    last_item = split_legal_dp[len(split_legal_dp) - 1]
                                    split_last_item = last_item.split("khoản ")
                                    if len(split_last_item) > 1:
                                        for split_point in split_legal_dp:
                                            if split_point.startswith("điểm"):
                                                solutions.append({
                                                    "solution": split_solution[1],
                                                    "legal": (split_point if split_point == last_item else f"{split_point} khoản {split_last_item[1]}") + f" Điều {article['so']} Nghị định 100",
                                                    "main_legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100"
                                                })
            count = count_substring_occurrences(fine, "đồng")
            # if len(clause["diems"]) == 0:
            #     if count == 2:
            #         split_fine = fine.split(f" đối với {violator}")
            #         if len(split_fine) > 1:
            #             split_fine_2 = split_fine[1].split(", trừ ")
            #             note = ""
            #             if len(split_fine_2) > 1:
            #                 note = "Trừ " + split_fine_2[1]
            #             violations.append({
            #                 "violator": violator, 
            #                 "fine":split_fine[0],
            #                 "content": split_fine_2[0],
            #                 "legal": f"Khoản {clause['so']} Điều {article['so']} Nghị định 100",
            #                 "num": point['so'],
            #                 "id": point['id'],
            #                 "note":note,
            #             })

            if count == 2:
                for point in clause["diems"]:
                    content = point["content"]
                    split_content = content.split(", trừ ")
                    note = ""
                    if len(split_content) > 1:
                        note = "Trừ " + split_content[1]
                    violations.append({
                        "violator":f"{violator}", 
                        "fine":fine.split(" đối với")[0],
                        "content": split_content[0],
                        "legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100",
                        "num": point['so'],
                        "id": point['id'],
                        "note":note,
                    })
        
    if count_hv > 0:
        violator = "Cá nhân"
        count_dsat = count_substring_occurrences(article["content"], "đường sắt")
        if count_dsat == 0:
            for clause in article["khoans"]:
                fine = clause["content"].replace(" thực hiện một trong các hành vi vi phạm sau đây:", "").replace(" đối với một trong các hành vi vi phạm sau đây:", "")
                count = count_substring_occurrences(fine, "đồng")
                split_fine = fine.split(" đối với ")
                if count_substring_occurrences(fine, "Ngoài việc bị phạt tiền") > 0:
                    count_sau_day = count_substring_occurrences(fine, "sau đây:")
                    if count_sau_day > 0:
                        for point in clause["diems"]:
                            filtered_result = filter_addition(point["content"])
                            for result in filtered_result:
                                addition_punishment = result["value"]
                                text = result["key"]
                                split_text = text.split("; ")
                                for legal in split_text:
                                    split_legal = legal.split(", ")
                                    if len(split_legal) > 1:
                                        clause_num = split_legal[len(split_legal) - 1].split("khoản ")[1]
                                        
                                        for _legal in split_legal:
                                            if _legal.startswith("điểm"):
                                                addition_punishments.append({
                                                    # "legals": point_legal + " khoản " + last_clause_legals,
                                                    "addition_punishment":addition_punishment,
                                                    "legal":(_legal if split_legal[len(split_legal) - 1] == _legal else f'{_legal} khoản {clause_num}') + f" Điều {article['so']} Nghị định 100",
                                                    "main_legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100",
                                                    # "fine": result["fine"]
                                                })
                                    else:
                                        if legal.startswith("điểm"):
                                            addition_punishments.append({
                                                # "legals": point_legal + " khoản " + last_clause_legals,
                                                "addition_punishment":addition_punishment,
                                                "legal":f"{legal} Điều {article['so']} Nghị định 100",
                                                "main_legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100",
                                                # "fine": result["fine"]
                                            })
                if fine.startswith("Ngoài việc bị áp dụng hình thức xử phạt"):
                    count_sau_day = count_substring_occurrences(fine, "sau đây:")
                    if count_sau_day > 0:
                        for point in clause["diems"]:
                            solution = point["content"].replace("Thực hiện hành vi quy định tại ", "")
                            split_solution = solution.split(" Điều này ")
                            if len(split_solution) > 1:
                                split_solution_2 = split_solution[0].split(";")
                                for legal_clause in split_solution_2:
                                    count_khoan = count_substring_occurrences(legal_clause, ",")
                                    if count_khoan == 0:
                                        if legal_clause.startswith("điểm"):
                                            solutions.append({
                                                "solution": split_solution[1],
                                                "legal": legal_clause+f" Điều {article['so']} Nghị định 100",
                                                "main_legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100"
                                            })
                                    else:
                                        split_legal_dp = legal_clause.split(", ")
                                        last_item = split_legal_dp[len(split_legal_dp) - 1]
                                        split_last_item = last_item.split("khoản ")
                                        if len(split_last_item) > 1:
                                            for split_point in split_legal_dp:
                                                if split_point.startswith("điểm"):
                                                    solutions.append({
                                                        "solution": split_solution[1],
                                                        "legal": (split_point if split_point == last_item else f"{split_point} khoản {split_last_item[1]}") + f" Điều {article['so']} Nghị định 100",
                                                        "main_legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100"
                                                    })
                if count == 2:
                    for point in clause["diems"]:
                        content = point["content"]
                        split_content = content.split(", trừ ")
                        note = ""
                        if len(split_content) > 1:
                            note = "Trừ " + split_content[1]
                        violations.append({
                            "violator":(split_fine[1] if len(split_fine) > 1 else "Cá nhân").capitalize(), 
                            "content": split_content[0],
                            "fine":split_fine[0],
                            "id": point['id'],
                            "note":note,
                            "num": point['so'],
                            "legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100",
                        })
                split_fine_2 = fine.split(" cá nhân, ")
                if count > 2:
                    for point in clause["diems"]:
                        violator = "Cá nhân"
                        content = point["content"]
                        split_content = content.split(", trừ ")
                        note = ""
                        if len(split_content) > 1:
                            note = "Trừ " + split_content[1]
                        if len(split_fine_2) > 1:
                            split_fine_3 = split_fine_2[1].split(" đối với ")
                            if len(split_fine_3) > 1:
                                violator += ", " + split_fine_3[1]
                        violations.append({
                            "violator": violator, 
                            "content": split_content[0],
                            "fine":fine,
                            "id": point['id'],
                            "note":note,
                            "num": point['so'],
                            "legal": f"Điểm {'đ' if point['so'] == 'dd' else point['so']} Khoản {clause['so']} Điều {article['so']} Nghị định 100",
                            
                        })
    return {
        "violations": violations,
        "addition_punishments":addition_punishments,
        "solutions": solutions
    }

def filter_addition(fine):
    # fine = """Thực hiện hành vi quy định tại điểm a khoản 6; điểm a, điểm b khoản 7; điểm a, điểm b, điểm c, điểm d khoản 8 Điều này bị tước quyền sử dụng Giấy phép lái xe từ 02 tháng đến 04 tháng; tái phạm hoặc vi phạm nhiều lần hành vi quy định tại điểm a, điểm b, điểm c, điểm d khoản 8 Điều này bị tước quyền sử dụng Giấy phép lái xe từ 03 tháng đến 05 tháng, tịch thu phương tiện. Thực hiện hành vi quy định tại một trong các điểm, khoản sau của Điều này mà gây tai nạn giao thông thì bị tước quyền sử dụng Giấy phép lái xe từ 02 tháng đến 04 tháng: Điểm a, điểm g, điểm h, điểm k, điểm 1, điểm m, điểm n, điểm q khoản 1; điểm b, điểm d, điểm e, điểm g, điểm 1, điểm m khoản 2; điểm b, điểm c, điểm k, điểm m khoản 3; điểm đ, điểm e, điểm g, điểm h khoản 4 Điều này;"""

    # fine = "Thực hiện hành vi quy định tại điểm g khoản 2 Điều này bị tịch thu thiết bị phát tín hiệu ưu tiên lắp đặt, sử dụng trái quy định;"
    addition_punishments = []

    sentences = fine.replace("Thực hiện ","").replace("hành vi quy định tại ", "").split(".")

    for sentence in sentences: 

        count_tai_pham = count_substring_occurrences(sentence, "; tái phạm")
        count_tai_nan = count_substring_occurrences(sentence, "mà gây tai nạn giao thông thì")
        if count_tai_nan > 0:
            text = "nếu gây tai nạn giao thông thì" + sentence.split("gây tai nạn giao thông thì")[1]
            split_2_cham = text.split(": ")
            addition_punishments.append({
                "key": (split_2_cham[1] if len(split_2_cham) > 1 else split_2_cham[0]).replace(" Điều này;", ""),
                "value": split_2_cham[0],
                "fine": fine
            })
        elif count_tai_pham > 0:
            small_sentences = "tái phạm" + sentence.split("; tái phạm")[1]
            for small_sentence in small_sentences:
                
                split_dieu_nay = small_sentence[0].split(" Điều này bị ")
                if len(small_sentence) > 1:
                    addition_punishments.append({
                        "key": split_dieu_nay[0],
                        "value":  small_sentence[1],
                        "fine": fine
                    })
        else:
            small_sentences = sentence.split(" Điều này ")
            if len(small_sentences) > 1:
                addition_punishments.append({
                    "key": small_sentences[0],
                    "value":  small_sentences[1],
                    "fine": fine
                })

        # split_fine1 = (split_file[1] if len(split_file) > 1 else split_file[0] ).split("gây tai nạn giao thông")
        # arr = [
        #     split_file[0],
        
        # ]
        # if len(split_fine1) > 1:
        #     arr.append( ("tái phạm "+split_fine1[0]).split(".")[0])
        # if len(split_fine1) > 1:
        #     arr.append("gây tai nạn giao thông"+split_fine1[1])
        # for item in arr:
        #     split_item = item.split(" Điều này ")
        #     if len(split_item) > 1:
        #         split_item_2 = split_item[0].split(" hành vi quy định tại ")
        #         if len(split_item_2) > 1:

        #             addition_punishments.append({
        #                 "key": split_item_2[1],
        #                 "value":  split_item[1] if split_item_2[0].startswith("Thực hiện") else split_item_2[0] + " " + split_item[1],
        #                 "fine": "fine"
        #             })
        #     else:
        #         split_item = item.split(": ")
        #         if len(split_item) > 1:
        #             addition_punishments.append({
        #                 "key": split_item[1].split(" Điều này")[0],
        #                 "value":  split_item[0],
        #                 "fine": "fine"
        #             })
    return addition_punishments
