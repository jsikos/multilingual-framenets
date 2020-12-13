#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import argparse
import os

from data_parsers import parse_latvian, parse_german, parse_english, parse_dutch, parse_french, parse_swedish, \
    annotation_output

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()

parser.add_argument("--data_dir",
                    default=None,
                    type=str,
                    required=True,
                    help="The input data dir. Should contain the original FrameNet annotations (or other data files) for the task.")

parser.add_argument("--output_dir", default=None, type=str, required=False,
                    help="the output data dir.")

parser.add_argument("--split_file", default=None, type=str, required=False,
                    help="the dir with split (train/test/dev) info")

parser.add_argument("--language", default=None, type=str, required=True,
                    help="language of the FrameNet to parse")
args = parser.parse_args()


def get_parser(language, data_dir):
    frames = []
    sentences = []

    if language == "english":
        frames = parse_english.getFrames(data_dir)
        all_frames = []
        for frame in frames:
            for f in frame:
                all_frames.append(f)

        if args.split_file:
            annotation_output.splitFile(args.split_file, all_frames, args.output_dir)

    if language == "latvian":
        frames = parse_latvian.getFrames(data_dir)

    if language == "swedish":
        frames = parse_swedish.getFrames(data_dir)

    if language == "german":
        frames = parse_german.getFrames(data_dir)
        if args.split_file:
            annotation_output.splitFile(args.split_file, frames, args.output_dir)

    if language == "french":
        frames = parse_french.getFrames(data_dir)
        if args.split_file:
            annotation_output.splitFile(args.split_file, frames, args.output_dir)

    if language == "dutch":
        frames, sentences = parse_dutch.getFrames(data_dir)
    return frames, sentences


if __name__ == '__main__':
    if not args.output_dir:
        args.output_dir = os.getcwd()
    frames, sentences = get_parser(args.language, args.data_dir)
    if args.output_dir and not args.split_file:
        print("Please specify a file with the train/test/dev splits")