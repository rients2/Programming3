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


def make_server_manager(port, authkey):
    """ Create a manager for the server, listening on the given port.
        Return a manager object with get_job_q and get_result_q methods.
    """
    job_q = queue.Queue()
    result_q = queue.Queue()

    # This is based on the examples in the official docs of multiprocessing.
    # get_{job|result}_q return synchronized proxies for the actual Queue
    # objects.
    class QueueManager(BaseManager):
        pass

    QueueManager.register('get_job_q', callable=lambda: job_q)
    QueueManager.register('get_result_q', callable=lambda: result_q)

    manager = QueueManager(address=('', port), authkey=authkey)
    manager.start()
    print('Server started at port %s' % port)
    return manager

def runserver(fn, data, PORTNUM, amount=10):
    # Start a shared manager server and access its queues
    manager = make_server_manager(PORTNUM, b'whathasitgotinitspocketsesss?')
    shared_job_q = manager.get_job_q()
    shared_result_q = manager.get_result_q()
    
    if not data:
        print("Gimme something to do here!")
        return
    
    print("Sending data!")
    for d in data:
        shared_job_q.put({'fn' : fn, 'arg' : d, 'amount': amount})
    
    time.sleep(2)  
    
    results = []
    while True:
        try:
            result = shared_result_q.get_nowait()
            results.append(result)
            print("Got result!", result)
            if len(results) == len(data):
                print("Got all results!")
                break
        except queue.Empty:
            time.sleep(1)
            continue
    # Tell the client process no more data will be forthcoming
    print("Time to kill some peons!")
    shared_job_q.put(POISONPILL)
    # Sleep a bit before shutting down the server - to give clients time to
    # realize the job queue is empty and exit in an orderly way.
    time.sleep(5)
    print("Aaaaaand we're done for the server!")
    manager.shutdown()
    print(results)


def make_client_manager(ip, port, authkey):
    """ Create a manager for a client. This manager connects to a server on the
        given address and exposes the get_job_q and get_result_q methods for
        accessing the shared queues from the server.
        Return a manager object.
    """
    class ServerQueueManager(BaseManager):
        pass

    ServerQueueManager.register('get_job_q')
    ServerQueueManager.register('get_result_q')

    manager = ServerQueueManager(address=(ip, port), authkey=authkey)
    manager.connect()

    print('Client connected to %s:%s' % (ip, port))
    return manager




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

def xml_parser(pubmed_id):
        title = pubmed_id.replace("\'","")
        old_tuple = ()

        try:
            mytree = ET.parse(f'output/{title}.xml')
            myroot = mytree.getroot()
            for firstname, lastname in zip(myroot.iter('given-names'),myroot.iter('surname')):
                full_name = [str(firstname.text) + ' ' + str(lastname.text)]
                new_tuple = tuple(full_name)
                old_tuple = old_tuple + new_tuple


            with open(f'output/{title}.authors.pickle', 'wb') as f:
                pickle.dump(old_tuple, f)
        except:
            with open(f'output/{title}.authors.pickle', 'wb') as f:
                pickle.dump(old_tuple, f)
                print('nothing written.')


# Function that obtains and writes the xml file for a given pubmed id
def fetcher(pmid_ref):
    
    title = pmid_ref.replace("\'","")

    handle = Entrez.efetch(db="pmc", id=pmid_ref, rettype="XML", retmode="text",
                        api_key='b73a5ffde89ba2ae4feca63960fdac659009')

    with open(f'output/{title}.xml', 'wb') as file:
        file.write(handle.read())
        file.close()
        handle.close()
        
    try:
        xml_parser(pubmed_id=pmid_ref)
        print('Finnished')
    except:
        print('pmid not found.')


def runclient(IP,PORTNUM,num_processes):
    manager = make_client_manager(IP, PORTNUM, AUTHKEY)
    job_q = manager.get_job_q()
    result_q = manager.get_result_q()
    run_workers(job_q, result_q, num_processes)
    
def run_workers(job_q, result_q, num_processes):
    processes = []
    for p in range(num_processes):
        temP = mp.Process(target=peon, args=(job_q, result_q))
        processes.append(temP)
        temP.start()
    print("Started %s workers!" % len(processes))
    for temP in processes:
        temP.join()

def peon(job_q, result_q):
    my_name = mp.current_process().name
    while True:
        try:
            job = job_q.get_nowait()
            if job == POISONPILL:
                job_q.put(POISONPILL)
                print("Aaaaaaargh", my_name)
                return
            else:
                try:
                    result = job['fn'](job['arg'])
                    print("Peon %s Workwork on %s!" % (my_name, job['arg']))
                    result_q.put({'job': job, 'result' : result})
                except NameError:
                    print("Can't find yer fun Bob!")
                    result_q.put({'job': job, 'result' : ERROR})

        except queue.Empty:
            print("sleepytime for", my_name)
            time.sleep(1)

def runner(pmid, amount=10):
    refs = final_script(pmid)

    try:
        refs = refs[:amount]
    except: 
        refs = refs[:len(refs)]

    cpus = mp.cpu_count()

    with mp.Pool(cpus) as pool:
        results = pool.map(fetcher, refs)