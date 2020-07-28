from ws.main import api, browser
from flask import jsonify
from flask_restx import Resource
from ws.pageobjects.TrackPage import TrackPage

track_page = TrackPage(browser)
ns = api.namespace("ws")


@ns.route("/samples/<string:artist>/<string:track>")
class Track(Resource):
    @ns.param("artist", "The artist name.")
    @ns.param("track", "The track name.")
    @ns.response(200, "Object with track samples")
    def get(self, artist, track):
        """Get all samples and covers"""
        try:
            track_page.get_track_page(artist, track)
            samples = track_page.get_samples()
            return jsonify(samples)
        except Exception as e:
            print(e)
            return "Error while crawling WS", 500
