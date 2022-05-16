import multiprocessing as mp
import Bio
from Bio import Entrez
from Bio import Medline
import json
import numpy as np
import argparse as ap
#

Entrez.api_key = 'b73a5ffde89ba2ae4feca63960fdac659009'
Entrez.email = 'rie123@live.nl'
#pmid = "30049270"

# Function that obtains the references from pubmed based on a pubmed id
def final_script(pmid):
    references = []
    k = 0
    record = Entrez.elink(dbfrom="pubmed",
                            db="pmc",
                            LinkName="pubmed_pmc_refs",
                            id=pmid,
                            api_key='b73a5ffde89ba2ae4feca63960fdac659009')

    record = Entrez.read(record)
    records = record[0]['LinkSetDb'][0]['Link']
    for link in records:
        references.append("\'" + link['Id'] + "\'")

    return references

# Function that obtains and writes the xml file for a given pubmed id
def fetcher(pmid_ref):
    
    title = pmid_ref.replace("\'","")

    handle = Entrez.efetch(db="pmc", id=pmid_ref, rettype="XML", retmode="text",
                        api_key='b73a5ffde89ba2ae4feca63960fdac659009')

    with open(f'output/{title}.xml', 'wb') as file:
        file.write(handle.read())
        file.close()
        handle.close()
        print('Finnished')

# Function that runs the fetcher process on multiple processors.
def runner(pmid):
    refs = final_script(pmid)

    try:
        refs = refs[:10]
    except: 
        refs = refs[:len(refs)]

    cpus = mp.cpu_count()

    with mp.Pool(cpus) as pool:
        results = pool.map(fetcher, refs)

if __name__ == "__main__":
    argparser = ap.ArgumentParser(description="Script that downloads (default) 10 articles referenced by the given PubMed ID concurrently.")
    argparser.add_argument("-n", action="store",
                           dest="n", required=False, type=int,
                           help="Number of references to download concurrently.")
    argparser.add_argument("pubmed_id", action="store", type=str, nargs=1, help="Pubmed ID of the article to harvest for references to download.")
    args = argparser.parse_args()
    print("Getting: ", args.pubmed_id, args.n)

    runner(args.pubmed_id)