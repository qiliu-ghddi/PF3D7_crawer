def parse_publication(section):
    # 初始化JSON数据结构
    json_data = {}

    name = section.find("h2").get_text()
    print(f"{name}")
    json_data[name] = {}

    table = section.find("table")
    rows = table.find_all("tr")
    if rows and len(rows)>=1:
        json_data[name]["Num of Associated Publications"] = len(rows)-1
    else:
        json_data[name]["Num of Associated Publications"] = 0
    return json_data
