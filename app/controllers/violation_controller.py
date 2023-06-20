import math
import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL, RDFS, XSD
from app.helpers.find_item import find_item

def handle_result(result):
    data = json.loads('{}')
    list_id = []
    violations = []
    list_solution_id = []
    list_pbs_id = []

    for item in result:
        # fine = item.get("fine_value")
        # code = item.get("violation").split("#")[1]
        # violator = item.get("violator_name")
        # legal = item.get("legal_name")

        # if code in data:
        #     index_violator = find_item(data[code]['violators'], violator)
        #     if index_violator < 0:
        #         data[code]['violators'].append(violator)
        # else:
        #     data[code] = {
        #         "id": code,
        #         "legal": {
        #             "num": item.get("text_num"),
        #             "name": item.get("text_name"),
        #             "chapter": {
        #                 "name": item.get("chapter_name"),
        #                 "num": item.get("chapter_num"),
        #             },
        #             "section": {
        #                 "name": item.get("section_name"),
        #                 "num": item.get("section_num"),
        #             },
        #             "article": {
        #                 "name": item.get("article_name"),
        #                 "num": item.get("article_num"),
        #             },
        #             "clause": {
        #                 "name": item.get("clause_name"),
        #                 "num": item.get("clause_num"),
        #             },
        #             "point": {
        #                 "name": item.get("point_name"),
        #                 "num": item.get("point_num"),
        #             },
        #         },
        #         "violators": [violator],
        #         "fine": fine
        #     }
        #     list_id.append(code)

        # print("code", code)

        code = item.get("vipham").split("#")[1]
        name = item.get("tenvipham")
        legal = item.get("chitietvipham")
        fine = item.get("mucphattien")
        violator = item.get("tendoituongxuphat")
        behavior = item.get("tenhanhvivipham")
        about = item.get("tendoituongbitacdong")
        violations.append({
            "id": code,
            "name": name,
            "legal": legal,
            "fine": fine,
            "violator": violator,
            "behavior": behavior,
            "about": about
        })

        # code = item.get("mavipham")
        # content = item.get("noidungvipham")
        # legal = item.get("luatvipham")
        # fine = item.get("mucphat")
        # violator = item.get("doituongxuphat")
        # keywords = item.get("tukhoa")
        # pbs = {
        #     "id": item.get("maphatbosung"),
        #     "content": item.get("noidungphatbosung"),
        #     "legal": item.get("luatphatbosung")
        # }
        # solution = {
        #     "id": item.get("mabienphapkhacphuc"),
        #     "content": item.get("noidungbienphapkhacphuc"),
        #     "legal": item.get("luatbienphapkhacphuc")
        # }
        # if code in data:
        #     found_pbs = False
        #     for item in data[code]["addition_punishments"]:
        #         if item["id"] == pbs["id"]:
        #             found_pbs = True
        #     if found_pbs == False:
        #         data[code]["addition_punishments"].append(pbs)
        #     found_solution = False
        #     for item in data[code]["solutions"]:
        #         if item["id"] == solution["id"]:
        #             found_solution = True
        #     if found_solution == False:
        #         data[code]["solutions"].append(solution)
        # else:
        #     data[code] = {
        #         "id": code,
        #         "content": content,
        #         "legal": legal,
        #         "fine": fine,
        #         "violator": violator,
        #         "addition_punishments": [],
        #         "keywords": keywords,
        #         "solutions": []
        #     }         
        #     if pbs["id"]:
        #         data[code]["addition_punishments"].append(pbs)
        #     if solution["id"]:
        #         data[code]["solutions"].append(solution)
        #     list_id.append(code)

    # for id_item in list_id:
    #     if id_item in data:
    #         violations.append(data[id_item])

    for id_item in list_id:
        if id_item in data:
            data[id_item]["violators"] = ", ".join(
                data[id_item]["violators"])
            violations.append(data[id_item])

    return violations


