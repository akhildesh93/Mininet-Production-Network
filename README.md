topology.png:
  - Example production network containing hosts, switches, core, datacenter, and untrusted Host (internet traffic)

adeshmu1_final_topo.py:
  - Configures Mininet Topology based on topology.png
  - Sets up links based off source ports

adeshmu1_final_controller.py:

      Controller firewall follows the following rules:
      - All hosts are able to communicate EXCEPT
      - Untrusted Host (Internet) cannot send ICMP traffic to Host 1, Host 2, Host 3, Host 4 or the servers
      - The Untrusted Host cannot send any IP traffic to the servers
  
  - For every switch that connects, sets up a firewall object
  - For each packet, configures connection status
  - based on type of packet and its source, determines whether to accept, flood, or drop the packet
      ex. ICMP traffic from Untrusted Host is dropped
          ARP traffic from anywhere is flooded
          TCP traffic from Hosts are accepted 

      - doPort() assigns appropriate source port for a connection
      - accept() and acceptFlood() accepts a packet and sends to appropriate port
      - drop() drops a packet
  
      
  
