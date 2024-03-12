import json
import re

def parse_binding(section):
    # 初始化JSON数据结构
    json_data = {}

    # 提取相关信息填充JSON数据结构
    name = section.find("h2").get_text()
    print(f"{name}")
    json_data[name] = {}

    # AlphaFill Uniprot ID
    Uniprot_ID = section.find(
        'b', text='AlphaFill Uniprot ID: ').find_next_sibling('a').get_text().strip()
    json_data[name]['AlphaFill Uniprot ID'] = Uniprot_ID
    
    # 获取Ortholog Group (OrthoMCL)
    ligand_hit = section.find(
        'b', text='"Best" AlphaFill ligand hit: ').parent.get_text().strip().replace("\n", "").replace("        ", " ")
    ligand_hit_k, ligand_v = ligand_hit.split(": ")
    json_data[name][ligand_hit_k] = ligand_v

    # 获取 BRENDA 和 BindingDB
    tables = section.find_all('table')
    num_tables = len(tables)
    # print(f"num_tables: {num_tables}")
    if section.find("i", text="No associated EC numbers"):
        json_data[name]['BRENDA ID'] = []
    else:
        BRENDA_info = []
        for tr in tables[0].find_all('tr'):
            td_elements = tr.find_all('td')
            BRENDA_r = {
                'ID': td_elements[0].get_text().strip("\n"),
                'Description': td_elements[1].get_text().strip("\n")
            }
            BRENDA_info.append(BRENDA_r)        
        
        json_data[name]['BRENDA ID'] = BRENDA_info
    
    if section.find("i", text="No evidence of orthology to BindingDB entries"):
        json_data[name]['Num of Orthology to BindingDB Entries'] = 0
    else:
        json_data[name]['Num of Orthology to BindingDB Entries'] = len(tables[-1].find_all('tr'))

    # data_json = json.dumps(json_data, indent=4)
    # with open(f'{name.replace(" ", "_")}.json', 'w') as fout:
    #     fout.write(data_json)
    
    return json_data

