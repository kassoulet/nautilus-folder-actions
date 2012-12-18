mkdir /tmp/nautilus-test
mkdir -p ~/.nautilus/python-extensions/
cp nautilus-folder-actions.py ~/.nautilus/python-extensions/
killall -9 nautilus
TMPDIR=/tmp/nautilus-test nautilus --no-desktop .
