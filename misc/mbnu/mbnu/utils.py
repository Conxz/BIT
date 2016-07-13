# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from base import readsessid
import os


def mbnu_prep(sessid_file, src_dir, tgt_dir):
    
    sessid_list = readsessid(sessfile)
    
    if not os.path.exists(tgt_dir):
        os.mkdir(tgt_dir)

    for sessid in sessid_list:
        filename = 'smwc1' + sessid + '_anat.nii' 
        src_file = os.path.join(src_dir, filename)

        sess_dir = os.path.join(tgt_dir, sessid)
        if not os.path.exists(sess_dir):
            os.mkdir(sess_dir)
        tgt_file = os.path.join(sess_dir, filename)
    
        cp_str = 'ln -s ' + srcfile + ' ' + tgtfile
    
        print cp_str
        os.system(cp_str)

