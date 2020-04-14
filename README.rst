*********************
TCPWave's IPAM Client
*********************
Python client for communication with Tcpwave's IPAM.

Pre-requisites
##############
Basic Authentication is not supported. Only certificates based authentication is supported.
So client must have a proper certificate and these certificates must be added to IPAM.\

Certificate files required:

* client certificate.
* client key.

Supported Operations
####################
Following operations are supported:

* Create/list/detail/delete Network
* Create/list/detail/delete Subnet
* Fetches Next Available IP in the Subnet
* Create/delete IP Object

Installing library
##################
Run below command from python virtual environment::

    pip install tcpwave-client

Sample Examples
###############

Create Network
**************
Below is a complete program showing the use of this library.\
This example shows how to create network in IPAM using this library::

    from client.networks import NetworkManager
    from client.exceptions import APICallFailedException
    import json

    def create_network():
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

    if __name__ == "__main__":
        provider = {
            'cert': '/path/to/cert/client.crt',
            'key': '/path/to/key/client.key',
            'host': '192.168.0.116'
        }
        create_network()


List Network
************
This snippet shows only the complete payload required for thr API call to work for listing all networks::

    def networks_list():
        """
        List all networks
        :return:
        """
        try:
            list_payload = {
                'provider': {
                    'cert': '/path/to/client.crt',
                    'key': '/path/to/client.key',
                    'host': '192.168.0.116'
                }
            }
            rsp = NetworkManager.list_all_networks(network=json.dumps(list_payload))
            print("Networks Count : " + str(len(rsp)))
            for i in range(0, len(rsp)):
                print(str(rsp[i]))
        except APICallFailedException as ex:
            print(ex.msg)

Delete Network
**************
This example shows the deletion of a network::

    def test_network_delete():
        """
        Deletes given network
        :return:
        """
        try:
            nw_create_payload = {
                'address': '153.168.0.0/16',
                'organization_name': 'Tcpwave',
                'provider': {
                    'cert': '/path/to/client.crt',
                    'key': '/path/to/client.key',
                    'host': '192.168.0.116'
                }
            }
            rsp = NetworkManager.delete_network(network=json.dumps(nw_create_payload))
            print(str(rsp))
        except APICallFailedException as ex:
            print(ex.msg)


Create Subnet
*************
This example shows creation of a subnet::

    def subnet_create():
        """
        Creates test subnet
        :return:
        """
        try:
            subnet_payload = {
                'provider': {
                    'cert': '/path/to/client.crt',
                    'key': '/path/to/client.key',
                    'host': '192.168.0.116'
                },
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


Next Free IP
************
This fetch the next free IP::

    def next_available_ip():
        """
        Fetches next available ip
        :return:
        """
        try:
            subnet_payload = {
                'provider': {
                    'cert': '/path/to/client.crt',
                    'key': '/path/to/client.key',
                    'host': '192.168.0.116'
                },
                'organization_name': 'Tcpwave',
                'subnet_address': '153.168.0.0/16'
            }
            rsp = NetworkManager.get_next_available_ip(subnet=json.dumps(subnet_payload))
            print('Next available IP : ', str(rsp))
            return str(rsp)
        except APICallFailedException as ex:
            print(ex.msg)


Creates IP Object
*****************
This example shows creating an object.::

    def create_object():
        """
        Creates IP Object
        :return:
        """
        try:
            ip_payload = {
                'provider': {
                    'cert': '/path/to/client.crt',
                    'key': '/path/to/client.key',
                    'host': '192.168.0.116'
                },
                'organization_name': 'Tcpwave',
                'subnet_address': '153.168.0.0/16',
                'ip_address': '153.168.0.5',
                'name': 'tst obj  1',
                'domain_name': 'test.tcpwave.com'

            }
            rsp = NetworkManager.create_ip(ip_payload=json.dumps(ip_payload))
            print(str(rsp))
        except APICallFailedException as ex:
            print(ex.msg)

Deletes Object
**************
This example shows deletion of an object::

    def delete_object(ip):
        """
        Releases the ip
        :return:
        """
        try:
            ip_payload = {
                'provider': {
                    'cert': '/path/to/client.crt',
                    'key': '/path/to/client.key',
                    'host': '192.168.0.116'
                },
                'organization_name': 'Tcpwave',
                'ip_address': ip
            }
            rsp = NetworkManager.release_ip(ip_payload=json.dumps(ip_payload))
            print(str(rsp))
        except APICallFailedException as ex:
            print(ex.msg)
