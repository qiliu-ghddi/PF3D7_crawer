# Author: Qi Liu
# E-mail: qi.liu@ghddi.org
# Copyright: GHDDI
from pathlib import Path
import pandas as pd
import requests

# Download htmls
def download_htmls():
    gene_df = pd.read_csv("../data/gene_links.csv")
    print(gene_df.head())

    url_list = gene_df['Gene Info Link'].tolist()
    print(len(url_list))
    # print(url_list)

    # save html to local
    html_dir = "../save/html"
    Path(html_dir).mkdir(parents=True, exist_ok=True)
    for i, url in enumerate(url_list):
        # request url and get html
        response = requests.get(url)
        fname = url.split("/")[-1]
        # Check if the request was successful
        if response.status_code == 200:
            # Save the content of the request to a local file
            html_fname = f'{html_dir}/{fname}.html'
            print(f"{i} ... saving to {html_fname}")
            with open(html_fname, 'w', encoding='utf-8') as html_fout:
                html_fout.write(response.text)
        else:
            print(
                f"Failed to retrieve the webpage {url}: status code {response.status_code}")


download_htmls()
