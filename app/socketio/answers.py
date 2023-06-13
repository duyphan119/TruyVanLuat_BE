from rdflib import Graph
import json
from app.helpers.find_item import find_item
from app.helpers.random_item import random_item
from app.data.sample_answers import sample_answers, unclear_answers
from wit import Wit
import os
from app.helpers.get_most_common_elements import get_most_common_elements
from app.controllers.violation_controller import handle_result


def find_most_frequent_element(arr):
    counts = {}
    for item in arr:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    max_count = max(counts.values())
    most_frequent_elements = [item for item,
    count in counts.items() if count == max_count]
    return most_frequent_elements


def handle_violation(entities):
    message = ''
    list_id = []
    violations = []
    filter_string = ''
    filters = []

    for entity in entities:
        name = entity["entity"]
        value = entity["value"]
        if name == "hanh_vi_vi_pham":
            filters.append(
                f'''contains(LCASE(?tenhanhvivipham), "{value.lower()}")''')
        if name == "vi_pham_ve":
            filters.append(
                f'''contains(LCASE(?tenviphamve), "{value.lower()}")''')
        if name == "doi_tuong_tham_gia_giao_thong":
            filters.append(
                f'''(contains(LCASE(?tendoituongxuphat), "{value.lower()}") || contains(LCASE(?tenviphamve), "{value.lower()}"))''')
        if name == "khu_vuc":
            filters.append(
                f'''contains(LCASE(?tenkhuvuc), "{value.lower()}")''')
    if len(filters) > 0:
        filter_string += f'''filter ({" && ".join(filters)}) \n.'''
    # Tạo Graph
    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")
    # Tạo chuỗi query

    # query = (
    #     'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
    #     'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
    #     'SELECT * WHERE {\n'
    #     '   ?violation \n'
    #     '       :CoDiem ?legal ;\n'
    #     '       :CoDoiTuongXuPhat ?violator ;\n'
    #     '       :ThuocNhomViPham ?group ;\n'
    #     '       :BiPhatTien ?fine ;\n'
    #     '       :CoHanhViViPham ?action .\n'
    #     '   ?action :Ten ?action_name .\n'
    #     '   ?legal :Ten ?legal_name .\n'
    #     '   ?violator :Ten ?violator_name .\n'
    #     '   ?fine :TienPhat ?fine_value .\n'
    #     f'   {filter_string}'
    #     '   OPTIONAL { \n'
    #     '       ?violation\n'
    #     '           :XayRaTai ?where ;\n'
    #     '           :XayRaVao ?time ;\n'
    #     '           :CoDoiTuongThamGia ?traffic_participant .\n'
    #     '       ?traffic_participant :Ten ?traffic_participant_name .\n'
    #     '   }\n'
    #     '}\n'
    # )
    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?vipham\n'
        '       :Ten ?tenvipham ;\n'
        '       :ChiTiet ?chitietvipham ;\n'
        '       :CoDoiTuongXuPhat ?doituongxuphat ;\n'
        '       :BiPhatTien ?mucphat ;\n'
        '       :CoHanhViViPham ?hanhvivipham ;\n'
        '       :XayRaTai ?khuvuc ;\n'
        '       :ViPhamVe ?viphamve .\n'
        '   ?doituongxuphat\n'
        '       :Ten ?tendoituongxuphat .\n'
        '   ?mucphat\n'
        '       :TienPhat ?mucphattien .\n'
        '   ?hanhvivipham\n'
        '       :Ten ?tenhanhvivipham .\n'
        '   ?viphamve\n'
        '       :Ten ?tenviphamve .\n'
        '   ?khuvuc\n'
        '       :Ten ?tenkhuvuc .\n'
        f'  {filter_string}\n'
        '}\n'
     )
    # query = (
    #     'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
    #     'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
    #     'SELECT * WHERE {\n'
    #     '   ?violation \n'
    #     '       :So ?point_num ;\n'
    #     '       :Ten ?point_name ;\n'
    #     '       :ThuocKhoan ?clause ;\n'
    #     '       :CoDoiTuongXuPhat ?violator ;\n'
    #     '       :BiPhatTien ?fine ;\n'
    #     '       :CoDoiTuongThamGia ?traffic_participant ;\n'
    #     '       :CoHanhViViPham ?action .\n'
    #     '   ?action :Ten ?action_name .\n'
    #     '   ?violator :Ten ?violator_name .\n'
    #     '   ?fine :TienPhat ?fine_value .\n'
    #     '   ?clause :So ?clause_num .\n'
    #     '   ?clause :Ten ?clause_name .\n'
    #     '   ?clause :ThuocDieu ?article .\n'
    #     '   ?article :So ?article_num .\n'
    #     '   ?article :Ten ?article_name .\n'
    #     '   ?article :ThuocMuc ?section .\n'
    #     '   ?section :So ?section_num .\n'
    #     '   ?section :Ten ?section_name .\n'
    #     '   ?section :ThuocChuong ?chapter .\n'
    #     '   ?chapter :So ?chapter_num .\n'
    #     '   ?chapter :Ten ?chapter_name .\n'
    #     '   ?chapter :ThuocVanBan ?text .\n'
    #     '   ?text :So ?text_num .\n'
    #     '   ?text :Ten ?text_name .\n'
    #     f'   {filter_string}'
    #     '   OPTIONAL { \n'
    #     '       ?violation\n'
    #     '           :XayRaTai ?where ;\n'
    #     '           :XayRaVao ?time .\n'
    #     '       ?traffic_participant :Ten ?traffic_participant_name .\n'
    #     '   }\n'
    #     '}\n'
    # )

    print(query)
    data = json.loads('{}')
    list_code = []

    result = g.query(query)

    violations = handle_result(result)

    # for item in result:
    #     # fine = item.get("fine_value")
    #     code = item.get("violation").split("#")[1]
    #     violator = item.get("violator_name")
    #     # legal = item.get("legal_name")
    #     list_code.append(code)

    #     if code in data:
    #         index_violator = find_item(data[code]['violators'], violator)
    #         if index_violator < 0:
    #             data[code]['violators'].append(violator)
    #     else:
    #         data[code] = {
    #             "id": code,
    #             "legal": {
    #                 "num": item.get("text_num"),
    #                 "name": item.get("text_name"),
    #                 "chapter": {
    #                     "name": item.get("chapter_name"),
    #                     "num": item.get("chapter_num"),
    #                 },
    #                 "section": {
    #                     "name": item.get("section_name"),
    #                     "num": item.get("section_num"),
    #                 },
    #                 "article": {
    #                     "name": item.get("article_name"),
    #                     "num": item.get("article_num"),
    #                 },
    #                 "clause": {
    #                     "name": item.get("clause_name"),
    #                     "num": item.get("clause_num"),
    #                 },
    #                 "point": {
    #                     "name": item.get("point_name"),
    #                     "num": item.get("point_num"),
    #                 },
    #             },
    #             "violators": [violator]
    #         }
    #         list_id.append(code)

    # for item in result:
    #     fine = item.get("fine_value")
    #     code = item.get("violation").split("#")[1]
    #     violator = item.get("violator_name")
    #     legal = item.get("legal_name")
    #     list_code.append(code)

    #     if code in data:
    #         index_violator = find_item(data[code]['violators'], violator)
    #         if index_violator < 0:
    #             data[code]['violators'].append(violator)
    #     else:
    #         data[code] = {
    #             "id": code,
    #             "fine": fine,
    #             "legal": legal,
    #             "violators": [violator]
    #         }
    #         list_id.append(code)
    # most_code = get_most_common_elements(list_code)
    # print(list_code)
    # for result_code in most_code:
    #     if result_code in data:
    #         data[result_code]["violators"] = ", ".join(
    #             data[result_code]["violators"])
    #         violations.append(data[result_code])

    i = 0

    # for violation in violations:
    #     values = []
    #     for entity in entities:
    #         value = entity['value']
    #         values.insert(0, f'''contains(LCASE(?content), "{value}")''')
    if len(violations) > 0:
        message += f'<div>Có {len(violations)} hình phạt tương ứng:</div>'
    for violation in violations:
        message += f'<div>'
        # message += f"""<div>Theo {violation["legal"]["num"]} chương {violation["legal"]["chapter"]["num"]} mục {violation["legal"]["section"]["num"]} điều {violation["legal"]["article"]["num"]}. {violation["legal"]["article"]["name"]}</div>"""
        # message += f'''<div>{violation["legal"]["clause"]["num"]}. {violation["legal"]["clause"]["name"]}</div>'''
        # message += f'''<div>{violation["legal"]["point"]["num"]}. {violation["legal"]["point"]["name"]}</div>'''
        # message += f'''<div>Đối tượng xử phạt: {violation["violators"]}</div>'''
        # message += f'''<div>{violation["legal"]}</div>'''
        # message += f'''<div>{violation["fine"]}</div>'''
        # message += f'''<div>Vi phạm: {violation['content']}</div>
        #         <div>Đối tượng: {violation['violator']}</div>
        #         <div>{violation['punishment']}</div>'''
        # addition_punishment_string = ''
        # for addition_punishment in violation['addition_punishments']:
        #     addition_punishment_string += f'''<div>{addition_punishment['content']}</div>'''
        # if addition_punishment_string != '':
        #     message += f'''<div>{addition_punishment_string}</div>'''
        message += f'''<div>{i+1}. {violation["name"]}</div>'''
        message += f'''<div>{violation["fine"]}</div>'''
        message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
        message += '</div>'
        i = i + 1

    return message


