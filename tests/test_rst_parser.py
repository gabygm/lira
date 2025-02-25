from pathlib import Path

from lira.parsers.rst import RSTParser

books_path = Path(__file__).parent / "data/books"


class TestRSTParser:
    def setup_method(self):
        file = books_path / "example/intro.rst"
        with file.open() as f:
            content = f.read()
        self.parser = RSTParser(
            content=content,
            source=file,
        )

    def test_parse_metadata(self):
        metadata = self.parser.parse_metadata()
        expected = {
            "tags": "comments",
            "level": "easy",
        }
        assert metadata == expected

    def test_parse_section(self):
        content = self.parser.parse_content()

        assert len(content) == 1

        section = content[0]
        assert section.tagname == "Section"
        assert section.options["title"] == "Comments"
        assert len(section.children) == 4

    def test_parse_paragraph(self):
        content = self.parser.parse_content()
        paragraph = content[0].children[0]

        assert paragraph.tagname == "Paragraph"
        assert len(paragraph.children) == 7

        assert paragraph.children[0].tagname == "Text"
        assert paragraph.children[0].text() == "Comments in "

        assert paragraph.children[1].tagname == "Emphasis"
        assert paragraph.children[1].text() == "Python"

        assert paragraph.children[2].tagname == "Text"
        assert paragraph.children[2].text() == " start with the hash character ("

        assert paragraph.children[3].tagname == "Literal"
        assert paragraph.children[3].text() == "#"

        assert paragraph.children[4].tagname == "Text"
        assert (
            paragraph.children[4].text()
            == "),\nand extend to the end of the line.\nA comment may appear at the "
        )

        assert paragraph.children[5].tagname == "Strong"
        assert (
            paragraph.children[5].text()
            == "start of the line or following whitespace or code"
        )

        assert paragraph.children[6].tagname == "Text"
        assert paragraph.children[6].text() == "."

    def test_parse_code_block(self):
        content = self.parser.parse_content()
        codeblock = content[0].children[1]

        assert codeblock.tagname == "CodeBlock"
        assert codeblock.options["language"] == "python"
        assert codeblock.content == [
            "# This is a comment",
            "spam = 1  # and this is another one!",
        ]

    def test_parse_test_block(self):
        content = self.parser.parse_content()
        testblock = content[0].children[2]

        assert testblock.tagname == "TestBlock"
        assert testblock.options["description"] == "Write a comment"
        assert testblock.options["help"] == ""
        assert testblock.options["validator"] == "lira.validators.CommentValidator"

        testblock = content[0].children[3]
        assert testblock.tagname == "TestBlock"
        assert testblock.options["description"] == "Write another comment"
        assert testblock.options["help"] == "Just write another comment :)"
        assert testblock.options["validator"] == "lira.validators.CommentValidator"
