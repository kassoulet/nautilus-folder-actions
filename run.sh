mkdir /tmp/nautilus-test
cp nautilus-folder-actions.py ~/.nautilus/python-extensions/
killall -9 nautilus
TMPDIR=/tmp/nautilus-test nautilus --no-desktop .