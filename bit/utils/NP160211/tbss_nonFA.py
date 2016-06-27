# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
A pipeline that uses several interfaces to perform tbss_non_FA.
"""

import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import os                                    # system functions
from nipype.workflows.dmri.fsl.tbss import create_tbss_non_FA


sessdir = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/NPpara/DTIFit/'
sessid = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/subj/sesslist'
fsessid = open(sessid)
subject_list = [line.strip() for line in fsessid]

sinkdir = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/NPpara/TBSS'
tbssDir = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/workingdir/'

skeleton_thr = 0.2
nonFA = 'MD'#'AD'/'RD'/'MD'/'MO'

"""Here we get the FA list including all the subjects.
"""
def get_nonFAList(subject_list):
    file_list = []
    for subject_id in subject_list:
        #file_list.append(os.path.join(sessdir, subject_id, 'dtifit', subject_id+'_'+nonFA))
        file_list.append(os.path.join(sessdir, subject_id+'_'+nonFA))
    return file_list
def getfieldList(subject_list):
    field_list = []
    for subject_id in subject_list:
        field_list.append(os.path.join(sinkdir, subject_id+'_FA_prep_fieldwarp'))
    return field_list

tbss_source = pe.Node(interface=nio.DataGrabber(outfiles=['file_list','field_list']),name='tbss_source')
tbss_source.inputs.base_directory = os.path.abspath('/')
tbss_source.inputs.sort_filelist = True
tbss_source.inputs.template = '%s.nii.gz'
tbss_source.inputs.template_args = dict(file_list=[[get_nonFAList(subject_list)]],
                                        field_list = [[getfieldList(subject_list)]]
                                        )

"""
Setup data storage area
"""
datasink = pe.Node(interface=nio.DataSink(parameterization=False),name='datasink')
datasink.inputs.base_directory = os.path.abspath(sinkdir)

'''
TBSS analysis
'''
tbss_nonFA = create_tbss_non_FA(name='tbss_'+nonFA)
tbss_nonFA.inputs.inputnode.skeleton_thresh = skeleton_thr
tbss_nonFA.inputs.inputnode.groupmask = os.path.join(sinkdir, 'brain_groupmask.nii.gz')
tbss_nonFA.inputs.inputnode.meanfa_file = os.path.join(sinkdir, 'mean_FA.nii.gz')
tbss_nonFA.inputs.inputnode.distance_map = os.path.join(sinkdir, 'distance_map.nii.gz')

rename_nonfa = pe.Node(util.Rename(format_string='all_'+nonFA+'_skeletonised.nii.gz'), name='renamenonfa')

tbss_nonFA_proc = pe.Workflow(name="tbss_" + nonFA + "_proc")
tbss_nonFA_proc.base_dir = os.path.abspath(tbssDir)
tbss_nonFA_proc.connect([
                (tbss_source, tbss_nonFA,[('file_list','inputnode.file_list'),
                                          ('field_list','inputnode.field_list')
                                          ]),
                (tbss_nonFA, rename_nonfa, [
                                            ('outputnode.projected_nonFA_file', 'in_file'),
                                             ]),
                (rename_nonfa, datasink, [
                                            ('out_file', '@projected_nonFA_file'),
                                             ]),
                #(tbss_nonFA, datasink,[
                #                    ('outputnode.projected_nonFA_file','@projected_nonFA_file'),
                #                    ]),
                ])


if __name__=='__main__':
    #tbss_nonFA_proc.run(plugin='MultiProc', plugin_args={'n_procs':10})
    tbss_nonFA_proc.run(plugin='SGE')
