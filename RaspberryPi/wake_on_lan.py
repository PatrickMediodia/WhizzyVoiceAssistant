'''
Enable WOL on terminal

Steps
1.) device manager
2.) network adaptors
3.) Ethernet Controller Properties
4.) Advanced
5.) Shutdown Wake-On-LAN/Enable PME
6.) Set to enabled
7.) Go to Power Management
8.) Click all checkbox
    - Allow the computer to turn off this device to save power
    - Allow this device to wake the computer
        - Only allow a magic packet to wake the computer
'''

from wakeonlan import send_magic_packet

def start_terminal(MAC_address):
    send_magic_packet(MAC_address)

print('\nMagic Packet Sent\n')