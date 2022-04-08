import socket
import random
import time

bufferSize  = 1024
serverAddressPort   = ("127.0.0.1", 7501)


print('this program will generate some test traffic for 2 players on the red ')
print('team as well as 2 players on the blue team')
print('')

red1 = input('Enter codename of red player 1 ==> ')
red2 = input('Enter codename of red player 2 ==> ')
blue1 = input('Enter codename of blue player 1 ==> ')
blue2 = input('Enter codename of blue player 2 ==> ')

print('')
counter = input('How many events do you want ==> ')

# Create datagram socket
UDPClientSocketTransmit = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# counter number of events, random player and order
i = 1
while i < int(counter):
	if random.randint(1,2) == 1:
		redplayer = red1
	else:
		redplayer = red2

	if random.randint(1,2) == 1:
		blueplayer = blue1
	else: 
		blueplayer = blue2	

	if random.randint(1,2) == 1:
		message = redplayer + " hit " + blueplayer
	else:
		message = blueplayer + " hit " + redplayer

	print(message)
	i+=1;
	UDPClientSocketTransmit.sendto(str.encode(str(message)), serverAddressPort)
	time.sleep(random.randint(1,3))
	
print("program complete")
