from flask import Flask, request, make_response, jsonify
import dbhelpers, apihelpers, dbcreds

app = Flask(__name__)

@app.post("/api/painting")
def post_painting():
    error = apihelpers.check_endpoint_info(request.json, ["artist", "name", "date_painted", "image_url"])
    if(error != None):
        return make_response(jsonify(error), 400)
    
    results = dbhelpers.run_procedure('call insert_painting(?,?,?,?)', 
                            [request.json.get("artist"),request.json.get("date_painted"),request.json.get("name"),request.json.get("image_url")])
    
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response("Sorry, there has been an error", 500)
    
@app.get("/api/painting")
def get_paintings():
    error = apihelpers.check_endpoint_info(request.args, ["artist"])
    if(error != None):
        return make_response(jsonify(error), 400)
    
    results = dbhelpers.run_procedure('call get_paintings(?)', 
                            [request.args.get("artist")])
    
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response("Sorry, there has been an error", 500)

if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Development Mode")
    app.run(debug=True)