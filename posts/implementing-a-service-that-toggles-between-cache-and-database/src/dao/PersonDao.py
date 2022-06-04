
class PersonDao:

    def __init__(self):
        self.use_db = False
        self.person_db_dao = PersonDbDao()
        self.person_cache_dao = PersonCacheDao()

    def is_use_db(self):
        return self.use_db

    def set_use_db(self, flag):
        self.use_db = flag

    def get(self, id):

