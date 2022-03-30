from flask import redirect, request, json, Flask
# from . import application
# import json
import en_core_web_sm
from app.hevyspacy import getjson_aif

app = Flask(__name__)

@app.route('/noop', methods=['GET', 'POST'])
def amf_schemes():
	if request.method == 'POST':
		f = request.files['file']
		f.save(f.filename)
		ff = open(f.filename, 'r')
		readcontent = ff.read()
		content = json.loads(readcontent)
		example = getjson_aif(content)
	return example
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int("5000"), debug=False)