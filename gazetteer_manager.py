import csv
import datetime
import json
import os
import sqlite3

from definitions import gazetteerDef


class Config(object):
    def __init__(self):
        self.data = []

    def load(self, fn):
        if os.path.exists(fn):
            self.data = json.load(open(fn, "rt"))
        else:
            self.data = []

    def save(self, fn):
        json.dump(self.data, open(fn, "wt"))

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value


class DatabaseManager(object):
    def __init__(self, gazetteer_def, db_name):
        self.gazetteer_def = gazetteer_def
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def create(self):
        for definition in self.gazetteer_def.tables:
            self.create_table(definition)

    def create_table(self, definition):
        fields = [x[0] + " string" for x in definition.config]
        if not definition.meta:
            fields += ["Status string"]
        cols = ",".join(fields)
        SQL = "CREATE TABLE %s (%s" % (definition.name, cols)
        if definition.PK:
            SQL += ",PRIMARY KEY (%s)" % ", ".join(definition.PK)
        SQL += ")"
        cursor = self.conn.cursor()
        cursor.execute(SQL)
        self.conn.commit()


class GazetteerManager(object):
    def __init__(self, dm):
        self.gazetteerDef = gazetteerDef
        self.dm = dm
        self.version = 1

    def get_gazetteer_files(self, selector):
        return [r".\KT-ABP\kt_001.csv", r".\KT-ABP\kt_002.csv", r".\KT-ABP\kt_003.csv"]

    def init_database(self):
        pass

    def load_data(self, version):
        self.version = version
        for fn in self.get_gazetteer_files(""):
            self.load_file(fn)

    def generate_full_dump(self):
        pass

    def generate_cou_dump(self):
        pass

    def clear_flags(self):
        pass

    def load_file(self, file):
        t = datetime.datetime.now()
        cursor = self.dm.cursor()
        count = 0
        src = csv.reader(open(file, "rb"))

        for line in src:
            ID = line[0]
            definition = self.gazetteerDef.map[ID]
            data = line
            if self.version == 1:
                if ID == "11":  # Street
                    data.insert(17, "")
                    data.insert(18, "")
                    data.insert(21, "")
                    data.insert(22, "")
                elif ID == "21":  # BLPU
                    data.insert(10, "")
                    data.insert(11, "")
                    data.insert(14, "")
                    pass
                elif ID == "28":  # DeliveryPointAddress
                    del data[4]
                    data.insert(17, "")
                elif ID == "15":  # StreetDescriptor
                    data.insert(9, "")
                    data.insert(10, "")
                    data.insert(11, "")
                    data.insert(12, "")

            data = [x.decode("utf-8") for x in data]
            ID = data.pop(0)
            change_type = data.pop(0) if not definition.meta else "I"
            pro_order = data.pop(0) if not definition.meta else ""

            if change_type == "I":
                SQL = definition.insert
                values = data[:]
                cursor.execute(SQL, values)

            if change_type == "D":
                SQL = definition.delete
                key = [data[i] for i in definition.PK_index]
                cursor.execute(SQL, key)

            if change_type == "U":
                SQL = definition.update
                key = [data[i] for i in definition.PK_index]
                values = [data[i] for i in definition.field_index]
                # print SQL
                cursor.execute(SQL, values + key)

            count += 1
            if count > 5000:
                self.dm.commit()
                # sys.stdout.write(".")
                # sys.stdout.flush()
                count = 0
        self.dm.commit()
        print datetime.datetime.now() - t

    def update_organisation(self, UPRN, OrgKey, Organisation, LegalName):
        pass


def load_data():
    try:
        os.remove(r".\gazetteer.sqlite")
    except WindowsError, exc:
        pass
    dm = DatabaseManager(gazetteerDef, r".\gazetteer.sqlite")
    dm.create()
    gm = GazetteerManager(dm)
    gm.init_database()
    gm.load_data(1)


OPTIONS = """Options
=======

Q - quit
CS - Create Staging DB
DS - Delete Staging DB
CG - Create Gazetteer
DG - Delete Gazetteer
I  - Import AB data
U  - Update gazetteer
"""


class Commands(object):
    def __init__(self):
        self.config = Config()
        self.config.load("config.json")

    def save(self):
        self.config.save("config.json")

    def run(self):
        while True:
            print OPTIONS
            cmd = raw_input("select option : ").upper()
            if cmd == "Q":
                break


if __name__ == "__main__":
    cmd = Commands()
    cmd.run()
    cmd.save()
    # load_data()
