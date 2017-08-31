import json
from reader_aio import FileReader
from database import DataBase


class LogFile(FileReader):
    def __init__(self, name, mtime=0, offset=0):
        self.name = name  # ToDo make sure that this variable is full path
        self.mtime = mtime  # Current modify time
        self.last_mtime = 0   # Modify time from os.stat
        self.offset = offset
        self.db = DataBase("test.db")

    @property
    def need_update(self):
        return self.mtime > self.last_mtime

    def sync_from_db(self,):
        self.db.insert_ignore_file(self.name, 0)
        f = self.db.get_file(self.name)
        self.offset = f[2]
        self.last_mtime = f[1]

    def sync_to_db(self, mtime_update=False):
        if mtime_update:
            self.last_mtime = self.mtime
        self.db.update_file(self.name, self.offset, self.last_mtime)

    def line_to_json(self, line, offset):
        data = {
            "message": line.decode('utf-8', 'replace'),
            "fields": {
                "program": 'mt4'
            },
            "source": self.name,
            "offset": offset,
        }
        return json.dumps(data) + '\n'

    def __repr__(self):
        return "<LogFile: {}, {}, {}>".format(
            self.name, self.mtime, self.offset)
