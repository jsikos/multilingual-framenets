#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

def splitFile(split_file, frames, output_file):

    train_ids = []
    test_ids = []
    dev_ids = []

    with open(split_file, 'r') as splitfile:
        lines = splitfile.readlines()
        for line in lines:
            split = line.strip().split(" ")
            if ("Training:" in split[0]):
                train_ids = split[1:]
            if("Development:" in split[0]):
                dev_ids = split[1:]
            if("Test:" in split[0]):
                test_ids = split[1:]

    train_frames = []
    test_frames = []
    dev_frames = []

    for frame in frames:
        if frame.sentence_index:
            if frame.sentence_index in train_ids:
                train_frames.append(frame)
            if frame.sentence_index in dev_ids:
                dev_frames.append(frame)
            if frame.sentence_index in test_ids:
                test_frames.append(frame)
        if frame.file_index:
            if frame.file_index in train_ids:
                train_frames.append(frame)
            if frame.file_index in dev_ids:
                dev_frames.append(frame)
            if frame.file_index in test_ids:
                test_frames.append(frame)

    trainfile = codecs.open(output_file+"/train.tsv", "w", "utf-8")
    printFile(train_frames, trainfile)
    trainfile.close()

    testfile = codecs.open(output_file+"/test.tsv", "w", "utf-8")
    printFile(test_frames, testfile)
    testfile.close()

    devfile = codecs.open(output_file+"/dev.tsv", "w", "utf-8")
    printFile(dev_frames, devfile)
    devfile.close()


def printFile(frames, filename):

    for i, frame in enumerate(frames):
        frame_labels = ["0"]*len(frame.sentence)
        frame_predicates = frame.sentence[:]

        try:
            for index in frame.indices:
                frame_labels[int(index)] = frame.frame_name
                frame_predicates[int(index)] = frame.lu
        except:
            frame_labels[frame.indices] = frame.frame_name
            frame_predicates[frame.indices] = frame.lu

        sentence = " ".join(frame.sentence)
        predicates = " ".join(frame_predicates)

        filename.write(str(i))
        filename.write("\t")
        filename.write(sentence)
        filename.write("\t")
        filename.write(" ".join(frame_labels))
        filename.write("\t")
        filename.write(predicates)
        filename.write("\n")
