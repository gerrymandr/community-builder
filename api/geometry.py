import geopandas as gpd


def load_block_groups():
    return gpd.read_file("../data/north_carolina_block_groups.json")


def load_edge():
    return gpd.read_file("../data/north_carolina_boundary.json")


def filter_geo(available, filter_geoids):
    return available[available["GEOID"].isin(filter_geoids)]\


def units_in_box(units, xmin, xmax, ymin, ymax):
    pass


def padded_bbox(bbox, padding=1.25):
    return {
        "xmin": (bbox["xmax"]+bbox["xmin"])/2 - padding*(bbox["xmax"]-bbox["xmin"])/2,
        "xmax": (bbox["xmax"]+bbox["xmin"])/2 + padding*(bbox["xmax"]-bbox["xmin"])/2,
        "ymin": (bbox["ymax"]+bbox["ymin"])/2 - padding*(bbox["ymax"]-bbox["ymin"])/2,
        "ymax": (bbox["ymax"]+bbox["ymin"])/2 + padding*(bbox["ymax"]-bbox["ymin"])/2
    }


def units_to_dict(units, geo):
    out = {}
    features = []
    for u in units:
        coords = [[c[0], c[1]] for c in geo[geo["GEOID"] == u["geoid"]]["geometry"].exterior.coords.xy]

        feat = {
            "type": "Feature",
            "properties": {
                "id": u["geoid"],
                "bbox": [u["xmin"], u["ymin"], u["xmax"], u["ymax"]],
                "geometry": {
                    "type": "Polygon",
                    "coordinates": coords
                }
            }
        }
    out["type"] = "FeatureCollection"
    out["bbox"] = []
    out["Features"] = units

    return out