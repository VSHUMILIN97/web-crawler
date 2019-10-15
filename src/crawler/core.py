""" Crawler core w/ public interfaces """
from __future__ import annotations

import asyncio
import os

from typing import List

from aiohttp.client import ClientSession
from aiofiles import open

from src.crawler.utils import get_dirty_links, tokenize_link


def setup(argv: List[str]) -> Crawler:
    """ Define public module entry-point """
    return Crawler(argv[1])


class Crawler(object):

    def __init__(self, core_link: str) -> None:
        """ Simple HTML crawler (specify -v for verbosity) """
        self.core_link = core_link

    async def _grep_links(self) -> str:
        """ Simple task for getting result """
        try:
            async with ClientSession().get(
                    self.core_link, timeout=None
            ) as session:
                resp = await session.text()
            return resp
        except asyncio.TimeoutError:
            exit(
                '%s does not available ATM. Try another website'
                % self.core_link
            )

    async def run(self):
        """ Crawler entry point for parsing web-page """
        content = await self._grep_links()
        links = [
            link for link in [
                tokenize_link(link, self.core_link)
                for link in get_dirty_links(string=content)
            ]
            if link is not None
        ]
        tasks = [self._get_content(link) for link in links]
        print('Links to parse - %s ' % len(tasks))
        await asyncio.gather(*tasks)

    async def _get_content(self, link: str) -> None:
        """ Task template """
        async with ClientSession().get(url=link, timeout=None) as session:
            if not session._body:
                await session.read()
        data = session._body
        async with open(
                os.path.join('parsed', link.replace('/', '_'))[:250],
                'wb'
        ) as writer:
            await writer.write(data)
