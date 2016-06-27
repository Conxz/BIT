# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""A pipeline that uses tbss_all to perform TBSS.

"""

import os                                    # system functions
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
from nipype.workflows.dmri.fsl import tbss


sessdir = '/nfs/p1/public_dataset/datasets/Conxz/NP160211/NPpara_new/DTIFit/'
sessid = '/nfs/p1/public_dataset/datasets/Conxz/NP160211/subj/sesslist'
fsessid = open(sessid)
subject_list = [line.strip() for line in fsessid]

sinkdir = '/nfs/p1/public_dataset/datasets/Conxz/NP160211/NPpara_new'
workingdir = '/nfs/p1/public_dataset/datasets/Conxz/NP160211/workingdir_new/'
skeleton_thr = 0.2

def getFAList(subject_list):
    fa_list = []
    for subject_id in subject_list:
        fa_list.append(os.path.join(subject_id+'_FA'))
    return fa_list

tbss_source = pe.Node(interface=nio.DataGrabber(outfiles=['fa_list']),name='tbss_source')
tbss_source.inputs.base_directory = os.path.abspath(sessdir)
tbss_source.inputs.sort_filelist = True
tbss_source.inputs.template = '%s.nii.gz'
tbss_source.inputs.template_args = dict(fa_list=[[getFAList(subject_list)]])


"""TBSS analysis.
"""

tbss1 = tbss.create_tbss_1_preproc(name='tbss1')
tbss2 = tbss.create_tbss_2_reg(name='tbss2')
tbss2.inputs.inputnode.target = fsl.Info.standard_image("FMRIB58_FA_1mm.nii.gz")
tbss3 = tbss.create_tbss_3_postreg(name='tbss3', estimate_skeleton=True)
tbss4 = tbss.create_tbss_4_prestats(name='tbss4')
tbss4.inputs.inputnode.skeleton_thresh = skeleton_thr

tbss_all = pe.Workflow(name='tbssproc')
tbss_all.base_dir = os.path.abspath(workingdir)
tbss_all.connect([
            (tbss_source, tbss1, [('fa_list', 'inputnode.fa_list')]),
            (tbss1, tbss2, [('outputnode.fa_list', 'inputnode.fa_list'),
                            ('outputnode.mask_list', 'inputnode.mask_list')]),
            (tbss1, tbss3, [('outputnode.fa_list', 'inputnode.fa_list')]),
            (tbss2, tbss3, [('outputnode.field_list', 'inputnode.field_list')]),
            (tbss3, tbss4, [
                            ('outputnode.groupmask', 'inputnode.groupmask'),
                            ('outputnode.skeleton_file', 'inputnode.skeleton_file'),
                            ('outputnode.meanfa_file', 'inputnode.meanfa_file'),
                            ('outputnode.mergefa_file', 'inputnode.mergefa_file')
                        ])
                ])

"""Setup data storage area.
"""
datasink = pe.Node(interface=nio.DataSink(parameterization=False),name='datasink')
datasink.inputs.base_directory = os.path.abspath(sinkdir)

tbss_all.connect([
                (tbss4, datasink, [
                                    ('outputnode.skeleton_file', 'TBSS.@skeleton_file'),
                                    ('outputnode.skeleton_mask', 'TBSS.@skeleton_mask'),
                                    ('outputnode.projectedfa_file', 'TBSS.@projectedfa_file'),
                                    ('outputnode.distance_map', 'TBSS.@distance_map'),
                                    ]),
                (tbss2, datasink, [('outputnode.field_list', 'TBSS.@field_list')]),
                (tbss3, datasink, [
                                    ('outputnode.groupmask', 'TBSS.@groupmask'),
                                    ('outputnode.meanfa_file', 'TBSS.@meanfa_file'),
                                    ])
                ])


if __name__=='__main__':
    #tbss_all.run(plugin='MultiProc', plugin_args={'n_procs':12})
    tbss_all.run(plugin='SGE')

