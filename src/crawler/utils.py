""" TODO: """
import re

from functools import partial
from typing import Optional

LINK = re.compile(r'href=[\'"]?([^\'" >]+)')
SCHEMA = re.compile(r'(http[s]?|ftp):')

# Get links from content
get_dirty_links = partial(re.findall, LINK)


def process_link(link: str, core_link: str) -> Optional[str]:
    """ Clear links array """
    if link.startswith('#'):
        return None
    if link.startswith('/'):
        if core_link.endswith('/'):
            return "".join([core_link, link[1:]])
        return "".join([core_link, link])
    if link.startswith('//'):
        schema = re.search(SCHEMA, core_link)
        return ":".join([schema.group(1), link]) if schema else None
