# vi: set ft=python sts=4 ts=4 sw=4 et: 
"""
A pipeline that uses several interfaces to perform crossing-fibre modelling.
"""
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import os                                    # system functions
from nipype.workflows.dmri.fsl.dti import create_eddy_correct_pipeline, create_bedpostx_pipeline

workingDir = '/nfs/p1/public_dataset/datasets/NKI_Sample/workingdir'
sessidFile = '/nfs/p1/public_dataset/datasets/NKI_Sample/docs/sessid_mri_dti_rest.txt'

fsessid = open(sessidFile)
subject_list = [line.strip() for line in fsessid]

databank = '/nfs/p1/public_dataset/datasets/NKI_Sample/data'
sinkDir = '/nfs/p1/public_dataset/datasets/NKI_Sample/preproc/bedpostx'
bet_frac = 0.2

def subjrlf(subject_id):
    import os
    databank = '/nfs/p1/public_dataset/datasets/NKI_Sample/data'
    mri_n = 'MPRAGE_1'
    dti_n = 'DTI64_1'
    info = dict(
                dwi = [[subject_id,'session_1',dti_n,'d.nii.gz']],
                bvecs = [[subject_id,'session_1',dti_n,'d.bvec']],
                bvals = [[subject_id,'session_1',dti_n,'d.bval']],
                mri = [[subject_id,'session_1',mri_n,'anat_brain.nii.gz']]
                )
    return info

infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),
                     name="infosource")
infosource.iterables = ('subject_id', subject_list)

datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                               outfields=['dwi','bvecs','bvals','mri']),
                     name = 'datasource')
datasource.inputs.sort_filelist = True
datasource.inputs.template = "%s/%s/%s/%s"
datasource.inputs.base_directory = os.path.abspath(databank)

"""
extract the volume with b=0 (nodif_brain)
"""
fslroi = pe.Node(interface=fsl.ExtractROI(),name='fslroi')
fslroi.inputs.t_min=0
fslroi.inputs.t_size=1 # 1 b0 volumes which is averaged by x.py

"""
correct the diffusion weighted images for eddy_currents
"""
eddycorrect = create_eddy_correct_pipeline(name='eddycorrect')
eddycorrect.inputs.inputnode.ref_num=0

"""
create a brain mask from the nodif_brain
"""
bet = pe.Node(interface=fsl.BET(),name='bet')
bet.inputs.mask=True
bet.inputs.frac=bet_frac

"""
register T1-->b0 And MNI152-->T1 to get the transformation matrixes
"""
anat2b0 = pe.Node(interface=fsl.FLIRT(dof=6),name='anat2b0')
anat2b0.inputs.cost_func='mutualinfo' # between-modality
mni2anat = pe.Node(interface=fsl.FLIRT(dof=12),name='mni2anat')
mni2anat.inputs.in_file=fsl.Info.standard_image('MNI152_T1_2mm_brain.nii.gz')
mni2anat.inputs.cost_func='corratio'

"""
register MNI152-->b0 using matrixes we have got above 
"""
xfmconcat = pe.Node(interface=fsl.ConvertXFM(concat_xfm=True),name='xfmconcat')

"""
estimate the diffusion parameters: phi, theta, and so on
"""
bedpostx = create_bedpostx_pipeline(name='bedpostx')
bedpostx.inputs.xfibres.n_fibres = 2


preTract = pe.Workflow(name='preTract')
preTract.base_dir = workingDir
preTract.connect([
                (infosource, datasource, [
                                        ('subject_id','subject_id'),
                                        (('subject_id',subjrlf),'template_args')]),
                (datasource, fslroi, [('dwi','in_file')]),
                
                (datasource, eddycorrect, [('dwi','inputnode.in_file')]),
                (fslroi, bet, [('roi_file','in_file')]),
                
                (fslroi, anat2b0, [('roi_file','reference')]),
                (datasource, anat2b0, [('mri','in_file')]),

                (datasource, mni2anat,[('mri','reference')]),

                (mni2anat,xfmconcat,[('out_matrix_file','in_file')]),
                (anat2b0,xfmconcat,[('out_matrix_file','in_file2')]),

                (datasource, bedpostx, [
                                        ('bvals','inputnode.bvals'),
                                        ('bvecs','inputnode.bvecs')]),
                (eddycorrect, bedpostx,[('outputnode.eddy_corrected','inputnode.dwi')]),
                (bet, bedpostx,[('mask_file','inputnode.mask')]),
                ])

'''
Setup data storage area
'''
datasink = pe.Node(interface=nio.DataSink(parameterization=False),name='datasink')
datasink.inputs.base_directory = os.path.abspath(sinkDir)

preTract.connect([
                (infosource, datasink, [('subject_id','container')]),
                (bedpostx, datasink, [  
                                        ('outputnode.thsamples','thsamples'),
                                        ('outputnode.phsamples','phsamples'),
                                        ('outputnode.fsamples','fsamples'),
                                    ]),
                (xfmconcat, datasink, [('out_file','xfm')]),
                (bet, datasink, [('mask_file','mask')]),                
                ])

if __name__ == '__main__':
    print 'Start to run!\n'
    #preTract.run(plugin='MultiProc', plugin_args={'n_procs' : 16})
    preTract.run(plugin='SGE')
