#!.env/bin/python
from flask import Flask, jsonify, make_response
import config as cfg
from project import Project
import geopandas as gpd

bg = gpd.read_file("../data/north_carolina_block_groups.json")

app = Flask(__name__)

@app.route('/')
def index():
    return cfg.settings["census"]["key"]
    # return "Hello!"


@app.route('/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    proj = Project(project_id, populate=True)
    return jsonify(proj.dict())

#@app.route('project/')

if __name__ == '__main__':
    app.run(debug=True)