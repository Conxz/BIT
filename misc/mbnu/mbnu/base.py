# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Base functions and classes for MBNU 

"""

def readsessid(fsessid):
    """Read session indetifier file.
    
    input:
    fsessid:  file for session indentifier
    output:
    sessid: a list for session indentifier
    
    """  
    fsessid = open(fsessid)
    sessid  = [line.strip() for line in fsessid]
    return sessid


