from models import db, Artist, Album, Track, Playlist, playlist_tracks
from flask_restful import Resource, reqparse, marshal_with, abort, fields
from flask import request
from sqlalchemy import select, delete, or_

track_fields = {
                "id": fields.Integer,
                "title": fields.String,
                "album": fields.String(attribute='album.name')
                }

artist_fields = {
                "id": fields.Integer,
                "name": fields.String
                }


artist_search_args = reqparse.RequestParser()
artist_search_args.add_argument('name', type = str, required = True, help = 'Artist name or part of is needed')

class TracksByArtist(Resource):
    @marshal_with(track_fields)
    def get(self, artist_id):
        #make sure the artist is valid
        artist = Artist.query.get(artist_id)
        if not artist:
             abort(http_status_code=404, message="Artist not found")
        
        tracks = Track.query.join(Album).filter(Album.artist_id == artist_id).order_by(Album.name).all()

        return tracks

class SearchForArtist(Resource):
    @marshal_with(artist_fields)
    def get(self):
        # get the name parameter from the query body

        args = artist_search_args.parse_args()
        name = args["name"]

        #look for anyartists containing the search string
        artists = Artist.query.filter(Artist.name.ilike(f'%{name}%')).all()

        return artists

        