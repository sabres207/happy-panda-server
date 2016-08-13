import pymongo


class MongoError(BaseException):
    pass


class MongoDAL(object):
    def __init__(self, username='doroncoman', password='doroncoman', ip='ds153735.mlab.com', database='doroncoman',
                 auth_mechanism='SCRAM-SHA-1', port=53735):
        self.username = username
        self.password = password
        self.ip = ip
        self.database = database
        self.auth_mechanism = auth_mechanism
        self.mongouri = "mongodb://{0}:{1}@{2}/{3}?authMechanism={4}"
        self.port = port

        self.client = None

    def connect(self):
        self.client = pymongo.MongoClient(self.format_uri(), self.port)

    def disconnect(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def save(self, collection_name, dict_to_save):
        if self.client is not None:
            self.client[self.database][collection_name].save(dict_to_save)
        else:
            raise MongoError("client is not connected")

    def find(self, collection_name, dict_to_find):
        if self.client is not None:
            return self.client[self.database][collection_name].find(dict_to_find)
        else:
            raise MongoError("client is not connected")

    def find_one(self, collection_name, dict_to_find):
        if self.client is not None:
            return self.client[self.database][collection_name].find_one(dict_to_find)
        else:
            raise MongoError("client is not connected")

    def format_uri(self):
        return self.mongouri.format(self.username, self.password, self.ip, self.database, self.auth_mechanism)

    def db(self):
        return self.client[self.database]


def usemain(key, value):
    mongodal = MongoDAL()
    mongodal.connect()

    coll_name = "mycollection"

    # me = {"name": "doron", "age": 25, "what more": [1, 4, 23, "chicken"]}
    # mongodal.save(coll_name, me)
    #
    # him = {"name": "itsik", "age": 30}
    # mongodal.save(coll_name, him)
    #
    # other = {"name": "dudi", "agse": 25}
    # mongodal.save(coll_name, other)

    things = mongodal.find(coll_name, {key, value})

    return [entry for entry in things]