def handle_list_violation(entities):
    message = ''
    list_id = []
    violations = []
    filter_string = ''
    filters = []

    for entity in entities:
        name = entity["entity"]
        value = entity["value"]
        if name == "hanh_vi_vi_pham":
            filters.append(
                f'''regex(LCASE(?action_name), "{value.lower()}")''')
        if name == "doi_tuong_tham_gia_giao_thong" or name == "doi_tuong_khac":
            filters.append(
                f'''regex(LCASE(?traffic_participant_name), "{value.lower()}")''')
    if len(filters) > 0:
        filter_string += f'''filter ({" || ".join(filters)}) \n.'''

    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?violation \n'
        '       :So ?point_num ;\n'
        '       :Ten ?point_name ;\n'
        '       :ThuocKhoan ?clause ;\n'
        '       :CoDoiTuongXuPhat ?violator ;\n'
        '       :BiPhatTien ?fine ;\n'
        '       :CoHanhViViPham ?action .\n'
        '   ?action :Ten ?action_name .\n'
        '   ?violator :Ten ?violator_name .\n'
        '   ?fine :TienPhat ?fine_value .\n'
        '   ?clause :So ?clause_num .\n'
        '   ?clause :Ten ?clause_name .\n'
        '   ?clause :ThuocDieu ?article .\n'
        '   ?article :So ?article_num .\n'
        '   ?article :Ten ?article_name .\n'
        '   ?article :ThuocMuc ?section .\n'
        '   ?section :So ?section_num .\n'
        '   ?section :Ten ?section_name .\n'
        '   ?section :ThuocChuong ?chapter .\n'
        '   ?chapter :So ?chapter_num .\n'
        '   ?chapter :Ten ?chapter_name .\n'
        '   ?chapter :ThuocVanBan ?text .\n'
        '   ?text :So ?text_num .\n'
        '   ?text :Ten ?text_name .\n'
        f'   {filter_string}'
        '   OPTIONAL { \n'
        '       ?violation\n'
        '           :XayRaTai ?where ;\n'
        '           :XayRaVao ?time ;\n'
        '           :CoDoiTuongThamGia ?traffic_participant .\n'
        '       ?traffic_participant :Ten ?traffic_participant_name .\n'
        '   }\n'
        '}\n'
    )

    print(query)
    data = json.loads('{}')

    result = g.query(query)

    for item in result:
        # fine = item.get("fine_value")
        code = item.get("violation").split("#")[1]
        violator = item.get("violator_name")
        # legal = item.get("legal_name")

        if code in data:
            index_violator = find_item(data[code]['violators'], violator)
            if index_violator < 0:
                data[code]['violators'].append(violator)
        else:
            data[code] = {
                "id": code,
                "legal": {
                    "num": item.get("text_num"),
                    "name": item.get("text_name"),
                    "chapter": {
                        "name": item.get("chapter_name"),
                        "num": item.get("chapter_num"),
                    },
                    "section": {
                        "name": item.get("section_name"),
                        "num": item.get("section_num"),
                    },
                    "article": {
                        "name": item.get("article_name"),
                        "num": item.get("article_num"),
                    },
                    "clause": {
                        "name": item.get("clause_name"),
                        "num": item.get("clause_num"),
                    },
                    "point": {
                        "name": item.get("point_name"),
                        "num": item.get("point_num"),
                    },
                },
                "violators": [violator]
            }
            list_id.append(code)

    # for item in result:
    #     fine = item.get("fine_value")
    #     code = item.get("violation").split("#")[1]
    #     violator = item.get("violator_name")
    #     legal = item.get("legal_name")
    #     list_code.append(code)

    #     if code in data:
    #         index_violator = find_item(data[code]['violators'], violator)
    #         if index_violator < 0:
    #             data[code]['violators'].append(violator)
    #     else:
    #         data[code] = {
    #             "id": code,
    #             "fine": fine,
    #             "legal": legal,
    #             "violators": [violator]
    #         }
    #         list_id.append(code)

    for item_id in list_id:
        if item_id in data:
            violations.append(data[item_id])

    i = 0

    # for violation in violations:
    #     values = []
    #     for entity in entities:
    #         value = entity['value']
    #         values.insert(0, f'''contains(LCASE(?content), "{value}")''')

    for violation in violations:
        if i != 0:
            message += '<br/>'
        message += '<div>'
        message += f"""<div>Theo {violation["legal"]["name"].split(violation["legal"]["num"])[0]}{violation["legal"]["num"]} chương {violation["legal"]["chapter"]["num"]} mục {violation["legal"]["section"]["num"]} điều {violation["legal"]["article"]["num"]}. {violation["legal"]["article"]["name"]}</div>"""
        message += f'''<div>{violation["legal"]["clause"]["num"]}. {violation["legal"]["clause"]["name"]}</div>'''
        message += f'''<div>{violation["legal"]["point"]["num"]}. {violation["legal"]["point"]["name"]}</div>'''
        # message += f'''<div>Đối tượng xử phạt: {violation["violators"]}</div>'''
        # message += f'''<div>{violation["legal"]}</div>'''
        # message += f'''<div>{violation["fine"]}</div>'''
        # message += f'''<div>Vi phạm: {violation['content']}</div>
        #         <div>Đối tượng: {violation['violator']}</div>
        #         <div>{violation['punishment']}</div>'''
        # addition_punishment_string = ''
        # for addition_punishment in violation['addition_punishments']:
        #     addition_punishment_string += f'''<div>{addition_punishment['content']}</div>'''
        # if addition_punishment_string != '':
        #     message += f'''<div>{addition_punishment_string}</div>'''
        message += '</div>'
        i = i + 1

    return message


