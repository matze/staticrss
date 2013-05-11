import os
import logging
import yaml
from xml.etree import ElementTree


CONFIG_FILENAME = '_config.yml'


def import_ompl(filename):
    """Import *filename* as OMPL and write contents as _config.yml."""
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    config = {'feeds': []}

    def is_feed(node):
        return 'type' in node.attrib and node.attrib['type'] == 'rss'

    for outline in root.iter('outline'):
        if is_feed(outline):
            config['feeds'].append(outline.attrib['xmlUrl'])

    yaml.dump(config, open(CONFIG_FILENAME, 'w'), default_flow_style=False)


def read():
    """Read configuration dict from _config.yml."""

    config = {
        'feeds': [],
        'layouts': './_layouts',
        'source': '.',
        'destination': './_site'
    }

    if os.path.exists(CONFIG_FILENAME):
        with open(CONFIG_FILENAME, 'r') as stream:
            config.update(yaml.load(stream).items())
    else:
        msg = "{0} not found, site will be pretty much empty"
        logging.warn(msg.format(CONFIG_FILENAME))

    return config
