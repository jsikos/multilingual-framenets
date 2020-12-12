
from lexicons import english_fn_database, german_fn_database, french_fn_database

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()

parser.add_argument("--lexicon_dir", default=None, type=str, required=True,
                    help="the directory with FrameNet lexicon.")

args = parser.parse_args()

def get_lexicon(language, lexicon_dir):
    if language == "english":
        lexicon = english_fn_database.EnglishFrameNet(lexicon_dir)
    if language == "german":
        lexicon = german_fn_database.GermanFrameNet(lexicon_dir)
    if language == "french":
        lexicon = french_fn_database.FrenchFrameNet(lexicon_dir)
    return lexicon

if __name__ == '__main__':
    lexicon = get_lexicon(args.language, args.lexicon_dir)