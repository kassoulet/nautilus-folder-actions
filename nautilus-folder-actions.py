#!/usr/bin/env python
# nautilus-folder-actions by Gautier Portet <kassoulet gmail.com>

'''
This little script for Nautilus allows you to add actions in Nautilus.
For now, only toolbar buttons are supported.
--

 - buttons
 - menu items
 - menu background item

 - run command (optionnally in terminal)
 - show a progressbar with an optionnal terminal like synaptic
 - display "errors"
   - program output (stdout and/or stderr)
   - error extracting (+link to files if I want to be a hero...)

Name
Comment
Icon=
Exec=soundconverter %U
Terminal=false

nautilus folder buttons



'''

import os
import sys
import urllib

TERMINAL_KEY = '/desktop/gnome/applications/terminal/exec'

print 'Initializing nautilus-folder-actions'

import gtk
import nautilus
import gconf

CONF_FILENAME = 'nautilus-folder-actions'

class Action():
    def __init__(self):
        self.name = ''
        self.icon = 'extension'
        self.command = ''
        self.comment = ''

def get_folder_actions(folder):
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

    def _open_terminal(self, file, action):
        filename = urllib.unquote(file.get_uri()[7:])
        #terminal = self.client.get_string(TERMINAL_KEY)

        os.chdir(filename)
        #print "RUNNING:", filename, '%s --command "%s" ' % (terminal, action)
        #os.system('%s --command %s ' % (terminal, action))
        os.system(action)

    def _menu_activate_cb(self, menu, file):
        self._open_terminal(file)

    def menu_background_activate_cb(self, menu, params):

        file, action = params
        print 'click:', file.get_uri()
        self._open_terminal(file, action)

    def get_toolbar_items(self, window, file):
        print file.get_uri()

        folder = urllib.unquote(file.get_uri()[7:])
        actions = get_folder_actions(folder)

        items = []
        for action in actions:
            item = nautilus.MenuItem('NautilusPython::build_item',
                                     action.name,
                                     action.comment,
                                     action.icon)
            item.connect('activate', self.menu_background_activate_cb, [file, action.command])
            items.append(item)

        return items



