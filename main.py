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

video_update_args = reqparse.RequestParser()

video_update_args.add_argument("name",
                               type=str,
                               help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")


# VALIDATION
def abort_if_id_doesnt_exists():
    abort(404, message="Video id does not exist")


def abort_if_id_exists():
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
        result = VideoModel.query.filter_by(id=video_id).first()
        # result = VideoModel.query.filter_by(views=video_id).all()
        if not result:
            abort_if_id_doesnt_exists()
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()

        if result:
            abort_if_id_exists()
        video = VideoModel(id=video_id,
                           name=args['name'],
                           views=args['views'],
                           likes=args['likes'])

        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort_if_id_doesnt_exists()
        if args['name']:
            result.name = args['name']
        if args['likes']:
            result.likes = args['likes']
        if args['views']:
            result.views = args['views']

        db.session.commit()

        return result, 201

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort_if_id_doesnt_exists(video_id)

        VideoModel.query.filter_by(id=video_id).delete()

        db.session.commit()
        return 'Video deleted successfully', 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
