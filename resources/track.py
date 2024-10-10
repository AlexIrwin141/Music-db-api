from models import db, Artist, Album, Track

from flask_restful import Resource, reqparse, marshal_with, abort, fields



track_args = reqparse.RequestParser()
track_args.add_argument('title', type = str, required = True, help = 'Track name is needed')
track_args.add_argument('album_id', type = int, help = 'Album is needed')


trackFields = {
    'id':fields.Integer,
    'title':fields.String,
    'album_id':fields.Integer
    }


class TrackResource(Resource):
    @marshal_with(trackFields)
    def post(self, album_id):
        args = track_args.parse_args()
        # get artist from the artist id

        album = Album.query.get(album_id)
        if not album:
               abort(http_status_code=404, message="Album not found")
        
        new_track = Track(title = args["title"],
        album_id = album_id)


        db.session.add(new_track)
        db.session.commit()
        tracks = Track.query.filter_by(album_id = album_id).all()
        return tracks, 201
    



    
    @marshal_with(trackFields)
    def get(self, album_id):
        args = track_args.parse_args()
        # get artist from the artist id
        album = Album.query.get(album_id)
        if not album:
                abort(http_status_code=404, message="Album not found")
        this_album = Album.query.filter_by(id = album_id).first()
        #if not this_album:
        
            #album_tracks = Track.query.all()
        album_tracks = Track.query.filter_by(album_id = album_id).all()
        if not album_tracks:
            abort(http_status_code=404, message="No tracks found for this albumb")
        return album_tracks, 201

    def delete(self, track_id):
     
        track = Track.query.filter_by(id = track_id).first()
        if not track:
            abort(http_status_code=404, message="Track not found")
        db.session.delete(track)
        db.session.commit()
        return {'message': f'The toon called {track.title} is gorn'}, 200
    
    @marshal_with(trackFields)
    def put(self, track_id):
        track = Track.query.get(track_id) 
        if not track:
             abort(404, message = 'Track not found')
        args = track_args.parse_args()
        track.title = args['title']

        album = args['album_id']
        new_album = Album.query.get(album)
        #new_name = args['name']
        if not new_album:
            abort(http_status_code=404, message="Album not found")
        track.album_id = album
        db.session.commit()
        return track, 200
        