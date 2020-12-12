'''
Dutch FrameNet is based on frames from FrameNet 1.7 inventory
'''

from data_parsers import frame_instance
from data_parsers import role_instance
import xml.etree.ElementTree as et
import glob


class ReadAllDutchFileFrames(object):

    def __init__(self, directory):
        filenames = self.readDirectory(directory)
        self.frames = self.combineFrameData(filenames)

    def readDirectory(self, directory):
        filenames = glob.glob(directory + "*.xml")
        return filenames

    def combineFrameData(self, filenames):
        all_frames = []

        for file in filenames:
            singleFrameFile = ReadSingleDutchAnnotationFile(file)
            frames = singleFrameFile.frames
            all_frames.extend(frames)
        return all_frames


class ReadSingleDutchAnnotationFile(object):
    '''
    This class reads a single Salsa XML file and returns the annotated data
    '''
    def __init__(self, filename):
        self.frames = self.readFrameAssignment(filename)

    @classmethod
    def readFrameAssignment(self, filename):

        frames = []

        tree = et.parse(filename, parser=et.XMLParser(encoding='utf-8'))
        file_root = tree.getroot()

        event_mentions = dict()
        entity_mentions = dict()
        sentences = dict()
        token_id_info = dict()
        t_id_dict = dict()

        #have to do this stupid thing because the dutch FN stores the same frame in different rows for ea FE
        m_id_frames = dict()
        m_id_targets = dict()
        source_ids = set()

        #all tokens and sentence text
        for child in file_root.findall('token'):
            token_id_info[child.get('t_id')] = child.attrib
            t_id_dict[child.get("t_id")] = child.text
            sentence_id = child.get('sentence')
            if sentence_id in sentences:
                sentence = sentences[sentence_id]
                sentence.append(child.text)
                sentences[sentence_id] = sentence
            if sentence_id not in sentences:
                sentence = []
                sentence.append(child.text)
                sentences[sentence_id] = sentence

        #event and entity mentions
        for child in file_root.findall('Markables'):
            for mention in child.findall("EVENT_MENTION"):
                tags = []
                for anchor in mention.findall("token_anchor"):
                    tags.append(anchor.get("t_id"))
                event_mentions[mention.get("m_id")] = tags
            for mention in child.findall("ENTITY_MENTION"):
                tags = []
                for anchor in mention.findall("t_id"):
                    tags.append(anchor.get("t_id"))
                entity_mentions[mention.get("m_id")] = tags

        #frame and roles
        for child in file_root.findall("Relations"):
            for participant in child.findall("HAS_PARTICIPANT"):
                frame = FrameInstance()
                frame.frame_name = participant.get("frame")
                source_id = ""
                for source in participant.findall("source"):
                    m_id = source.get("m_id")
                    source_id = m_id
                    source_ids.add(source_id)
                    if m_id in m_id_frames:
                        attrib = m_id_frames[m_id]
                        attrib.append(participant.attrib)
                        m_id_frames[m_id] = attrib
                    if m_id not in m_id_frames:
                        attrib = []
                        attrib.append(participant.attrib)
                        m_id_frames[m_id] = attrib

                for target in participant.findall("target"):
                    if source_id in m_id_targets:
                        targets = m_id_targets[source_id]
                        targets.append(target.get("m_id"))
                        m_id_targets[source_id] = targets
                    if source_id not in m_id_targets:
                        targets = []
                        targets.append(target.get("m_id"))
                        m_id_targets[source_id] = targets

        #frames
        for m_id in source_ids:
            frame = frame_instance.FrameInstance()
            frame_name = ""
            roles = []
            attributes = m_id_frames[m_id]
            frame_t_id = event_mentions[m_id][0]
            id_info = token_id_info[frame_t_id]
            role_targets = m_id_targets[m_id]
            for i in range(len(attributes)):
                role = role_instance.RoleInstance()
                attribute = attributes[i]
                frame_name = attribute.get("frame")
                role.role = attribute.get("frame_element")
                role.indices = role_targets[i]
                roles.append(role)
            frame.frame_name = frame_name
            frame.sentence = sentences.get(id_info.get("sentence"))
            frame.sentence_index = id_info.get("sentence")
            frame.roles = roles
            frame.indices = id_info.get("number")
            frames.append(frame)

        return frames



def getFrames(dir):
    framenet = ReadAllDutchFileFrames(dir)
    return framenet.frames