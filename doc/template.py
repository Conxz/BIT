#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Docstrings for the modula.
usage: tbss_deproject-pre [-h] -sf sessid-file -g grotfile

prepare for tbss_deproject.

optional arguments:
  -h, --help       show this help message and exit
  -sf sessid-file  an input file containing subject id list.
  -g grotfile      grotfile.

"""

import argparse
from pynit.base import readsessid
from pynit.dti.preparation import pre_tbss_deproject

def testfunction(sesslist):
    """Docstrings for the function.
    
    Parameters:
    -----------    

    Contribution:
    -------------
        Author: kongxiangzheng@gmail.com
        Date: 2012.05.26
        Editors: [plz add own name after edit here]
    
    """
    
    for sess in sesslist:
        print sess


def main():
    parser = argparse.ArgumentParser(description = 'prepare for tbss_deproject.',
                                     prog = 'tbss_deproject-pre')
    parser.add_argument('-sf',
                        dest = 'sessfile',
                        required = True,
                        metavar = 'sessid-file',
                        help = 'an input file containing subject id list.')
    parser.add_argument('-g',
                        dest = 'grot',
                        required = True,
                        metavar = 'grotfile',
                        help = 'grotfile.')

    args = parser.parse_args()
    
    
    sesslist = readsessid(args.sessfile)
    testfunction(sesslist)


if __name__ == '__main__':
    main()