def handle_concept(entities):
    message = ""
    # Tạo Graph
    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    filter_string = ""
    filters = []

    for entity in entities:
        value = entity['value']
        filters.append(f'''(LCASE(?keyword) =  "{value.lower()}")''')

    if len(filters) > 0:
        filter_string = f'''filter ({" || ".join(filters)})'''

    # Tạo chuỗi query
    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?concept\n'
        '       :Ten ?name ;\n'
        '       :YNghia ?meaning ;\n'
        '       :TuKhoa ?keyword .\n'
        f'{filter_string} . \n'
        '}\n'
    )
    print(query)
    result = g.query(query)

    concepts = []
    data = json.loads("{}")
    list_code = []

    for item in result:
        name = item.get("name")
        meaning = item.get("meaning")
        keyword = item.get("keyword")
        code = item.get("concept").split("#")[1]
        list_code.append(code)
        if code in data:
            data[code]["keywords"].append(keyword)
        else:
            data[code] = {
                "id": code,
                "meaning": meaning,
                "name": name,
                "keywords": [keyword]
            }

    most_code = get_most_common_elements(list_code)
    print(list_code)

    if len(most_code) > 0:
        random_code = random_item(most_code)
        message += f'''
            <div>{data[random_code]["name"]} {data[random_code]["meaning"]}</div>
        '''

    return message


