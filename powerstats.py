#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject
from threading import Thread

import battery

currpath = os.path.dirname(os.path.realpath(__file__))
iconpath = currpath + "/icons/battery-no.png"

last_percentage = 200 # value not possible

battery_arr = []
# length of mean
N = 5
for i in range(N):
    battery_arr.append(None)

def mean(arr):
    return float(sum(arr))/len(arr)

class Indicator():
    def __init__(self):
        self.app = 'powerstats'
        self.indicator = AppIndicator3.Indicator.new(self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_label("?",self.app)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        
        self.update = Thread(target=self.update)
        self.update.setDaemon(True)
        self.update.start()
        
    def create_menu(self):
        menu = Gtk.Menu()
        
        self.menu_power = Gtk.MenuItem("?")
        menu.append(self.menu_power)
        
        quit = Gtk.MenuItem("Quit")
        quit.connect('activate',self.quit)
        menu.append(quit)
        
        menu.show_all()
        return menu
        
    def update(self):
        while True:
            battery_otp = battery.battery()
            if debug: print battery_otp
             
            battery_str = "" 
             
            percentage = battery_otp["percentage"]
            icon_percentage = int((percentage+5)/10) * 10
            if debug: print "icon used:" + " battery-%d.png" % icon_percentage
            if last_percentage != icon_percentage:
                # if percentage change icon
                iconpath = currpath + "/icons/battery-%d.png" % icon_percentage
                GObject.idle_add(self.indicator.set_icon_full, iconpath, self.app, priority=GObject.PRIORITY_DEFAULT)
            battery_str += "%d%%" % percentage
            
            status = battery_otp["status"]
            if status == 1: battery_str += " ↑"
            if status == -1: battery_str += " ↓"
            
            tr = battery_otp["time"]            
            if tr: battery_str += " " + "%d:%02d" % ( tr, int(tr%1*12)*5 )
            
            power = battery_otp["power"]
            GObject.idle_add(self.menu_power.set_label, "%.2fW" % power)
            
            GObject.idle_add(self.indicator.set_label, battery_str, self.app, priority=GObject.PRIORITY_DEFAULT)
            time.sleep(10)
            
    def quit(self,widget):
        Gtk.main_quit()
    
debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
        print "Debugging"
        debug = True

Indicator()
GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
