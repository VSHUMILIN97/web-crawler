""" Crawler core w/ public interfaces """
from __future__ import annotations

import asyncio
import os

from typing import List

from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientError
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
            async with ClientSession() as session:
                response = await session.get(self.core_link, timeout=None)
                text = await response.text()
            return text
        except asyncio.TimeoutError:
            exit(
                '%s does not available ATM. Try another website'
                % self.core_link
            )
        finally:
            await session.close()

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

    @staticmethod
    async def _get_content(link: str) -> None:
        """ Task template """
        print(f'{link} parsing this site ATM')
        try:
            async with ClientSession() as session:
                response = await session.get(url=link, timeout=None)
                if response.status != 200:
                    print(f'{link} does not contain useful content')
                    return
                if not response._body:
                    data = await response.read()
                else:
                    data = response._body
        except ClientError:
            print(f'{link} not parsed')
            return
        finally:
            await session.close()
        async with open(
                os.path.join('parsed', link.replace('/', '_'))[:250],
                'wb'
        ) as writer:
            await writer.write(data)
