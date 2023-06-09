import math
import json
from rdflib import Graph
from app.helpers.find_item import find_item


def handle_result(result):
    data = json.loads('{}')
    list_id = []
    violations = []

    for item in result:
        fine = item.get("fine_value")
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
                "violators": [violator],
                "fine": fine
            }
            list_id.append(code)

    for id_item in list_id:
        if id_item in data:
            data[id_item]["violators"] = ", ".join(
                data[id_item]["violators"])
            violations.append(data[id_item])

    return violations


def search_violations(keyword, limit, page):
    g = Graph()
    g.parse("./app/ontology/luatgt.rdf", format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?violation \n'
        '       :So ?point_num ;\n'
        '       :Ten ?point_name ;\n'
        '       :ThuocKhoan ?clause ;\n'
        '       :CoDoiTuongXuPhat ?violator ;\n'
        '       :BiPhatTien ?fine .\n'
        '   ?fine :TienPhat ?fine_value .\n'
        '   ?violator :Ten ?violator_name .\n'
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
        f'  filter (regex(LCASE(?point_name), "{keyword.lower()}")) .\n'
        '}\n'
    )

    print(query)

    result = g.query(query)

    violations = handle_result(result)

    count = len(violations)
    total_pages = math.ceil(count / limit)

    start = limit * (page - 1)
    end = start + limit

    return {
        "count": count,
        "total_pages": total_pages,
        "rows": violations[start:end],
    }


def get_violation_by_id(id):
    g = Graph()
    g.parse("./app/ontology/luatgt.rdf", format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?violation \n'
        '       :So ?point_num ;\n'
        '       :Ten ?point_name ;\n'
        '       :ThuocKhoan ?clause ;\n'
        '       :CoDoiTuongXuPhat ?violator ;\n'
        '       :BiPhatTien ?fine .\n'
        '   ?fine :TienPhat ?fine_value .\n'
        '   ?violator :Ten ?violator_name .\n'
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
        f'   filter(?violation = :{id})'
        '}\n'
    )

    print(query)

    result = g.query(query)

    violations = handle_result(result)

    if len(violations) > 0:
        return violations[0]

    return None
