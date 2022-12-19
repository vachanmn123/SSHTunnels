# main.py
#
# Copyright 2022 Vachan MN
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi



gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import SshtunnelsWindow
from .utils import create_tunnel

class SshtunnelsApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.vachanmn.SSHTunnels',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('connect', self.connect_action)
        # self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = SshtunnelsWindow(application=self)
        self.win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='sshtunnels',
                                application_icon='com.vachanmn.SSHTunnels',
                                developer_name='Vachan MN',
                                version='0.1.0',
                                developers=['Vachan MN'],
                                copyright='© 2022 Vachan MN')
        about.present()

    #def on_preferences_action(self, widget, _):
    #    """Callback for the app.preferences action."""
    #    print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def connect_action(self, widget, _):
        ip = self.win.ip.get_buffer().get_text()
        uname = self.win.uname.get_buffer().get_text()
        passwd = self.win.passwd.get_text()
        local_port = self.win.localport.get_buffer().get_text()
        remote_port = self.win.remoteport.get_buffer().get_text()
        print(ip, uname, passwd, local_port, remote_port)
        alert_window = Gtk.AlertDialog()
        alert_window.set_message(f"IP: {ip}\nuname: {uname}\npasswd: {passwd}\nlocal port: {local_port}\nremote port: {remote_port}")
        alert_window.show()

def main(version):
    """The application's entry point."""
    app = SshtunnelsApplication()
    return app.run(sys.argv)
