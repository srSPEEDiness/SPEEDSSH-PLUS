import argparse
import logging

logger = logging.getLogger(__name__)

__version__ = '1.3.0'
__author__ = 'Glemison C. Dutra'
__email__ = 'glemyson20@gmail.com'

__description__ = (
    'DTChecker - CHECKUSER | '
    'BY ' + __author__ + ' <' + __email__ + '> | '
    'VERSION: ' + __version__
)

args = argparse.ArgumentParser(description=__description__)
args.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s ' + __version__,
)
