bash env.sh
SCRIPT_DIRECTORY=$(dirname $(readlink -f "$0"))
echo 'alias media_compressor="python' $SCRIPT_DIRECTORY'/media_compressor.py"' >> $HOME/.bashrc
source $HOME/.bashrc