def search_violations(keyword, limit, page, sort_by, sort_type):
    g = Graph()
    g.parse("./app/ontology/luatgt copy 4.rdf", format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        # '   ?vipham\n'
        # '       :MaViPham ?mavipham ;\n'
        # '       :NoiDung ?noidungvipham ;\n'
        # '       :Luat ?luatvipham ;\n'
        # '       :DoiTuongXuPhat ?doituongxuphat ;\n'
        # '       :TuKhoa ?tukhoa ;'
        # '       :HinhPhat ?mucphat .\n'
        # f'  filter (regex(LCASE(?noidungvipham), "{keyword.lower()}")) .\n'
        # '   OPTIONAL {\n'
        # '       ?vipham\n'
        # '           :PhatBoSung ?phatbosung .\n'
        # '       ?phatbosung\n'
        # '           :MaPhatBoSung ?maphatbosung ;\n'
        # '           :NoiDung ?noidungphatbosung ;\n'
        # '           :Luat ?luatphatbosung .\n'
        # '   }\n'
        # '   OPTIONAL {\n'
        # '       ?vipham\n'
        # '           :KhacPhuc ?bienphapkhacphuc .\n'
        # '       ?bienphapkhacphuc\n'
        # '           :MaBienPhap ?mabienphapkhacphuc ;\n'
        # '           :NoiDung ?noidungbienphapkhacphuc ;\n'
        # '           :Luat ?luatbienphapkhacphuc .\n'
        # '   }\n'
        # '}\n'
        # f'order by {sort_type}(?{sort_by})'

        '   ?vipham\n'
        '       :Ten ?tenvipham ;\n'
        '       :ChiTiet ?chitietvipham ;\n'
        '       :CoDoiTuongXuPhat ?doituongxuphat ;\n'
        '       :BiPhatTien ?mucphat ;\n'
        '       :CoHanhViViPham ?hanhvivipham ;\n'
        '       :XayRaVoi ?doituongbitacdong .\n'
        '   ?doituongxuphat\n'
        '       :Ten ?tendoituongxuphat .\n'
        '   ?mucphat\n'
        '       :TienPhat ?mucphattien .\n'
        '   ?hanhvivipham\n'
        '       :Ten ?tenhanhvivipham .\n'
        '   ?doituongbitacdong :Ten ?tendoituongbitacdong .\n'
        f'  filter (regex(LCASE(?tenvipham), "{keyword.lower()}")) .\n'
        '}\n'

        # '   ?violation \n'
        # '       :So ?point_num ;\n'
        # '       :Ten ?point_name ;\n'
        # '       :ThuocKhoan ?clause ;\n'
        # '       :CoDoiTuongXuPhat ?violator ;\n'
        # '       :BiPhatTien ?fine .\n'
        # '   ?fine :TienPhat ?fine_value .\n'
        # '   ?violator :Ten ?violator_name .\n'
        # '   ?clause :So ?clause_num .\n'
        # '   ?clause :Ten ?clause_name .\n'
        # '   ?clause :ThuocDieu ?article .\n'
        # '   ?article :So ?article_num .\n'
        # '   ?article :Ten ?article_name .\n'
        # '   ?article :ThuocMuc ?section .\n'
        # '   ?section :So ?section_num .\n'
        # '   ?section :Ten ?section_name .\n'
        # '   ?section :ThuocChuong ?chapter .\n'
        # '   ?chapter :So ?chapter_num .\n'
        # '   ?chapter :Ten ?chapter_name .\n'
        # '   ?chapter :ThuocVanBan ?text .\n'
        # '   ?text :So ?text_num .\n'
        # '   ?text :Ten ?text_name .\n'
        # f'  filter (regex(LCASE(?point_name), "{keyword.lower()}")) .\n'
        # '}\n'
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
    g.parse("./app/ontology/luatgt copy 4.rdf", format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        # 'SELECT * WHERE {\n'
        # '   ?vipham\n'
        # '       :MaViPham ?mavipham ;\n'
        # '       :NoiDung ?noidungvipham ;\n'
        # '       :Luat ?luatvipham ;\n'
        # '       :DoiTuongXuPhat ?doituongxuphat ;\n'
        # '       :TuKhoa ?tukhoa ;'
    # '       :HinhPhat ?mucphat .\n'
        # f'  filter (?mavipham = "{id}") .\n'
        # '   OPTIONAL {\n'
        # '       ?vipham\n'
        # '           :PhatBoSung ?phatbosung .\n'
        # '       ?phatbosung\n'
        # '           :MaPhatBoSung ?maphatbosung ;\n'
        # '           :NoiDung ?noidungphatbosung ;\n'
        # '           :Luat ?luatphatbosung .\n'
        # '   }\n'
        # '   OPTIONAL {\n'
        # '       ?vipham\n'
        # '           :KhacPhuc ?bienphapkhacphuc .\n'
        # '       ?bienphapkhacphuc\n'
        # '           :MaBienPhap ?mabienphapkhacphuc ;\n'
        # '           :NoiDung ?noidungbienphapkhacphuc ;\n'
        # '           :Luat ?luatbienphapkhacphuc .\n'
        # '   }\n'
        # '}\n'
        'SELECT * WHERE {\n'
        '   ?vipham\n'
        '       :Ten ?tenvipham ;\n'
        '       :ChiTiet ?chitietvipham ;\n'
        '       :CoDoiTuongXuPhat ?doituongxuphat ;\n'
        '       :BiPhatTien ?mucphat ;\n'
        '       :CoHanhViViPham ?hanhvivipham ;\n'
        '       :XayRaVoi ?doituongbitacdong .\n'
        '   ?doituongxuphat\n'
        '       :Ten ?tendoituongxuphat .\n'
        '   ?mucphat\n'
        '       :TienPhat ?mucphattien .\n'
        '   ?hanhvivipham\n'
        '       :Ten ?tenhanhvivipham .\n'
        '   ?doituongbitacdong :Ten ?tendoituongbitacdong .\n'
        f'  filter (?vipham = :{id}) .\n'
        '}\n'
        # '   ?violation \n'
        # '       :So ?point_num ;\n'
        # '       :Ten ?point_name ;\n'
        # '       :ThuocKhoan ?clause ;\n'
        # '       :CoDoiTuongXuPhat ?violator ;\n'
        # '       :BiPhatTien ?fine .\n'
        # '   ?fine :TienPhat ?fine_value .\n'
        # '   ?violator :Ten ?violator_name .\n'
        # '   ?clause :So ?clause_num .\n'
        # '   ?clause :Ten ?clause_name .\n'
        # '   ?clause :ThuocDieu ?article .\n'
        # '   ?article :So ?article_num .\n'
        # '   ?article :Ten ?article_name .\n'
        # '   ?article :ThuocMuc ?section .\n'
        # '   ?section :So ?section_num .\n'
        # '   ?section :Ten ?section_name .\n'
        # '   ?section :ThuocChuong ?chapter .\n'
        # '   ?chapter :So ?chapter_num .\n'
        # '   ?chapter :Ten ?chapter_name .\n'
        # '   ?chapter :ThuocVanBan ?text .\n'
        # '   ?text :So ?text_num .\n'
        # '   ?text :Ten ?text_name .\n'
        # f'   filter(?violation = :{id})'
        # '}\n'
    )

    print(query)

    result = g.query(query)

    violations = handle_result(result)

    if len(violations) > 0:
        return violations[0]

    return None


def get_classes():

    behaviors = []
    vehicles = []

    g = Graph()
    g.parse("./app/ontology/luatgt copy 4.rdf", format="application/rdf+xml")

    query = (
        'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n'
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?x rdfs:subClassOf :HanhViViPham .\n'
        '   ?hv\n'
        '       rdf:type ?x ;\n'
        '       :Ten ?name .\n'
        '}\n'
    )

    print (query)
    result = g.query(query)

    for item in result:
        name = item.get("name")
        code = item.get("hv").split("#")[1]

        behaviors.append({
            "name": name,
            "id": code
        })
    
    query = (
        'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n'
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/luatgt#>\n'
        'SELECT * WHERE {\n'
        '   ?x rdfs:subClassOf :DoiTuongThamGiaGiaoThong .\n'
        '   ?hv\n'
        '       rdf:type ?x ;\n'
        '       :Ten ?name .\n'
        '}\n'
    )

    print (query)
    result = g.query(query)

    for item in result:
        name = item.get("name")
        code = item.get("hv").split("#")[1]

        vehicles.append({
            "name": name,
            "id": code
        })

    return {
        "behaviors": behaviors,
        "vehicles": vehicles
    }


def get_related_violations(id):

    violations = []

    g = Graph()
    g.parse("./app/ontology/luatgt copy 4.rdf", format="application/rdf+xml")

    violation = get_violation_by_id(id)

    about = violation["about"]
    code = violation["id"]
    legal = violation["legal"]
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
        '       :XayRaVoi ?doituongbitacdong .\n'
        '   ?doituongxuphat\n'
        '       :Ten ?tendoituongxuphat .\n'
        '   ?mucphat\n'
        '       :TienPhat ?mucphattien .\n'
        '   ?hanhvivipham\n'
        '       :Ten ?tenhanhvivipham .\n'
        '   ?doituongbitacdong :Ten ?tendoituongbitacdong .\n'
        f'  filter (?tenhanhvivipham = "{about}" && ?chitietvipham != "{legal}" && ?vipham != :{code}) .\n'
        '}\n'
    )

    print(query)

    result = g.query(query)

    violations = handle_result(result)

    return violations


