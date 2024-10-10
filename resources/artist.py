from models import db, Artist

from flask_restful import Resource, reqparse, marshal_with, abort, fields


artist_args = reqparse.RequestParser()
artist_args.add_argument('name', type = str, required = True, help = 'Name of artist is needed')
artist_args.add_argument('nationality', type = str, required = True, help = 'Nationality of artist is needed')
artist_args.add_argument('year_formed', type = int, help = 'Year the artist came to fruition')


artistFields = {
    'id':fields.Integer,
    'name':fields.String,
    'nationality':fields.String,
    'year_formed':fields.Integer
    }

class ArtistResource(Resource):
    # Get Artist details
    @marshal_with(artistFields)
    def get(self, artist_id = None):
        if artist_id:
            # look for specified artist
            this_artist = Artist.query.filter_by(id = artist_id).first()
            if not this_artist:
                abort(404, message = 'Artist not found')
            return this_artist
        # show all artists
        all_artists = Artist.query.all()
        return all_artists
    
    # Add a new artist
    @marshal_with(artistFields)
    def post(self):
        args = artist_args.parse_args()
        new_artist = Artist(name = args["name"],
        nationality = args["nationality"],
        year_formed = args["year_formed"])
        
        db.session.add(new_artist)
        db.session.commit()
        artists = Artist.query.all()
        return artists, 201
    
    # Delete an artist
    def delete(self, artist_id):
        artist = Artist.query.filter_by(id = artist_id).first()
        if not artist:
            abort(http_status_code=404, message="Artist not found")
        db.session.delete(artist)
        db.session.commit()
        return {'message': f'The artis know as  {artist.name} is gorn'}, 200
    

    # Update an artist's details
    @marshal_with(artistFields)
    def put(self, artist_id):
        artist = Artist.query.get(artist_id)
        if not artist:
           abort(404, message = 'Artist not found')
        args = artist_args.parse_args()
        artist.name = args['name']
        artist.nationality = args["nationality"]
        artist.year_formed = args["year_formed"]
        
        db.session.commit()
        #artists = Artist.query.all()
        return artist, 200
        

""" 
        new_team = team(team_name = args["team_name"], team_country = args["team_country"], team_ground = args["team_ground"], year_founded = args["year_founded"])
        db.session.add(new_team)
        db.session.commit()
        teams = team.query.all()
        return teams, 201
 """