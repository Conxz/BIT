#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

"""Get behavior data.

"""

import os, csv
import glob

subj = 'Subject'
beh_list = [subj, 'Gender', 'Age']
new_beh_list = ['SID'] + beh_list[1:]

logdir = '/nfs/p1/public_dataset/datasets/NKI_Sample/log'
if not os.path.exists(logdir):
    os.mkdir(logdir)

out_csv_file = os.path.join(logdir, 'out_csv_file.csv')
out_csv_f = open(out_csv_file, 'w')
out_csv_writer = csv.writer(out_csv_f)
out_csv_writer.writerow(new_beh_list)

datdir = '/nfs/p1/public_dataset/datasets/NKI_Sample/data'
os.chdir(datdir)
sidlist = glob.glob('*')

pheno = 'phenotypic'

for sid in sidlist:
    print sid
    pheno_dir = os.path.join(sid, pheno)
    beh_dat = []
    if os.path.exists(pheno_dir):
        pheno_file = os.path.join(pheno_dir, sid + '.csv')
        
        csv_f = open(pheno_file)
        csv_dat = csv.reader(csv_f)
        xlabel = []
        xdata = []
        for i, raw in enumerate(csv_dat):
            if i == 0:
                xlabel = raw
            elif i == 1:
                xdata = raw
        for beh in beh_list:
            if beh in xlabel:
                beh_dat.append(xdata[xlabel.index(beh)])
            else:
                print beh, ' Not Exist!'
        
        out_csv_writer.writerow(beh_dat)
        csv_f.close()

out_csv_f.close()

