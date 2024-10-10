from models import db, Album, Artist
from flask import jsonify
import datetime

from flask_restful import Resource, reqparse, marshal_with, abort, fields


album_args = reqparse.RequestParser()
album_args.add_argument('name', type = str, required = True, help = 'Name of artist is needed')
#album_args.add_argument('release_date', type = lambda d: datetime.strptime(d, '%Y-%m-%d'), required = True, help = 'Release date is needed')
album_args.add_argument('release_date', type = str, required = True, help = 'Release date is needed')
album_args.add_argument('artist_id', type = int, help = 'Artist id is needed')


albumFields = {
    'id':fields.Integer,
    'name':fields.String,
    'release_date':fields.String,
    'artist_id':fields.Integer
    }

class AlbumResource(Resource):
    @marshal_with(albumFields)
    def post(self, artist_id):
        args = album_args.parse_args()
        # get artist from the artist id
        artist = Artist.query.get(artist_id)
        if not artist:
            return {"error": "artist not found"},  404
        try:
            rel_date = datetime.datetime.strptime(args['release_date'], "%Y-%m-%d")
        except ValueError:
            abort(http_status_code=404, message="Invalis date format")
        
        new_album = Album(name = args["name"],
        release_date = rel_date,
        artist_id = artist_id)
        
        db.session.add(new_album)
        db.session.commit()
        albums = Album.query.filter_by(artist_id = artist_id).order_by(Album.release_date).all()
        return albums, 201
    
    @marshal_with(albumFields)
    def get(self, album_id = None, artist_id = None):
          
        if artist_id:
            this_artist = Artist.query.filter_by(id = artist_id).first()
            if not this_artist:
               abort(http_status_code=404, message="Artist not found")
            artist_albums = this_artist.albums.order_by(Album.release_date).all()
            #artist_albums = Album.query.filter_by(artist_id = artist_id).all()
            return artist_albums, 201
        if album_id:
            albums = Album.query.filter_by(id = album_id).first()
            if not albums:
                abort(http_status_code=404, message="Album not found")
            this_album = Album.query.get(album_id)
            return this_album, 201
        all_albums = Album.query.order_by(Album.artist_id, Album.release_date).all()
        return all_albums, 201

    #@marshal_with(albumFields)
    def delete(self, album_id):
        album = Album.query.filter_by(id = album_id).first()
        if not album:
            abort(http_status_code=404, message="Album not found")
        db.session.delete(album)
        db.session.commit()
        return {'message': f'User bum {album.name}'}, 200
    
    @marshal_with(albumFields)
    def put(self, album_id):
        album = Album.query.filter_by(id = album_id).first()
        if not album:
            abort(http_status_code=404, message="Album not found")
        args = album_args.parse_args()
        album.name = args['name']        

        artist = args['artist_id']
        new_artist = Artist.query.get(artist)
        #new_name = args['name']
        if not new_artist:
            abort(http_status_code=404, message="Artist not found")
        album.artist_id = artist
        thid = args['release_date']
        fgf = datetime.datetime.strptime(thid, "%Y-%m-%d")

        if args['release_date']:
            try:
#                rel_date = datetime.datetime.strptime(args['release_date'], "%Y-%m-%d")
                rel_date = fgf
            except ValueError:
                abort(http_status_code=404, message="Invalis date format")
        album.release_date = rel_date
        db.session.commit()
        #albums = Album.query.all()
        return album, 201


"""     def put(self, artist_id):
        artist = Artist.query.get(artist_id)
        if not artist:
           abort(404, message = 'Artist not found')
        args = artist_args.parse_args()
        artist.name = args['name']
        artist.nationality = args["nationality"]
        artist.year_formed = args["year_formed"]
        
        db.session.commit()
        #artists = Artist.query.all()
        return artist, 200    """       

""" 
        new_team = team(team_name = args["team_name"], team_country = args["team_country"], team_ground = args["team_ground"], year_founded = args["year_founded"])
        db.session.add(new_team)
        db.session.commit()
        teams = team.query.all()
        return teams, 201
 """