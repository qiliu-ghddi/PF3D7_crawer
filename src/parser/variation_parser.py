def parse_variation(section):
    json_data = {}

    name = section.find("h2").get_text()
    print(f"{name}")
    json_data[name] = {}
    
    PlasmoDB = section.find('b', text="PlasmoDB Total SNPs: ")
    PlasmoDB_p = PlasmoDB.find_parent('p')
    try:
        value = float(PlasmoDB.find_next_sibling('em').get_text())  # 尝试将字符串值转换为浮点数
    except ValueError:
        value = PlasmoDB.find_next_sibling('em').get_text()
    json_data[name]['PlasmoDB Total SNPs'] = value
    
    snp_p = PlasmoDB_p.find_next_sibling('p')
    json_data[name]['PlasmoDB SNP count'] = snp_p.get_text()
    
    return json_data
