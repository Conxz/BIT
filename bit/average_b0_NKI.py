#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

"""Prepare d.nii.gz, d.bval, and d.bvec for multiple b0 scanning.

"""
import numpy as np
import os
import glob

logdir = '/nfs/p1/public_dataset/datasets/NKI_Sample/log'
if not os.path.exists(logdir):
    os.mkdir(logdir)

datdir = '/nfs/p1/public_dataset/datasets/NKI_Sample/data'
os.chdir(datdir)
sidlist = glob.glob('*')
sidlist.sort()

scans = ['session_1', 'session_2']
sesslist = ['DTI64_1']
dti = 'DTI.nii.gz'
dti_out = 'd.nii.gz'
b0s = 'b0s.nii.gz'
b0 = 'b0.nii.gz'

bval = 'DTI.bval'
bval_out = 'd.bval'

bvec = 'DTI.bvec'
bvec_out = 'd.bvec'

run = 1

for scan in scans:
    print scan
    for sid in sidlist:
        print sid
        for i, sess in enumerate(sesslist):
            scandir = os.path.join(datdir, sid, scan, sess)
            if os.path.exists(scandir):
                os.chdir(scandir)
                cmd_fslroi = 'fslroi ' + dti + ' ' + b0s +' 0 12'

                cmd_fslmaths = 'fslmaths ' + b0s + ' -Tmean ' + b0
                
                cmd_fslroi2 = 'fslroi ' + dti + ' ' + dti_out +' 12 -1'
                cmd_fslmerge = 'fslmerge -t ' + dti_out + ' ' + b0 + ' ' + dti_out

                cmd_strs = '\n'.join([cmd_fslroi, cmd_fslmaths, cmd_fslroi2, cmd_fslmerge]) + '\n'
                f_cmdlog = open('cmdlog.txt', 'w+')
                f_cmdlog.write(cmd_strs)
                f_cmdlog.close()

                if run == 1:
                    os.system('chmod 755 ./cmdlog.txt')
                    os.system('fsl_sub -l ' + logdir + ' ./cmdlog.txt')
                
                bval_dat = np.loadtxt(bval)
                print sum(bval_dat == 0), 'b0 images.'
                bval_dat = bval_dat[11:]
                np.savetxt(bval_out, bval_dat.reshape(1, bval_dat.shape[0]), fmt='%d')

                bvec_dat = np.loadtxt(bvec)
                bvec_dat = bvec_dat[:,11:]
                np.savetxt(bvec_out,bvec_dat.reshape(3, bval_dat.shape[0]), fmt='%.14f')
