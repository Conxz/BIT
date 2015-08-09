

bb = [-90 -126 -72; 90 90 108];
vox_size = [2 2 2];
file_list = {'lPPA.hdr'  'lRSC.hdr'  'lTOS.hdr' 'rPPA.hdr'	'rRSC.hdr'  'rTOS.hdr'};
nfile = length(file_list);

for i=1:nfile
    file
    file = strcat('../', file_list{i});
    resize_img(file, vox_size, bb);
end