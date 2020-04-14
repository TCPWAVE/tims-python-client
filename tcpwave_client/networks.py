import ipaddress
import json
import re

from tcpwave_client import Connector


class NetworkManager(object):
    """
    This class will house all operations that can be
    performed on a network
    """
    @classmethod
    def create_network(cls, network):
        """
        Create network with the given ip.
        :param network:
        :return:
        """
        network_obj = json.loads(network)
        address = network_obj['network_address']
        cert = network_obj['provider']['cert']
        key = network_obj['provider']['key']
        network_address = ipaddress.ip_network(address, strict=False)
        mask_len = network_address.prefixlen
        network_ip = str(network_address.network_address)
        ips = network_ip.split(".")
        payload = {
            "body": {
                "address": network_ip,
                "addr1": str(ips[0]),
                "addr2": str(ips[1]),
                "addr3": str(ips[2]),
                "addr4": str(ips[3]),
                "mask_length": mask_len,
                "organization_id": network_obj.get("organization_id") or "",
                "organization_name": network_obj.get("organization_name") or "",
                "name": network_obj["name"],
                "description": network_obj.get("description") or "",
                "createRevZone": network_obj.get("createRevZone") or "no",
                "dmzVisible": network_obj.get("dmzVisible") or "no",
                "dnssec_enable": network_obj.get("dnssec_enable") or "no",
                "nsec_option": network_obj.get("nsec_option") or "NSEC3",
                "monitoringService": network_obj.get("monitoringService") or "no",
                "enable_discovery": network_obj.get("enable_discovery") or "no",
                "discovery_template": network_obj.get("discovery_template") or "",
                "region": network_obj.get("region") or "",
                "percentageFull": network_obj.get("percentageFull") or 100,
                "email_check": network_obj.get("email_check") or 1,
                "snmp_check": network_obj.get("snmp_check") or 0,
                "log_check": network_obj.get("log_check") or 0,
                "rrs": network_obj.get("rrs") or [],
                "zoneTemplateId": network_obj.get("zoneTemplateId") or "",
                "zoneTemplateName": network_obj.get("zoneTemplateName") or "",
                "extensions": network_obj.get("extensions") or []
            },
            "method": "POST",
            "rel_url": "/network/add",
            "headers": {
                "Content-Type": "application/json",
                "Accept-Type": "application/json"
            },
            'provider': network_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.create_object(payload=payload)
        return rsp

    @classmethod
    def get_network_detail(cls, network):
        """
        Given a network ip get all the details.
        :param network:
        :return:
        """
        network_obj = json.loads(network)
        ip_address = str(network_obj["network_address"])
        network_address = ipaddress.ip_network(ip_address, strict=False)
        network_ip = str(network_address.network_address)
        ip_bits = network_ip.split(".")
        cert = network_obj['provider']['cert']
        key = network_obj['provider']['key']
        payload = {
            "method": "GET",
            "rel_url": "/network/detailsByIP",
            "headers": {
                "Content-Type": "text/plain",
                "Accept-Type": "application/json"
            },
            "params": {
                "organizationName": network_obj['organization_name'],
                "addr1": ip_bits[0],
                "addr2": ip_bits[1],
                "addr3": ip_bits[2],
                "addr4": ip_bits[3],
                "address": ip_address
            },
            'provider': network_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.get_object(payload=payload)
        return rsp

    @classmethod
    def list_all_networks(cls, network):
        """
        List all networks visible to the user.
        :return:
        """
        network_obj = json.loads(network)
        cert = network_obj['provider']['cert']
        key = network_obj['provider']['key']
        page_size = 100
        payload = {
            "method": "GET",
            "rel_url": "/network/paged",
            "headers": {
                "Content-Type": "text/plain",
                "Accept-Type": "application/json"
            },
            "params": {
                "start": 0,
                "length": page_size,
                "sort": "name",
                "order": "asc"
            },
            'provider': network_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.get_object(payload=payload)
        total = rsp.get("recordsTotal")
        if total % page_size > 0:
            pages = 1
        else:
            pages = 0
        pages += total//page_size
        res = list()
        res.extend(rsp.get("data"))
        for i in range(1, pages):
            payload["params"]["start"] = i * page_size
            rsp = conn.get_object(payload=payload)
            res.extend(rsp.get("data"))

        return res

    @classmethod
    def delete_network(cls, network):
        """
        Deletes the given network
        :param network:
        :return:
        """
        network_obj = json.loads(network)
        address = network_obj['address']
        org = network_obj['organization_name']
        cert = network_obj['provider']['cert']
        key = network_obj['provider']['key']
        payload = {
            "body": {
                "address": str(address),
                "organization_name": org,
                "id": network_obj.get("id") or ""
            },
            "method": "POST",
            "rel_url": "/network/delete",
            "headers": {
                "Content-Type": "application/json",
                "Accept-Type": "application/json"
            },
            'provider': network_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.delete_object(payload=payload)
        return rsp

    @classmethod
    def create_subnet(cls, subnet):
        """
        Creates the given subnet in the given network
        :param subnet:
        :return:
        """
        subnet_obj = json.loads(subnet)
        n_address = subnet_obj['network_address']
        cert = subnet_obj['provider']['cert']
        key = subnet_obj['provider']['key']
        network_address = ipaddress.ip_network(n_address, strict=False)
        mask_len = network_address.prefixlen
        network_ip = str(network_address.network_address)
        ips = network_ip.split(".")
        payload = {
            "body": {
                "network_address": network_ip,
                "addr1": str(ips[0]),
                "addr2": str(ips[1]),
                "addr3": str(ips[2]),
                "addr4": str(ips[3]),
                "network_mask": mask_len,
                "mask_length": mask_len,
                "organization_id": subnet_obj.get("organization_id") or "",
                "organization_name": subnet_obj.get("organization_name") or "",
                "name": subnet_obj["name"],
                "description": subnet_obj.get("description") or "",
                "createRevZone": subnet_obj.get("createRevZone") or "no",
                "dmzVisible": subnet_obj.get("dmzVisible") or "no",
                "dnssec_enable": subnet_obj.get("dnssec_enable") or "no",
                "nsec_option": subnet_obj.get("nsec_option") or "NSEC3",
                "monitoringService": subnet_obj.get("monitoringService") or "no",
                "enable_discovery": subnet_obj.get("enable_discovery") or "no",
                "discovery_template": subnet_obj.get("discovery_template") or None,
                "network_id": subnet_obj.get("network_id") or None,
                "primary_domain": subnet_obj["primary_domain"],
                "routerAddress": subnet_obj["router_address"],
                "primary_dhcp_server": subnet_obj.get("primary_dhcp_server") or None,
                "template_id": subnet_obj.get("template_id") or None,
                "cloudProviderId": subnet_obj.get("cloudProviderId") or None,
                "zoneTemplateName": subnet_obj.get("zoneTemplateName") or None,
                "extensions": subnet_obj.get("extensions") or []
            },
            "method": "POST",
            "rel_url": "/subnet/add",
            "headers": {
                "Content-Type": "application/json",
                "Accept-Type": "application/json"
            },
            'provider': subnet_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.create_object(payload=payload)
        return rsp

    @classmethod
    def get_subnet_detail(cls, subnet):
        """
        Given a subnet ip get all the details.
        :param subnet
        :return:
        """
        subnet_obj = json.loads(subnet)
        cert = subnet_obj['provider']['cert']
        key = subnet_obj['provider']['key']
        subnet_address = ipaddress.ip_network(subnet_obj['subnet_address'], strict=False)
        payload = {
            "method": "GET",
            "rel_url": "/subnet/getSubnetData",
            "headers": {
                "Content-Type": "text/plain",
                "Accept-Type": "application/json"
            },
            "params": {
                "subnet_address": str(subnet_address.network_address),
                "org_name": subnet_obj['organization_name']
            },
            'provider': subnet_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.get_object(payload=payload)
        return rsp

    @classmethod
    def list_all_subnets(cls, subnet):
        """
        List all Subnets visible to the user.
        :param subnet
        :return:
        """
        subnet_obj = json.loads(subnet)
        cert = subnet_obj['provider']['cert']
        key = subnet_obj['provider']['key']
        network_address = ipaddress.ip_network(subnet_obj['network_address'], strict=False)
        page_size = 100
        payload = {
            "method": "GET",
            "rel_url": "/subnet/paged",
            "headers": {
                "Content-Type": "text/plain",
                "Accept-Type": "application/json"
            },
            "params": {
                "network_address": str(network_address.network_address),
                "org_name": subnet_obj['organization_name'],
                "start": 0,
                "length": page_size,
                "sort": "fullAddress",
                "order": "asc"
            },
            'provider': subnet_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.get_object(payload=payload)
        total = rsp.get("recordsTotal")
        if total % page_size > 0:
            pages = 1
        else:
            pages = 0
        pages += total//page_size
        res = list()
        res.extend(rsp.get("data"))
        for i in range(1, pages):
            payload["params"]["start"] = i * page_size
            rsp = conn.get_object(payload=payload)
            res.extend(rsp.get("data"))

        return res

    @classmethod
    def delete_subnet(cls, subnet):
        """
        Deletes the given subnet
        :param subnet:
        :return:
        """
        subnet_obj = json.loads(subnet)
        address_list = subnet_obj['address_list']
        org = subnet_obj['organization_name']
        cert = subnet_obj['provider']['cert']
        key = subnet_obj['provider']['key']
        payload = {
            "body": {
                "addressList": address_list,
                "organizationName": org,
                "isDeleterrsChecked": 1
            },
            "method": "POST",
            "rel_url": "/subnet/delete",
            "headers": {
                "Content-Type": "application/json",
                "Accept-Type": "application/json"
            },
            'provider': subnet_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.delete_object(payload=payload)
        return rsp

    @classmethod
    def get_next_available_ip(cls, subnet):
        """
        Return next free ip in given network and subnet.
        :param subnet:
        :return:
        """
        subnet_obj = json.loads(subnet)
        subnet_address = ipaddress.ip_network(subnet_obj['subnet_address'], strict=False)
        cert = subnet_obj['provider']['cert']
        key = subnet_obj['provider']['key']
        payload = {
            "method": "GET",
            "rel_url": "/object/getNextFreeIP",
            "headers": {
                "Content-Type": "text/plain",
                "Accept-Type": "application/json"
            },
            "params": {
                "org_name": subnet_obj['organization_name'],
                "subnet_addr": str(subnet_address.network_address)
            },
            'provider': subnet_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.get_object(payload=payload)
        return rsp.decode("utf-8")

    @classmethod
    def release_ip(cls, ip_payload):
        """
        Deletes the ip object.
        :param ip_payload:
        :return:
        """
        ip_obj = json.loads(ip_payload)
        ip_address = str(ip_obj["ip_address"])
        cert = ip_obj['provider']['cert']
        key = ip_obj['provider']['key']
        payload = {
            "method": "POST",
            "rel_url": "/object/reclaimObjects",
            "headers": {
                "Content-Type": "application/json",
                "Accept-Type": "application/json"
            },
            "body": {
                "organization_name": ip_obj['organization_name'],
                "isDeleterrsChecked": 0,
                "addressArray": [ip_address]
            },
            'provider': ip_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.delete_object(payload=payload)
        return rsp

    @classmethod
    def create_ip(cls, ip_payload):
        """
        Creates the ip object.
        :param ip_payload:
        :return:
        """
        ip_obj = json.loads(ip_payload)
        ip_address = ipaddress.ip_network(ip_obj["ip_address"], strict=False)
        ip_bits = str(ip_address.network_address).split(".")
        subnet_ip = ipaddress.ip_network(ip_obj["subnet_address"], strict=False)
        cert = ip_obj['provider']['cert']
        key = ip_obj['provider']['key']
        obj_name = ip_obj['name']
        obj_name = re.sub(r'\s+', '-', obj_name)
        payload = {
            "method": "POST",
            "rel_url": "/object/add",
            "headers": {
                "Content-Type": "application/json",
                "Accept-Type": "application/json"
            },
            "body": {
                "organization_name": ip_obj['organization_name'],
                "name": obj_name,
                "address": str(ip_address.network_address),
                "addr1": str(ip_bits[0]),
                "addr2": str(ip_bits[1]),
                "addr3": str(ip_bits[2]),
                "addr4": str(ip_bits[3]),
                "class_code": ip_obj.get('class_code') or 'Others',
                "domain_name": ip_obj['domain_name'],
                "alloc_type": int(ip_obj.get('alloc_type') or '1'),
                "mac": ip_obj.get('mac') or None,
                "subnet_address": str(subnet_ip.network_address),
                "update_ns_a": ip_obj.get('update_ns_a') or True,
                "update_ns_ptr": ip_obj.get('update_ns_ptr') or True,
                "dyn_update_rrs_a": ip_obj.get('dyn_update_rrs_a') or True,
                "dyn_update_rrs_ptr": ip_obj.get('dyn_update_rrs_ptr') or True,
                "dyn_update_rrs_cname": ip_obj.get('dyn_update_rrs_cname') or True,
                "dyn_update_rrs_mx": ip_obj.get('dyn_update_rrs_mx') or True
            },
            'provider': ip_obj['provider']
        }
        conn = Connector(cert=cert, key=key)
        rsp = conn.create_object(payload=payload)
        return rsp
