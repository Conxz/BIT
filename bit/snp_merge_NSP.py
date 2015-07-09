#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Merge SNP data for NSP.

"""
import glob
import os
import numpy as np

def main():
    snp_dir = '/nfs/p1/public_dataset/datasets/Conxz/64SNPs_subID'
    txtlist = glob.glob(os.path.join(snp_dir, 'rs*.txt'))
    txtlist.sort()
    dat_list = []
    all_sid = []
    out_file = os.path.join(snp_dir, '../all_64SNP.data')
    #out_file = os.path.join(snp_dir, '../all_64SNP.gender')
    fout = open(out_file, 'w+')
    snp_ids = ['SID']

    for txt in txtlist:
        snp_id = os.path.basename(txt[:-4])
        snp_ids.append(snp_id)
        dat = np.loadtxt(txt, dtype='str', skiprows=8, delimiter='\t')
        dat_list.append(dat)
        all_sid = list(set(all_sid).union(set(dat[:,3])))
    
    fout.write('\t'.join(snp_ids)+'\n')
    all_sid.sort()

    for sid in all_sid:
        snp_dat = [sid]
        #gender_dat = [sid]
        for dat in dat_list:
            sesslist = dat[:,3]
            if sid in list(sesslist):
                sid_index = list(sesslist).index(sid)
                genetypelist = dat[:,1]
                #genderlist = dat[:,2]
                snp_dat.append(genetypelist[sid_index])
                #gender_dat.append(genderlist[sid_index])
            else:
                snp_dat.append('0')
                #gender_dat.append('0')

        fout.write('\t'.join(snp_dat)+'\n')
        #fout.write('\t'.join(gender_dat)+'\n')
    
    fout.close()

if __name__ == '__main__':
    main()
