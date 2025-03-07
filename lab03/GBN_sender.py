import socket
import pickle
import sys
import binascii

# Basic logging configuration
import logging
logging.basicConfig(format='\r[%(levelname)s: line %(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Packet class
class Packet:
    def __init__(self, seq_num: int, data: str, checksum: int) -> None:
        self.seq_num = seq_num
        self.data = data
        self.checksum = checksum


# GBN sender class
class GBN_Sender:
    def __init__(self, sender_ip: str, sender_port: int, receiver_ip: str, receiver_port: int, window_size: int, timeout: float,  data_file: str, receive_buffer_size: int) -> None:
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.window_size = window_size
        self.data_file = data_file
        self.receive_buffer_size = receive_buffer_size

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # bind the socket to the sender's IP and port
        self.sock.bind((sender_ip, sender_port))

        # Set timeout
        self.sock.settimeout(timeout)

        # Read data file
        with open(self.data_file, 'r') as f:
            self.data_buffer = f.readlines()


    def udt_send(self, sndpkt: Packet) -> None:
        logger.info('send pkt%d', sndpkt.seq_num)
        # serialize packet (necessary for sending packet object over socket)
        sndpkt = pickle.dumps(sndpkt)
        # Send packet to the receiver
       # min kode:
        self.sock.sendto(sndpkt,(self.receiver_ip, self.receiver_port))


    def make_pkt(self, nextseqnum: int, data: str, checksum: int) -> Packet:
        # Create packet
        pkt = Packet(nextseqnum, data, checksum)
        # Return packet
        return pkt


    def getacknum(self, rcvpkt: Packet) -> int:
        # Return ACK number from received packet
        return rcvpkt.seq_num

    def notcorrupt(self, rcvpkt: Packet) -> bool:
        # Check if received packet is corrupted
        checksum = self.compute_checksum(rcvpkt.seq_num, rcvpkt.data)
        return checksum == rcvpkt.checksum

    def rdt_rcv(self) -> Packet:
        # Receive ACK from receiver
        rcvpkt, addr = self.sock.recvfrom(1024)
        rcvpkt = pickle.loads(rcvpkt)
        logger.info('rcv ACK%d', self.getacknum(rcvpkt))
        return rcvpkt

    def compute_checksum(self, seqnum: int, data: str) -> int:
        # Compute checksum from bytes-like (next_seq_num and data)
        checksum = binascii.crc32((str(seqnum) + data).encode())
        return checksum


    def run(self) -> None:
        logger.info('############## Sending packets ##############')

        # Initialize variables
        # FIGURE 1, CIRCLE 1: INITIAL STATE OF GBN SENDER
        # Start with 0 to be compatible with python (0 based indexing)
        base = 0
        nextseqnum = 0

        # loop until all packets in data buffer are sent
        while base < len(self.data_buffer):

            # FIGURE 1, CIRCLE 2: rdt_send(data)
            while nextseqnum < base + self.window_size and nextseqnum < len(self.data_buffer):
                # Get data from data buffer
                data = self.data_buffer[nextseqnum]
                # checksum from bytes-like (next_seq_num and data)
                checksum = self.compute_checksum(nextseqnum, data)

                # Create packet using make_pkt()
                sndpkt = self.make_pkt(nextseqnum, data, checksum)

                # Send packet using udt_send()
                self.udt_send(sndpkt)

                if base == nextseqnum:
                    # Start timer
                    # By sending a packet through socket, it will start the socket timeout
                    pass

                # Increment next sequence number
                nextseqnum += 1

            try:
                # FIGURE 1, CIRCLE 4: rdt_rcv(rcvpkt) && notcorrupt(rcvpkt)
                # Receive ACK from receiver, using rdt_rcv()
                rcvpkt = self.rdt_rcv()
                # Check if ACK is corrupted, using notcorrupt()
                if self.notcorrupt(rcvpkt):
                    # Update base using getacknum()
                    base = self.getacknum(rcvpkt)

                    if base == nextseqnum:
                        # Stop timer
                        # We are using the socket timeout, thus when it receives ACK, it will stop the timer automatically
                        pass
                    else:
                        # Start timer
                        # By receiving a packet through socket, it will start the socket timeout
                        pass
                # FIGURE 1, CIRCLE 5: rdt_rcv(rcvpkt) && corrupt(rcvpkt)
                else:
                    # Do nothing
                    pass

            # FIGURE 1, CIRCLE 3: timeout (Note: This is an approximation only)
            except socket.timeout:
                logger.info('pkt%d timeout', base)
                # resend all packets in window
                # HINT: reset next_seq_num to base, thus when the loop continues, it will resend all packets in window in the second while loop
                nextseqnum = base 

        # After all packets are sent and ACKs are received, send EOT packet
        data = 'EOT'
        checksum = self.compute_checksum(nextseqnum, data)
        # Create EOT packet, using make_pkt()
        sndpkt = self.make_pkt(nextseqnum, data, checksum)
        # Send EOT packet, using udt_send()
        self.udt_send(sndpkt)
        logger.info(' ############## Sent EOT Packet ##############')
        # Close socket
        self.sock.close()


if __name__ == '__main__':

    # Constants
    SENDER_IP = "10.0.0.2"
    SENDER_PORT = 5002
    RECEIVER_IP = "11.0.0.2"
    RECEIVER_PORT = 5006
    WINDOW_SIZE = 4
    TIMEOUT = 5.0  # === YOUR CODE HERE ===. Try several values (e.g. 1.0, 3.0 and 5.0)
    DATA_FILE = 'data.txt'
    RECEIVE_BUFFER_SIZE = 1024

    # Create GBN sender
    gbn_sender = GBN_Sender(SENDER_IP, SENDER_PORT, RECEIVER_IP, RECEIVER_PORT, WINDOW_SIZE, TIMEOUT, DATA_FILE, RECEIVE_BUFFER_SIZE)

    # Run GBN sender
    gbn_sender.run()

