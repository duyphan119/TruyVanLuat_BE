import requests
from rdflib import Graph
import os
import json
from app.helpers.find_item import find_item


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
                f'''regex(LCASE(?action_name), "{value.lower()}")''')
        if name == "doi_tuong_tham_gia_giao_thong" or name == "doi_tuong_khac":
            filters.append(
                f'''regex(LCASE(?traffic_participant_name), "{value.lower()}")''')
    if len(filters) > 0:
        filter_string += f'''filter ({" || ".join(filters)}) \n.'''
    # Tạo Graph
    g = Graph()
    g.parse('./app/ontology/luatgt.rdf', format="application/rdf+xml")
    # Tạo chuỗi query

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?violation \n'
        '       :CoDiem ?legal ;\n'
        '       :CoDoiTuongXuPhat ?violator ;\n'
        '       :ThuocNhomViPham ?group ;\n'
        '       :BiPhatTien ?fine ;\n'
        '       :CoHanhViViPham ?action .\n'
        '   ?action :Ten ?action_name .\n'
        '   ?legal :Ten ?legal_name .\n'
        '   ?violator :Ten ?violator_name .\n'
        '   ?fine :TienPhat ?fine_value .\n'
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
    list_code = []

    result = g.query(query)

    for item in result:
        fine = item.get("fine_value")
        code = item.get("violation").split("#")[1]
        violator = item.get("violator_name")
        legal = item.get("legal_name")
        list_code.append(code)

        if code in data:
            index_violator = find_item(data[code]['violators'], violator)
            if index_violator < 0:
                data[code]['violators'].append(violator)
        else:
            data[code] = {
                "id": code,
                "fine": fine,
                "legal": legal,
                "violators": [violator]
            }
            list_id.append(code)

    result_code = find_most_frequent_element(list_code)[0]

    if result_code in data:
        print("HELLO:::::::", data[result_code])
        data[result_code]["violators"] = ", ".join(
            data[result_code]["violators"])
        violations.append(data[result_code])

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
        message += f'''<div>Đối tượng xử phạt: {violation["violators"]}</div>'''
        message += f'''<div>{violation["legal"]}</div>'''
        message += f'''<div>{violation["fine"]}</div>'''
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
    g.parse('./app/ontology/luatgt.rdf', format="application/rdf+xml")

    filter_string = ""
    filters = []

    for entity in entities:
        value = entity['value']
        filters.append(f'''(LCASE(?keywords) =  "{value.lower()}")''')

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
        '       :TuKhoa ?keywords .\n'
        f'{filter_string} . \n'
        '}\n'
    )
    print(query)
    result = g.query(query)

    for item in result:
        name = item.get("name")
        meaning = item.get("meaning")

        message += f'''
                <div>{name} {meaning}</div>
            '''
        break

    return message


def get_answer(data):
    message = ""

    url = "https://v3-api.fpt.ai/api/v3/predict"
    token_bot = os.getenv("TOKEN_BOT")

    response = requests.post(url, json={"content": data, "save_history": False}, headers={
                             "Authorization": f"Bearer {token_bot}"})

    json_obj = response.json()

    data = json_obj["data"]
    intents = data["intents"]
    entities = data["entities"]

    if len(intents) > 0:
        intent_high_confidence = intents[0]
        label = intent_high_confidence['label']

        if label == "hinh_phat":
            message = handle_violation(entities)
        elif label == 'khai_niem':
            message = handle_concept(entities)
        # if label == 'xem_dieu_khoan':
        #     message = handle_xem_dieu_khoan(entities)
        # elif label == "hinh_phat":
        #     message = handle_violation(entities)
    if message == '':
        return 'Xin lỗi, bạn vui lòng hỏi câu khác'
    return message
