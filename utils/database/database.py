import MySQLdb
from django.utils import timezone
from environs import Env

env = Env()
env.read_env()


class DatabaseBot:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.create()

    def create(self):
        if not self.connection:
            try:
                self.connection = MySQLdb.connect(
                    host=env.str('USAT_DB_HOST'),
                    port=env.int('USAT_DB_PORT'),
                    user=env.str('USAT_DB_USER'),
                    passwd=env.str('USAT_DB_PASSWORD'),
                    db=env.str('USAT_DB_NAME'),
                    charset='utf8mb4',
                    use_unicode=True
                )
                self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            except MySQLdb.Error as e:
                pass

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.connection = None
        self.cursor = None

    def execute(self, query: str, args: tuple = (), fetchone: bool = False, fetchall: bool = False):
        try:
            self.cursor.execute(query, args)
            if fetchone:
                result = self.cursor.fetchone()
                return result if result else None
            if fetchall:
                result = self.cursor.fetchall()
                return result if result else ()
        except MySQLdb.Error as e:
            print(f"Error executing query: {e}")

    def update_application_status(self, tgId, new_status):
        query = "UPDATE applicants SET applicationStatus = %s WHERE tgId = %s;"
        self.execute(query, (new_status, tgId))

    def get_application_status(self, tgId):
        query = "SELECT applicationStatus AS status FROM applicants WHERE tgId = %s;"
        return self.execute(query, (tgId,), fetchone=True)

    def get_exam_result(self, tgId):
        query = "SELECT applicant_id, totalScore FROM exam_results WHERE applicant_id = %s;"
        return self.execute(query, (tgId,), fetchone=True)


class DatabaseMessage:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.create()

    def create(self):
        if not self.connection:
            try:
                self.connection = MySQLdb.connect(
                    host=env.str('DB_HOST'),
                    port=env.int('DB_PORT'),
                    user=env.str('DB_USER'),
                    passwd=env.str('DB_PASSWORD'),
                    db=env.str('DB_NAME'),
                    charset='utf8mb4',
                    use_unicode=True
                )
                self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            except MySQLdb.Error as e:
                print(f"Error connecting to MySQL: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.connection = None
        self.cursor = None

    def execute(self, query: str, args: tuple = (), fetchone: bool = False, fetchall: bool = False):
        try:
            self.cursor.execute(query, args)
            if fetchone:
                result = self.cursor.fetchone()
                return result if result else None
            if fetchall:
                result = self.cursor.fetchall()
                return result if result else ()
        except MySQLdb.Error as e:
            pass

    def get_active_token(self):
        query = "SELECT id, token, is_active, created_at FROM tokens WHERE is_active = TRUE;"
        return self.execute(query, fetchone=True)

    def add_active_token(self, token):
        # Deactivate all active tokens
        self.execute("UPDATE tokens SET is_active = FALSE WHERE is_active = TRUE")
        # Insert the new active token
        query = "INSERT INTO tokens (token, is_active, created_at) VALUES (%s, TRUE, %s)"
        self.execute(query, (token, timezone.now()))
