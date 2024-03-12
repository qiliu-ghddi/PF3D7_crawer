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


def parse_protein(section):
    # 初始化JSON数据结构
    json_data = {}

    # 提取相关信息填充JSON数据结构
    name = section.find("h2").get_text()
    print(f"{name}")
    json_data[name] = {}

    # Extract protein length
    protein_length_em = section.find('b', string='Protein length: ').find_next('em')
    json_data[name]['Protein length'] = int(protein_length_em.text)

    # Extract molecular weight
    molecular_weight_em = section.find('b', string='Molecular Weight (kDa): ').find_next('em')
    json_data[name]['Molecular Weight (kDa)'] = float(molecular_weight_em.text)

    # Extract isoelectric point
    isoelectric_point_em = section.find('b', string='Isoelectric Point: ').find_next('em')
    json_data[name]['Isoelectric Point'] = float(isoelectric_point_em.text)

    # Extract UniProt IDs
    uniProt_IDs = []
    uniProt_elements = section.find('b', string='UniProt ID(s): ').find_next_siblings('a')
    for element in uniProt_elements:
        uniProt_id_dict = {
            'UniProt ID': element.text,
            'UniProt Link': element['href']
        }
        uniProt_IDs.append(uniProt_id_dict)
    json_data[name]['UniProt IDs'] = uniProt_IDs

    # Extract Protein Domain Annotations
    domain_annotations = []
    annotations_table = section.find('table')
    for row in annotations_table.find_all('tr'):
        cells = row.find_all('td')
        domain_annotation = {
            'Database': cells[0].text,
            'ID': cells[1].text,
            'Description': cells[2].text
        }
        domain_annotations.append(domain_annotation)
    json_data[name]['Num of Protein Domain Annotations'] = len(domain_annotations)
    json_data[name]['Protein Domain Annotations'] = domain_annotations

    # Extract PDB IDs
    pdb_b = section.find("b", text="PDB ID(s): ")
    pdb_p = pdb_b.find_parent()
    pdb_key, pdb_id_str = pdb_p.get_text().strip().split(": ")
    if pdb_id_str == "None":
        json_data[name][pdb_key] = None
        json_data[name]["Num of PDB ID"] = 0
    else:
        pdb_ids = pdb_id_str.split(", ")
        json_data[name][pdb_key] = pdb_ids
        json_data[name]["Num of PDB ID"] = len(pdb_ids)

    # data_json = json.dumps(json_data, indent=4)
    # with open(f'{name.replace(" ", "_")}.json', 'w') as fout:
    #     fout.write(data_json)
        
    return json_data

