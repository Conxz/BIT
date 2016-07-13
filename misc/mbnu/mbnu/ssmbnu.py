# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import os
import glob 
from base import readsessid

def calc_pdfs(data_dir, seg_file, label_file, sessid_file=None):
    if sessid_file == None:
        sessid_list = []
        sess_dir_list = glob.glob(os.path.join(data_dir, '*'))
        for sess_dir in sess_dir_list:
            sessid_list.append(os.path.split(sess_dir)[-1])
    else:
        sessid_list = readsessid(sessid_file)

    vmin = 0
    vmax = 1
    n_pdf = 100

    label_img = nib.load(seg_file)
    label_dat = label_img.get_data()
    label_list = np.unique(label_dat)

    label_name_file = label_file
    label_name_list = readsessid(label_name_file)[:-1]
    figname = 'pdfs.png'
    dataname = 'databank'

    for sess in sessid_list:
        print sess
        sess_dir = os.path.join(data_dir, sess)
        outfig = os.path.join(sess_dir, figname)
        outdata = os.path.join(sess_dir, dataname)
        data_file = os.path.join(sess_dir, 'smwc1'+sess+'_anat.nii')
        img = nib.load(data_file)
        dat = img.get_data()

        databank = np.zeros((n_pdf, len(label_list[1:])))
        for label in label_list[1:]:
            label_voxel = (label_dat == label)
            label_voxel_index = label_voxel.nonzero()
            #label_size.append(len(label_voxel_index))
            dat_tmp = dat[label_voxel_index]
            dens = stats.kde.gaussian_kde(dat_tmp)
            x_tmp = np.linspace(vmin, vmax, n_pdf)
            freq = dens(x_tmp)
            databank[:, label-1] = freq
        
        # For plotting each freq plot
        plt.plot(np.linspace(0,1,100), databank)
        plt.title('Distributions for Each Node')
        ('Distributions for Each Node')
        plt.xlabel('Gray Matter Volume')
        plt.ylabel('Probability')
        plt.savefig(outfig, dpi=600)
        
        np.savez(outdata, databank=databank)


def get_dkl(dat, i, j, n_samp):
    """
    One symmetric Kullback-Leibler (KL) divergence measure.
    DKL(p,q) = sum(p*log(p/q) + q*log(q/p))
    The KL divergence can be converted to a similarity measure
    (ranging from 0 to 1) using this expression:
    SKL = exp(-DKL(p,q)).
    
    See Hazen, Direct and Latent Modeling Techniques for Computing 
    Spoken Document Similarity, 2005.
    
    """
    tmp = 0
    for k in range(n_samp):
        tmp += dat[i,k]*np.log(dat[i,k]/dat[j,k]) \
                + dat[j,k]*np.log(dat[j,k]/dat[i,k])    
    return tmp


def reorder_mat(mat):
    """
    """
    # For row
    mat = np.append(mat[::2], mat[1::2], axis=0)
    # For colom
    mat = np.append(mat[:,::2], mat[:,1::2], axis=1)
    
    return mat


def calc_kls_mat(data_dir, sessid_file=None):
    """
    """
    if sessid_file == None:
        sessid_list = []
        sess_dir_list = glob.glob(os.path.join(data_dir, '*'))
        for sess_dir in sess_dir_list:
            sessid_list.append(os.path.split(sess_dir)[-1])
    else:
        sessid_list = readsessid(sessid_file)

    databank = 'databank.npz'
    mat_fig = 'skl_mat.png'
    mat_dat = 'skl_mat'
    rmat_fig = 'skl_mat_reordered.png'
    rmat_dat = 'skl_mat_reordered'
    
    for sess in sessid_list:
        print sess
        sessdir = os.path.join(data_dir, sess)
        mat_fig_file = os.path.join(sessdir, mat_fig)
        mat_dat_file = os.path.join(sessdir, mat_dat)
        rmat_fig_file = os.path.join(sessdir, rmat_fig)
        rmat_dat_file = os.path.join(sessdir, rmat_dat)
        
        data_file = os.path.join(sessdir, databank)
        dat = np.load(data_file)
        dat = dat['databank']
        dat = np.where(dat == 0, dat[dat!=0].min(), dat)
        dat = dat.T
        
        n_roi = dat.shape[0]
        n_samp = dat.shape[1]
        im = np.zeros((n_roi, n_roi))
        
        for i in range(n_roi):
            for j in range(n_roi):
                if i < j:
                    dkl = get_dkl(dat, i, j, n_samp)
                    skl = np.exp(-dkl)
                    im[i,j] = skl
                    im[j,i] = skl
                    
        # Save mat
        np.savez(mat_dat_file, im=im)
        np.savetxt(mat_dat_file+'.txt', im, fmt='%.4e', delimiter='    ')
        plt.imshow(im, origin='lower',interpolation='nearest')
        plt.colorbar(ticks=[0, 0.5, 1])   
        plt.savefig(mat_fig_file, dpi=600)
        plt.close()
        
        # Reorder the mat
        im = reorder_mat(im)
        
        np.savez(rmat_dat_file, im=im)
        np.savetxt(rmat_dat_file+'.txt', im, fmt='%.4e', delimiter='    ')
        plt.imshow(im, origin='lower',interpolation='nearest')
        plt.colorbar(ticks=[0, 0.5, 1])   
        plt.savefig(rmat_fig_file, dpi=600)
        plt.close()

def ssmbnu(data_dir, seg_file, label_file, sessid_file=None):
    """
    single-subject morphological brain network utilities
    """
    print data_dir, seg_file, label_file, sessid_file
    #calc_pdfs(data_dir, seg_file, label_file, sessid_file)
    #calc_kls_mat(data_dir, sessid_file)
    return 1

