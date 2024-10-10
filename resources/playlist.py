from models import db, Track, Playlist, playlist_tracks

from flask_restful import Resource, reqparse, marshal_with, abort, fields
from sqlalchemy import select, delete


playlist_args = reqparse.RequestParser()
playlist_args.add_argument('name', type = str, required = True, help = 'Playlist name is needed')


trackModifyFields = {
    'id':fields.Integer,
    'name':fields.String
}

trackFields = {
    'id':fields.Integer,
    'title':fields.String,
    'artist':fields.String(attribute=lambda track: track.album.artist.name)
}

playlistFields = {
    'id':fields.Integer,
    'name':fields.String,
    'tracks':fields.List(fields.Nested(trackFields))
    }


class PlaylistResource(Resource):

# Get playlist details
    @marshal_with(playlistFields)
    def get(self, playlist_id = None):
        if not playlist_id:
            playlist = Playlist.query.all()
        else:
            playlist = Playlist.query.filter_by(id = playlist_id).first()
        if not playlist:
            abort(404, message = 'Playlist nopt found')
        return playlist
    

# Add new playlist
    @marshal_with(playlistFields)
    def post(self):
        args = playlist_args.parse_args()
        new_playlist = Playlist(name = args["name"])
        
        db.session.add(new_playlist)
        db.session.commit()
        playlists = Playlist.query.all()
        return playlists, 201
    
# delete a playlist
    def delete(self, playlist_id):
        playlist = Playlist.query.filter_by(id = playlist_id).first()
        if not playlist:
            abort(http_status_code=404, message="Playlist not found")
        #playlist.tracks = []
        ass = db.session.execute(select(playlist_tracks).where(playlist_tracks.c.playlist_id == playlist_id)).fetchall()
        db.session.execute(playlist_tracks.delete().where(playlist_tracks.c.playlist_id == playlist_id))
        db.session.delete(playlist)
        db.session.commit()
        return {'message': f'Bootrd {playlist.name}'}, 200
        
# modify playlist
    @marshal_with(playlistFields)
    def put(self, playlist_id):
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
           abort(404, message = 'Playlist not found')
        args = playlist_args.parse_args()
        playlist.name = args['name']
        
        db.session.commit()
        return playlist, 200
        