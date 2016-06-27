# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""A pipeline that uses several interfaces to compute tensor.

"""

import os                                    # system functions
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
from nipype.workflows.dmri.fsl.dti import create_eddy_correct_pipeline

sessidFile = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/subj/sesslist'
fsessid = open(sessidFile)
subject_list = [line.strip() for line in fsessid]

databank = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/data'
workingdir = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/workingdir'
sinkdir = '/nfs/p1/public_dataset/datasets/Conxz/NP150721/NPpara'
bet_frac = 0.2

def subjrlf(subject_id):
    dti_n = 'DTI64_1'
    info = dict(
            dwi = [[subject_id, 'd.nii.gz']],
            bvecs = [[subject_id, 'd.bvec']],
            bvals = [[subject_id, 'd.bval']],
            )
    return info

subjsource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),
                     name="subjsource")
subjsource.iterables = ('subject_id', subject_list)

datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                               outfields=['dwi','bvecs','bvals']),
                     name = 'datasource')
datasource.inputs.sort_filelist = True
datasource.inputs.template = "%s/%s"
datasource.inputs.base_directory = os.path.abspath(databank)

computeTensor = pe.Workflow(name='computeTensor')

extractb0 = pe.Node(interface=fsl.ExtractROI(), name='extractb0')
extractb0.inputs.t_min = 0
extractb0.inputs.t_size = 1

bet = pe.Node(interface=fsl.BET(),name='bet')
bet.inputs.mask=True
bet.inputs.frac=bet_frac

eddycorrect = create_eddy_correct_pipeline(name='eddycorrect')
eddycorrect.inputs.inputnode.ref_num=0

dtifit = pe.Node(interface=fsl.DTIFit(),name='dtifit')
dtifit.inputs.save_tensor=True

computeTensor.connect([
                        (extractb0,bet,[('roi_file','in_file')]),
                        (eddycorrect,dtifit,[('outputnode.eddy_corrected','dwi')]),
                        (subjsource, dtifit,[['subject_id','base_name']]),
                        (bet,dtifit,[('mask_file','mask')])
                      ])

def forRD_op_string(infile2):
                        op_string = []
                        op_string = '-add %s -div 2'%infile2
                        return op_string
def renameRD(org_RD):
                        from shutil import copy
                        RD_suffix = '_RD.nii.gz'
                        RD_prefix = org_RD[:-13]
                        RD = RD_prefix + RD_suffix
                        copy(org_RD,RD)
                        return RD
forRD =pe.Node(fsl.ImageMaths(suffix="_RD"),name='forRD')

def renameAD(org_AD):
                        from shutil import copy
                        AD_suffix = '_AD.nii.gz'
                        AD_prefix = org_AD[:-13]
                        AD = AD_prefix + AD_suffix
                        copy(org_AD,AD)
                        return AD 
forAD =pe.Node(fsl.ImageMaths(suffix="_AD"),name='forAD')
forAD.inputs.op_string = '-add 0'

computeTensor.connect([
                        (dtifit,forRD,[
                                       ('L2','in_file'),
                                       (('L3',forRD_op_string),'op_string')
                                       ]),
                        (dtifit,forAD,[('L1','in_file')])
                        ])

"""
Setup data storage area
"""
datasink = pe.Node(interface=nio.DataSink(parameterization=False),name='datasink')
datasink.inputs.base_directory = os.path.abspath(sinkdir)

"""
Setup the pipeline 
----------------------------------------------------------------------------------
"""

dtiproc = pe.Workflow(name="dtifit_workingdir")
dtiproc.base_dir = os.path.abspath(workingdir)
dtiproc.connect([
                    (subjsource,datasource,[('subject_id', 'subject_id'),
                                                (('subject_id',subjrlf),'template_args')
                                                ]),
                    (datasource,computeTensor,[('dwi','extractb0.in_file'),
                                               ('bvals','dtifit.bvals'),
                                               ('bvecs','dtifit.bvecs'),
                                               ('dwi','eddycorrect.inputnode.in_file')
                                               ]),
                    (computeTensor,datasink,[   ('dtifit.FA','DTIFit.@FA'),
                                                ('dtifit.L1','DTIFit.@L1'),
                                                ('dtifit.L2','DTIFit.@L2'),
                                                ('dtifit.L3','DTIFit.@L3'),
                                                ('dtifit.MD','DTIFit.@MD'),
                                                ('dtifit.S0','DTIFit.@S0'),
                                                ('dtifit.tensor','DTIFit.@tensor'),
                                                ('dtifit.V1','DTIFit.@V1'),
                                                ('dtifit.V2','DTIFit.@V2'),
                                                ('dtifit.V3','DTIFit.@V3'),
                                                ('dtifit.MO','DTIFit.@MO'),
                                                (('forRD.out_file',renameRD),'DTIFit.@RD'),
                                                (('forAD.out_file',renameAD),'DTIFit.@AD'),
                                                ]),
                    ])

if __name__=='__main__':
    #dtiproc.run(plugin='MultiProc', plugin_args={'n_procs':10})
    dtiproc.run(plugin='SGE')