def get_answer(text):
    message = ""
    # try:
    print("TOKEN=", os.getenv("SERVER_ACCESS_TOKEN"))
    client = Wit(os.getenv("SERVER_ACCESS_TOKEN"))
    data = client.get_message(text)
    print(data)
    intents = []
    if "intent" in data["outcomes"][0]["entities"]:
        intents = data["outcomes"][0]["entities"]["intent"]
    entities = []
    keys = data["outcomes"][0]["entities"].keys()
    for key in keys:
        if key != "intent":
            for obj in data["outcomes"][0]["entities"][key]:
                split_key = key.split(":")
                entity = {
                    "value": obj["value"],
                    "entity": split_key[0] if len(split_key) > 0 else key
                }

                entities.append(entity)

    if len(intents) > 0:
        intent_high_confidence = intents[0]
        label = intent_high_confidence['value']
        if label in sample_answers:
            message = random_item(sample_answers[label])
        elif label == "xem_muc_phat" or label == "liet_ke_vi_pham":
            message = handle_violation(entities)
        elif label == 'xem_khai_niem':
            message = handle_concept(entities)
        # elif label == 'liet_ke_vi_pham':
        #     message = handle_list_violation(entities)
    if message == '':
        return random_item(unclear_answers)
    return message
    # except:
    #     return random_item(unclear_answers)
