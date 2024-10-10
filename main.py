from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from resources.artist import ArtistResource
from resources.album import AlbumResource
from resources.track import TrackResource
from resources.playlist import PlaylistResource
from resources.playlistTrack import playlistTrackResource
from resources.search_and_filter import TracksByArtist, SearchForArtist

from models import db

import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#db = SQLAlchemy(app)
db.init_app(app)
api = Api(app)





@app.route('/')
def home():
    return 'All my bums'

api.add_resource(ArtistResource, '/artist', '/artist/<int:artist_id>')
api.add_resource(AlbumResource, '/albums/<int:album_id>', '/artist/<int:artist_id>/albums', '/albums')
api.add_resource(TrackResource, '/albums/<int:album_id>/tracks', '/tracks/<int:track_id>')
api.add_resource(PlaylistResource, '/playlist/<int:playlist_id>', '/playlists')
api.add_resource(playlistTrackResource, '/playlists/<int:playlist_id>/tracks/<int:track_id>')
api.add_resource(TracksByArtist, '/artist/<int:artist_id>/tracks')
api.add_resource(SearchForArtist, '/artist/search')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

