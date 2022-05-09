import multiprocessing as mp
import Bio
from Bio import Entrez
from Bio import Medline

Entrez.api_key = 'b73a5ffde89ba2ae4feca63960fdac659009'
Entrez.email = 'rie123@live.nl'


#handle = Entrez.efetch(db="pubmed", id=" 33525617", retmax=10)
handle = Entrez.elink(dbfrom= 'pubmed', id="33537979", linkname="pubmed_pubmed")

print(handle.readline().strip())
# LOCUS       AY851612                 892 bp    DNA     linear   PLN 10-APR-2007
handle.close()


# def func(uid="19304878"):
#     pmid = uid
#     handle = Entrez.elink(dbfrom="pubmed", id=pmid, linkname="pubmed_pubmed")
#     record = Entrez.read(handle)
#     handle.close()
#     print(record[0]["LinkSetDb"][0]["LinkName"])
#     pubmed_pubmed
#     linked = [link["Id"] for link in record[0]["LinkSetDb"][0]["Link"]]
#     "17121776" in linked