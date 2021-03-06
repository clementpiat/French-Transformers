import argparse
import json
import pandas as pd
import os
"""
pip install pyspellchecker
pip install spacy
python -m spacy download fr
python -m spacy download fr_core_news_md
pip install pandarallel
"""
from spellchecker import SpellChecker
import spacy
from pandarallel import pandarallel

from utils import get_dataset_path

nlp = spacy.load('fr')
pandarallel.initialize(progress_bar=True)

def main(dataset, distance):
    """
    Corrects a dataset with SpellChecker and creates a new one.

    Inputs: please refer bellow, to the argparse arguments.
    """

    spell = SpellChecker(language='fr',distance=distance)

    def transform_one_sentence(sentence):
        """
        Transforms a sentence as a string into another setence with the unknown words being corrected
        """
        words = list(map(str, nlp(sentence)))
        return ' '.join(list(map(spell.correction, words)))


    csv_path = get_dataset_path(dataset)
    df = pd.read_csv(csv_path)
    df.text = df.text.parallel_apply(transform_one_sentence)
    
    correction_dataset = f'_correction_{distance}.csv'.join(csv_path.split(".csv"))
    print(f"Saving the corrected dataset into {correction_dataset}...")
    df.to_csv(correction_dataset, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, default="french_tweets_short.csv", 
        help="dataset filename")
    parser.add_argument("-n", "--distance", type=int, default=2, 
        help="distance parameter for SpellChecker")

    args = parser.parse_args()
    print(f"\n> args:\n{json.dumps(vars(args), sort_keys=True, indent=4)}\n")
    main(args.dataset, args.distance)