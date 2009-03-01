#!/usr/bin/env python
# nautilus-folder-actions by Gautier Portet <kassoulet gmail.com>

__author__ = 'Gautier Portet <kassoulet gmail.com>'
__version__ = '0.1.0'

'''
This little script for Nautilus allows you to add actions in Nautilus.
For now, only toolbar buttons are supported.
'''

import os
import sys
import urllib
from threading import Thread

TERMINAL_KEY = '/desktop/gnome/applications/terminal/exec'

print 'Initializing nautilus-folder-actions ' + __version__

import gtk
import nautilus
import gconf

CONF_FILENAME = 'nautilus-folder-actions'


class Command(Thread):
    """
    Launch a background command.
    """

    def __init__(self, command, folder):
        Thread.__init__(self)
        self.command = command
        self.folder = folder
    
    def run(self):
        os.chdir(self.folder)
        os.system(self.command)


class Action():
    """
    One action from the current folder.
    """
    def __init__(self):
        self.name = ''
        self.icon = 'extension'
        self.command = ''
        self.comment = ''

    def run(self, folder):
        command = Command(self.command, folder)
        command.start()


def get_folder_actions(folder):
    """
    Return the list of action for the given folder.
    """
    import ConfigParser
    config = ConfigParser.SafeConfigParser()
    filename = os.path.join(folder, CONF_FILENAME)
    print 'reading:', filename
    config.read(filename)

    actions = []
    for section in config.sections():
        action = Action()
        action.name = section
        items = dict(config.items(section))

        if 'exec' in items:
            action.command = items['exec']
        if 'name' in items:
            action.name = items['name']
        if 'icon' in items:
            action.icon = items['icon']
        if 'comment' in items:
            action.comment = items['comment']

        actions.append(action)
    return actions


class NautilusBuildExtension(nautilus.MenuProvider):
    def __init__(self):
        self.client = gconf.client_get_default()

    def activate_cb(self, menu, params):
        file, action = params
        print 'click:', file.get_uri()
        folder = urllib.unquote(file.get_uri()[7:])
        action.run(folder)

    def get_toolbar_items(self, window, file):
        print file.get_uri()

        folder = urllib.unquote(file.get_uri()[7:])
        actions = get_folder_actions(folder)

        items = []
        for action in actions:
            item = nautilus.MenuItem('NautilusPython::folder-actions::%s' % action.name,
                                     action.name,
                                     action.comment,
                                     action.icon)
            item.connect('activate', self.activate_cb, [file, action])
            items.append(item)

        return items



