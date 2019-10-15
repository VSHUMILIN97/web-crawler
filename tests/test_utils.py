import os
import re

import pytest

from src.crawler.utils import get_dirty_links, LINK, tokenize_link


class TestRegExp(object):
    """ Test case for regexp-based utils """

    def setup_class(self):
        with open(os.path.join('data', 'short-example.html')) as reader:
            _content = reader.read()
        self.html_short = _content

    def test_grep_links(self):
        """ Checks: Possibility to get links iterator """
        short_iter = get_dirty_links(self.html_short)
        assert getattr(short_iter, '__iter__', False) is not False
        assert len(short_iter) == 2

    def test_grep_links_extract_first_one(self):
        """ Checks: Possibility to get first result through iterator """

    @pytest.mark.parametrize(
        'src, result', [
            (
                '<a href="https://www.yandex.ru/core">CLICK</a>',
                'https://www.yandex.ru/core'
            ),
            (
                '<a param again href="relative/part/of/the/link"></a>',
                'relative/part/of/the/link'
            )
        ]
    )
    def test_compiled_link_regexp(self, src, result):
        """ Checks: Possibility to use LINK regexp to get links """
        links = re.findall(LINK, src)
        assert links[0] == result


@pytest.mark.parametrize(
    'core, link, exp',
    [
        ('vk.com', 'https://www.yandex.ru/core', 'https://www.yandex.ru/core'),
        ('vk.com', '#', None),
        ('vk.com/', '/url/to/parse', 'vk.com/url/to/parse'),
        ('https://vk.com', '//url/to/parse', 'https://url/to/parse'),
        ('http://vk.com', '//url/to/parse', 'http://url/to/parse'),
        ('vk.com', '//url/to/parse', None)
    ]
)
def test_link_parser(core, link, exp):
    """ Checks: Possibility to extract correct link (i.e. non-absolutes) """
    actual = tokenize_link(link, core)
    assert actual == exp
