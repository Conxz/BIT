# .bashrc

# Source global definitions
#if [ -f /bin/zsh ]; then
#	. /bin/zsh
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions

#BASHRC_VER='DIS'
BASHRC_VER='DEV'
# DIS for distributed version; 
# DEV for developing version;

export BASHRC_VER

if [ $BASHRC_VER == 'DIS' ]; then 
	echo "Code Version: Distributed($BASHRC_VER)"
	source /usr/local/neurosoft/labtool/labtoolSetup.sh
	export SVN_EDITOR=/usr/bin/vim
	export PYTHONPATH=/nfs/j3/userhome/kongxiangzhen/workingdir/svnDir/nitk/nitk-pipeline/trunk:$PYTHONPATH
else
	echo "Code Version: Developing($BASHRC_VER)"
	source ~/.bashrc_dev
fi

