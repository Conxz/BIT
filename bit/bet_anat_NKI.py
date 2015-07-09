#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

"""Bet T1 data.

"""

import os
import glob
#import subprocess

logdir = '/nfs/p1/public_dataset/datasets/NKI_Sample/log'
if not os.path.exists(logdir):
    os.mkdir(logdir)

datdir = '/nfs/p1/public_dataset/datasets/NKI_Sample/data'
os.chdir(datdir)
sidlist = glob.glob('*')

scans = ['session_1', 'session_2']
sesslist = ['MPRAGE_1', 'MPRAGEshorter_1']
mri = ['defaced_MPRAGE.nii.gz', 'defaced_MPRAGEshorter.nii.gz']

anat_out = 'anat_brain.nii.gz'

run = 1

for scan in scans:
    print scan
    for sid in sidlist:
        print sid
        for i, sess in enumerate(sesslist):
            scandir = os.path.join(sid, scan, sess)
            if os.path.exists(scandir):
                mri_file = os.path.join(scandir, mri[i])
                anat_brain = os.path.join(scandir, anat_out)
                cmd_bet = 'bet ' + mri_file + ' ' + anat_brain+ ' -f 0.4 -m'
                print cmd_bet
                if run == 1:
                    os.system('fsl_sub -l ' + logdir + ' ' + cmd_bet)
                    #subprocess.call(cmd_bet, shell=True)

