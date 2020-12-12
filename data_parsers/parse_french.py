
from data_parsers import frame_instance

class ReadFrenchFile(object):
    '''
    This class reads the entire conll-style FN file for French
    '''
    def __init__(self, filename):
        frames = self.readFile(filename)
        self.frames = frames

    def readFile(self, filename):
        frames = []
        sentences = []

        raw_sentences = []
        with open(filename, "r") as frenchfile:
            lines = frenchfile.readlines()
            temp_line = []
            for line in lines:
                if not line.strip():
                    raw_sentences.append(temp_line)
                    temp_line = []
                else:
                    temp_line.append(line)

        #get all the frames
        for sent in raw_sentences:
            tokens = []
            sentences.append(tokens)
            id = ""
            for line in sent:
                token_line = line.split("\t")
                tokens.append(token_line[1])

            #set new frame
            frame = frame_instance.FrameInstance()
            frame_indices = []
            frame_lemma = ""
            frame_name = ""
            frame_pos = ""

            frame_id = ""

            for line in sent:
                token_line = line.split("\t")
                if "sentid" in token_line[5]:
                    stoken = token_line[5].split("|")
                    for tid in stoken:
                        if "sentid" in tid:
                            id = tid.strip("sentid=")

                #line containing the frame info
                if "frame=" in token_line[5]:
                    stoken = token_line[5].split("|")
                    for i, tid in enumerate(stoken):
                        if "frame=" in tid:
                            #component of prior frame: necessary because some frames are annotated over
                            if frame_id == tid:
                                frame_indices.append(int(token_line[0])-1)
                                if token_line[2] not in frame_lemma:
                                    frame_lemma += "_" + (token_line[2])

                            #new frame
                            else:
                                if frame_indices:
                                    frame.sentence_index = id
                                    frame.pos = frame_pos
                                    frame.sentence = tokens
                                    frame.frame_name = frame_name
                                    frame.lemma = frame_lemma
                                    frame.indices = frame_indices
                                    frame.lu = convertLU(frame)
                                    frames.append(frame)

                                    frame = frame_instance.FrameInstance()
                                    frame_indices = []

                                frame_id = tid
                                if "le/lui" in token_line[2]:
                                    frame_lemma = token_line[1]
                                else:
                                    frame_lemma = token_line[2]
                                frame_indices.append(int(token_line[0])-1)
                                frame_name = frame_id.split('#')[1]
                                frame_pos = token_line[4]

            #last frame of the sentence
            if frame_indices:
                frame.sentence_index = id
                frame.pos = frame_pos
                frame.sentence = tokens
                frame.frame_name = frame_name
                frame.lemma = frame_lemma
                frame.indices = frame_indices
                frame.lu = convertLU(frame)
                frames.append(frame)

        return frames


'''
Convert annotated lemmas into the forms given in the lexicon

POS tags such as prepositions and conjunctions are annotated with "p" and "cs", but lexicon lists these LUs as "prep" and "conj".
This conversion is necessary to map the annotations to the lexicon.

Likewise, articles (de, ce, le) are inflected in the annotations for gender, plurality, and negation. Many MWE lemmas are mismatched
in the articles annotated and the forms in the lexicon.

Finally some MWE LUs are separated by "_" in annotations but not the lexicon
'''
def convertLU(frame):

    lu = frame.lemma + "." + frame.pos.lower()
    #pos mismatches
    if frame.pos.lower().startswith("adv"):
        lu = frame.lemma + "." + "adv"
    if frame.pos.lower().startswith("p"):
        lu = frame.lemma + "." + "prep"
    if frame.pos.lower().startswith("v") or frame.pos.lower().startswith("n"):
        lu = frame.lemma + "." + frame.pos[0].lower()
    if frame.pos.lower().startswith("cs"):
        lu = frame.lemma + "." + "conj"
    lu = lu.replace("_", " ")
    try:
        frames_for_lu[lu]
    except:
        try:
            temp_lu = lu
            #article mismatches
            if "de " in frame.lemma:
                temp_lu = lu.replace("de ", "d'")
            if "ce " in frame.lemma:
                temp_lu = lu.replace("ce ", "c'")
            if "le " in frame.lemma:
                temp_lu = lu.replace("le ", "l'")
            try:
                frames_for_lu[temp_lu]
                return temp_lu
            except:
                return lu.replace("_", " ")
        except:
            return lu.replace("_", " ")
    return lu.replace("_", " ")


def getFrames(data_dir):
    framenet = ReadFrenchFile(data_dir)
    return framenet.frames