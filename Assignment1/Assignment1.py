import multiprocessing as mp
import Bio
from Bio import Entrez
from Bio import Medline
import json

Entrez.api_key = 'b73a5ffde89ba2ae4feca63960fdac659009'
Entrez.email = 'rie123@live.nl'
pmid = "24524923"

def fetching(pmid):
    handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
    record = Entrez.read(handle)
    handle.close()
    return record


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

    for item in references[1:]:
        k = k + 1
        if k <= 10:
            record = fetching(item)
            with open('output/'+ item + '.xml','w') as to_write:
                to_write.write(json.dumps(record['PubmedArticle'][0]))
            to_write.close()
            print(k)
        else:
            print('Finnished')
            break


def multi_process(pmid):
    if __name__ == "__main__":
        cpus = mp.cpu_count()
        with mp.Pool(cpus) as pool:
            results = pool.map(final_script, pmid)