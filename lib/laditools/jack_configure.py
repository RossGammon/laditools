# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2007-2008, Marc-Olivier Barre and Nedko Arnaudov.
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

import dbus

name_base = 'org.jackaudio'
controller_interface_name = name_base + '.JackConfigure'
service_name = name_base + '.service'

def dbus_type_to_python_type(dbus_value):
    if type(dbus_value) == dbus.Boolean:
        return bool(dbus_value)
    if type(dbus_value) == dbus.Int32 or type(dbus_value) == dbus.UInt32:
        return int(dbus_value)
    if type(dbus_value) == dbus.String:
        return str(dbus_value)
    if type(dbus_value) == dbus.Byte:
        return str(dbus_value)
    return dbus_value

class jack_configure:
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.controller = self.bus.get_object(service_name, "/org/jackaudio/Controller")
        self.iface = dbus.Interface(self.controller, controller_interface_name)

    def get_available_driver(self):
        return self.iface.GetAvailableDrivers()

    def get_selected_driver(self):
        return self.iface.GetSelectedDriver()
    
    def select_driver(self, driver):
        self.iface.SelectDriver(driver)

    def get_driver_param_names(self):
        infos = self.iface.GetDriverParametersInfo()
        names = []
        for info in infos:
            names.append(info[1])
        return names

    def get_driver_short_description(self, param):
        type_char, name, short_descr, long_descr = self.iface.GetDriverParameterInfo(param)
        return short_descr

    def get_driver_long_description(self, param):
        type_char, name, short_descr, long_descr = self.iface.GetDriverParameterInfo(param)
        return long_descr

    def get_driver_param_type(self, param):
        type_char, name, short_descr, long_descr = self.iface.GetDriverParameterInfo(param)
        return str(type_char)

    def get_driver_param_value(self, param):
        isset, default, value = self.iface.GetDriverParameterValue(param)
        isset = bool(isset)
        default = dbus_type_to_python_type(default)
        value = dbus_type_to_python_type(value)
        return isset, default, value

    def set_driver_param_value(self, param, value):
        typestr = self.get_driver_param_type(param)
        if typestr == "b":
            value = dbus.Boolean(value)
        elif typestr == "y":
            value = dbus.Byte(value)
        elif typestr == "i":
            value = dbus.Int32(value)	
        elif typestr == "u":
            value = dbus.UInt32(value)
        self.iface.SetDriverParameterValue(param, value)

    def driver_param_has_range(self, param):
        is_range, is_strict, is_fake_value, values = self.iface.GetDriverParameterConstraint(param)
        return bool(is_range)

    def driver_param_has_enum(self, param):
        is_range, is_strict, is_fake_value, values = self.iface.GetDriverParameterConstraint(param)
        return not is_range and len(values) != 0

    def driver_param_is_strict_enum(self, param):
        is_range, is_strict, is_fake_value, values = self.iface.GetDriverParameterConstraint(param)
        return is_strict

    def driver_param_is_fake_value(self, param):
        is_range, is_strict, is_fake_value, values = self.iface.GetDriverParameterConstraint(param)
        return is_fake_value

    def driver_param_get_enum_values(self, param):
        is_range, is_strict, is_fake_value, dbus_values = self.iface.GetDriverParameterConstraint(param)
        values = []

        if not is_range and len(dbus_values) != 0:
            for dbus_value in dbus_values:
                values.append([dbus_type_to_python_type(dbus_value[0]), dbus_type_to_python_type(dbus_value[1])])

        return values

    def get_engine_param_names(self):
        infos = self.iface.GetEngineParametersInfo()
        names = []
        for info in infos:
            names.append(info[1])
        return names

    def get_engine_short_description(self, param):
        type_char, name, short_descr, long_descr = self.iface.GetEngineParameterInfo(param)
        return short_descr

    def get_engine_long_description(self, param):
        type_char, name, short_descr, long_descr = self.iface.GetEngineParameterInfo(param)
        return long_descr

    def get_engine_param_type(self, param):
        type_char, name, short_descr, long_descr = self.iface.GetEngineParameterInfo(param)
        return str(type_char)

    def get_engine_param_value(self, param):
        isset, default, value = self.iface.GetEngineParameterValue(param)
        isset = bool(isset)
        default = dbus_type_to_python_type(default)
        value = dbus_type_to_python_type(value)
        return isset, default, value

    def set_engine_param_value(self, param, value):
        typestr = self.get_engine_param_type(param)
        if typestr == "b":
            value = dbus.Boolean(value)
        elif typestr == "y":
            value = dbus.Byte(value)
        elif typestr == "i":
            value = dbus.Int32(value)
        elif typestr == "u":
            value = dbus.UInt32(value)
        self.iface.SetEngineParameterValue(param, value)
