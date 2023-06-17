import math
import json
from rdflib import Graph
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

        # code = item.get("vipham").split("#")[1]
        # name = item.get("tenvipham")
        # legal = item.get("chitietvipham")
        # fine = item.get("mucphattien")
        # violator = item.get("tendoituongxuphat")
        # violations.append({
        #     "id": code,
        #     "name": name,
        #     "legal": legal,
        #     "fine": fine,
        #     "violator": violator
        # })

        code = item.get("mavipham")
        content = item.get("noidungvipham")
        legal = item.get("luatvipham")
        fine = item.get("mucphat")
        violator = item.get("doituongxuphat")
        pbs = {
            "id": item.get("maphatbosung"),
            "content": item.get("noidungphatbosung"),
            "legal": item.get("luatphatbosung")
        }
        solution = {
            "id": item.get("mabienphapkhacphuc"),
            "content": item.get("noidungbienphapkhacphuc"),
            "legal": item.get("luatbienphapkhacphuc")
        }
        if code in data:
            found_pbs = False
            for item in data[code]["addition_punishments"]:
                if item["id"] == pbs["id"]:
                    found_pbs = True
            if found_pbs == False:
                data[code]["addition_punishments"].append(pbs)
            found_solution = False
            for item in data[code]["solutions"]:
                if item["id"] == solution["id"]:
                    found_solution = True
            if found_solution == False:
                data[code]["solutions"].append(solution)
        else:
            data[code] = {
                "id": code,
                "content": content,
                "legal": legal,
                "fine": fine,
                "violator": violator,
                "addition_punishments": [],
                "solutions": []
            }         
            if pbs["id"]:
                data[code]["addition_punishments"].append(pbs)
            if solution["id"]:
                data[code]["solutions"].append(solution)
            list_id.append(code)

    for id_item in list_id:
        if id_item in data:
            violations.append(data[id_item])

    # for id_item in list_id:
    #     if id_item in data:
    #         data[id_item]["violators"] = ", ".join(
    #             data[id_item]["violators"])
    #         violations.append(data[id_item])

    return violations


def search_violations(keyword, limit, page):
    g = Graph()
    g.parse("./app/ontology/trafficlaws.rdf", format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/trafficlaws#>\n'
        'SELECT * WHERE {\n'
        '   ?vipham\n'
        '       :MaViPham ?mavipham ;\n'
        '       :NoiDung ?noidungvipham ;\n'
        '       :Luat ?luatvipham ;\n'
        '       :DoiTuongXuPhat ?doituongxuphat ;\n'
        '       :HinhPhat ?mucphat .\n'
        f'  filter (regex(LCASE(?noidungvipham), "{keyword.lower()}")) .\n'
        '   OPTIONAL {\n'
        '       ?vipham\n'
        '           :PhatBoSung ?phatbosung .\n'
        '       ?phatbosung\n'
        '           :MaPhatBoSung ?maphatbosung ;\n'
        '           :NoiDung ?noidungphatbosung ;\n'
        '           :Luat ?luatphatbosung .\n'
        '   }\n'
        '   OPTIONAL {\n'
        '       ?vipham\n'
        '           :KhacPhuc ?bienphapkhacphuc .\n'
        '       ?bienphapkhacphuc\n'
        '           :MaBienPhap ?mabienphapkhacphuc ;\n'
        '           :NoiDung ?noidungbienphapkhacphuc ;\n'
        '           :Luat ?luatbienphapkhacphuc .\n'
        '   }\n'
        '}\n'

        # '   ?vipham\n'
        # '       :Ten ?tenvipham ;\n'
        # '       :ChiTiet ?chitietvipham ;\n'
        # '       :CoDoiTuongXuPhat ?doituongxuphat ;\n'
        # '       :BiPhatTien ?mucphat ;\n'
        # '       :CoHanhViViPham ?hanhvivipham ;\n'
        # '       :ViPhamVe ?viphamve .\n'
        # '   ?doituongxuphat\n'
        # '       :Ten ?tendoituongxuphat .\n'
        # '   ?mucphat\n'
        # '       :TienPhat ?mucphattien .\n'
        # '   ?hanhvivipham\n'
        # '       :Ten ?tenhanhvivipham .\n'
        # '   ?viphamve\n'
        # '       :Ten ?tenviphamve .\n'
        # f'  filter (regex(LCASE(?tenvipham), "{keyword.lower()}")) .\n'

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
    g.parse("./app/ontology/trafficlaws.rdf", format="application/rdf+xml")

    query = (
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        'PREFIX : <http://www.semanticweb.org/duyphan/ontologies/2023/5/trafficlaws#>\n'
        'SELECT * WHERE {\n'
        '   ?vipham\n'
        '       :MaViPham ?mavipham ;\n'
        '       :NoiDung ?noidungvipham ;\n'
        '       :Luat ?luatvipham ;\n'
        '       :DoiTuongXuPhat ?doituongxuphat ;\n'
        '       :HinhPhat ?mucphat .\n'
        f'  filter (?mavipham = "{id}") .\n'
        '   OPTIONAL {\n'
        '       ?vipham\n'
        '           :PhatBoSung ?phatbosung .\n'
        '       ?phatbosung\n'
        '           :MaPhatBoSung ?maphatbosung ;\n'
        '           :NoiDung ?noidungphatbosung ;\n'
        '           :Luat ?luatphatbosung .\n'
        '   }\n'
        '   OPTIONAL {\n'
        '       ?vipham\n'
        '           :KhacPhuc ?bienphapkhacphuc .\n'
        '       ?bienphapkhacphuc\n'
        '           :MaBienPhap ?mabienphapkhacphuc ;\n'
        '           :NoiDung ?noidungbienphapkhacphuc ;\n'
        '           :Luat ?luatbienphapkhacphuc .\n'
        '   }\n'
        '}\n'
        # 'SELECT * WHERE {\n'
        # '   ?vipham\n'
        # '       :Ten ?tenvipham ;\n'
        # '       :ChiTiet ?chitietvipham ;\n'
        # '       :CoDoiTuongXuPhat ?doituongxuphat ;\n'
        # '       :BiPhatTien ?mucphat ;\n'
        # '       :CoHanhViViPham ?hanhvivipham ;\n'
        # '       :ViPhamVe ?viphamve .\n'
        # '   ?doituongxuphat\n'
        # '       :Ten ?tendoituongxuphat .\n'
        # '   ?mucphat\n'
        # '       :TienPhat ?mucphattien .\n'
        # '   ?hanhvivipham\n'
        # '       :Ten ?tenhanhvivipham .\n'
        # '   ?viphamve\n'
        # '       :Ten ?tenviphamve .\n'
        # f'  filter (?vipham = :{id}) .\n'
        # '}\n'
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
