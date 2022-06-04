
class PersonServiceImpl(PersonService):

    def __init__(self):
        self.person_dao = PersonDao()

    def get(self, id):
        return self.person_dao.get(id)
