from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL, RDFS
from app.helpers.to_code import to_code
import math


def handle_result(result):
    traffic_signs = []

    for item in result:
        g_name = item.get("g_name")
        g_effect = item.get("g_effect")
        g_description = item.get("g_description")
        code = item.get("code")
        g_id = item.get("groupTrafficSign").split("#")[1]
        image = item.get("image")
        name = item.get("name")
        description = item.get("description")

        traffic_signs.append({
           "id": item.get("trafficSign").split("#")[1],
           "code": code,
           "description": description,
           "name": name,
           "image": image,
           "groupTrafficSignId": g_id,
           "groupTrafficSign": {
               "id" : g_id,
               "name": g_name,
               "effect": g_effect,
               "description": g_description
           }
        })

    return traffic_signs


def get_traffic_signs(p, limit, sort_by, sort_type):
    g = Graph()
    g.parse('./app/ontology/luatgt.rdf', format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?groupTrafficSign\n'
        '       :TacDung ?g_effect ;\n'
        '       :MoTa ?g_description ;\n'
        '       :Ten ?g_name .\n'
        '   ?trafficSign\n'
        '       :ThuocBienBao ?groupTrafficSign ;\n'
        '       :MaBienBao ?code ;\n'
        '       :HinhAnh ?image ;\n'
        '       :MoTa ?description ;\n'
        '       :Ten ?name .\n'
        '}\n'
        f'order by {sort_type}(?{sort_by})'
    )
    print(query)
    result = g.query(query)

    traffic_signs = handle_result(result)

    count = len(traffic_signs)

    start = 0
    end = count - 1
    total_pages = 1
    rows = traffic_signs

    if limit > -1 and p > -1:
        start = limit * (p - 1)
        end = start + limit
        total_pages = math.ceil(count / limit)
        rows = traffic_signs[start:end]


    return {
        "rows": rows,
        "total_pages": total_pages,
        "count": count
    }


def create_traffic_sign(json_dto):

    code = json_dto["code"]
    description = json_dto["description"]
    name = json_dto["name"]
    image = json_dto["image"]
    group_traffic_sign_id = json_dto["groupTrafficSignId"]
    name_individual = "BienBao"+to_code(code)

    g = Graph()
    g.parse('./app/ontology/luatgt.rdf', format="application/rdf+xml")

    name_space = "http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#"

    # Định nghĩa các namespace
    ns = Namespace(name_space)

    # Định nghĩa các URIRef
    uri_name = URIRef(f'{name_space}Ten')
    uri_id = URIRef(f'{name_space}MaBienBao')
    uri_description = URIRef(f'{name_space}MoTa')
    uri_image = URIRef(f'{name_space}HinhAnh')
    uri_super_class = URIRef(f'{name_space}{group_traffic_sign_id}')
    uri_class = URIRef(f'{name_space}{name_individual}')
    uri_op = URIRef(f'{name_space}ThuocBienBao')

    # Tạo các đối tượng URIRef và Literal
    g.add((ns[name_individual], RDFS.subClassOf, uri_super_class))
    g.add((ns[name_individual], RDF.type, uri_class))
    g.add((ns[name_individual], uri_op, uri_super_class))
    g.add((ns[name_individual], uri_name, Literal(name)))
    g.add((ns[name_individual], uri_image, Literal(image)))
    g.add((ns[name_individual], uri_id, Literal(code)))
    g.add((ns[name_individual], uri_description, Literal(description)))
    g.serialize('./app/ontology/luatgt.rdf', format="application/rdf+xml")

    return {
        "id": name_individual,
        "code": code,
        "image": image,
        "groupTrafficId": group_traffic_sign_id,
        "description": description,
        "name": name
    }
