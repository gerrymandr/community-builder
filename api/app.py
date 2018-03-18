#!.env/bin/python
from flask import Flask, jsonify, make_response, request
import config as cfg
from project import Project
import geometry


app = Flask(__name__)

@app.route('/')
def index():
    return cfg.settings["census"]["key"]
    # return "Hello!"


@app.route('/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    proj = Project(project_id, populate=True)
    return jsonify(proj.dict())

@app.route('/project/<int:project_id>/display_units/', methods=['GET', 'POST'])
def get_display_units(project_id):
    proj = Project(project_id, populate=True)
    all_geo = geometry.load_block_groups()

    padded_bbox = geometry.padded_bbox({
        "xmin": float(request.args.get("xmin")),
        "xmax": float(request.args.get("xmax")),
        "ymin": float(request.args.get("ymin")),
        "ymax": float(request.args.get("ymax"))
    })

    units = proj.get_filtered_units(padded_bbox)

    # filtered_geo = geometry.filter_geo(all_geo, units)

    return jsonify(geometry.units_to_dict(units, all_geo))

#@app.route('project/')

if __name__ == '__main__':
    app.run(debug=True)