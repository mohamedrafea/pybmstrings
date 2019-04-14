import re
from unittest import TestCase
from pybmstrings import stringmatcher
from pycommonutil import string_util
import sys
class TableObjectTest(TestCase):
    def test_1_MatchIndices(self):
        l = [True, False, True]
        #print(l)
        mi = stringmatcher.listToMatchingIndices(l)
        self.assertEqual(mi,[0,2])

    def test_2_WordScore(self):
        wordList = string_util.loadList("countries.txt",True)
        bm = stringmatcher.suggestions(wordList,"great bretain")
        self.assertTrue(set(bm).__contains__('great britain'))

    def test_3_Score(self):
        wordList = string_util.loadList("countries.txt", True)
        bm = stringmatcher.suggestions(wordList, "bretain")
        self.assertTrue(set(bm).__contains__('great britain'))
    def test_4_Score(self):
        wordList = string_util.loadList("countries.txt", True)
        bm = stringmatcher.suggestions(wordList, "france")
        self.assertTrue(set(bm).__contains__('france'))


    def test_5_Score(self):
        self.assertEqual(stringmatcher.score("8 EEEE US", "8 EEEE US"),1)
    def test_6_Score(self):
        wordList = string_util.loadList("countries.txt", True)
        bm = stringmatcher.suggestions(wordList, "unitedstates")
        #print('bm6: ',bm)
        self.assertTrue(set(bm).__contains__('united states of america'))


    def test_7_Score(self):
        #print('enc:',sys.stdout.encoding)
        wordList = string_util.loadList("countries.txt", True)
        #print('wordList:',wordList)
        bm = stringmatcher.suggestions(wordList, "مصر")
        #print('bm:',bm)
        self.assertTrue(set(bm).__contains__('جمهورية مصر العربية'))

    """
    def test_8_Score(self):
        print('ar test: ',stringmatcher.suggestions(['جمهورية مصر العربية','xyz'],'مصر'),True)
        #print('ar test: ', stringmatcher.score('مصر', 'جمهورية مصر العربية'), True)
    
    def test_7_Dynamic(self):
        wordList = loadCountriesList()
        try:
            while True:
                word = str(input('>'))
                possibilities = stringmatcher.suggestions(wordList, word.lower())
                print(possibilities)
        except (EOFError, KeyboardInterrupt):
            exit(0)
    """