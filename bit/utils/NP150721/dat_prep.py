#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

"""For data prepare.

"""

import glob
import os
import numpy as np

srcdir = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/raw/'
subdirs = ['Ctrls', 'Exps']

tgtdir = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/data/'

subjfile = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/subj/sesslist'
sesslist = []
fsess = open(subjfile, 'w+')

for subdir_n in subdirs:
    print subdir_n, '...'
    subdir = os.path.join(srcdir, subdir_n)
    d_list = glob.glob(os.path.join(subdir, 'dti.nii.gz', '*.nii.gz'))
    d_list.sort()
    
    for dfile in d_list:
        sid = os.path.basename(dfile).split('.')[0]
        print sid
        sesslist.append(sid)
        fsess.write(sid+'\n')
    
        sessdir = os.path.join(tgtdir, sid)
        if not os.path.exists(sessdir):
            print 'mk ', sessdir
            os.mkdir(sessdir)
        
        # for dti.nii.gz
        tgtfile = os.path.join(sessdir, 'DTI.nii.gz')
        cmdstr = ' '.join(['ln --symbolic ', dfile, tgtfile])
        print cmdstr
        os.system(cmdstr)
        
        valfile = os.path.join(sessdir, 'DTI.bval')
        srcfile = os.path.join(subdir, 'bvals', sid+'.bval')
        cmdstr = ' '.join(['ln --symbolic ', srcfile, valfile])
        #print cmdstr
        os.system(cmdstr)

        vecfile = os.path.join(sessdir, 'DTI.bvec')
        srcfile = os.path.join(subdir, 'bvecs', sid+'.bvec')
        cmdstr = ' '.join(['ln --symbolic ', srcfile, vecfile])
        #print cmdstr
        os.system(cmdstr)

fsess.close()

print 'finished!'
