import unittest
from emmet import Attribute, Element, expand_abbreviation, add_tabstops


class TestEmmetStringRepresentations(unittest.TestCase):
    def test_attribute_filters_empty_values(self):
        attr = Attribute("class", ["foo", "", "bar", " ", "  "])
        self.assertEqual('class="foo bar"', str(attr))

    def test_empty_element_has_placeholder(self):
        el = Element()
        el.name = "div"
        self.assertEqual("<div>{}</div>", str(el))

    def test_element_with_text_content(self):
        el = Element()
        el.name = "div"
        el.content = ["some text"]
        self.assertEqual("<div>some text</div>", str(el))

    def test_element_with_multiple_text_content(self):
        el = Element()
        el.name = "div"

        el.content = ["some text", "and some more"]
        self.assertEqual("<div>\n\tsome text\n\tand some more\n</div>", str(el))

        el.content = ["some text", "and some more", "third"]
        self.assertEqual(
            "<div>\n\tsome text\n\tand some more\n\tthird\n</div>", str(el)
        )

    def test_nested_elements(self):
        el = Element("div")
        el.content = [Element("i")]
        self.assertEqual("<div>\n\t<i>{}</i>\n</div>", str(el))

    def test_nested_elements_with_siblings(self):
        el = Element("div")
        el.content = [Element("em"), Element("strong")]
        self.assertEqual("<div>\n\t<em>{}</em>\n\t<strong>{}</strong>\n</div>", str(el))


class TestEmmetParser(unittest.TestCase):
    def test_tag(self):
        self.assertEqual("<p>$0</p>", expand_abbreviation("p"))

    def test_tag_with_class(self):
        self.assertEqual('<p class="foo">$0</p>', expand_abbreviation("p.foo"))

    def test_delimited_keywords(self):
        self.assertEqual("<my-tag>$0</my-tag>", expand_abbreviation("my-tag"))
        self.assertEqual(
            '<p class="text-center">$0</p>', expand_abbreviation("p.text-center")
        )
        self.assertEqual(
            '<p id="my-paragraph">$0</p>', expand_abbreviation("p#my-paragraph")
        )
        self.assertEqual(
            '<p id="myParagraph">$0</p>', expand_abbreviation("p#myParagraph")
        )
        self.assertEqual(
            '<p class="text-center sm:text-left sm:flex-grow">$0</p>',
            expand_abbreviation("p.text-center.sm:text-left.sm:flex-grow"),
        )

    def test_class(self):
        self.assertEqual('<div class="foo">$0</div>', expand_abbreviation(".foo"))

    def test_classes(self):
        self.assertEqual(
            '<div class="foo bar">$0</div>', expand_abbreviation(".foo.bar")
        )

    def test_id(self):
        self.assertEqual('<div id="foo">$0</div>', expand_abbreviation("#foo"))

    def test_ids(self):
        self.assertEqual('<div id="bar">$0</div>', expand_abbreviation("#foo#bar"))

    def test_tabstops(self):
        self.assertEqual("<div>$0</div>", add_tabstops("<div>{}</div>"))
        self.assertEqual(
            "<div>$1</div><div>$0</div>", add_tabstops("<div>{}</div><div>{}</div>")
        )
        self.assertEqual(
            "<div>$1</div><div>$2</div><div>$0</div>",
            add_tabstops("<div>{}</div><div>{}</div><div>{}</div>"),
        )

    def test_repeat(self):
        self.assertEqual("<div>$1</div>\n<div>$0</div>", expand_abbreviation("div*2"))
        self.assertEqual(
            '<div class="foo" id="bar">$1</div>\n<div class="foo" id="bar">$0</div>',
            expand_abbreviation(".foo#bar*2"),
        )


if __name__ == "__main__":
    unittest.main()
