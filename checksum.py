################################################################################
#Created by:    Batikuling Cruz
#Created on:    
#Version:       
#Descreption:    
################################################################################

import struct, socket, sys, time

def checksum(data):
    """
        returns the checksum of the data bytes in
        network unsigned short form

        The checksum is computed per 16 bits(2 bytes)
        and if the sum exceeds, it is truncated
    """


    csum = 0

    #decode the data based on endianess
    if sys.byteorder == 'little':
        #print("little endian")
        s = struct.Struct("<H")
    else:
        #print("big endian")
        s = struct.Struct(">H")

    
    if len(data) % 2 != 0: #if odd, do not include last byte
        up_to = len(data) - 1
    else:
        up_to = len(data)

    #go over every 2 bytes and add each result        
    for i in range(0, up_to, 2):
        d = data[i : i + 2]
        csum += s.unpack(d)[0]

    if len(data) % 2 != 0:
        csum += data[-1]

    #convert sum to 32 bits
    #csum &= 0xffffffff

    #if bits is more than 16, convert to 16 bits only
    first_16 = csum >> 16
    last_16 = csum & 0xffff
    csum = first_16 + last_16
    
    #invert checksum and truncate to 16 bits
    csum = ~csum & 0xffff

    return socket.htons(csum)
    



if __name__ == '__main__':

    print(checksum(struct.pack("!III", 10, 20, 30)))
    print(sys.byteorder)
