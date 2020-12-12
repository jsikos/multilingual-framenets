'''
The role instance is a semantic role for the given frame.
Lemma, pos tags, and indices are lists for roles with multiple tokens
'''
class RoleInstance:

    def __init__(self):
        self.type = "role"
        self.lemma = []
        self.role = None
        self.pos = []
        self.indices = []

    @property
    def lemma(self):
        return self.__lemma

    @property
    def role(self):
        return self.__role

    @property
    def pos(self):
        return self.__pos

    @property
    def indices(self):
        return self.__indices

    @lemma.setter
    def lemma(self, lemma):
        self.__lemma = lemma

    @role.setter
    def role(self, role):
        self.__role = role

    @pos.setter
    def pos(self, pos):
        self.__pos = pos

    @indices.setter
    def indices(self, indices):
        self.__indices = indices
