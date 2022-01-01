import unittest

from alectryon.core import *

class TestFragmentContent(unittest.TestCase):
    # __init__
    def test_init_empty(self):
        instance = FragmentContent.create()
        self.assertEqual(instance.tokens, [])

    def test_init_str(self):
        string = "test"
        instance = FragmentContent.create(string)
        self.assertEqual(instance.tokens, [Token(string, None, None)])

    def test_init_tokens(self):
        tokens = [Token("test", None, None)]
        instance = FragmentContent.create(tokens)
        self.assertEqual(instance.tokens, tokens)

    def test_init_contents(self):
        tokens = [Token("test", None, None)]
        instance = FragmentContent.create(tokens)
        second_instance = FragmentContent.create(Contents(tokens=tokens))
        self.assertEqual(second_instance, instance)

    # __eq__
    def test_eq_reflexive(self):
        instance = FragmentContent.create("Test")
        self.assertEqual(instance, instance)

    def test_eq_similar(self):
        tokens = [Token("1", None, None)]
        first_instance = FragmentContent.create(tokens)
        second_instance = FragmentContent.create(tokens)
        self.assertEqual(first_instance, second_instance)

    # __add__
    def test_add_self(self):
        first_token = [Token("1", None, None)]
        first_instance = FragmentContent.create(first_token)
        second_token = [Token("2", None, None)]
        second_instance = FragmentContent.create(second_token)
        sum_instance = first_instance + second_instance
        self.assertEqual(first_instance.tokens, first_token)
        self.assertEqual(second_instance.tokens, second_token)
        self.assertEqual(sum_instance.tokens, first_token + second_token)

    def test_add_token(self):
        tokens = [Token("First", None, None), Token("Test", None, None)]
        instance = FragmentContent.create(tokens[0])
        sum_instance = instance + tokens[1]
        self.assertEqual(sum_instance.tokens, tokens)

    # __str__
    def test_empty_str(self):
        instance = FragmentContent.create()
        self.assertEqual(str(instance), "")

    def test_str(self):
        tokens = [Token("First", None, None), Token("Test", None, None)]
        instance = FragmentContent.create(tokens)
        self.assertEqual(str(instance), tokens[0].raw + tokens[1].raw)

    # __len__
    def test_empty_len(self):
        instance = FragmentContent.create()
        self.assertEqual(len(instance), 0)

    def test_len(self):
        tokens = [Token("First", None, None), Token("Test", None, None)]
        instance = FragmentContent.create(tokens)
        self.assertEqual(len(instance), len(tokens[0].raw) + len(tokens[1].raw))

    # split_at_str
    def test_empty_split_at_str(self):
        instance = FragmentContent.create()
        splitted = instance.split_at_str(" ")[0]
        self.assertEqual(instance, splitted)
        self.assertEqual(len(splitted), 0)

    def test_empty_split_at_str(self):
        tokens = [Token("First|"), Token("Te|st"), Token("Last")]
        full_instance = FragmentContent.create(tokens)
        splitted = full_instance.split_at_str("|")
        expected = [FragmentContent.create("First"), FragmentContent.create("Te"), FragmentContent.create([Token("st"), Token("Last")])]
        self.assertEqual(expected, splitted)

    # split_at_pos
    def test_empty_split_at_pos(self):
        instance = FragmentContent.create()
        splitted = instance.split_at_pos(10)
        self.assertEqual(len(splitted), 2)
        self.assertEqual(splitted[0], instance)

    def test_split_at_negative_pos(self):
        string = "TestString"
        instance = FragmentContent.create(string)
        splitted = instance.split_at_pos(-6)
        self.assertEqual(len(splitted), 2)
        self.assertEqual(splitted[0], FragmentContent.create("Test"))
        self.assertEqual(splitted[1], FragmentContent.create("String"))

    def test_split_at_pos(self):
        string = "TestString"
        instance = FragmentContent.create(string)
        splitted = instance.split_at_pos(4)
        self.assertEqual(len(splitted), 2)
        self.assertEqual(splitted[0], FragmentContent.create("Test"))
        self.assertEqual(splitted[1], FragmentContent.create("String"))

    # to_contents
    def test_empty_to_contents(self):
        instance = FragmentContent([])
        self.assertEqual(instance.to_contents(), Contents([]))

    def test_to_contents(self):
        tokens = [Token("First", None, None), Token("Test", None, None)]
        instance = FragmentContent(tokens)
        self.assertEqual(instance.to_contents(), Contents(tokens))

    # endswith
    def test_empty_endswith(self):
        instance = FragmentContent([])
        self.assertFalse(instance.endswith("Test"))

    def test_endswith(self):
        instance = FragmentContent([Token("Endsw"), Token("ith")])
        self.assertTrue(instance.endswith("with"))

    # re_sub
    def test_re_sub_empty(self):
        instance = FragmentContent([])
        self.assertEqual(instance.re_sub(re.compile("<>")), instance)

    def test_re_sub(self):
        instance = FragmentContent([Token("En<>ds"), Token("wi<>th")])
        expected = FragmentContent([Token("En"), Token("ds"), Token("wi"), Token("th")])
        self.assertEqual(expected, instance.re_sub(re.compile("<>")))

    def test_re_sub_inter_token(self):
        instance = FragmentContent([Token("Ends<"), Token(">with")])
        expected = FragmentContent([Token("Ends"), Token("with")])
        self.assertEqual(instance.re_sub(re.compile("<>")), expected)

    def test_re_sub_token(self):
        sub_token = [Token("SUB")]
        instance = FragmentContent([Token("En<>ds"), Token("wi<>th")])
        expected = FragmentContent([Token("En"), Token("SUB"), Token("ds"), Token("wi"), Token("SUB"), Token("th")])
        self.assertEqual(expected, instance.re_sub(re.compile("<>"), sub_token))

    # re_match_groups
    def test_re_match_groups_empty(self):
        instance = FragmentContent([])
        first, second, third = instance.re_match_groups(re.compile("<>"))
        self.assertEqual(first, instance)
        self.assertEqual(second, FragmentContent([]))
        self.assertEqual(third, FragmentContent([]))

    def test_re_match_groups_no_match(self):
        instance = FragmentContent.create("Some test text")
        first, second, third = instance.re_match_groups((re.compile("<>")))
        self.assertEqual(first, instance)
        self.assertEqual(second, FragmentContent([]))
        self.assertEqual(third, FragmentContent([]))

    def test_re_match_groups_single_match(self):
        instance = FragmentContent.create("<>ds")
        first, second, third = instance.re_match_groups((re.compile("<>")))
        self.assertEqual(first, FragmentContent([Token("")]))
        self.assertEqual(second, FragmentContent([Token("<>")]))
        self.assertEqual(third, FragmentContent([Token("ds")]))

    def test_re_match_groups_inter_token_match(self):
        instance = FragmentContent([Token("<"), Token(">d"), Token("s")])
        first, second, third = instance.re_match_groups((re.compile("<>")))
        self.assertEqual(first, FragmentContent([Token("")]))
        self.assertEqual(second, FragmentContent([Token("<"), Token(">")]))
        self.assertEqual(third, FragmentContent([Token("d"), Token("s")]))

if __name__ == '__main__':
    unittest.main()
