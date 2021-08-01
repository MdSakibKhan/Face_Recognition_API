from flask import Flask, request, jsonify
import argparse
import base64
import uuid
from deepface import DeepFace
from fuzzy import fuzzyCheck

app = Flask(__name__)

@app.route("/api", methods=["GET"])
def test():
    return jsonify({'API' : 'Running'})

@app.route("/api/attributeCheck", methods=["POST"])
def attributeCheck():
    # Get the requested Data 
    requested_data = request.get_json()
    
    # Get Data.
    info1 = requested_data["info1"]
    info2 = requested_data["info2"]

    score, strength = fuzzyCheck(info1, info2)

    results = {
            "score" : score,
            "strength" : strength
        }

    return jsonify(results)


@app.route("/api/findOne", methods=["POST"])
def findOne():
    
    # Get the requested Data 
    requested_data = request.get_json()
    
    # Convert byte64 to Image.
    test_image_data = base64.b64decode(requested_data["img"])
    
    #Save image with unique name
    img_file = './image_test/' + str(uuid.uuid4()) + requested_data["img_format"]
    with open(img_file, 'wb') as f:  # The 'wb' indicates that the file is opened for writing in binary mode. 
        f.write(test_image_data)

    # Run Analysis
    results = DeepFace.find(img_path = img_file, db_path = "./image_db")
    results = results[results["VGG-Face_cosine"]<0.20].iloc[:1,:]
    return results.to_json()


@app.route("/api/findAll", methods=["POST"])
def findAll():
    
    # Get the requested Data 
    requested_data = request.get_json()
    
    # Convert byte64 to Image.
    test_image_data = base64.b64decode(requested_data["img"])
    
    #Save image with unique name
    img_file = './image_test/' + str(uuid.uuid4()) + requested_data["img_format"]
    with open(img_file, 'wb') as f: # The 'wb' indicates that the file is opened for writing in binary mode. 
        f.write(test_image_data)
        
    # Run Analysis
    results = DeepFace.find(img_path = img_file, db_path = "./image_db")

    return results.to_json()



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-p', '--port',
		type=int,
		default=5000,
		help='Port of serving api')
	args = parser.parse_args()
	app.run(host='0.0.0.0', port=args.port)