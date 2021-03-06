#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Check directory structure for NKI Sample.

"""
import os
import glob

def main():
    datdir = '/nfs/p1/public_dataset/datasets/NKI_Sample/data/'
    os.chdir(datdir)
    sesslist = glob.glob('*')
    sesslist.sort()
    scans = ['session_1', 'session_2']
    brains = ['MPRAGE_1', 'DTI64_1', 'BOLDrestingCAP_1', 'MPRAGEshorter_1']

    #sids_with_alldat = []
    
    for scan in scans:
        print scan
        sids_with_alldat = []
        print 'SID\t', 'phenotypic\t', '\t'.join(brains)
        for sid in sesslist:
            boollist = [sid, '0', '0', '0', '0', '0']
            
            behdir = os.path.join(sid, 'phenotypic')
            if os.path.exists(behdir):
                boollist[1] = '1'
            
            scandir = os.path.join(sid, scan)
            if os.path.exists(scandir):
                for i, brain in enumerate(brains):
                    braindir = os.path.join(scandir, brain)
                    if os.path.exists(braindir):
                        boollist[i+2] = '1'
            
            print '\t'.join(boollist)
            
            if ''.join(boollist[1:4]) == '111':
                sids_with_alldat.append(sid)
        
        print 'Sessid with all data, including MPRAGE, DTI, and Resting.'
        print 'SID'
        print '\n'.join(sids_with_alldat)

if __name__ == '__main__':
    main()
