from data_parsers import frame_instance
from data_parsers import role_instance
import glob

class ReadLatvianFileFrames(object):

    def __init__(self, directory):
        filenames = self.readDirectory(directory)
        self.all_frames = self.combineFrameData(filenames)

    def readDirectory(self, directory):
        filenames = glob.glob(directory + "*.conll2009")
        return filenames

    def combineFrameData(self, filenames):
        all_frames = []

        for filename in filenames:
            singleFrameFile = self.ReadSingleFileLatvianFrames(filename)
            frames = singleFrameFile.frames
            all_frames.extend(frames)
        return all_frames

    class ReadSingleFileLatvianFrames(object):

        def __init__(self, filename):
            self.frames = self.singleFile(filename)

        def singleFile(self, file):

            frames = []
            with open(file, 'r') as filename:
                lines = filename.readlines()
                count = 0
                sentence = []
                frame = frame_instance.FrameInstance()
                roles = []

                for i, line in enumerate(lines):
                    if not line.strip():
                        frame.roles = roles
                        frame.sentence = sentence
                        frames.append(frame)
                        frame = frame_instance.FrameInstance()
                        roles = []
                        continue
                    if line.startswith("# sent_id"):
                        frame.sentence_index = line.split("=")[1].strip()
                        continue
                    if line.startswith("# text"):
                        continue

                    token = line.strip().split("\t")
                    sentence.append(token[1])

                    #token[9] indicates if it is the frame or not
                    if token[9] != "_":
                        frame.lemma = token[2]
                        frame.frame_name = token[10]
                        frame.pos = token[3]
                        frame.indices = int(token[0])-1

                    #token[11] indicates if it is a role or not
                    if token[11] != "_":
                        role = role_instance.RoleInstance()
                        role.pos = token[3]
                        role.indices = int(token[0])-1
                        role.lemma = token[2]
                        role.role = token[11]
                        roles.append(role)
                frames.append(frame)
            return frames


def getFrames(data_dir):
    framenet = ReadLatvianFileFrames(data_dir)
    return framenet.all_frames