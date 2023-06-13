from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL, RDFS
from app.helpers.to_code import to_code
import math
import json


def get_group_traffic_signs(p, limit, sort_by, sort_type):
    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?group_traffic_sign\n'
        '       :Ten ?name ;\n'
        '       :TacDung ?effect ;\n'
        '       :MoTa ?description .\n'
        '   OPTIONAL {\n'
        '       ?traffic_sign\n'
        '           :ThuocBienBao ?group_traffic_sign ;\n'
        '           :MaBienBao ?c_code ;\n'
        '           :HinhAnh ?image ;\n'
        '           :MoTa ?c_description ;\n'
        '           :Ten ?c_name .\n'
        '   }\n'
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
        description = item.get("description")
        code = item.get("group_traffic_sign").split("#")[1]
        
        traffic_sign = None
        if item.get("traffic_sign"):
            image = item.get("image")
            c_name = item.get("c_name")
            c_description = item.get("c_description")
            c_code = item.get("c_code")
            c_id = item.get("traffic_sign").split("#")[1],
            traffic_sign = {
                "id": item.get("traffic_sign").split("#")[1],
                "code": c_code,
                "description": c_description,
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
                "description": description,
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
    description = json_dto["description"]
    code = to_code(name)


    g = Graph()
    g.parse('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    name_space = "http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#"

    # Định nghĩa các namespace
    ns = Namespace(name_space)

    # Định nghĩa các URIRef
    uri_name = URIRef(f'{name_space}Ten')
    uri_effect = URIRef(f'{name_space}TacDung')
    uri_description = URIRef(f'{name_space}MoTa')
    uri_super_class = URIRef(f'{name_space}BienBaoGiaoThong')
    uri_class = URIRef(f'{name_space}{code}')

    # Tạo các đối tượng URIRef và Literal
    g.add((ns[code], RDFS.subClassOf, uri_super_class))
    g.add((ns[code], RDF.type, uri_class))
    g.add((ns[code], uri_name, Literal(name)))
    g.add((ns[code], uri_effect, Literal(effect)))
    g.add((ns[code], uri_description, Literal(description)))
    g.serialize('./app/ontology/luatgt copy 4.rdf', format="application/rdf+xml")

    return {
        "id": code,
        "name": name,
        "effect": effect,
        "description": description
    }