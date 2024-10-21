# AUTHOR: David Vach
# KONTROLNY BOD
# P2P, Handshake
# Custom Header
# 18.10.2024 23:53

#libs
import socket
import threading
import struct
#import keyboard

#custom_separator function for better visib
def separator(size):
    print("-"*size)

#custom_header class 
class PacketHeader:
    #konstruktor budu polia v hlavicke 
    def __init__(self, message_type, identifier, sequence_num, flags, fragment_offset, data_size, checksum, ack_number, window_size):
        self.message_type = message_type
        self.identifier = identifier
        self.sequence_num = sequence_num
        self.flags = flags
        self.fragment_offset = fragment_offset
        self.data_size = data_size
        self.checksum = checksum
        self.ack_number = ack_number
        self.window_size = window_size

    #funkcia na prevedenie hlavicky na bajty
    def to_bytes(self):
        return struct.pack("!BBHBBHHHH",
                           self.message_type,
                           self.identifier,
                           self.sequence_num,
                           self.flags,
                           self.fragment_offset,
                           self.data_size,
                           self.checksum,
                           self.ack_number,
                           self.window_size)
    
    #funkcia na prevedenie bajtov na hlavicku
    @staticmethod
    def from_bytes(packet_bytes):
        #ak nemam 14 bytov tak sa nieco pokazilo = Vypis chybovu hlasku
        if len(packet_bytes) < 14:
            raise ValueError("Neúplný paket: očakáva sa 14 bajtov")
        message_type, identifier, sequence_num, flags, fragment_offset, data_size, checksum, ack_number, window_size = struct.unpack(
            "!BBHBBHHHH", packet_bytes)
        return PacketHeader(message_type, identifier, sequence_num, flags, fragment_offset, data_size, checksum,
                            ack_number, window_size)

    #staticke metody  pre vytvaranie SYN, ACK, FIN, NACK .. special for every case
    @staticmethod
    def create_syn(identifier, sequence_num): #flags = 2
        flags = 0b000010
        message_type = 1
        return PacketHeader(message_type, identifier, sequence_num, flags, 0, 0, 0, 0, 0)

    @staticmethod
    def create_ack(identifier, ack_number): #flags = 16
        flags = 0b010000
        message_type = 2
        return PacketHeader(message_type, identifier, 0, flags, 0, 0, 0, ack_number, 0)

    @staticmethod
    def create_fin(identifier, sequence_num): #flags = 1
        flags = 0b000001
        message_type = 3
        return PacketHeader(message_type, identifier, sequence_num, flags, 0, 0, 0, 0, 0)

    @staticmethod
    def create_nack(identifier, sequence_num):
        return None

#funkcia na vypis hlavicky protokolu
def write_protocol_header(header):
    return f"ack_number: {header.ack_number}, message_type: {header.message_type}, flags: {header.flags}"

