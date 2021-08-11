import _sqlite3 as db

class DataBase:

    def __init__(self):
        self.open_connection()
        self.c.execute("""CREATE TABLE IF NOT EXISTS files(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uploader TEXT,
                time TEXT,
                file_name TEXT,
                file TEXT
            )""")
        self.conn.close()

    def open_connection(self):
        self.conn = db.connect('stored_files.db')
        self.c = self.conn.cursor()

    def file_metadata(self,uploader :str, date :str,file_name :str, file_url :str):
        self.open_connection()
        self.c.execute("SELECT COUNT(file) FROM files WHERE file_name = ?",(file_name,))
        if not self.c.fetchall()[0][0]:
            self.c.execute("INSERT INTO files(uploader,time,file_name,file) VALUES(?,?,?,?)",(uploader,date,file_name,file_url))
            self.conn.commit()
            self.conn.close()
            return 1
        else:
            self.conn.close()
            return 0
    
    def file_retrieve(self,file_name :str, uploader :str = None):
        self.open_connection()
        self.c.execute("SELECT COUNT(file_name) FROM files where file_name = ?",(file_name,))
        if self.c.fetchall()[0][0]:
            self.c.execute("SELECT * FROM files WHERE file_name = ?",(file_name,))
            data = self.c.fetchone()
            self.conn.close()
            return data
        else :
            self.conn.close()
            return 0

