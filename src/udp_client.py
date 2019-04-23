# UDP client
import socket
import logging
import argparse
from util import construieste_mesaj_raw
from udp_server import calculeaza_checksum

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)


def send_message(address, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_actual = socket.gethostbyname(socket.gethostname())
    port=20000
    address_act=(ip_actual,port)
    sock.bind(address_act)

    try:
        logging.info('Trimitem mesajul "%s" catre %s:%d', message, address[0], address[1])
        sock.sendto(message.encode('utf-8'), address)

        logging.info('Asteptam un raspuns...')
        data, server = sock.recvfrom(4096)
        mesaj_binar = construieste_mesaj_raw(ip_actual,server[0],port,server[1],data)
        logging.info('Content primit: "%s"', data)
        logging.info('Checksum calculat: %s', str(hex(calculeaza_checksum(mesaj_binar))))


    finally:
        logging.info('closing socket')
        sock.close()


def main():
    parser = argparse.ArgumentParser(description='Client UDP',
                                 formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--server', '-s', dest='server', action='store',
                        required=True, help='Adresa IP a serverului')
    parser.add_argument('--port', '-p', dest='port', action='store', type=int,
                        required=True, help='Portul serverului.')
    parser.add_argument('--mesaj', '-m', dest='mesaj', action='store',
                        default="", help='Mesaj de trimis prin UDP')
    args = parser.parse_args()
    server_address = (args.server, args.port)

    send_message(server_address, args.mesaj)


if __name__ == '__main__':
    main()