def update_violation(id, body):
    g = Graph()
    g.parse('./app/ontology/trafficlaws.rdf', format="application/rdf+xml")

    name_space = "http://www.semanticweb.org/duyphan/ontologies/2023/5/trafficlaws#"

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/trafficlaws#>\n'
        'SELECT * WHERE {\n'
        '   ?vipham :MaViPham ?mavipham .\n'
        f'  filter (?mavipham = "{id}") .\n'
        '}\n'
    )

    result = g.query(query)

    for item in result:
        violation_code = item.get("vipham").split("#")[1]
        ns = Namespace(name_space)
        if body["content"]:
            g.set((ns[violation_code], URIRef(f'{name_space}NoiDung'), Literal(body["content"])))
        if body["violator"]:
            g.set((ns[violation_code], URIRef(f'{name_space}DoiTuongXuPhat'), Literal(body["violator"])))
        if body["legal"]:
            g.set((ns[violation_code], URIRef(f'{name_space}Luat'), Literal(body["legal"])))
        if body["fine"]:
            g.set((ns[violation_code], URIRef(f'{name_space}HinhPhat'), Literal(body["fine"])))
        if body["note"]:
            g.set((ns[violation_code], URIRef(f'{name_space}GhiChu'), Literal(body["note"])))
        if body["keywords"]:
            g.set((ns[violation_code], URIRef(f'{name_space}TuKhoa'), Literal(body["keywords"])))

        g.serialize('./app/ontology/trafficlaws.rdf', format="application/rdf+xml")
        break

    return {
        "is_success": True
    }