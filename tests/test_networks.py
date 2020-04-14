from client.networks import NetworkManager
from client.exceptions import APICallFailedException
import json


def test_network_creation():
    """
    Create test network
    :return:
    """
    try:
        nw_create_payload = {
            'network_address': '153.168.0.0/16',
            'name': 'Test Network 3',
            'organization_name': 'Tcpwave',
            'provider': provider
        }
        rsp = NetworkManager.create_network(network=json.dumps(nw_create_payload))
        print(str(rsp))
    except APICallFailedException as ex:
        print(ex.msg)


def test_network_delete():
    """
    Deletes given network
    :return:
    """
    try:
        nw_create_payload = {
            'address': '153.168.0.0/16',
            'organization_name': 'Tcpwave',
            'provider': provider
        }
        rsp = NetworkManager.delete_network(network=json.dumps(nw_create_payload))
        print(str(rsp))
    except APICallFailedException as ex:
        print(ex.msg)


def test_networks_list():
    """
    List all networks
    :return:
    """
    try:
        list_payload = {
            'provider': provider
        }
        rsp = NetworkManager.list_all_networks(network=json.dumps(list_payload))
        print("Networks Count : " + str(len(rsp)))
        for i in range(0, len(rsp)):
            print(str(rsp[i]))
    except APICallFailedException as ex:
        print(ex.msg)


def test_network_detail():
    """
    Fetch network details
    :return:
    """
    try:
        list_payload = {
            'provider': provider,
            'organization_name': 'Tcpwave',
            'network_address': '153.168.0.0/16'
        }
        rsp = NetworkManager.get_network_detail(network=json.dumps(list_payload))
        print(str(rsp))
    except APICallFailedException as ex:
        print(ex.msg)


def test_subnet_create():
    """
    Creates test subnet
    :return:
    """
    try:
        subnet_payload = {
            'provider': provider,
            'organization_name': 'Tcpwave',
            'name': 'Test Subnet 1',
            'router_address': '153.168.0.1',
            'network_address': '153.168.0.0/16',
            'primary_domain': 'test.tcpwave.com'
        }
        rsp = NetworkManager.create_subnet(subnet=json.dumps(subnet_payload))
        print(str(rsp))
    except APICallFailedException as ex:
        print(ex.msg)


def test_subnet_delete():
    """
    Deletes given subnet
    :return:
    """
    try:
        subnet_payload = {
            'provider': provider,
            'organization_name': 'Tcpwave',
            'address_list': ['153.168.0.0/16']
        }
        rsp = NetworkManager.delete_subnet(subnet=json.dumps(subnet_payload))
        print(str(rsp))
    except APICallFailedException as ex:
        print(ex.msg)


def test_subnet_list():
    """
    List all subnets
    :return:
    """
    try:
        subnet_payload = {
            'provider': provider,
            'organization_name': 'Tcpwave',
            'network_address': '172.168.0.0/20'
        }
        rsp = NetworkManager.list_all_subnets(subnet=json.dumps(subnet_payload))
        print("Subnets Count : " + str(len(rsp)))
        for i in range(0, len(rsp)):
            print(str(rsp[i]))
    except APICallFailedException as ex:
        print(ex.msg)


def test_subnet_detail():
    """
    Fetch subnet details
    :return:
    """
    try:
        subnet_payload = {
            'provider': provider,
            'organization_name': 'Tcpwave',
            'subnet_address': '153.168.0.0/16'
        }
        rsp = NetworkManager.get_subnet_detail(subnet=json.dumps(subnet_payload))
        print(str(rsp))
    except APICallFailedException as ex:
        print(ex.msg)


def test_next_available_ip():
    """
    Fetches next available ip
    :return:
    """
    try:
        subnet_payload = {
            'provider': provider,
            'organization_name': 'Tcpwave',
            'subnet_address': '153.168.0.0/16'
        }
        rsp = NetworkManager.get_next_available_ip(subnet=json.dumps(subnet_payload))
        print('Next available IP : ', str(rsp))
        return str(rsp)
    except APICallFailedException as ex:
        print(ex.msg)


def test_ip_create(ip):
    """
    Creates IP Object
    :return:
    """
    try:
        ip_payload = {
            'provider': provider,
            'organization_name': 'Tcpwave',
            'subnet_address': '153.168.0.0/16',
            'ip_address': ip,
            'name': 'tst obj  1',
            'domain_name': 'test.tcpwave.com'

        }
        rsp = NetworkManager.create_ip(ip_payload=json.dumps(ip_payload))
        print(str(rsp))
    except APICallFailedException as ex:
        print(ex.msg)


def test_ip_delete(ip):
    """
    Releases the ip
    :return:
    """
    try:
        ip_payload = {
            'provider': provider,
            'organization_name': 'Tcpwave',
            'ip_address': ip
        }
        rsp = NetworkManager.release_ip(ip_payload=json.dumps(ip_payload))
        print(str(rsp))
    except APICallFailedException as ex:
        print(ex.msg)


def test_complete_flow():
    print('Creating Network : 153.168.0.0/16')
    test_network_creation()

    print("Listing all networks")
    test_networks_list()

    print("Network Details for 153.168.0.0/16")
    test_network_detail()

    print("Creating Subnet : 153.168.0.0/16")
    test_subnet_create()

    print("Listing all subnets")
    test_subnet_list()

    print("Subnet Details for 153.168.0.0/16")
    test_subnet_detail()

    print("Getting next free ip")
    ip = test_next_available_ip()

    print("creating available ip : ", ip)
    test_ip_create(ip)

    print("Getting next free ip")
    ip1 = test_next_available_ip()

    print("Deleting object ", ip)
    test_ip_delete(ip)

    print("Deleting subnet")
    test_subnet_delete()

    print("Deleting network")
    test_network_delete()


if __name__ == "__main__":
    provider = {
        'cert': 'client.crt',
        'key': 'client.key',
        'host': '192.168.0.116',
        'port': 1234
    }

    test_complete_flow()






