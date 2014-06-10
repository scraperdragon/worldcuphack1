import requests
import sys


""" for the two months, all mentioned players - how many counts."""


baseurl = "https://knowledgestore.fbk.eu/nwr/worldcup-hackathon/sparql"
auth = ("nwr_hack", "london_2014")
query = """SELECT ?s ?o ?v WHERE {{
            <http://news.bbc.co.uk/sport2/hi/football/africa/9109765.stm#nafHeader_fileDesc_creationtime> ?o ?v
}}
 LIMIT 10

            """

def get_events_for_framenet():
    j = requests.get(baseurl, auth=auth, params={'query': query}).json()
    print len(j)
    return j

print get_events_for_framenet()
