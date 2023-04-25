
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
    "first_name": "John",
    "age" : 33,
    "lucky_numbers" : [7,13,22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers":[10,14,3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/member", methods=["POST"])
def handle_new_member():
    request_body = request.get_json()
    if request_body is None:
        raise APIException("request body must de JSON", 400)
        member = {
            "id": jackson_family._generateId(),
            "first_name": request_body.get("first_name", ""),
            "last_name":"Jackson",
            "age": request_body.get ("age", 0),
            "lucky_numbers": request_body.get("lucky_numbers", [])
        }
    jackson_family.add_member(member)
    response_body = {
        "id" : member ["id"],
        "first_name":member["first_name"],
        "age":member["age"],
        "lucky_numbers":member["lucky_numbers"]
    }
    
    return jsonify(response_body), 200



@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = members

    return jsonify(response_body), 200

@app.route("/member/<int:id>", methods=["GET"])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        raise APIException("Member not found", 404)
    return jsonify(member), 200

@app.route("/member/<int:id>", methods=["DELETE"])
def handle_delete_member(id):
    deleted = jackson_family.delete_member(id)
    if not deleted:
        raise APIException("Member not Found",404)
    return jsonify({"msg":"Member deleted successfully"}), 200

@app.errorhandler(APIException)
def handle_api_exception(error):
    return jsonify ({"msg": error.message}), error.status_code
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
