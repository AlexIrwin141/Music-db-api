from models import db, Track, Playlist
from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort, fields



class playlistTrackResource(Resource):
    def post(self, playlist_id, track_id):
        # validate playlist and track
        playlist = Playlist.query.get_or_404(playlist_id)
        track = Track.query.get_or_404(track_id)

        # look and see if we already have this track in the playlist
        if track in playlist.tracks:
            return {"message": "This track is alreay in the playlist"}, 400



        #Add track to playliust
        playlist.tracks.append(track)
        db.session.commit()
        return {"message": "added track to playlist"}, 200
    
    def delete(self, playlist_id, track_id):
        # check it is a valid playlist

        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            abort(404, message = f"Playlist with id {playlist_id} not found")

        # check it is a valid track
        track = Track.query.get(track_id)
        if not track:
            abort(404, message = f"track with id {track_id} not found")

        #make sure the rtack is actually in the playlist

        if track not in playlist.tracks:
            abort(http_status_code=404, message="Track not found in playlist")

        #delete track from playlist
        playlist.tracks.remove(track)
        db.session.commit()

        return{"message": f"removed {track.title} from playlist {playlist.name}"}, 200


