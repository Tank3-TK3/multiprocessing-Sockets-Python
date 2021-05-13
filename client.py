###################################################################################################
#                                           <MODULES>
import socket

###################################################################################################
#                                           <FUNCTIONS>
def clientServerConnection():
    client = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    client.connect( ( 'localhost' , 6000 ) )
    print( '>>>CLIENT: OPERATIONAL<<<' )
    try:
        with open( './client/video.mp4' , 'rb' ) as file:
            data = file.read( 1024 )
            while data:
                client.send( data )
                data = file.read( 1024 )
    finally:
        print( '<<<Video Sent Successfully>>>' )
        client.close()

###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    clientServerConnection()