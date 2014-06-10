from app import db

class Player(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	position = db.Column(db.String(100), index = True, unique = False)
	dbpedia_ID = db.Column(db.String(200), index = True, unique = True)
	name = db.Column(db.String(200), index = True, unique = False)

	def __repr__(self):
		return 'Player: %r' % (self.name)