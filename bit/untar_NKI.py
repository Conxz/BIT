#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
extract files from NKI Sample archives.
"""
import os
import glob

def untar_NKI(tar_file, tgt_dir):
    if tar_file == 'NKI.archive.36-39.001.LiteNIFTI.tar.gz':
        cmdstr = 'tar xzvf ' + tar_file + ' -C ' + tgt_dir
    else:
        cmdstr = 'tar xzvf ' + tar_file + ' --strip-components 1 -C ' + tgt_dir
    
    print cmdstr
    os.system(cmdstr)
    
def main():
    src_dir = '/nfs/p1/public_dataset/datasets/NKI_Sample/tar.gz'
    tgt_dir = '/nfs/p1/public_dataset/datasets/NKI_Sample/data'
    os.chdir(src_dir)
    
    tar_list = glob.glob('NKI.archive.*.tar.gz')
    tar_list.sort(key=lambda x:int(x.split('.')[2].split('-')[0]))
    
    for tar_file in tar_list:
        untar_NKI(tar_file, tgt_dir)

if __name__ == '__main__':
    main()