#tato klassa bude sluzit na to aby sme inicializovali spojenie medzi dvoma uzlami -> Oba sa budud spravat takisto
class ConnetionP2P:
    def __init__(self, ip, listen_port, connect_ip, connect_port, is_initiator):
        self.ip = ip
        self.listen_port = listen_port
        self.connect_ip = connect_ip
        self.connect_port = connect_port
        self.identifier = 1
        self.sequence_num = 0
        self.connection_established = False
        self.is_initiator = is_initiator
        self.lock = threading.Lock()
        self.partner_identifier = None
        self.partner_port = None

    #ak som iniciator tak si nastavim thread na pocuvanie ak nie tak si ho nastavim na pocuvanie
    def start(self):
        if self.is_initiator:
            threading.Thread(target=self.connect_and_send).start()
            threading.Thread(target=self.listen).start()
        else:
            threading.Thread(target=self.listen).start()
            threading.Thread(target=self.connect_and_send).start()

    #co som dostal?
    def receive_exact(self, conn, length):
        data = b''
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data

    #cakam na inicializovanie spojenia
    def listen(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.ip, self.listen_port))
        listen_socket.listen(1)
        print(f"Počúvam na {self.ip}:{self.listen_port}")

        while not self.connection_established:
            try:
                conn, addr = listen_socket.accept()
                with self.lock:
                    if self.connection_established:
                        conn.close()
                        return
                    print(f"Pripojený peer: {addr}")
                    packet = self.receive_exact(conn, 14)
                    if packet is None:
                        conn.close()
                        continue

                    header = PacketHeader.from_bytes(packet)
                    if header.flags & 0b000010:
                        print("Dostal som SYN, odpovedám s SYN-ACK")
                        print("Co som dostal: {}")
                        print(write_protocol_header(header))

                        self.partner_identifier = header.identifier
                        self.partner_port = addr[1]
                        response_header = PacketHeader.create_syn(self.identifier, self.sequence_num)
                        conn.sendall(response_header.to_bytes())

                        packet = self.receive_exact(conn, 14)
                        if packet is None:
                            conn.close()
                            continue

                        ack_header = PacketHeader.from_bytes(packet)
                        if ack_header.flags & 0b010000:
                            print("Handshake úspešne dokončený, spojenie je pripravené.")
                            print("Co som dostal:")
                            print(write_protocol_header(ack_header))

                            # Pridáme výpis separátora a textu
                            separator(90)
                            print("YOUR CHAT")
                            separator(90)

                            self.connection_established = True
                            threading.Thread(target=self.receive_messages, args=(conn,)).start()
                            self.send_messages(conn)
                        else:
                            conn.close()
                    else:
                        conn.close()
            except ConnectionResetError:
                conn.close()

    #funkcia na pripojenie a odoslanie sprav
    def connect_and_send(self):
        while not self.connection_established:
            try:
                conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn_socket.connect((self.connect_ip, self.connect_port))
                with self.lock:
                    if self.connection_established:
                        conn_socket.close()
                        return

                    print(f"Pripojený na peer: {self.connect_ip}:{self.connect_port}")
                    print("Posielam SYN na nadviazanie spojenia")
                    syn_header = PacketHeader.create_syn(self.identifier, self.sequence_num)
                    conn_socket.sendall(syn_header.to_bytes())

                    packet = self.receive_exact(conn_socket, 14)
                    if packet is None:
                        conn_socket.close()
                        continue

                    syn_ack_header = PacketHeader.from_bytes(packet)
                    if syn_ack_header.flags & 0b000010:
                        print("Dostal som SYN-ACK, odpovedám s ACK")
                        print("Co som dostal:")
                        print(write_protocol_header(syn_ack_header))
                        #print(syn_ack_header.message_type)

                        self.partner_identifier = syn_ack_header.identifier
                        self.partner_port = self.connect_port
                        ack_header = PacketHeader.create_ack(self.identifier, syn_ack_header.sequence_num + 1)
                        conn_socket.sendall(ack_header.to_bytes())
                        print("Handshake úspešne dokončený, spojenie je pripravené.")

                        # Pridáme výpis separátora a textu
                        separator(90)
                        print("YOUR CHAT")
                        separator(90)

                        self.connection_established = True
                        threading.Thread(target=self.receive_messages, args=(conn_socket,)).start()
                        self.send_messages(conn_socket)
                    else:
                        conn_socket.close()
                break
            except (ConnectionRefusedError, ConnectionResetError):
                
                conn_socket.close()
    
    #sending messages
    def send_messages(self, conn):
        while True:
            try:
                msg = input()
            except EOFError:
                break
            
            #ukonci komunikaciu
            if msg.lower() == "exit":
                try:
                    fin_packet = PacketHeader.create_fin(self.identifier, self.sequence_num)
                    conn.sendall(fin_packet.to_bytes())
                    print("Odoslaný FIN, ukončujem spojenie.")
                    break
                except OSError:
                    break
            #ak to nie je exit tak rozbal packet a precitaj ho druhej strane
            else:
                try:
                    data = msg.encode() #prevedie na bajty
                    data_size = len(data) #velkost dat
                    message_header = PacketHeader(
                        message_type=0,
                        identifier=self.identifier,
                        sequence_num=self.sequence_num,
                        flags=0,
                        fragment_offset=0,
                        data_size=data_size,
                        checksum=0,
                        ack_number=0,
                        window_size=0
                    )
                    conn.sendall(message_header.to_bytes() + data)
                    #musim pridat seq num aby som vedel ze posielam dalsi
                    self.sequence_num += 1
                except OSError:
                    break
        #inak ukonci spojenie ak sa nieco deje

        conn.close()
        print("Spojenie je ukončené, program sa vypne.")
        exit(0)

    #funkcia na spracovanie sprav
    def receive_messages(self, conn):
        #skusaj donekonecma
        while True:
            try: 
                packet = self.receive_exact(conn, 14)
                if not packet:
                    break
                header = PacketHeader.from_bytes(packet)
                data_size = header.data_size
                data = self.receive_exact(conn, data_size)
                if data is None: break
                if header.flags & 0b000001:
                    print("Prijatý FIN, ukončujem spojenie.")
                    print("Co som dostal:")
                    print(write_protocol_header(header))
                    #TODO pridaj sem nieco co automaticky odpali enter
                    break
                else:
                    decoded_msg = data.decode('utf-8')
                    print(f"Partner (ID: {header.identifier}, PORT: {self.partner_port}, MESSAGE_TYPE: {header.message_type}): {decoded_msg}")
            except (OSError, ValueError, UnicodeDecodeError):
                break

        
        conn.close()
        print("Spojenie je ukončené, program sa vypne.")
        print("Pre ukončenie programu stlačte ENTER")
        exit(0)


#starting app here
if __name__ == "__main__":
    separator(90)
    print("Pozadovany vstup: <tvoja_IP> <IP_druhého_zariadenia> <tvoj_port> <port_druhého_zariadenia>")
    separator(90)
    inputs = input("Zadaj svoje údaje: ")
    input_list = inputs.split()
    if len(input_list) != 4: # smth went badly catch err
        print("nespravny pocet argumentov -> ocakavaju sa 4 argumenty.")
        exit(1)
    separator(90)

    #daj si vstup do premennych
    ip = input_list[0]
    connect_ip = input_list[1]
    listen_port = int(input_list[2])
    connect_port = int(input_list[3])

    #inicializujes spojenie?
    is_initiator = listen_port < connect_port
    connection = ConnetionP2P(ip, listen_port, connect_ip, connect_port, is_initiator)
    connection.start()



#inputs home
#192.168.1.152 192.168.1.152 5000 5001
#192.168.1.152 192.168.1.152 5001 5000

#inputs localhost intrak
#172.20.10.14 172.20.10.14 5000 5001
#172.20.10.14 172.20.10.14 5001 5000

#inputs skusanie s druhym clovekom
#172.20.10.14 tvoja_IP 5000 5001
#tvoja_IP 172.20.10.14 5001 5000