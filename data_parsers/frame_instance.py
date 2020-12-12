'''
Single frame instance
'''

class FrameInstance:

    def __init__(self):
        self.type = "frame"
        self.sentence_index = None
        self.frame_name = None
        self.lemma = None
        self.pos = None
        self.indices = []
        self.roles = []
        self.lu = None
        self.sentence = []
        self.file_index = None

    @property
    def sentence_index(self):
        return self.__sentence_index

    @property
    def frame_name(self):
        return self.__frame_name

    @property
    def lemma(self):
        return self.__lemma

    @property
    def pos(self):
        return self.__pos

    @property
    def indices(self):
        return self.__indices

    @property
    def roles(self):
        return self.__roles

    @property
    def sentence(self):
        return self.__sentence

    @property
    def lu(self):
        return self.__lu

    @property
    def file_index(self):
        return self.__file_index


    @sentence_index.setter
    def sentence_index(self, sentence_index):
        self.__sentence_index = sentence_index


    @frame_name.setter
    def frame_name(self, frame_name):
        self.__frame_name = frame_name

    @lemma.setter
    def lemma(self, lemma):
        self.__lemma = lemma

    @pos.setter
    def pos(self, pos):
        self.__pos = pos

    @indices.setter
    def indices(self, indices):
        self.__indices = indices

    @roles.setter
    def roles(self, roles):
        self.__roles = roles

    @sentence.setter
    def sentence(self, sentence):
        self.__sentence = sentence

    @lu.setter
    def lu(self, lu):
        self.__lu = lu

    @file_index.setter
    def file_index(self, file_index):
        self.__file_index = file_index

