def parse_resistome(section):
    json_data = {}

    name = section.find("h2").get_text()
    print(f"{name}")
    json_data[name] = {}

    # Resistome Missense Mutations
    resistome_muts = section.find("b", text="Resistome Missense Mutations: ")
    resistome_muts_p = resistome_muts.find_parent()
    mut_str = resistome_muts_p.get_text()
    mut_key, mut_id_str = mut_str.split(": ")
    if mut_id_str == "None":
        json_data[name][mut_key] = None
        json_data[name]["Num of Resistome Missense Mutations"] = 0
    else:
        mut_ids = mut_id_str.split(", ")
        json_data[name][mut_key] = mut_ids
        json_data[name]["Num of Resistome Missense Mutations"] = len(mut_ids)
        
    # Resistome Compounds with Missense Mutations
    resistome_cmps_p = section.find(
        "b", text="Resistome Compounds with Missense Mutations: ").find_parent()
    cmps_str = resistome_cmps_p.get_text()
    cmps_key, cmp_id_str = cmps_str.split(": ")
    if cmp_id_str == "None":
        json_data[name][cmps_key] = None
        json_data[name]["Num of Resistome Compounds with Missense Mutations"] = 0
    else:
        cmp_ids = cmp_id_str.split(", ")
        json_data[name][cmps_key] = cmp_ids
        json_data[name]["Num of Resistome Compounds with Missense Mutations"] = len(cmp_ids)

    # Resistome Compounds with Missense Mutations
    disruptive_p = section.find(
        "b", text="Resistome # Samples with Disruptive Mutations: ").find_parent()
    disruptive_str = disruptive_p.get_text()
    num_samples = disruptive_str.split(": ")[1].strip().replace("\n", "")
    json_data[name]["Num of Samples with Disruptive Mutations"] = num_samples
    
    return json_data
    
    
    
    
