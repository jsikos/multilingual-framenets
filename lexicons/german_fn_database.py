# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 21:18:00 2016
Iterates over frame files, loads dictionaries containing the frame's lus and the frames for ea. unique lu

@author: sikos
"""
import xml.etree.cElementTree as et

frames = []
frames_for_lu = dict()
lus_in_frame = dict()

class GermanFrameNet(object):

    def __init__(self, file):
        self.name = "salsa"
        fillSalsaDictionaries(file)
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
def fillSalsaDictionaries(file):
    tree = et.parse(file, parser=et.XMLParser(encoding='UTF-8'))
    file_root = tree.getroot()
    buildFrames(file_root)
    buildFrameLexicalUnitsDict(file_root)
    buildFramesForLexicalUnitsDict(file_root)


def buildFrames(file_root):
    for child in file_root.findall('frame'):
        frame_name = child.get('name')
        frames.append(frame_name)


# Build dictionary for all LUs in a frame
def buildFrameLexicalUnitsDict(file_root):
    for child in file_root.findall('frame'):
        frame_name = child.get('name')
        for lexeme in child.iter('lexunits'):
            for lexunit in lexeme.findall('lexunit'):
                lexeme_name = lexunit.get('name').lower()
                if frame_name in lus_in_frame:
                    lus = lus_in_frame[frame_name]
                    lus.append(lexeme_name)
                    lus_in_frame[frame_name] = lus
                else:
                    lus = []
                    lus.append(lexeme_name)
                    lus_in_frame[frame_name] = lus


# Build dictionary for all frames for a LU
def buildFramesForLexicalUnitsDict(file_root):
    for child in file_root.findall('frame'):
        frame_name = child.get('name')
        for lexeme in child.iter('lexunits'):
            for lexunit in lexeme.findall('lexunit'):
                lexeme_name = lexunit.get('name').lower()
                if lexeme_name in frames_for_lu:
                    frames = frames_for_lu[lexeme_name]
                    frames.append(frame_name)
                    frames_for_lu[lexeme_name] = frames
                else:
                    frames = []
                    frames.append(frame_name)
                    frames_for_lu[lexeme_name] = frames


# Frame index is the arbitrary index number assigned to each frame
def getFrameIndex(frames, frame):
    for index, item in enumerate(frames):
        frame_name = item.decode('utf-8').strip()
        if frame.lower() == frame_name.lower():
            return index
