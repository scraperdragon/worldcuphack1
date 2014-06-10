import requests
import json
import sys


""" for the two months, all mentioned players - how many counts."""


baseurl = "https://knowledgestore.fbk.eu/nwr/worldcup-hackathon/sparql"
auth = ("nwr_hack", "london_2014")
query = """SELECT ?footballer (COUNT(?event) as ?q) WHERE {
           ?event sem:hasActor ?footballer .
           ?footballer a dbo:SoccerPlayer .
           ?event sem:hasTime ?t .
           ?t rdfs:label ?outtime .
           FILTER(STRSTARTS(STR(?outtime), "2010-06"))
          }
           GROUP BY ?footballer
           ORDER BY DESC(?q)
           LIMIT 40
            """

def get_events_for_framenet():
    j = requests.get(baseurl, auth=auth, params={'query': query}).json()
    print len(j)
    return j

def pretty_j(j):
    builder = []
    for item in j['results']['bindings']:
        row = []
        for col in item:
            row.append(item[col]['value'])
        builder.append(row)
    return json.dumps(builder, indent=2)

e = get_events_for_framenet()
try:
    print pretty_j(e)
except Exception:
    print e



"""


           ?event sem:hasActor ?filterfield .
           ?filterfield a dbo:SoccerPlayer .


"""
