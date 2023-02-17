SCRIPT_DIRECTORY=$(dirname $(readlink -f "$0"))
echo 'alias media_compressor="python '"$SCRIPT_DIRECTORY"'/media_compressor.py"' >> /etc/profile
echo 'alias prog_scanner="python '"$SCRIPT_DIRECTORY"'/prog_scanner.py"' >> /etc/profile
echo 'alias size_calc="python '"$SCRIPT_DIRECTORY"'/size_calc.py"' >> /etc/profile

echo "source /etc/profile or re-login to apply changes"
