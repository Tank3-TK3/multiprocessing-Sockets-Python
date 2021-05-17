###################################################################################################
#                                           <MODULES>
import sys
import socket
###################################################################################################
#                                           <FUNCTIONS>
def clientServerConnection():
    client = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    client.connect( ( 'localhost' , 6000 ) )
    print( '>>>CLIENT -> OPERATIVE<<<' )
    try:
        with open( './client/video.mp4' , 'rb' ) as file:
            data = file.read( 1024 )
            while data:
                client.send( data )
                data = file.read( 1024 )
    finally:
        print( '<<<Video Sent Successfully>>>' )
        client.close()

def serverClientConnection():
    client = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    client.bind( ( 'localhost' , 6004 ) )
    client.listen( 1 )
    while True:
        connection, client_address = client.accept()
        try:
            with open( './client/processedvideo.mp4' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
            print( '<<<Video Received Successfully>>>' )
        finally:
            connection.close()
            client.close()
            break
###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    sys.stdout.flush()
    clientServerConnection()
    sys.stdout.flush()
    serverClientConnection()