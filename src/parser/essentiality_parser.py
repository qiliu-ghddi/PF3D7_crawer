import json

def extract_info_from_ul(ul_element):
    info = {}
    for li in ul_element.find_all('li'):
        text_parts = li.get_text().split(': ')
        key = text_parts[0].strip()
        value = text_parts[1].strip()
        try:
            value = float(value)  # 尝试将字符串值转换为浮点数
        except ValueError:
            pass  # 保持原始字符串值
        info[key] = value
    return info


def parse_essentiality(section):
    # 初始化JSON数据结构
    json_data = {}

    # 提取相关信息填充JSON数据结构
    name = section.find("h2").get_text()
    print(f"{name}")
    json_data[name] = {}
    
    # TODO:
    Zhang_phenotype = section.find("a", text="Zhang")
    p = Zhang_phenotype.find_parent('p')
    if p.find('b') and p.find('em'):
        key = p.get_text().strip().replace('\n', '')
        print(key)
        # key = p.get_text().strip().split(': ')[0]
        sub_info = p.find('em').get_text().strip()
        ul_element = p.find_next_sibling('ul')
        if ul_element:
            json_data[name][key] = extract_info_from_ul(
                ul_element)
            # json_data[name][key]['Phenotype'] = sub_info
    
    PlasmoGEM_phenotype = section.find("a", text="PlasmoGEM")
    RMgmDB_phenotype = section.find("a", text="Zhang")
    
    for p in section.find_all('p'):
        if p.find('b') and p.find('em'):
            key = p.get_text().strip().replace('\n', '')
            print(key)
            # key = p.get_text().strip().split(': ')[0]
            sub_info = p.find('em').get_text().strip()
            ul_element = p.find_next_sibling('ul')
            if ul_element:
                json_data[name][key] = extract_info_from_ul(
                    ul_element)
                # json_data[name][key]['Phenotype'] = sub_info

    # data_json = json.dumps(json_data, indent=4)
    # with open(f'{name}.json', 'w') as fout:
    #     fout.write(data_json)
    return json_data

