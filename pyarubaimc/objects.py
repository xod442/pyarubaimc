#!/usr/bin/env python3
# coding=utf-8
# author: @netmanchris
# -*- coding: utf-8 -*-
"""
This module contains class objects for working with the specific types of network
infrastructure equipment in the aruba IMC NMS using the RESTful API. These objects
rely on various other functions from within this library.

"""

# This section imports required libraries
from pyarubaimc.plat.device import *
from pyarubaimc.plat.alarms import *

from pyarubaimc.auth import HEADERS


# IMC Device Class


class IMCDev:
    """
    imc_dev class takes in the ip_address which is used as the primary key to gather
    the following attributes
    for a device which as been previously discovered in the HP IMC Network Management
    platform.

     Each instance of this class should have the following attributes

     ip: The IP address used to manage the device in HP IMC
     description: returns the description of the device as discovered in HP IMC
     location: returns the location of the device as discovered in HP IMC
     contact: returns the contact of the device as discovered in HP IMC
     type: returns the type of the device as discovered in HP IMC
     name: returns the name of the device as discovered in HP IMC
     status: returns the current alarm status as discovered in HP IMC
     devid: returns the current devid used to internally identify the device
     as discovered in HP IMC
     interfacelist: returns the current list of interfaces for the device as
     discovered in HP IMC
     numinterface: returns a count of the number of interfaces in the interfacelist
     attribute
     vlans: returns the current vlans existing in the device as discovered in HP IMC.
     Device must be supported in the HP IMC Platform VLAN manager module.
     accessinterfaces: returns the device interfaces configured as access interfaces.
     Device must be supported in the HP IMC Platform VLAN manager module.
     trunkinterfaces: returns the device interfaces configured as trunk interfaces.
     Device must be supported in the HP IMC Platform VLAN manager module.
     alarm: returns the current unrecovered alarms as known by HP IMC.
     num alarms: returns a count of the number of alarms as returned by the alarm
     attribute
     serial: returns the network assets, including serial numbers for the device as
     discovered by HP IMC. The device must support the ENTITY MIB ( rfc 4133 ) for
     this value to be returned.
     runconfig: returns the most recent running configuration for the device as known
     by HP IMC. The device must be be supported in the HP IMC platform ICC module.
     startconfig: returns the most recent startup configuration for the device as known
     by HP IMC. The device must be supported in the HP IMC platform ICC module.
     ipmacarp: returns the current device maciparp table as discovered by HP IMC.

     The imc_dev class supports the following methods which can be called upon an instance of
     this class

     getvlans: This method executes the getvlans function on the specific instance of the imc_dev
     object and populates the return into the self.vlans attribute. Devices must be supported in
     the aruba IMC Platform VLAN Manager module
     addvlan: This method executes the addvlan function on the specific instance of the imc_dev
     object. Devices must supported in the HP IMC Platform VLAN Manager module.

     """


    def __init__(self, ip_address, auth, url):
        """
        Function take in input of ipv4 address, auth and url and returns and object of type IMCDev
        :param ip_address: valid IPv4 address
        :param auth: requests auth object #usually auth.creds from auth pyarubaimc.auth.class
        :param url: base url of IMC RS interface #usually auth.url from pyarubaimc.auth.authclass
        :return IMCDev object
        :rtype IMCDev
        """
        self.auth = auth
        self.url = url
        self.dev_details = get_dev_details(ip_address, auth, url)
        self.ip = self.dev_details['ip']
        self.description = self.dev_details['sysDescription']
        self.location = self.dev_details['location']
        self.contact = self.dev_details['contact']
        self.type = self.dev_details['typeName']
        self.name = self.dev_details['sysName']
        self.status = self.dev_details['statusDesc']
        self.devid = self.dev_details['id']
        self.interfacelist = get_all_interface_details(auth, url, devip=self.ip)
        self.numinterface = len(self.interfacelist)
        self.vlans = get_dev_vlans(auth, url, devid=None, devip=self.ip)
        self.accessinterfaces = get_device_access_interfaces(auth, url, devip=self.ip)
        self.trunkinterfaces = get_trunk_interfaces(auth, url, devip = self.ip)
        self.alarm = get_dev_alarms(auth, url, devip = self.ip)
        self.numalarm = len(self.alarm)
        self.assets = get_dev_asset_details(self.ip, auth, url)
        self.serials = [({'name': asset['name'], 'serialNum': asset['serialNum']}) for asset in
                         self.assets]
        self.runconfig = get_dev_latest_run_config(auth, url, devip = self.ip)
        self.startconfig = get_dev_latest_start_config(auth, url, devip = self.ip)
        self.ipmacarp = get_ip_mac_arp_list(auth, url, devip = self.ip)

    def getvlans(self):
        """
        Function operates on the IMCDev object and updates the vlans attribute
        :return:
        """
        self.vlans = get_dev_vlans( self.auth, self.url, devid=self.devid)

    def addvlan(self, vlanid, vlan_name):
        """
        Function operates on the IMCDev object. Takes input of vlanid (1-4094), str of vlan_name,
        auth and url to execute the create_dev_vlan method on the IMCDev object. Device must be
        supported in the aruba IMC Platform VLAN Manager module.
        :param vlanid: str of VLANId ( valid 1-4094 )
        :param vlan_name: str of vlan_name
        :return:
        """
        create_dev_vlan( vlanid, vlan_name, self.auth, self.url, devid = self.devid)

    def delvlan(self, vlanid):
        """
        Function operates on the IMCDev object. Takes input of vlanid (1-4094),
        auth and url to execute the delete_dev_vlans method on the IMCDev object. Device must be
        supported in the aruba IMC Platform VLAN Manager module.
        :param vlanid: str of VLANId ( valid 1-4094 )
        :return:
        """
        delete_dev_vlans( vlanid, self.auth, self.url, devid = self.devid)

    def getipmacarp(self):
        """
        Function operates on the IMCDev object and updates the ipmacarp attribute
        :return:
        """
        self.ipmacarp = get_ip_mac_arp_list(self.auth, self.url, devid = self.devid)


