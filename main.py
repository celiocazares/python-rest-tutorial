from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"video(name={name}, views={views}, likes={likes})"


# CREATE DATABASE
# db.create_all()

# ARGUMENTS FOR THE API
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",
                            type=str,
                            help="Name of the video is required",
                            required=True)
video_put_args.add_argument("views",
                            type=int,
                            help="Views of the video",
                            required=True)
video_put_args.add_argument("likes",
                            type=int,
                            help="Likes on the video",
                            required=True)


# VALIDATION
def abort_if_id_doesnt_exists(video_id):
    if (video_id not in videos):
        abort(404, message="Video id does not exist")


def abort_if_id_exists(video_id):
    if (video_id in videos):
        abort(409, message="Video id already exists")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.get(video_id)
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id,
                           name=args['name'],
                           views=args['views'],
                           likes=args['likes'])

        db.session.add(video)
        db.session.commit()
        return video, 201

    def delete(self, video_id):
        abort_if_id_doesnt_exists(video_id)
        del videos[video_id]
        return '', 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
