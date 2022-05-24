from functions import run_workers
from functions import runner
from functions import runserver
from functions import runclient

import multiprocessing as mp
from multiprocessing.managers import BaseManager, SyncManager
import os, sys, time, queue
import xml.etree.ElementTree as ET
import pickle
from Bio import Entrez
import argparse as ap


POISONPILL = "MEMENTOMORI"
ERROR = "DOH"
AUTHKEY = b'whathasitgotinitspocketsesss?'
Entrez.api_key = 'b73a5ffde89ba2ae4feca63960fdac659009'
Entrez.email = 'rie123@live.nl'


if __name__ == "__main__":
    argparser = ap.ArgumentParser(description="Script that downloads (default) 10 articles referenced by the given PubMed ID concurrently.")
    argparser.add_argument("-n", action="store",
                           dest="n", required=True, type=int,
                           help="number_of_peons_per_client")
    argparser.add_argument("-a", action="store",
                           dest="a", required=False, type=int,
                           help="Number of references to download concurrently.")
    argparser.add_argument("--port", action="store",
                           dest="port", required=True, type=int,
                           help="Port nr")
    argparser.add_argument("--host", action="store",
                           dest="host", required=True, type=str,
                           help="Host nr")

    argparser.add_argument("-s", action="store_true",
                           dest="s", required=False,help="server")
    argparser.add_argument("-c", action="store_true",
                           dest="c",help="client")

    argparser.add_argument("pubmed_id", action="store", type=str, nargs=1, help="Pubmed ID of the article to harvest for references to download.")
    args = argparser.parse_args()
    print("Getting: ", args.pubmed_id, args.n, args.a, args.c, args.s, args.host, args.port)



    if args.s:
        server = mp.Process(target=runserver, args=(runner, args.pubmed_id, args.port))
        server.start()
        time.sleep(1)
    if args.c:
        client = mp.Process(target=runclient, args=(args.host,args.port,args.n))
        client.start()
        server.join()
        client.join()