class IMCInterface:
    """
    Class instantiates an object to gather and manipulate attributes and methods of a single
    interface on a single infrastructure device, such as a switch or router.
    """

    def __init__(self, ip_address, ifindex, auth, url):
        self.auth = auth
        self.url = url
        self.dev_details = get_dev_details(ip_address, auth, url)
        self.ip = self.dev_details['ip']
        self.devid = self.dev_details['id']
        self.sysdescription = self.dev_details['sysDescription']
        self.location = self.dev_details['location']
        self.contact = self.dev_details['contact']
        self.type = self.dev_details['typeName']
        self.sysname = self.dev_details['sysName']
        self.status = self.dev_details['statusDesc']
        self.interface_details = get_interface_details(ifindex, self.auth, self.url, devip=self.ip)
        self.ifIndex = self.interface_details['ifIndex']
        self.macaddress = self.interface_details[
            'phyAddress']
        self.status = self.interface_details['statusDesc']
        self.adminstatus = self.interface_details[
            'adminStatusDesc']
        self.name = self.interface_details['ifDescription']
        self.description = self.interface_details[
            'ifAlias']
        self.mtu = self.interface_details['mtu']
        self.speed = self.interface_details['ifspeed']
        self.accessinterfaces = get_device_access_interfaces(self.auth, self.url, devip = self.ip)
        self.pvid = get_access_interface_vlan(self.ifIndex, self.accessinterfaces)
        self.lastchange = self.interface_details['lastChange']

    def down(self):
        """
        Function operates on the IMCInterface object and configures the interface into an
        administratively down state and refreshes contents of self.adminstatus
        :return:
        """
        set_interface_down(self.ifIndex, self.auth, self.url, devip=self.ip)
        self.adminstatus = get_interface_details(self.ifIndex, self.auth, self.url, devip=self.ip)[
            'adminStatusDesc']

    def up(self):
        """
                Function operates on the IMCInterface object and configures the interface into an
                administratively up state and refreshes contents of self.adminstatus
                :return:
                """
        set_interface_up(self.ifIndex, self.auth, self.url, devip=self.ip)
        self.adminstatus = get_interface_details(self.ifIndex, self.auth, self.url, devip=self.ip)[
            'adminStatusDesc']


# TODO refactor deallocateIp method for human consumption
# TODO Add real_time_locate functionality to nextfreeip method to search IP address before offering

class IPScope:
    """
        Class instantiates an object to gather and manipulate attributes and methods of a IP
        scope as configured in the aruba IMC Platform Terminal Access module. Note: IPScope must already exist.
        """

    def __init__(self, netaddr, auth, url):
        self.id = get_scope_id(netaddr, auth, url)
        self.details = get_ip_scope_detail(auth, url, self.id)
        self.hosts = get_ip_scope_hosts(auth, url, self.id)
        self.auth = auth
        self.url = url
        self.netaddr = ipaddress.ip_network(netaddr)
        self.startip = get_ip_scope_detail(auth, url, self.id)['startIp']
        self.endip = get_ip_scope_detail(auth, url, self.id)['endIp']
        if 'assignedIpScope' in self.details:
            self.child = get_ip_scope_detail(auth, url, self.id)['assignedIpScope']

    def allocate_ip(self, hostipaddress, name, description):
        """
        Object method takes in input of hostipaddress, name and description and adds them to the
        parent ip scope.
        :param hostipaddress: str of ipv4 address of the target host ip record
        :param name: str of the name of the owner of the target host ip record
        :param description: str of a description of the target host ip record
        :return:
        """
        add_scope_ip(hostipaddress, name, description, self.auth, self.url, scopeid=self.id)

    def deallocate_ip(self, hostipaddress):
        """
        Object method takes in input of hostip address,removes them from the parent ip scope.
        :param hostid: str of the hostid of  the target host ip record

        :return:
        """
        delete_host_from_segment(hostipaddress, self.netaddr, self.auth, self.url)

    def gethosts(self):
        """
        Method gets all hosts currently allocated to the target scope and refreashes the self.hosts
        attributes of the object
        :return:
        """
        self.hosts = get_ip_scope_hosts(self.auth, self.url, self.id)

    def nextfreeip(self):
        """
        Method searches for the next free ip address in the scope object and returns it as a str
        value.
        :return:
        """
        allocated_ips = [ipaddress.ip_address(host['ip']) for host in self.hosts]
        for ip in self.netaddr:
            if str(ip).split('.')[-1] == '0':
                continue
            if ip not in allocated_ips:
                return ip

    def addchild(self, startip, endip, name, description):
        """
        Method takes inpur of str startip, str endip, name, and description and adds a child scope.
        The startip and endip MUST be in the IP address range of the parent scope.
        :param startip: str of ipv4 address of the first address in the child scope
        :param endip: str of ipv4 address of the last address in the child scope
        :param name: of the owner of the child scope
        :param description: description of the child scope
        :return:
        """
        add_child_ip_scope(self.auth, self.url, startip, endip, name, description, self.id)
