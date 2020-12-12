from data_parsers import frame_instance
from data_parsers import role_instance
import xml.etree.ElementTree as et


class ReadSwedishFile(object):
    '''
    This class reads the entire xml-style FN file for Swedish
    '''
    def __init__(self, filename):
        frames = self.readXMLSentences(filename)
        self.frames = frames

    @classmethod
    def readXMLSentences(self, filename):
        file = et.parse(filename)
        root = file.getroot()

        frames = []

        for child in root.iter("text"):
            frame_name = child.get("frame")
            lexical_units_in_frame = child.get("lexical_units_saldo")
            core_elements_in_frame = child.get("core_elements")

            for sentence in child.iter("sentence"):
                id = sentence.get("id")
                frame = frame_instance.FrameInstance()
                tokens = []
                lu = ''
                lemma = []
                roles = []
                lu_indices = []
                for word in sentence.iter("w"):
                    tokens.append(word.text)
                for element in sentence.iter("element"):
                    if(element.get("name") == "LU"):
                        for w in element.iter("w"):
                            lu += w.text + " "
                            lu_indices.append(int(w.get("ref"))-1)
                            try:
                                lemma.append(w.lemma.strip("|"))
                            except:
                                lemma.append(w.text)
                    if(element.get("name") in core_elements_in_frame):
                        role = role_instance.RoleInstance()
                        role.role = element.get("name")
                        lemma = []
                        pos = []
                        indices = []
                        for w in element.iter("w"):
                            pos.append(w.get("pos"))
                            lemma.append(w.get("lemma").strip("|"))
                            indices.append(w.get("ref"))
                        role.lemma = lemma
                        role.pos = pos
                        role.indices = indices
                        roles.append(role)
                frame.frame_name = frame_name
                frame.lu = lu.strip()
                frame.sentence_index = id
                frame.sentence = tokens
                frame.lemma = lemma
                frame.roles = roles
                frame.indices = lu_indices
                frames.append(frame)
        return frames

def getFrames(dir):
    framenet = ReadSwedishFile(dir)
    return framenet.frames