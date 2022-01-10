import unittest

from alectryon.core import *
from alectryon.transforms import *

class TestTransforms(unittest.TestCase):
    # transform_contents_to_tokens
    def test_transform_contents_to_tokens_empty(self):
        self.assertEqual([], transform_contents_to_tokens([]))

    def test_transform_contents_to_tokens(self):
        fragments = [
            Text(contents="First"),
            Text(contents=Contents(tokens=[FragmentToken(raw="Second"), FragmentToken(raw="Third")])),
            Text(contents=Contents(tokens=[])),
            Text(contents=FragmentContent.create("Third")),
            Sentence(contents="First", messages=[], goals=[]),
            Sentence(contents=Contents(tokens=[FragmentToken(raw="Second"), FragmentToken(raw="Third")]), messages=[], goals=[]),
            Sentence(contents=Contents(tokens=[]), messages=[], goals=[]),
            Sentence(contents=FragmentContent.create("Third"), messages=[], goals=[]),
        ]
        expected = [
            Text(contents=FragmentContent.create("First")),
            Text(contents=FragmentContent([FragmentToken(raw="Second"), FragmentToken(raw="Third")])),
            Text(contents=FragmentContent([])),
            Text(contents=FragmentContent.create("Third")),
            Sentence(contents=FragmentContent.create("First"), messages=[], goals=[]),
            Sentence(contents=FragmentContent([FragmentToken(raw="Second"), FragmentToken(raw="Third")]), messages=[], goals=[]),
            Sentence(contents=FragmentContent([]), messages=[], goals=[]),
            Sentence(contents=FragmentContent.create("Third"), messages=[], goals=[]),
        ]

        result = transform_contents_to_tokens(fragments)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
