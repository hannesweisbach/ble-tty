#!/usr/bin/env python3

import dbus
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import sys

from dbus.mainloop.glib import DBusGMainLoop

bus = None
mainloop = None

BLUEZ_SERVICE_NAME = 'org.bluez'
DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

GATT_SERVICE_IFACE = 'org.bluez.BLETTY'
GATT_TX_IFACE =    'org.bluez.BLETTYTx'
GATT_RX_IFACE =    'org.bluez.BLETTYRx'

TTY_SVC_UUID = ''

tty_service = None

def generic_error_cb(error):
    print('D-Bus call failed: ' + str(error))
    mainloop.quit()

def interfaces_removed_cb(object_path, interfaces):
    if not hr_service:
        return

    if object_path == hr_service[2]:
        print('Service was removed')
#        mainloop.quit()

def process_service(service_path, chrc_paths):
    service = bus.get_object(BLUEZ_SERVICE_NAME, service_path)
    service_props = service.GetAll(GATT_SERVICE_IFACE,
                                   dbus_interface=DBUS_PROP_IFACE)

    uuid = service_props['UUID']

    if uuid != TTY_SVC_UUID:
        return False

    print('TTY Service found: ' + service_path)

    # Process the characteristics.
    for chrc_path in chrc_paths:
        process_chrc(chrc_path)

    global tty_service
    tty_service = (service, service_props, service_path)

    return True

def scan_for_tty_service

def main():
    # Set up the main loop.
    DBusGMainLoop(set_as_default=True)
    global bus
    bus = dbus.SystemBus()
    global mainloop
    mainloop = GObject.MainLoop()

    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'), DBUS_OM_IFACE)
    om.connect_to_signal('InterfacesRemoved', interfaces_removed_cb)

    print('Getting objects...')
    objects = om.GetManagedObjects()
    chrcs = []

    # List characteristics found
    for path, interfaces in objects.items():
        if GATT_TX_IFACE not in interfaces.keys():
            continue
        elif GATT_RX_IFACE not in interfaces.keys():
            continue
        chrcs.append(path)

    # List sevices found
    for path, interfaces in objects.items():
        if GATT_SERVICE_IFACE not in interfaces.keys():
            continue

        chrc_paths = [d for d in chrcs if d.startswith(path + "/")]

        if process_service(path, chrc_paths):
            break

    if not tty_service:
        print('No TTY Service found')
        sys.exit(1)

    start_client()

    mainloop.run()


if __name__ == '__main__':
    main()


