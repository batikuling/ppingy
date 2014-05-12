################################################################################
#Created by: Batikuling Cruz
#Created on: 
#
#Descreption: utility class and functions for raw socket programming
################################################################################


import struct


class IPHeader(object):
    """
    this class represents the header of an IP packet
    each info from the header is available as an attr of the instance of this
    class
    """
    def __init__(self, packet):
        """
        packet : any byte object whose first 20 bytes is an IP header
        """
        header = packet[:20]
        
        temp, self.service_type, self.total_len,\
        self.id, self.flags, self.ttl, self.protocol,\
        self.checksum, self.sourceaddr,\
        self.destaddr = struct.unpack('!BBHHHBBHII', header)

        self.version = temp >> 4
        self.header_len = temp & 0b1111
        

def get_header(packet):
    """
    paket : any byte from the network; a packet, duh!

    returns an IPHeader object and the bytes not included as
    a header(the message)
    """
    ipheader = IPHeader(packet)

    return ipheader

