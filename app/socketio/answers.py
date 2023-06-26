from rdflib import Graph
import json
from app.helpers.find_item import find_item
from app.helpers.random_item import random_item
from app.data.sample_answers import sample_answers, unclear_answers
from wit import Wit
import os
from app.helpers.get_most_common_elements import get_most_common_elements
from app.controllers.violation_controller import handle_result, search_violations, get_all_violations
from app.controllers.message_controller import get_keywords
from app.models.user import find_by_id
from app.models.message import save_message_json, find_by_user_id, Message
from datetime import datetime
from unidecode import unidecode


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
    violations = get_all_violations()
    keywords = get_keywords(entities)

    new_violations = []

    for violation in violations:
        new_name = unidecode(violation["name"])
        matches = all(kw in new_name.lower() for kw in keywords)
        if matches:
            new_violations.append(violation)


    return new_violations
    message = ''
    list_id = []
    violations = []
    filter_string = ''
    filters = []

    for entity in entities:
        name = entity["entity"]
        value = entity["value"]
        if name == "doi_tuong_xu_phat":
            filters.append(
                f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?doituongxuphat), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
        else:
            filters.append(
                f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?tenvipham), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
        
        # if name == "hanh_vi_vi_pham":
        #     filters.append(
        #         f'''contains(LCASE(?tenhanhvivipham), "{value.lower()}")''')
        # if name == "vi_pham_ve":
        #     filters.append(
        #         f'''contains(LCASE(?tendoituongbitacdong), "{value.lower()}")''')
        # if name == "doi_tuong_tham_gia_giao_thong":
        #     filters.append(
        #         f'''(contains(LCASE(?tendoituongxuphat), "{value.lower()}") || contains(LCASE(?tendoituongbitacdong), "{value.lower()}"))''')
        # if name == "khu_vuc":
        #     filters.append(
        #         f'''contains(LCASE(?tenkhuvuc), "{value.lower()}")''')
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
    #     '   ?vipham\n'
    #     '       :Ten ?tenvipham ;\n'
    #     '       :ChiTiet ?chitietvipham ;\n'
    #     '       :CoDoiTuongXuPhat ?doituongxuphat ;\n'
    #     # '       :BiPhatTien ?mucphat ;\n'
    #     '       :TienPhat ?mucphattien ;\n'
    #     '       :CoHanhViViPham ?hanhvivipham ;\n'
    #     '       :XayRaVoi ?doituongbitacdong .\n'
    #     '   ?doituongxuphat\n'
    #     '       :Ten ?tendoituongxuphat .\n'
    #     # '   ?mucphat\n'
    #     # '       :TienPhat ?mucphattien .\n'
    #     '   ?hanhvivipham\n'
    #     '       :Ten ?tenhanhvivipham .\n'
    #     '   ?doituongbitacdong :Ten ?tendoituongbitacdong .\n'
    #     f'  {filter_string}\n'
    #     '}\n'
    # )
    # print(query)

    # result = g.query(query)

    # violations = handle_result(result)

    query1 = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?vipham\n'
        '       :Ten ?tenvipham ;\n'
        '       :ChiTiet ?chitietvipham ;\n'
        '       :DTXuPhat ?doituongxuphat ;\n'
        '       :TienPhat ?mucphattien .\n'
        '   OPTIONAL {\n'
        '       ?vipham\n'
        '           :PhatBoSung ?pbs ;\n'
        '           :ChiTietPhatBoSung ?ctpbs ;\n'
        '           :KhacPhuc ?kp ;\n'
        '           :ChiTietKhacPhuc ?ctkp ;\n'
        '           :GhiChu ?ghichu .\n'
        '   }\n'
        f'{filter_string}\n'
        '}\n'
    )
    print(query1)

    result = g.query(query1)

    violations = handle_result(result)

    return violations


