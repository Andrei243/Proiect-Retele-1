# UDP Server
import socket
import logging
import argparse
import struct

from util import construieste_mesaj_raw

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)



def calculeaza_checksum(mesaj_binar):
    '''
        TODO: scrieti o functie care primeste un mesaj raw de bytes
        si calculeaza checksum pentru UDP
        exemplu de calcul aici:
        https://www.securitynik.com/2015/08/calculating-udp-checksum-with-taste-of.html
    '''
    nrImpar = False
    if len(mesaj_binar) % 2 == 1:
        nrImpar = True
    nrBytes=len(mesaj_binar)//2
    if(nrImpar):
        nrBytes += 1
    bytes = []

    for i in range(nrBytes):
        if nrImpar and i == nrBytes-1:
            byte = struct.unpack("B", mesaj_binar[-1])
            byte *= 256
        else:
            byte = struct.unpack("!H", mesaj_binar[i*2: (i+1)*2])
        bytes.append(byte[0])
    checksum=0
    for i in bytes:
        checksum += i
    pad=2**16

    checksumfin=checksum%pad
    checksum=checksum/pad
    while checksum>0:
        checksumfin+=checksum%pad
        checksum/=pad

    return checksumfin



def run_server(server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    logging.info("Serverul a pornit pe %s si portnul portul %d", server_address[0], server_address[1])
    
    while True:
        logging.info('Asteptam mesaje...')
        data, address = sock.recvfrom(4096)
        
        logging.info("Am primit %s octeti de la %s", len(data), address)
        logging.info('Content primit: "%s"', data)
        mesaj_binar = construieste_mesaj_raw(address[0], server_address[0], address[1], server_address[1], data)
        valoare_numerica = calculeaza_checksum(mesaj_binar)
        valoare = hex(valoare_numerica)
        logging.info('Checksum calculat: %s', str(valoare))
        sock.sendto(str(valoare), address)
        

def main():
    parser = argparse.ArgumentParser(description='Server UDP',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--port', '-p', dest='port', action='store', type=int,
                        required=True, help='Portul serverului.')
    args = parser.parse_args()

    ip_server = socket.gethostbyname(socket.gethostname())
    server_address = (ip_server, args.port)
    run_server(server_address)


if __name__ == '__main__':
    main()
