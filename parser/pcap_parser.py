import dpkt
import socket
import datetime
import hexdump
import sys
from termcolor import colored


def info(filename):
	counter=0
	ipcounter=0
	tcpcounter=0
	udpcounter=0
	tcp=0
	udp=0
	for ts, pkt in dpkt.pcap.Reader(open(filename,'r')):

	    counter+=1          
	    eth = dpkt.ethernet.Ethernet(pkt) 
	    
	       
	    if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
	       continue

	    ip = eth.data
	    ipcounter+=1

	    if ip.p == dpkt.ip.IP_PROTO_TCP: 
	       tcpcounter+=1

	    if ip.p == dpkt.ip.IP_PROTO_UDP:
	       udpcounter+=1
	    
	    if ip.p == dpkt.ip.IP_PROTO_TCP:
	       tcp = ip.data
	    
	    if ip.p == dpkt.ip.IP_PROTO_UDP:
	       udp = ip.data
	                        
	print "Total number of packets in the pcap file: ", counter
	print "Total number of ip packets: ", ipcounter
	print "Total number of tcp packets: ", tcpcounter
	print "Total number of udp packets: ", udpcounter
	

	try :
		print('src port TCP:{}, dst port TCP:{}'.format(
	                        tcp.sport,
	                        tcp.dport
	                        ))
		print('src port UDP:{}, dst port UDP:{}'.format(
	                        udp.sport,
	                        udp.dport
	                        ))

	except: 	
		print "Source port not found."
	print "ip counter: ", ip.p



def packet_hexdump(filename):
	for ts, buf in dpkt.pcap.Reader(open(filename,'r')):
	    eth = dpkt.ethernet.Ethernet(buf)   
	    try:
	    	pkt=eth.data.data['data']
	    except:
	    	pkt=eth.data.data

	    if isinstance(pkt, basestring):	
	    	print hexdump.hexdump(pkt)
	    else:
	    	print str(pkt)	  


def mac_addr(address):
    return ':'.join('%02x' % compat_ord(b) for b in address)

def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def ip_info(filename):     
	for timestamp, buf in dpkt.pcap.Reader(open(filename,'r')):
	   
	    eth = dpkt.ethernet.Ethernet(buf)
	    start_date = ""
	    fmt = ""
	    start_date_dt = datetime.datetime.strptime(start_date, fmt)
	 
	    if not isinstance(eth.data, dpkt.ip.IP):
	        print 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
	        continue
	 
	    ip = eth.data

	    if isinstance(ip.data, dpkt.tcp.TCP):

	        tcp = ip.data

	        try:
	            request = dpkt.http.Request(tcp.data)
	        except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
	            continue

	        do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
	        more_fragments = bool(ip.off & dpkt.ip.IP_MF)
	        fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

	        print 'Timestamp: ', repr(datetime.datetime.utcfromtimestamp(timestamp))
	        print 'Ethernet Frame: ', repr(eth.src),repr(eth.dst), eth.type
	        print 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)' % \
	              (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset)
	        print 'HTTP request: %s\n' % repr(request)


if __name__ == "__main__":

    print colored('hello', 'red')

    print colored(
        " ____________________________________ \n|            DUMP.PCAP             |\n|               PARSER               |\n|____________________________________|",
        'red')

    while True:

	#filename='smallFlows.pcap'
        user_input = raw_input("What are you searching for ? ")
        if user_input in ["info", "inf"]:           
            info(sys.argv[2])
        elif user_input in ["hexdump"]:
            packet_hexdump(sys.argv[2])
        elif user_input in ["ipinfo"]:
            ip_info(sys.argv[2])
        elif user_input in ["done", "exit"]:
            exit()
else:
    print("PCAP.py is being imported into another module")
    info(sys.argv[2])
    packet_hexdump(sys.argv[2])
    ip_info(sys.argv[2])

    