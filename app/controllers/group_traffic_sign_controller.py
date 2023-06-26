from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL, RDFS
from app.helpers.to_code import to_code
import math
import json
from unidecode import unidecode


def get_group_traffic_signs(p, limit, sort_by, sort_type, keyword):
    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?group_traffic_sign\n'
        '       :Ten ?name ;\n'
        '       :YNghia ?effect .\n'
        '   OPTIONAL {\n'
        '       ?traffic_sign\n'
        '           :ThuocBienBao ?group_traffic_sign ;\n'
        '           :MaBienBao ?c_code ;\n'
        '           :HinhAnh ?image ;\n'
        '           :Ten ?c_name .\n'
        '   }\n'
        f'  filter (regex(replace(replace(replace(replace(replace(replace(LCASE(?c_name), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(keyword)}")) || regex(replace(replace(replace(replace(replace(replace(LCASE(?name), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(keyword)}")) || regex(replace(replace(replace(replace(replace(replace(LCASE(?effect), "[íìỉĩị]", "i"), "[đ]", "d"), "[úùủũụưứừửữự]", "u"), "[óòỏõọôốồổỗộơớờởỡợ]", "o"), "[éèẻẽẹêếềểễệ]", "e"), "[áàảãạấầẩẫậâăằẳẵặ]", "a"), LCASE("{unidecode(keyword)}"))) .\n'
        '}\n'

        f'order by {sort_type}(?{sort_by})'
    )
    print(query)
    result = g.query(query)

    group_traffic_signs = []
    data = json.loads("{}")
    list_id = []

    for item in result:
        name = item.get("name")
        effect = item.get("effect")
        code = item.get("group_traffic_sign").split("#")[1]
        
        traffic_sign = None
        if item.get("traffic_sign"):
            image = item.get("image")
            c_name = item.get("c_name")
            c_code = item.get("c_code")
            # c_id = item.get("traffic_sign").split("#")[1],
            traffic_sign = {
                "id": item.get("traffic_sign").split("#")[1],
                "code": c_code,
                "name": c_name,
                "image": image,
                "groupTrafficSignId": code
            }

        if code in data:
            if traffic_sign:
                data[code]["children"].append(traffic_sign)
        else:
            data[code] = {
                 "id": code,
                "name": name,
                "effect": effect,
                "children": []
            }
            if traffic_sign:
                data[code]["children"].append(traffic_sign)
            list_id.append(code)

    for result_code in list_id:
        group_traffic_signs.append(data[result_code])

    count = len(group_traffic_signs)

    start = 0
    end = count - 1
    total_pages = 1
    rows = group_traffic_signs

    if limit > -1 and p > -1:
        start = limit * (p - 1)
        end = start + limit
        total_pages = math.ceil(count / limit)
        rows = group_traffic_signs[start:end]


    return {
        "rows": rows,
        "total_pages": total_pages,
        "count": count
    }


def create_group_traffic_sign(json_dto):

    name = json_dto["name"]
    effect = json_dto["effect"]
    code = to_code(name)


    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    name_space = "http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#"

    # Định nghĩa các namespace
    ns = Namespace(name_space)

    # Định nghĩa các URIRef
    uri_name = URIRef(f'{name_space}Ten')
    uri_effect = URIRef(f'{name_space}TacDung')
    uri_super_class = URIRef(f'{name_space}BienBaoGiaoThong')
    uri_class = URIRef(f'{name_space}{code}')

    # Tạo các đối tượng URIRef và Literal
    g.add((ns[code], RDFS.subClassOf, uri_super_class))
    g.add((ns[code], RDF.type, uri_class))
    g.add((ns[code], uri_name, Literal(name)))
    g.add((ns[code], uri_effect, Literal(effect)))
    g.serialize('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    return {
        "id": code,
        "name": name,
        "effect": effect,
    }