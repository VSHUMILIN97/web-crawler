from sys import argv

import asyncio
import timeit
import os

import uvloop

from src.crawler.core import setup


def main() -> None:
    """ Use uvloop instead of default python asyncio implementation """
    uvloop.install()  # Run everything on uvloop
    asyncio.run(
        setup(argv).run()
    )


if __name__ == '__main__':
    if not os.path.exists('parsed'):
        os.mkdir('parsed')
    with open('parsed/timed.txt', 'a') as writer:
        writer.write(
            str(timeit.timeit('main()', 'from __main__ import main', number=1))
        )
        writer.write('\n')