def handle_list_violation(entities):
    violations = get_all_violations()
    keywords = get_keywords(entities)

    new_violations = []

    for violation in violations:
        new_name = unidecode(violation["name"])
        new_behavior = unidecode(violation["behavior"])
        new_violator = unidecode(violation["violator"])
        ok = True
        for entity in entities:
            if entity["entity"] == "hanh_vi_vi_pham":
                matches = all(kw in new_behavior.lower() for kw in unidecode(entity["value"]).lower().split(" "))
                if not matches:
                    ok = False
            elif entity["entity"] == "doi_tuong_xu_phat":
                matches = all(kw in new_violator.lower() for kw in unidecode(entity["value"]).lower().split(" "))
                if not matches:
                    ok = False
            else:
                matches = all(kw in new_name.lower() for kw in unidecode(entity["value"]).lower().split(" "))
                if not matches:
                    ok = False
        # matches = all(kw in new_name.lower() for kw in keywords)
        if ok:
            new_violations.append(violation)


    return new_violations


    message = ''
    list_id = []
    violations = []
    filter_string = ''
    filters = []
    dtxp_filters = []
    and_filters = []
    dtk_filters = []
    dttg_filters=[]

   

    for entity in entities:
        name = entity["entity"]
        value = entity["value"]
        print(name, value)
        # if name == "doi_tuong_khac" or name == "vi_pham_ve":
        #     dtk_filters.append(
        #         f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?tenvipham), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
        # elif name == "doi_tuong_tham_gia_giao_thong":
        #     dttg_filters.append(
        #         f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?tenvipham), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
        # elif name == "doi_tuong_xu_phat":
        #     dtxp_filters.append(
        #         f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?doituongxuphat), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
        # else:
        #     filters.append(
        #         f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?tenvipham), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
        if name == "hanh_vi_vi_pham":
            filters.append(
                f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?tenhanhvivipham), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
        elif name == "doi_tuong_tham_gia_giao_thong":
            filters.append(
                f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?tendoituongxuphat), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
        else:
            filters.append(
                f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?tendoituongbitacdong), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')
    
    # if len(filters) > 0:
    #     and_filters.append(f'''({" || ".join(filters)})''')
    # if len(dtxp_filters) > 0:
    #     and_filters.append(f'''({" || ".join(dtxp_filters)})''')
    # if len(dtk_filters) > 0:
    #     and_filters.append(f'''({" || ".join(dtk_filters)})''')
    # if len(dttg_filters) > 0:
    #     and_filters.append(f'''({" || ".join(dttg_filters)})''')
    # if len(and_filters) > 0 :
    #     filter_string += f'''filter ({" && ".join(and_filters)}) .'''
    if len(filters) > 0:
        filter_string += f'''filter ({" || ".join(filters)}) .'''

    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        # '   ?vipham\n'
        # '       :Ten ?tenvipham ;\n'
        # '       :ChiTiet ?chitietvipham ;\n'
        # '       :CoDoiTuongXuPhat ?doituongxuphat ;\n'
        #  '       :TienPhat ?mucphattien ;\n'
        # '       :CoHanhViViPham ?hanhvivipham ;\n'
        # '       :XayRaVoi ?doituongbitacdong .\n'
        # '   ?doituongxuphat\n'
        # '       :Ten ?tendoituongxuphat .\n'
        # '   ?hanhvivipham\n'
        # '       :Ten ?tenhanhvivipham .\n'
        # '   ?doituongbitacdong :Ten ?tendoituongbitacdong .\n'

        '   ?vipham\n'
        '       :Ten ?tenvipham ;\n'
        '       :ChiTiet ?chitietvipham ;\n'
        '       :CoDoiTuongXuPhat ?doituongxuphat ;\n'
        '       :CoHanhViViPham ?hanhvivipham ;\n'
        '       :TienPhat ?mucphattien .\n'
        '   ?hanhvivipham :Ten ?tenhanhvivipham .\n'
        '   ?doituongxuphat :Ten ?tendoituongxuphat .\n'
        '   OPTIONAL {\n'
        '       ?vipham :XayRaVoi ?doituongbitacdong .\n'
        '       ?doituongbitacdong :Ten ?tendoituongbitacdong .\n'
        '   }\n'


        f'  {filter_string}\n'
        '}\n'
    )
    # print(query)

    result = g.query(query)

    violations = handle_result(result)

    # query1 = (
    #     'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
    #     'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
    #     'SELECT * WHERE {\n'
    #     '   ?vipham\n'
    #     '       :Ten ?tenvipham ;\n'
    #     '       :ChiTiet ?chitietvipham ;\n'
    #     '       :DTXuPhat ?doituongxuphat ;\n'
    #     '       :TienPhat ?mucphattien .\n'
    #     '   OPTIONAL {\n'
    #     '       ?vipham\n'
    #     '           :PhatBoSung ?pbs ;\n'
    #     '           :ChiTietPhatBoSung ?ctpbs ;\n'
    #     '           :KhacPhuc ?kp ;\n'
    #     '           :ChiTietKhacPhuc ?ctkp ;\n'
    #     '           :GhiChu ?ghichu .\n'
    #     '   }\n'
    #     f'{filter_string}\n'
    #     '}\n'
    # )
    # print(query1)

    # result = g.query(query1)

    # violations = handle_result(result)

    return violations[0:5]


