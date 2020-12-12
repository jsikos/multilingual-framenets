# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 21:18:00 2016
Iterates over frame files, loads dictionaries containing the frame's lus and the frames for ea. unique lu

Input: asfalda_lexicon_from_annotations.bylemma.xml file

@author: sikos
"""
import xml.etree.cElementTree as et
import codecs

frames = []
frames_for_lu = dict()
lus_in_frame = dict()

class FrenchFrameNet(object):

    def __init__(self, file):
        self.name = "french"
        fillFrenchDictionaries(file)
        self._frames = frames
        self._lus_in_frame = lus_in_frame
        self._frames_for_lu = frames_for_lu

    @property
    def frames(self):
        return self._frames

    @property
    def lus_in_frame(self):
        return self._lus_in_frame

    @property
    def frames_for_lu(self):
        return self._frames_for_lu

    @frames_for_lu.setter
    def frames_for_lu(self, value):
        self._frames_for_lu = frames_for_lu

    @property
    def frame_relations(self):
        return self._frame_relation_map


# Iterate over the file for filling the frame dictionaries
def fillFrenchDictionaries(file):
    tree = et.parse(file, parser=et.XMLParser(encoding='UTF-8'))
    file_root = tree.getroot()
    buildFrames(file_root)
    buildFrameLexicalUnitsDict(file_root)
    buildFramesForLexicalUnitsDict(file_root)


def buildFrames(file_root):
    for child in file_root.findall('LEMMACAT'):
        for lemma in child.findall('LU'):
            frame_name = lemma.get('frame')
            if frame_name not in frames:
                #frame_name = frame_name.replace("FR_", "")
                frames.append(frame_name)

# Build dictionary for all LUs in a frame
def buildFrameLexicalUnitsDict(file_root):
    for child in file_root.findall('LEMMACAT'):
        for lemma in child.findall('LU'):
            frame_name = lemma.get('frame')
            #frame_name = frame_name.replace("FR_", "")
            lu_name = lemma.get('name')
            if frame_name in lus_in_frame:
                lus = lus_in_frame[frame_name]
                lus.append(lu_name)
                lus_in_frame[frame_name] = lus
            else:
                lus = []
                lus.append(lu_name)
                lus_in_frame[frame_name] = lus


# Build dictionary for all frames for a LU
def buildFramesForLexicalUnitsDict(file_root):
    for child in file_root.findall('LEMMACAT'):
        for lemma in child.findall('LU'):
            frame_name = lemma.get('frame')
            #frame_name = frame_name.replace("FR_", "")
            lu_name = lemma.get('name')
            if lu_name in frames_for_lu:
                frames = frames_for_lu[lu_name]
                frames.append(frame_name)
                frames_for_lu[lu_name] = frames
            else:
                frames = []
                frames.append(frame_name)
                frames_for_lu[lu_name] = frames


# Frame index is the arbitrary index number assigned to each frame
def getFrameIndex(frames, frame):
    for index, item in enumerate(frames):
        frame_name = item.decode('utf-8').strip()
        if frame.lower() == frame_name.lower():
            return index