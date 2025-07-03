from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    pictures = []
    for d in data:
        pictures.append(d['pic_url'])

    return jsonify(pictures), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for d in data:
        if d['id'] == id:
            return d, 200
    return "Not found", 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    if new_picture:
        if not new_picture.get('id'):
            return "No ID", 422

        pic_id = new_picture['id']
        for d in data:
            if d['id'] == pic_id:
                return jsonify(Message=f"picture with id {pic_id} already present"), 302

        data.append(new_picture)
        return jsonify(id=pic_id), 201

    return jsonify(Message="Invalid or missing data"), 422
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.get_json()
    if new_picture:
        pic_id = id
        for d in data:
            if d['id'] == pic_id:
                for k, v in new_picture.items():
                    d[k] = v
                return d, 201
        
        return jsonify(Message="picture not found"), 404

    return jsonify(Message="Invalid or missing data"), 422

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for d in data:
        if d['id'] == id:
            data.remove(d)
            return jsonify(Message=f"picture {id} successfully deleted"), 204
    
    return jsonify(Message="picture not found"), 404