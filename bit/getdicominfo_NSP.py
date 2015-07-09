#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Get info from dicom

"""
import os
import glob
import dicom

dirstr = '/nfs/s1/nspdicom/2008subj/stru/*_LIUJ_*'
#dirstr = '/nfs/s1/nspdicom/2006subj/stru/*_DONGQ_*'

dirlist = glob.glob(dirstr)
dirlist.sort()
for dicomdir in dirlist:
    dicomfilestr = '/*.1.1.*'
    dicomfile = glob.glob(dicomdir+dicomfilestr)

    dicominfo = dicom.read_file(dicomfile[0])
    print os.path.basename(dicomdir), 'T'+dicominfo.AcquisitionTime[:6]

