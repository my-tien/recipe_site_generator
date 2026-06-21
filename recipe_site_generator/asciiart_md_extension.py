"""
This extension adds Fenced Code Blocks to Python-Markdown.

See the [documentation](https://Python-Markdown.github.io/extensions/fenced_code_blocks)
for details.
"""

from __future__ import annotations

from textwrap import dedent
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markdown import Markdown


class ASCIIArtExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(ASCIIArtPreprocessor(md), 'ascii_art', 25)


class ASCIIArtPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile((r"```.*\n(?P<asciiart>([^`]+\n)*)```"))

    def __init__(self, md: Markdown):
        super().__init__(md)

    def run(self, lines: list[str]) -> list[str]:
        """ Match and store Fenced Code Blocks in the `HtmlStash`. """
        text = "\n".join(lines)
        index = 0
        while True:
            m = self.FENCED_BLOCK_RE.search(text, index)
            if m:
                asciiart = self._escape(m.group('asciiart'))
                asciiart = f'<pre>{asciiart}</pre>'

                placeholder = self.md.htmlStash.store(asciiart)
                text = f'{text[:m.start()]}\n{placeholder}\n{text[m.end():]}'
                # Continue from after the replaced text in the next iteration.
                index = m.start() + 1 + len(placeholder)
            else:
                break
        return text.split("\n")

    def _escape(self, txt: str) -> str:
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


def makeExtension(**kwargs):  # pragma: no cover
    return ASCIIArtExtension(**kwargs)
