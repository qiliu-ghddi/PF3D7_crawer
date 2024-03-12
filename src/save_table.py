# Author: Qi Liu
# E-mail: qi.liu@ghddi.org
# Copyright: GHDDI
import json
import pandas as pd
from collections import OrderedDict
from pathlib import Path

def key_starts_with(dict_data, starts_str):
    for key in dict_data:
        if key.startswith(starts_str):
            return key
    return False


def select_needed(json_data):
    one_record = []

    categories = [
        "Publications",
        "Essentiality", 
        "Binding Evidence",
        "Orthology Information", 
        "Protein Information",
        "Resistome Mutations"
        ]
    Publications_keys = {
        "Literature": ["Num of Associated Publications"]
    }
    Essentiality_keys = {
        "Zhang Phenotype": [
            "Mutagenesis Index Score (MIS)",
            "Mutagenesis Fitness Score (MFS)",
            "Number of insertions in CDS",
        ],
        "PlasmoGEM": [
            "Relative Growth Rate",
            # "Confidence",
        ],
        "RMgmDB": [
            "Gene Modification",
            # "RMgmDB ID Link",
        ]
    }
    Variation_keys = {
        "PlasmoDB": # resource
        {  
            "PlasmoDB Total SNPs", 
            "PlasmoDB SNP count"
        } # resource_v
    }
    Binding_keys = {
        "AlphaFill": [
            "AlphaFill Uniprot ID",
            "\"Best\" AlphaFill ligand hit"
        ],
        "BRENDA": [
            "BRENDA ID"
        ],
        "BindingDB": [
            "Num of Orthology to BindingDB Entries"
        ]
    }
    Orthology_keys = {
        "OrthoMCL": [
            "Most Similar Human Ortholog",
            "TM-align score",
            "TM-align length",
            "TM-align RMSD",
            "TM-align sequence identity",
        ],
        
    }
    Protein_keys = {
        "General": [
            "Protein length",
            "Molecular Weight (kDa)",
            "Isoelectric Point"
        ],
        "UniProt": [
            "UniProt IDs"
        ],
        "PDB": [
            "PDB ID(s)",
            "Num of PDB ID"
        ],
        "Domains": [
            "Num of Protein Domain Annotations"
        ]
    }

    Resistome_keys = {
        "Resistome Database": [
            "Num of Resistome Missense Mutations",
            "Num of Resistome Compounds with Missense Mutations",
            "Num of Samples with Disruptive Mutations",
        ]
    }
    
    index_keys = {  # Json key: custom key
        "Associated Publications": Publications_keys,
        "Essentiality": Essentiality_keys,
        "Genetic Variation": Variation_keys,
        "Binding Evidence": Binding_keys,
        "Orthology Information": Orthology_keys,
        "Protein Information": Protein_keys,
        "Resistome Mutations": Resistome_keys
    }

    one_record = OrderedDict({})
    for category, category_v in index_keys.items():
        for resource, resource_v in category_v.items():
            # print(f"resource: {resource}; resource_v: {resource_v} ")
            # print(f"category: {category}")
            resource_key = key_starts_with(json_data[category], resource)
            # print(f"resource_key: {resource_key}")
            if resource_key:
                for k in resource_v:
                    # print(f"k: {k}")
                    if k in {"PlasmoDB Total SNPs", "PlasmoDB SNP count"}:
                        one_record[k] = json_data[category][k]   
                    elif k in {"AlphaFill Uniprot ID", "\"Best\" AlphaFill ligand hit"}:
                        one_record[k] = json_data[category][k]
                    elif k in {"BRENDA ID"}:
                        content = json_data[category][k]
                        if len(content) > 0:
                            one_record[k] = [e['ID'] for e in content]
                        else:
                            one_record[k] = None
                    elif k in {"PDB ID(s)", "Num of PDB ID"}:
                        one_record[k] = json_data[category][k]
                    elif k in {"UniProt IDs"}:
                        uniprot_ids = json_data[category][k]
                        one_record[k] = [e["UniProt ID"] for e in uniprot_ids]
                    else:
                        # print(f"k: {k} category: {category} resource_key: {resource_key}")
                        one_record[k] = json_data[category][resource_key][k]
            else:
                # user custom
                for k in resource_v:
                    try:
                        if k in {"Num of Associated Publications"}:
                            one_record[k] = json_data[category][k]
                        elif k in {"PlasmoDB Total SNPs", "PlasmoDB SNP count"}:
                            one_record[k] = json_data[category][k]
                        elif k in {"Num of Orthology to BindingDB Entries"}:
                            one_record[k] = json_data[category][k]
                        elif k in {"Most Similar Human Ortholog"}:
                            one_record[k] = json_data[category][k]
                        elif k in ['TM-align score', 'TM-align length', 'TM-align RMSD', 'TM-align sequence identity']:
                            one_record[k] = json_data[category]['TM-align'][k]
                        elif k in ['Protein length', 'Molecular Weight (kDa)', 'Isoelectric Point']:
                            one_record[k] = json_data[category][k]
                        elif k in ["PDB ID(s)", "Num of PDB ID"]:
                            one_record[k] = json_data[category][k]
                        elif k in ['Num of Protein Domain Annotations']:
                            one_record[k] = json_data[category][k]
                        elif k in ["Num of Resistome Missense Mutations", "Num of Resistome Compounds with Missense Mutations", "Num of Samples with Disruptive Mutations"]:
                            one_record[k] = json_data[category][k]
                        else:
                            raise ValueError(f"Invalid key: {k}")
                    except Exception as e:
                        one_record[k] = None

    # print(f"one_record: {one_record}")
    return one_record


def save_to_table():
    # Select and output to a .csv file
    gene_df = pd.read_csv("../data/gene_links.csv")
    print(gene_df.head())

    url_list = gene_df['Gene Info Link'].tolist()
    print(len(url_list))

    json_dir = "../save/json"
    csv_dir = "../save/csv"
    Path(csv_dir).mkdir(exist_ok=True, parents=True)
    selected_data = []
    for i, url in enumerate(url_list):
        print(f"{i} ... {url}")
        fname = url.split("/")[-1]

        # for each json
        # select needed data
        full_fname = f"{json_dir}/{fname}.json"
        with open(full_fname, "r") as fin:
            record = json.load(fin)

        selected_recored = select_needed(record)
        df_ = pd.DataFrame([selected_recored])
        print(df_)
        df_.T.to_csv(f"{csv_dir}/{fname}.csv", index=True)

        selected_data.append((fname, selected_recored))
        # break

    # merge them to a table
    selected_df = pd.DataFrame.from_dict(
        {name: values for name, values in selected_data}, orient='index')
    # output to a .csv file

    Path(csv_dir).mkdir(parents=True, exist_ok=True)
    selected_df.T.to_csv(f"{csv_dir}/gene_links_demo.csv")
    selected_df.T.to_excel(f"{csv_dir}/gene_links_demo.xlsx")

save_to_table()