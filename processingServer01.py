###################################################################################################
#                                           <MODULES>
import os
import cv2
import sys
import socket
###################################################################################################
#                                           <FUNCTIONS>
def serverNode01Connection():
    serverNode01 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    serverNode01.bind( ( 'localhost' , 6001 ) )
    serverNode01.listen( 1 )
    info = 0
    print('>>>SERVER NODE 01 -> OPERATIVE<<<')
    connection, client_address = serverNode01.accept()
    try:
        data = connection.recv( 1024 )
        info = data
    finally:
        connection.close()
    info = int(info.decode('UTF-8'))
    serverNode01 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    serverNode01.bind( ( 'localhost' , 6001 ) )
    serverNode01.listen( 1 )
    num = 0
    while True:
        connection, client_address = serverNode01.accept()
        try:
            with open( './processingServer01/framesreceived/' + str( num+1 ) + '.jpg' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
                print( '<<<Frame ' + str( num+1 ) + ' Received Successfully>>>' )
        finally:
            num += 1
            if num < info:
                connection.close()
            else:
                connection.close()
                serverNode01.close()
                break

def frameProcessing():
    for x in range( 0 , len( os.listdir( './processingServer01/framesreceived/' ) ) ):
        imgname = './processingServer01/framesreceived/' + str( x+1 ) + '.jpg'
        imgpname = './processingServer01/processedframes/' + str( x+1 ) + '.jpg'
        img = cv2.imread( imgname , 2 )
        cv2.imwrite( imgpname , img )
        cv2.destroyAllWindows()
        print( '<<<Frame ' + str( x+1 ) + ' Processed Successfully>>>' )

def node01ServerConnection():
    serverNode01 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    serverNode01.connect( ( 'localhost' , 6001 ) )
    info = bytes( str( int( len( os.listdir( './processingServer01/processedframes/' ) ) ) ) , 'UTF-8' )
    serverNode01.send( info )
    serverNode01.close()
    numFrames = int( len( os.listdir( './processingServer01/processedframes/' ) ) )
    num = 1
    while num <= numFrames:      
        serverNode01 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        serverNode01.connect( ( 'localhost' , 6001 ) )
        try:
            with open( './processingServer01/processedframes/' + str( num ) + '.jpg' , 'rb' ) as file:
                data = file.read( 1024 )
                while data:
                    serverNode01.send( data )
                    data = file.read( 1024 )
        finally:
            print( '<<<Frame ' + str( num ) + ' Sent Successfully>>>' )
            num += 1
            serverNode01.close()
###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    sys.stdout.flush()
    serverNode01Connection()
    frameProcessing()
    sys.stdout.flush()
    node01ServerConnection()