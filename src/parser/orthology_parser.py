import json

def parse_orthology(section):
    # 初始化JSON数据结构
    json_data = {}

    # 提取相关信息填充JSON数据结构
    name = section.find("h2").get_text()
    print(f"{name}")
    json_data[name] = {}

    # 获取Ortholog Group (OrthoMCL)
    ortholog_group = section.find(
        'b', text='Ortholog Group (OrthoMCL): ').find_next_sibling('a').get_text().strip()
    json_data[name]['Ortholog Group (OrthoMCL)'] = ortholog_group

    if section.find('i', text='No human ortholog(s)'):
        json_data[name]['Most Similar Human Ortholog'] = None
        json_data[name]['TM-align'] = None
        json_data[name]['All Human Orthologs (OrthoMCL)'] = None
    else:
        # 获取Most Similar Human Ortholog
        most_similar_human_ortholog = section.find('b', text='Most Similar Human Ortholog: ')
        if most_similar_human_ortholog:
            json_data[name]['Most Similar Human Ortholog'] = most_similar_human_ortholog.find_next_sibling('a').get_text().strip()

        # 获取TM-align 信息
        tm_align_info = {}
        ul = section.find('ul')
        for li in ul.find_all('li'):
            key_value = li.get_text().split(': ')
            key = key_value[0].strip()
            value = key_value[1].strip()
            try:
                value = float(value)  # 转换为浮点数 如果合适的话
            except ValueError:
                pass  # 如果无法转换为数值，保留字符串
            tm_align_info[key] = value
        json_data[name]['TM-align'] = tm_align_info

        # 获取所有人类同源基因
        all_human_orthologs = []
        table = section.find('table')
        for tr in table.find_all('tr'):
            td_elements = tr.find_all('td')
            human_ortholog = {
                'ID': td_elements[0].get_text(),
                'Description': td_elements[1].get_text()
            }
            all_human_orthologs.append(human_ortholog)
            
        json_data[name]['All Human Orthologs (OrthoMCL)'] = all_human_orthologs

    # data_json = json.dumps(json_data, indent=4)
    # with open(f'{name.replace(" ", "_")}.json', 'w') as fout:
    #     fout.write(data_json)
        
    return json_data

