#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_parsers import frame_instance
from data_parsers import role_instance
import xml.etree.ElementTree as et
import glob
import re
import codecs
import os

class ReadAllFileFrames():

    def __init__(self, directory):
        filenames = self.readDirectory(directory)
        self.all_frames = self.combineFrameData(filenames)

    def readDirectory(self, directory):
        filenames = glob.glob(directory + "*.xml")
        return filenames

    def combineFrameData(self, filenames):
        all_frames = []

        for file in filenames:
            singleFrameFile = ReadSingleFileFrames(file)
            frames = singleFrameFile.frames
            all_frames.extend(frames)
        return all_frames


class ReadSingleFileFrames(object):
    '''
    This class reads a single parsed, xml-style FN file
    '''
    def __init__(self, filename):
        frames = self.readXMLSentences(filename)
        self.frames = frames

    @classmethod
    def readXMLSentences(self, filename):
        file_base_name = os.path.basename(filename)
        file = et.parse(filename)
        root = file.getroot()

        frames = []
        entire_sentences = []

        for child in root.iter('{http://framenet.icsi.berkeley.edu}sentence'):
            stext = ""
            tokens = []
            indices = []
            posTags = []
            sentenceFrames = []
            for t in child.iter('{http://framenet.icsi.berkeley.edu}text'):
                stext = t.text
            for sentence in child:
                for anno in sentence.iter('{http://framenet.icsi.berkeley.edu}annotationSet'):
                    frame = frame_instance.FrameInstance()
                    for layer in anno.iter('{http://framenet.icsi.berkeley.edu}layer'):

                        # PENN part of speech tags and tokenized text
                        if layer.get('name') == "PENN":
                            for label in layer.iter('{http://framenet.icsi.berkeley.edu}label'):
                                token = stext[int(label.get('start')): int(label.get('end'))+1]
                                tokens.append(token)
                                indices.append(label.get('start')+":"+label.get('end'))
                                posTags.append(label.get('name'))

                        #Frame Annotations
                        if layer.get('name') == "Target":
                            for label in layer.iter('{http://framenet.icsi.berkeley.edu}label'):
                                lu = anno.get('luName').replace(" ", "_")
                                frame.lu = lu.lower()
                                frame.sentence = tokens
                                frame_name = anno.get('frameName')
                                frame.frame_name = frame_name
                                frame.sentence_index = len(entire_sentences)
                                frame.file_index = file_base_name
                                ind = label.get('start') + ":" + label.get('end')
                                try:
                                    predicate_index = indices.index(ind)
                                    frame.indices = [predicate_index]
                                except:
                                    frame.indices = []
                                    for i, idx in enumerate(indices):
                                        if re.search(r'\b' + label.get('start') + ':', idx):
                                            frame.indices.append(i)
                                        if re.search(':' + label.get('end') + r'\b', idx):
                                            frame.indices.append(i)

                        #Frame elements
                        if layer.get('name') == "FE":
                            for label in layer.iter('{http://framenet.icsi.berkeley.edu}label'):
                                if label.get('itype') == "INI" or label.get('itype') == "CNI" or label.get('itype') == "DNI" or label.get('itype') == "INC":
                                    continue
                                role = role_instance.RoleInstance()
                                role.role = label.get('name')
                                ind = label.get('start') + ":" + label.get('end')
                                try:
                                    role_index = indices.index(ind)
                                    role.indices.append(role_index)
                                except:
                                    for i, idx in enumerate(indices):
                                        if re.search(r'\b' + label.get('start') + ':', idx):
                                            role.indices.append(i)
                                        if re.search(':' + label.get('end') + r'\b', idx):
                                            role.indices.append(i)
                                frame.roles.append(role)

                    #make sure frame is not empty
                    if frame.lu and frame.indices and not frame.frame_name == "Test35":
                        sentenceFrames.append(frame)

            #multiple frames for a single sentence
            frames.append(sentenceFrames)

        return frames


def getFrames(frame_dir):
    framenet = ReadAllFileFrames(frame_dir)
    return framenet.all_frames
