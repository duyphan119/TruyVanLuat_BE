from rdflib import Graph
import json


def handle_result(result):
    traffic_signs = []
    data = json.loads('{}')
    list_id = []

    for item in result:
        g_name = item.get("g_name")
        g_meaning = item.get("g_meaning")
        code = item.get("BienBao").split("#")[1]

        if code in data:
            item_code = item.get("code")
            image = item.get("image")
            name = item.get("name")
            data[code]["children"].append({
                "name": name,
                "image": image,
                "code": item_code
            })

        else:
            data[code] = {
                "id": code,
                "name": g_name,
                "meaning": g_meaning,
                "children": []
            }

        found = False

        for value in list_id:
            if value == code:
                found = True
        if not found:
            list_id.append(code)

    for sign_code in list_id:
        if sign_code in data:
            traffic_signs.append(data[sign_code])

    return traffic_signs


def get_traffic_signs():
    g = Graph()
    g.parse('./app/ontology/luatgt.rdf', format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?BienBao\n'
        '       :Ten ?g_name ;\n'
        '       :YNghia ?g_meaning .\n'
        '   ?ChiTietBienBao\n'
        '       :ThuocBienBao ?BienBao ;\n'
        '       :MaBienBao ?code ;\n'
        '       :HinhAnh ?image ;\n'
        '       :Ten ?name .\n'
        '}\n'
    )

    result = g.query(query)

    traffic_signs = handle_result(result)

    return {
        "rows": traffic_signs,
        "count": len(traffic_signs),
        "total_pages": 1
    }
