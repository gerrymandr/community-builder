from config import get_db_connection
import pandas as pd
from pymysql.cursors import DictCursor


class Project:

    conn = get_db_connection()
    populated = False

    def __init__(self, project_id, populate=False):
        self.project_id = project_id

        if populate:
            self.populate()


    def populate(self):
        with self.conn.cursor(DictCursor) as cursor:
            sql = "SELECT * FROM projects WHERE id = %s"
            cursor.execute(sql, (self.project_id))
            if cursor.rowcount > 0:
                res = cursor.fetchone()

                self.name = res["name"]
                self.description = res["description"]
                self.bounding_box_id = res["bounding_box_id"]

        self.populated = True


    def get_units(self):
        with self.conn.cursor(DictCursor) as cursor:
            sql = "SELECT geoid, xmin, xmax, ymin, ymax FROM project_units WHERE project_id = %s"
            cursor.execute(sql, (self.project_id))
            if cursor.rowcount > 0:
                return [cursor.fetchall()]
            else:
                return []

    def get_filtered_units(self, bbox):
        bbox["project_id"] = self.project_id
        with self.conn.cursor(DictCursor) as cursor:
            sql = """
                SELECT u.geoid, xmin, xmax, ymin, ymax
                FROM project_units pu
                    INNER JOIN units u ON u.geoid = pu.geoid
                WHERE pu.project_id = %(project_id)s AND
                    NOT (
                        u.xmax < %(xmin)s OR
                        %(xmax)s < u.xmin OR
                        u.ymax < %(ymin)s OR
                        %(ymax)s < u.ymin
                )
            """
            cursor.execute(sql, bbox)

            if cursor.rowcount > 0:
                return [{"geoid": u["geoid"], "xmin": float(u["xmin"]), "xmax": float(u["xmax"]), "ymin": float(u["ymin"]), "ymax": float(u["ymax"])} for u in cursor.fetchall()]
            else:
                return []

        pass


    def dict(self):
        if self.populated:
            return {
                "project_id": self.project_id,
                "name": self.name,
                "description": self.description,
                "bounding_box_id": self.bounding_box_id
            }
        else:
            return {
                "project_id": self.project_id
            }