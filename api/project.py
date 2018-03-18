from config import get_db_connection
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