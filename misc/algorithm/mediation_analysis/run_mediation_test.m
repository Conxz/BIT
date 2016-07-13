function run_mediation_brain(csvfile, xname, yname, mname, maskfile)
    %% This function does a robust search for mediators between two vars X
    %% and Y
    %% example:
    % csvfile = './sf.csv';
    % xname = 'c5';
    % yname = 'score';
    % mname = 'brain';
    % maskfile = '../mask.nii';
    % run_mediation_brain(csvfile, xname, yname, mname, maskfile)
    
basedir = pwd;
disp(basedir);
csvdata = importdata(csvfile);
sesslist = csvdata.textdata(2:end,1);
taglist = csvdata.textdata(1,:);

xindex = find(ismember(taglist, xname)==1);
xdata = csvdata.data(:, xindex);

yindex = find(ismember(taglist, yname)==1);
ydata = csvdata.data(:, yindex);

datadir = '/nfs/s2/nspworking/VBM/data/amount';

img_names = [repmat([datadir strcat(filesep, 'smwc1')], size(sesslist,1),1) char(sesslist)];
img_names = [img_names  repmat('_anat.nii',size(sesslist,1),1)];
    
    % make a new analysis directory
andir = 'Output_mediation';
mkdir(andir)
cd(andir)

results = mediation_brain(xdata, ydata, img_names, 'names', {'C5' 'Score' 'BrainMediator'}, 'mask', mask_name, 'boot', 'pvals', 5);

cd('../');