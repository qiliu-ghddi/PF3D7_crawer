# Author: Qi Liu
# E-mail: qi.liu@ghddi.org
# Copyright: GHDDI
from lxml import etree
import json
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import requests
from collections import OrderedDict
from parser.orthology_parser import parse_orthology
from parser.essentiality_parser import parse_essentiality
from parser.protein_parser import parse_protein
from parser.binding_parser import parse_binding
from parser.publication_parser import parse_publication
from parser.variation_parser import parse_variation
from parser.resistome_parser import parse_resistome


def parse(soup):
    # select sections
    pub_sec = soup.find('div', id='pub-div')
    ess_sec = soup.find('div', id='ess-div')
    variation_sec = soup.find('div', id='variation-div')
    
    binding_sec = soup.find('div', id='binding-div')
    ortho_sec = soup.find('div', id='ortho-div')
    protein_sec = soup.find('div', id='protein-div')
    resistome_sec = soup.find('div', id='resistome-div')
    
    data = {}
    # parse sections
    pub_data = parse_publication(pub_sec)
    ess_data = parse_essentiality(ess_sec)
    variation_data = parse_variation(variation_sec)
    binding_data = parse_binding(binding_sec)
    ortho_data = parse_orthology(ortho_sec)
    protein_data = parse_protein(protein_sec)
    resistome_data = parse_resistome(resistome_sec)

    for ele in [
        pub_data,
        ess_data,
        variation_data,
        binding_data, 
        ortho_data, 
        protein_data,
        resistome_data
        ]:
        k = list(ele)[0]
        data[k] = ele[k]
    return data


# Parse
def parse_htmls():
    # parse htmls
    html_dir = "../save/html"
    html_list = Path(html_dir).glob("PF3D7_*.html")
    html_list = [str(e) for e in html_list]
    # html_list = ["/home/qiliu02/project_marker_selection_2023/PF3D7_crawer/crawer3/save/html/PF3D7_0209300.html"]  # a case of PlasmoGEM Phenotype: N/A, RMgmDB ABS Phenotype: N/A
    # http://ec2-52-53-188-174.us-west-1.compute.amazonaws.com/PF3D7_0603300
    # html_list = ["/home/qiliu02/project_marker_selection_2023/PF3D7_crawer/crawer3/save/html/PF3D7_0603300.html"]
    # html_list = ["/home/qiliu02/project_marker_selection_2023/PF3D7_crawer/crawer3/save/html/PF3D7_0219600.html"]
    # html_list = ["/home/qiliu02/project_marker_selection_2023/PF3D7_crawer/crawer3/save/html/PF3D7_1450600.html"]  # a case of No human ortholog(s)

    print(html_list)
    for i, html_fn in enumerate(html_list):
        # read html file
        # parse
        html_path = Path(html_fn)
        print(f"{i} ... {html_path.stem}")

        # for each html:
        with open(html_fn, "r") as fin:
            html_doc = fin.read()

        # try:
        soup = BeautifulSoup(html_doc, 'html.parser')
        parsed_data = parse(soup)

        json_dir = "../save/json"
        Path(json_dir).mkdir(parents=True, exist_ok=True)
        data_json = json.dumps(parsed_data, indent=4)
        with open(f'{json_dir}/{html_path.stem}.json', 'w') as fout:
            fout.write(data_json)
        # except Exception as e:
        #     print(f"{e}")
        #     break


parse_htmls()
