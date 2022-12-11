from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    
    def doPort():
      ip = packet.find('ipv4')
      src = str(ip.srcip)
      dst = str(ip.dstip)
      port = 10

      if(switch_id == 0):
        port = 0

      if(switch_id == 1):
        if dst == '10.0.51.1':
          port = 1
        elif dst == '10.0.55.5' or dst == '10.0.56.6' or dst == '160.114.50.20':
          port = 2
        elif dst == '10.0.52.2' or dst == '10.0.53.3' or dst == '10.0.54.4':
          port = 2
        
      if(switch_id == 2):
        if dst == '10.0.52.2':
          port = 1
        elif dst == '10.0.55.5' or dst == '10.0.56.6' or dst == '160.114.50.20':
          port = 2
        elif dst == '10.0.51.1' or dst == '10.0.53.3' or dst == '10.0.54.4':
          port = 2
      
      if(switch_id == 3):
        if dst == '10.0.53.3':
          port = 1
        elif dst == '10.0.55.5' or dst == '10.0.56.6' or dst == '160.114.50.20':
          port = 2
        elif dst == '10.0.51.1' or dst == '10.0.52.2' or dst == '10.0.54.4':
          port = 2
      
      if(switch_id == 4):
        if dst == '10.0.54.4':
          port = 1
        elif dst == '10.0.55.5' or dst == '10.0.56.6' or dst == '160.114.50.20':
          port = 2
        elif dst == '10.0.51.1' or dst == '10.0.52.2' or dst == '10.0.53.3':
          port = 2
   
      if(switch_id == 5):
        if dst == '10.0.51.1':
          port = 1
        elif dst == '10.0.52.2':
          port = 2
        elif dst == '10.0.53.3':
          port = 3
        elif dst == '10.0.54.4':
          port = 4
        elif dst == '160.114.50.20':
          port = 5
        elif dst == '10.0.55.5' or dst == '10.0.56.6':
          port = 6
        
      if(switch_id == 6):
        if dst == '10.0.55.5':
          port = 2
        elif dst == '10.0.56.6':
          port = 3
        elif dst == '160.114.50.20' or dst == '10.0.51.1' or dst == '10.0.52.2' or dst == '10.0.53.3' or dst == '10.0.54.4':
          port = 1
        


      return port


    def accept():
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.actions.append(of.ofp_action_output(port=doPort()))
      msg.idle_timeout = 30
      msg.hard_timeout = 30
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)

    def acceptflood():
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      msg.idle_timeout = 30
      msg.hard_timeout = 30
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)

    def drop():
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 30
      msg.hard_timeout = 30
      self.connection.send(msg)



    ip = packet.find('ipv4')
    if(ip):
      src = str(ip.srcip)
      dst = str(ip.dstip)
    else:
      src = ''
      dst = ''

    icmp = packet.find('icmp')
    tcp = packet.find('tcp')
    arp = packet.find('arp')
    udp = packet.find('udp')
    
    if (arp):
      acceptflood()
    elif (icmp):
      if src == '160.114.50.20':
        drop()
      else:
        accept()
    elif (tcp or udp):
      if src == '160.114.50.20':
        if(dst == '10.0.55.5' or dst == '10.0.56.6'):
          drop()
        else:
          accept()
      else:
        accept()
    else:
      drop()

    

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
