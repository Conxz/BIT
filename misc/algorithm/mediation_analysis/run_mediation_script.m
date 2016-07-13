% Go to the directory this script is stored in and run the script from
% there.

basedir = pwd;
disp(basedir);

% List image names; may not work on all file systems
%img_names = filenames(fullfile('Images_for_mediation', 'con*img'), 'char')
%save img_names img_names

% load the list of image names
load img_names

% append your local directory names
img_names = [repmat([basedir filesep], size(img_names, 1), 1) img_names];

% img_names should now be a valid list of image names with full path
% information.

% Load X and Y variables from saved mediation output
load(fullfile('mediation_Example_Data_Wager2008_Msearch_R_XisRIFGstim_norobust', 'mediation_SETUP.mat'));

% specify mask file from saved mediation output
mask_name = fullfile('mediation_Example_Data_Wager2008_Msearch_R_XisRIFGstim_norobust', 'mask.img');

mask_name = fullfile(basedir, mask_name);

% make a new analysis directory
andir = 'Test_mediation';
mkdir(andir)
cd(andir)

results = mediation_brain(SETUP.X, SETUP.Y, img_names, 'names', {'IFG' 'ReappSuccess' 'BrainMediator'}, 'mask', mask_name, 'boot', 'pvals', 5);