def handle_concept(entities):
    message = ""
    # Tạo Graph
    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    filter_string = ""
    filters = []

    for entity in entities:
        value = entity['value']
        filters.append(
            f'''regex(replace(replace(replace(replace(replace(replace(LCASE(?keyword), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(value)}"))''')

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
        return data[random_code]
    #     message += f'''
    #         <div>{data[random_code]["name"]} {data[random_code]["meaning"]}</div>
    #     '''

    # return message
    return None
def generate_href_id(detail):
  split_txt = detail.split(" ")
  if split_txt[0] == "Điểm" :
    return f'''diem_{split_txt[5]}_{split_txt[3]}_{"dd" if split_txt[1] == "đ" else split_txt[1]}'''
  
  elif split_txt[0] == "Khoản":
    return f'''khoan_{split_txt[3]}_{"dd" if split_txt[1] == "đ" else split_txt[1]}'''
  elif split_txt[0] == "Điều" :
    return f'''dieu_{split_txt[1]}'''

  return ""


def get_answer(text, user_id, is_logged, list_bot_msg):
    try:
        message = ""

        client = Wit(os.getenv("SERVER_ACCESS_TOKEN"))
        data = client.get_message(text)
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
            print("label:", label)

            if is_logged:
                inserted_id = save_message_json({
                    "content": text,
                    "user_id": user_id,
                    "intent": label,
                    "entities": entities,
                    "is_sender": True,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                })

            data = {
                "content": message,
                "user_id": user_id,
                "intent": label,
                "entities": [],
                "is_sender": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            if label in sample_answers:
                message = random_item(sample_answers[label])
                data["content"] = message
                if is_logged:
                    inserted_id = save_message_json(data)
                    data["id"] = inserted_id
                    data["_id"] = inserted_id

                    return {
                        "answer": data
                    }
            elif label == "liet_ke_vi_pham" or label == "xem_muc_phat":
                if len(entities) == 0:
                    if len(list_bot_msg) > 0:
                        entities = list_bot_msg[0].entities
                if len(entities) > 0:
                    violations = handle_list_violation(entities)
                    print("DKM",len(violations))
                    i = 0
                    if len(violations) > 0:
                        message += f'<div>Có {len(violations)} hình phạt tương ứng:</div>'
                        for violation in violations:
                            message += f'<div>'
                            message += f'''<div style="font-weight: 600;">{i + 1}. {violation["name"]}</div>'''
                            message += f'''<div>{violation["fine"]}</div>'''
                            message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
                            message += '</div>'
                            i = i + 1
                    else:
                        message += f'<div>Xin lỗi, tôi không tìm thấy câu trả lời.</div>'
                    data["content"] = message
                    data["violations"] = violations
                    if is_logged:
                        inserted_id = save_message_json(data)

                        data["id"] = inserted_id
                        data["_id"] = inserted_id
                    return {
                        "answer": data
                    }
            # elif label == "xem_muc_phat":
            #     violations = handle_violation(entities)
            #     i = 0
            #     if len(violations) > 0:
            #         message += f'<div>Có {len(violations)} hình phạt tương ứng:</div>'
            #         for violation in violations:
            #             message += f'<div>'
            #             message += f'''<div>{i + 1}. {violation["name"]}</div>'''
            #             message += f'''<div>{violation["fine"]}</div>'''
            #             message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
            #             message += '</div>'
            #             i = i + 1
            #     else:
            #         message += f'<div>Xin lỗi, tôi không tìm thấy câu trả lời.</div>'
            #     data["content"] = message
            #     data["violations"] = violations
            #     if is_logged:
            #         inserted_id = save_message_json(data)

            #         data["id"] = inserted_id
            #         data["_id"] = inserted_id
            #     return {
            #         "answer": data
            #     }
            elif label == 'xem_khai_niem':
                concept = handle_concept(entities)
                if concept:
                    message += f'<div>{concept["name"]} {concept["meaning"]}</div>'
                    data["content"] = message
                    if is_logged:
                        inserted_id = save_message_json(data)

                        data["id"] = inserted_id
                        data["_id"] = inserted_id
                    return {
                        "answer": data
                    }
                else:
                    print("LON2", len(intents))
                    message += f'<div>Xin lỗi, tôi chưa biết khái niệm này là gì</div>'
                    data["content"] = message
                    if is_logged:
                        inserted_id = save_message_json(data)

                        data["id"] = inserted_id
                        data["_id"] = inserted_id
                    return {
                        "answer": data
                    }
            elif label == 'xem_chi_tiet_vi_pham':
                for entity in entities:
                    name = entity["entity"]
                    value = entity["value"]
                    if name == "index":
                        for bot_msg in list_bot_msg:
                            if "violations" in bot_msg:
                                index = 0
                                try:
                                    index = int(value)
                                    if len(bot_msg["violations"]) > index - 1:
                                        violation = bot_msg["violations"][index - 1]
                                        message += f'<div>'
                                        message += f'''<div><b>{violation["name"]}</b></div>'''
                                        message += f'''<div>{violation["fine"]}</div>'''
                                        message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
                                        message += f'''<a href="/nghi-dinh#{generate_href_id(violation["legal"])}" target="_blank"><u>Chi tiết: {violation["legal"]}</u></a>'''
                                        message += '</div>'
                                        data["content"] = message
                                        break
                                except:
                                    data["content"] = random_item(unclear_answers),
                                
                    else:
                        print("LON1", len(intents))
                        violations = handle_violation(entities)
                        if len(violations) > 0:
                            violation = violations[0]
                            message += f'<div>'
                            message += f'''<div><b>{violation["name"]}</b></div>'''
                            message += f'''<div>{violation["fine"]}</div>'''
                            message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
                            message += f'''<a href="/nghi-dinh#{generate_href_id(violation["legal"])}" target="_blank"><u>Chi tiết: {violation["legal"]}</u></a>'''
                            message += '</div>'
                            data["content"] = message
                            break
            else:
                print("ELSE NGU")
                if len(list_bot_msg) > 0:
                    msg = list_bot_msg[0]
                    lb = msg["intent"]
                    if lb in sample_answers:
                        message = random_item(sample_answers[lb])
                        data["content"] = message
                        if is_logged:
                            inserted_id = save_message_json(data)
                            data["id"] = inserted_id
                            data["_id"] = inserted_id

                            return {
                                "answer": data
                            }
                    elif lb == "liet_ke_vi_pham":
                        violations = handle_list_violation(entities)
                        i = 0
                        if len(violations) > 0:
                            message += f'<div>Có {len(violations)} hình phạt tương ứng:</div>'
                            for violation in violations:
                                message += f'<div>'
                                message += f'''<div>{i + 1}. {violation["name"]}</div>'''
                                message += f'''<div>{violation["fine"]}</div>'''
                                message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
                                message += '</div>'
                                i = i + 1
                        else:
                            message += f'<div>Xin lỗi, tôi không tìm thấy câu trả lời.</div>'
                        data["content"] = message
                        data["violations"] = violations
                        if is_logged:
                            inserted_id = save_message_json(data)

                            data["id"] = inserted_id
                            data["_id"] = inserted_id
                        return {
                            "answer": data
                        }
                    elif lb == "xem_muc_phat":
                        violations = handle_violation(entities)
                        i = 0
                        if len(violations) > 0:
                            message += f'<div>Có {len(violations)} hình phạt tương ứng:</div>'
                            for violation in violations:
                                message += f'<div>'
                                message += f'''<div>{i + 1}. {violation["name"]}</div>'''
                                message += f'''<div>{violation["fine"]}</div>'''
                                message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
                                message += '</div>'
                                i = i + 1
                        else:
                            message += f'<div>Xin lỗi, tôi không tìm thấy câu trả lời.</div>'
                        data["content"] = message
                        data["violations"] = violations
                        if is_logged:
                            inserted_id = save_message_json(data)

                            data["id"] = inserted_id
                            data["_id"] = inserted_id
                        return {
                            "answer": data
                        }
                    elif lb == 'xem_khai_niem':
                        concept = handle_concept(entities)
                        if concept:
                            message += f'<div>{concept["name"]} {concept["meaning"]}</div>'
                            data["content"] = message
                            if is_logged:
                                inserted_id = save_message_json(data)

                                data["id"] = inserted_id
                                data["_id"] = inserted_id
                            return {
                                "answer": data
                            }
                    elif lb == 'xem_chi_tiet_vi_pham':
                        for entity in entities:
                            name = entity["entity"]
                            value = entity["value"]
                            if name == "index":
                                for bot_msg in list_bot_msg:
                                    if "violations" in bot_msg:
                                        index = int(value)
                                        if len(bot_msg["violations"]) > index - 1:
                                            violation = bot_msg["violations"][index - 1]
                                            message += f'<div>'
                                            message += f'''<div>{violation["name"]}</div>'''
                                            message += f'''<div>{violation["fine"]}</div>'''
                                            message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
                                            message += f'''<div>Chi tiết: {violation["legal"]}</div>'''
                                            message += '</div>'
                                            data["content"] = message
                                            break
                            else:
                                violations = handle_violation(entities)
                                if len(violations) > 0:
                                    violation = violations[0]
                                    message += f'<div>'
                                    message += f'''<div>{violation["name"]}</div>'''
                                    message += f'''<div>{violation["fine"]}</div>'''
                                    message += f'''<div>Đối tượng xử phạt: {violation["violator"]}</div>'''
                                    message += f'''<div>Chi tiết: {violation["legal"]}</div>'''
                                    message += '</div>'
                                    data["content"] = message
                                    break
        
        if message == '':
            data["content"] = random_item(unclear_answers)
            if is_logged:
                inserted_id = save_message_json(data)
                data["id"] = inserted_id
                data["_id"] = inserted_id
                return {
                    "answer": data
                }
        if not is_logged:
            return {
                "answer": {
                    "content": message,
                    "user_id": user_id,
                    "intent": intents[0]["value"] if len(intents) > 0 else "",
                    "entities": entities,
                    "is_sender": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
        return {
            "answer": {
                "content": random_item(unclear_answers),
                "user_id": user_id,
                "intent": intents[0]["value"] if len(intents) > 0 else "",
                "entities": entities,
                "is_sender": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        }

    except:
        return {
            "answer": {
                "content": random_item(unclear_answers),
                "user_id": user_id,
                "intent": intents[0]["value"] if len(intents) > 0 else "",
                "entities": entities,
                "is_sender": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        } 