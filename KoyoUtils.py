import socket
from Koyo import Koyo

port = 28784
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def change_ip_from_mac(mac, new_ip):
        """

        :param mac: mac address of koyo
        :param new_ip: new ip address of koyo
        """
        msg = '4841506b04fa510f0015' + mac + '0c001000' + \
              '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, new_ip.split('.')))

        sock.sendto(bytearray.fromhex(msg), ('<broadcast>', port))
        sock.recvfrom(1024), sock.recvfrom(1024)


def change_ip_from_ip(old_ip, new_ip):
    mac = get_mac_from_ip(old_ip)
    change_ip_from_mac(mac, new_ip)


def find_koyos():
    msg = '484150f805a550010005'
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(3)
    sock.sendto(bytearray.fromhex(msg), ('<broadcast>', port))
    recv = ''
    koyos = []
    while True:
        try:
            newmesg = sock.recvfrom(1024)
        except socket.timeout:
            break
        ips = map(ord, str(newmesg[0]))
        ip = str(ips[len(ips) - 5]) + '.' + str(ips[len(ips) - 4]) + '.' + str(ips[len(ips) - 3]) + '.' + str(
            ips[len(ips) - 2])
        mac = str(hex(ips[len(ips) - 13])[2:].zfill(2)) + \
              str(hex(ips[len(ips) - 12])[2:].zfill(2)) + \
              str(hex(ips[len(ips) - 11])[2:].zfill(2)) + \
              str(hex(ips[len(ips) - 10])[2:].zfill(2)) + \
              str(hex(ips[len(ips) - 9])[2:].zfill(2)) + \
              str(hex(ips[len(ips) - 8])[2:].zfill(2))
        print ip, mac
        koyos.append(Koyo(ip, mac))
        newmesg = recv
    return koyos


def get_mac_from_ip(ip):
    for koyo in find_koyos():
        if koyo.ip == ip:
            return koyo.mac
