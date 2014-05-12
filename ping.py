################################################################################
#Created by:    Batikuling Cruz
#Version:       .1b
#Descreption:   A ping program
################################################################################


import socket, struct, time, os, signal, select

from checksum import checksum
from ipheader import *


#constants
ICMP_PROTO_NUM = 1

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

MAX_REC_SIZE = 1024 * 2



def ping(sock, dest_addr, id = os.getpid() & 0xffff, seq_num = 0,
         data = b'UNIX', timeout = 2):
    """
        sock:       the socket in this machine to use to ping
        dest_addr:  the IP address to ping
        id:         the desired id in the ICMP header
        seq_num:    also used in the ICMP header
        data:       the data to put and is echoed by the pinged address
        timeout:    the timeout before giving up on the address

        typical use: ping(socket_to_host, host_ip_in_str)

        returns (travel_time, TTL) on success and
        returns (0, 0) on failure
    """

    
    #SENDING PART
    #create ICMP header
    csum = 0
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, csum,
                         id, seq_num)

    csum = checksum(header + data)

    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, csum,
                         id, seq_num)

    #send the data
    #any exceptions recieved must be handled by the caller
    sock.sendto(header + data, (dest_addr, 1)) #port number is irrelevant

    #RECIEVING PART
    t = time.clock()
    
    ready_r, _, __ = select.select([sock], [], [], timeout)
    travel_time = time.clock() - t

    #if timedout
    if not ready_r:
        return 0, 0


    data, addr = sock.recvfrom(MAX_REC_SIZE) 

    ip_header = get_header(data)
    data = data[20:]


    return travel_time, ip_header.ttl

    

#test function
def is_alive(sock, ip_addr):

    addr = ''

    try:
        addr = socket.gethostbyname(ip_addr)
        name = socket.gethostbyaddr(addr)[0]
    except:
        name = '???'

    #in case the network is busy, try pinging 3 times
    for i in range(3):
        try:
            t, ttl = ping(sock, addr)
        except Exception as err:
            print("Failed: ", err)
            return
        
        if t:
            print("{} ({}) is alive.".format(addr, name))
            return
    

    
    #if failed in the 3 times, give up
    print("{} ({}) is not responding.".format(addr, name))
    

def main():

    dest = 'google.com' #####to be given in command line

    

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_PROTO_NUM)
    sock.settimeout(2)

    is_alive(sock, dest)


if __name__ == '__main__':
    main()
