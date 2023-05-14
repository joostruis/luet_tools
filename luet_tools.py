import os

euid = os.geteuid() 
if euid != 0:
  raise EnvironmentError('Luet operations require root: try running with sudo?')
  exit()

import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, GObject, Vte
#GObject is not required. I just import it everywhere just in case.
#Gtk, Vte, and GLib are required.
from gi.repository import GLib
import os
#os.environ['HOME'] helps to keep from hard coding the home string.
#os is not required unless you want that functionality.

class TheWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Luet toolkit")
        self.set_default_size(600, 300)
        self.terminal     = Vte.Terminal()
        self.terminal.spawn_async(
                Vte.PtyFlags.DEFAULT, # Pty Flags
                os.environ['HOME'], # Working DIR
                ["/bin/bash"], # Command/BIN (argv)
                None, # Environmental Variables (envv)
                GLib.SpawnFlags.DEFAULT, # Spawn Flags
                None, None, # Child Setup
                -1, # Timeout (-1 for indefinitely)
                None, # Cancellable
                None, # Callback
                None # User Data
                )

        button0 = Gtk.Button.new_with_label("Sync repositories")
        button0.connect("clicked", self.luet_repo_update)

        button1 = Gtk.Button.new_with_label("Enabled repositories")
        button1.connect("clicked", self.luet_repo_list)

        button2 = Gtk.Button.new_with_label("Installed packages")
        button2.connect("clicked", self.luet_list_installed)

        button3 = Gtk.Button.new_with_label("Luet version")
        button3.connect("clicked", self.luet_version)

        button4 = Gtk.Button.new_with_label("OS check")
        button4.connect("clicked", self.luet_oscheck)

        button5 = Gtk.Button.new_with_label("Clear")
        button5.connect("clicked", self.clear_terminal)

        button6 = Gtk.Button.new_with_label("Close")
        button6.connect("clicked", self.close_app)

        #set up the interface
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        grid = Gtk.Grid()
        grid.add(button0)
        grid.add(button1)
        grid.add(button2)
        grid.add(button3)
        grid.add(button4)
        grid.add(button5)
        grid.add(button6)
        box.pack_start(grid, False, True, 1)
        #a scroll window is required for the terminal
        scroller = Gtk.ScrolledWindow()
        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        scroller.add(self.terminal)
        box.pack_start(scroller, False, True, 2)
        self.add(box)

    def InputToTerm(self, clicker):
        #get the command when the button is clicked
        length = len(self.command)
        #A length is not required but is the easiest mechanism.
        #Otherwise the command must be null terminated.
        #Feed the command to the terminal.
        self.terminal.feed_child(self.command.encode("utf-8"))

    def luet_repo_update(self, button):
        command = "luet repo update\n"
        self.terminal.feed_child(command.encode("utf-8"))

    def luet_version(self, button):
        command = "luet --version\n"
        self.terminal.feed_child(command.encode("utf-8"))

    def luet_repo_list(self, button):
        command = "luet repo list -q\n"
        self.terminal.feed_child(command.encode("utf-8"))
    
    def luet_list_installed(self, button):
        command = "luet search --installed . -q\n"
        self.terminal.feed_child(command.encode("utf-8"))       

    def luet_oscheck(self, button):
        command = "luet oscheck --reinstall\n"
        self.terminal.feed_child(command.encode("utf-8"))

    def clear_terminal(self, button):
        command = "clear\n"
        self.terminal.feed_child(command.encode("utf-8"))

    def close_app(self, button):
        Gtk.main_quit()

win = TheWindow()
win.connect("delete-event", Gtk.main_quit)
win.set_title ("Luet toolkit")
win.show_all()
Gtk.main()