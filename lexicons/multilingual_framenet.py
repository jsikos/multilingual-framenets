from lexicons.english_fn_database import EnglishFrameNet
from lexicons.german_fn_database import GermanFrameNet
from lexicons.french_fn_database import FrenchFrameNet

'''
Combine lexicons from specified FrameNets

Input: list with languages (ex: ["english", "german"] and a 
list of the directory locations for the FN files
'''

class CombineFrameNets():

    def __init__(self, languages_to_concatenate, lexicons):
        framenets = []
        for language in languages_to_concatenate:
            lexicon = lexicons[language]
            framenets.append(self.retrieveFrameNetDatabase(language, lexicon))
        self.framenets = framenets
        self.lus_in_frame = self.combineFrameNets()
        self.intersection = self.getIntersectionFrames()
        self.frames = self.getFrames()

    def retrieveFrameNetDatabase(self, language, lexicon_dir):
        if language == "english":
            english = EnglishFrameNet(lexicon_dir)
            return english
        if language == "german":
            german = GermanFrameNet(lexicon_dir)
            return german
        if language == "french":
            french = FrenchFrameNet(lexicon_dir)
            return french

    'combine the framenet resources defined above'
    def combineFrameNets(self):
        combine_lus_in_frame = dict()
        for framenet in self.framenets:
            combine_lus_in_frame.update(framenet.frames_for_lu)
        return combine_lus_in_frame

    def getIntersectionFrames(self):
        intersection = set()

        [intersection.add(frame.split(".")[0]) for frame in self.framenets[0].frames]
        for i in range(len(self.framenets)):
            if i==0:
                continue
            frame_set = [frame.split(".")[0] for frame in self.framenets[i].frames]
            intersection = intersection.intersection(frame_set)

        intersection = list(intersection)
        return intersection

    def getFrames(self):
        frames = []
        for framenet in self.framenets:
            for frame in framenet.frames:
                if frame in frames:
                    continue
                frames.append(frame)
        return frames

def lookupLU(lu, lus_in_frame):
    for frame, lus in lus_in_frame.items():
        if lu in lus:
            print(frame)
