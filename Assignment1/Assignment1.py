import multiprocessing as mp
import Bio
from Bio import Entrez
from Bio import Medline
import json
import numpy as np

Entrez.api_key = 'b73a5ffde89ba2ae4feca63960fdac659009'
Entrez.email = 'rie123@live.nl'

def final_script(pmid):
    # input is an pubmed id
    # output is 10 xml articles based on refrences i hope.
    references = []
    k = 0

    links = Entrez.elink(dbfrom="pubmed", id=pmid, linkname="pubmed_pubmed")
    record = Entrez.read(links)
    records = record[0]['LinkSetDb'][0]['Link']

    for link in records:
        references.append(link['Id'])
    k = np.random.randint(0,len(references) - 1)
    k1 = k + 1

    for item in references[k:k1]:
        handle = Entrez.efetch(db="pubmed", id=item, retmode="xml")
        record = Entrez.read(handle)
        handle.close()
        with open('output/'+ item + '.xml','w') as to_write:
            to_write.write(json.dumps(record['PubmedArticle'][0]))
        to_write.close()
        print('Finnished with 1 ref')


nr = "1234567891"
def multi_process():
    cpus = mp.cpu_count()
    with mp.Pool(cpus) as pool:
        results = pool.map(final_script, nr)

        
if __name__ == "__main__":       
    multi_process()