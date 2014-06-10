from app import app
import requests
import json
from app import db, models
from flask import render_template
from flask import request
import requests
import sys
import collections


def count(player, date):
	player_utf8 = player.encode('utf-8')
	r = requests.get('https://newsreader.scraperwiki.com/summary_of_events_with_actor?uris.0=http://dbpedia.org/resource/{player}&datefilter={date}&output=json'.format(player=player_utf8, date=date))
	print r.content
	print r.url
	try:
	    result = r.json()
	    return result['count']
	except Exception:
		return -1

def get_player(p):
	dbpedia_ID = p.dbpedia_ID
	june_count = count(dbpedia_ID, '2010-06')
	july_count = count(dbpedia_ID, '2010-07')
	print p.name
	print june_count
	print july_count
	overall_count = june_count + july_count
	player_name = p.name
	player_position = p.position
	return({'player_name': player_name, 'player_position': player_position, 'count': overall_count})
	

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/team/2010')
def team():
	positions = ["Goalkeeper", "Defender", "Midfielder", "Striker"]
	team = collections.OrderedDict(((k,[]) for k in positions))
	for position in positions:
		players = models.Player.query.filter_by(position=position).all()
		for p in players:
			team[position].append(get_player(p))
	print team
	return render_template("team.html", team = team)


@app.route('/framenet/<framenet_term>')
def framenet(framenet_term):
	test = get_events_for_framenet(framenet_term)
	print test
	return render_template("test.html", test=test)

 
def get_events_for_framenet(framenet):
	baseurl = "https://knowledgestore.fbk.eu/nwr/worldcup-hackathon/sparql"
	auth = ("nwr_hack", "london_2014")
	basequery = """SELECT ?event WHERE {{?event rdf:type framenet:{}}} LIMIT 10"""
	query = basequery.format(framenet)
	j = requests.get(baseurl, auth=auth, params={'query': query}).json()
	return [item['event']['value'] for item in j['results']['bindings']]
 
def get_framenets_for_event(event):
	baseurl = "https://knowledgestore.fbk.eu/nwr/worldcup-hackathon/sparql"
	auth = ("nwr_hack", "london_2014")
	basequery = """SELECT ?framenet WHERE {{<{}> rdf:type ?framenet}} LIMIT 10"""
	query = basequery.format(event)
	j = requests.get(baseurl, auth=auth, params={'query': query}).json()
	print query
	return [item['framenet']['value'] for item in j['results']['bindings']]

@app.route('/event')
def event():
	event = request.args.get('event')
	print event
	test = get_framenets_for_event(event)
	print test
	return render_template("test.html", test=test)
