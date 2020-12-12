#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_parsers import frame_instance
import xml.etree.ElementTree as et
import glob

class ReadAllFileFrames(object):

    def __init__(self, directory):
        filenames = self.readDirectory(directory)
        self.all_frames = self.combineFrameData(filenames)

    def readDirectory(self, directory):
        filenames = glob.glob(directory + "*.xml")
        return filenames

    def combineFrameData(self, filenames):
        all_frames = []

        for file in filenames:
            singleFrameFile = ReadSingleSalsaAnnotationFile(file)
            frames = singleFrameFile.frames
            all_frames.extend(frames)
        return all_frames


class ReadSingleSalsaAnnotationFile(object):
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

        for child in file_root.findall('body'):
            for sent in child.findall('s'):
                id = (sent.get("id"))
                graph = sent.find('graph')
                sentence = []
                pos_tags = []
                lemmas = []

                #create dictionary of non-terminals to iterate over
                nonterminals = graph.find('nonterminals')
                nonterminal_dict = dict()
                for nonterminal in nonterminals.iter('nt'):
                    nt_id = nonterminal.get('id').split("_")[1]
                    for edge in nonterminal.iter('edge'):
                        edgeid = edge.get('idref').split("_")[1]
                        if nt_id in nonterminal_dict:
                            nt_list = nonterminal_dict[nt_id]
                            nt_list.append(edgeid)
                            nonterminal_dict[nt_id] = nt_list
                        else:
                            nt_list = []
                            nt_list.append(edgeid)
                            nonterminal_dict[nt_id] = nt_list

                #terminals - get all the words, pos tags, lemmas
                terminals = graph.find("terminals")
                for terminal in terminals.iter("t"):
                    word = terminal.get("word")
                    sentence.append(word)
                    lemma = terminal.get("lemma")
                    lemma = self.replaceUmlauts(lemma)
                    lemmas.append(lemma)
                    pos_tag = terminal.get("pos")
                    pos_tags.append(pos_tag)

                #frames
                sem = sent.find('sem')
                frame_annotation = sem.find('frames')
                if not frame_annotation:
                    continue

                for f_annotation in frame_annotation.iter('frame'):
                    frame = frame_instance.FrameInstance()
                    frame.frame_name = f_annotation.get("name")
                    frame.sentence = sentence
                    frame.sentence_index = id
                    indices = []
                    for target in f_annotation.iter("target"):
                        frame.lemma = target.get("lemma")
                        for index in target.iter("fenode"):

                            #fixing some inconsistencies in annotations
                            idref = index.get("idref").split("_")
                            ref = 0
                            for idx, r in enumerate(idref):
                                if r.startswith("s") and idx != len(idref)-1:
                                    ref = int(idref[idx+1])
                            self.getTokenIndices(nonterminal_dict, indices, ref)
                    frame.indices = indices

                    #retrieve POS and lemmas for the MWE predicates - if single predicate, take first
                    temp_pos = [pos_tags[index] for index in indices]
                    temp_lemmas = [lemmas[index] for index in indices]
                    if len(temp_pos) > 1 and len(temp_lemmas) > 1:
                        fixed_pos_tags, fixed_lemmas = self.adjustMWE(temp_pos, temp_lemmas)
                        frame.pos = fixed_pos_tags
                        frame.lemma = fixed_lemmas[0]
                        frame.lu = fixed_lemmas[0].lower() + "." + fixed_pos_tags[0][0].lower()
                    else:
                        frame.pos = pos_tags[indices[0]]
                        frame.lemma = lemmas[indices[0]]
                        frame.lu = frame.lemma.lower() + "." + frame.pos[0].lower()
                    frames.append(frame)
            return frames


    @classmethod
    def getTokenIndices(self, nonterminal_dict, indices, ref):
        #dealing with MWE predicates (esp. particles)
        if str(ref).startswith("5") and len(str(ref)) > 2:
            terms = nonterminal_dict[str(ref)]
            for term in terms:
                if len(term) > 2 and term.startswith("5"):
                    self.getTokenIndices(nonterminal_dict, indices, int(term))
                else:
                    indices.append(int(term)-1)
        else:
            indices.append(ref-1)

    '''Unfortunately, the Salsa lexicon doesn't have umlauts in LUs but some of the annotations do - 
    convert for looking up instances in the dictionary'''
    @classmethod
    def replaceUmlauts(self, lemma):
        lemma = lemma.replace(u'ü', 'ue')
        lemma = lemma.replace(u'ä', 'ae')
        lemma = lemma.replace(u'ß', 'ss')
        lemma = lemma.replace(u'ö', 'oe')
        return lemma

    '''distinguish particles - separable vs non-separable'''
    @classmethod
    def adjustMWE(self, pos_tags, lemmas):

        modified_lemmas = lemmas
        modified_pos = pos_tags

        #only take predicates with particles (not predicates that are phrases)
        if len(pos_tags) < 3 and len(lemmas) < 3:
            for i, pos in enumerate(pos_tags):

                #PTKZU/APPR/APPRART... are thrown away
                if pos == "PTKZU":
                    del modified_pos[i]
                    del modified_lemmas[i]

                #PTKVZ/VV should be normalized to PTKVZ_VV
                if pos == "PTKVZ":
                    if i == 0 or i < len(lemmas)-1:
                        lemma1 = self.replaceUmlauts(lemmas[i])
                        lemma2 = self.replaceUmlauts(lemmas[i+1])

                        modified_lemmas = [lemma1 + lemma2]
                        del modified_pos[i]
                        continue
                    else:
                        lemma1 = self.replaceUmlauts(lemmas[i-1])
                        lemma2 = self.replaceUmlauts(lemmas[i])
                        modified_lemmas = [lemma2 + lemma1]
                        del modified_pos[i]
                        continue

        return modified_pos, modified_lemmas


def getFrames(frame_dir):
    framenet = ReadAllFileFrames(frame_dir)
    return framenet.all_frames
