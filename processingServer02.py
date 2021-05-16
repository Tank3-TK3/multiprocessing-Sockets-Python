###################################################################################################
#                                           <MODULES>
import os
import cv2
import sys
import socket
###################################################################################################
#                                           <FUNCTIONS>
def serverNode02Connection():
    serverNode02 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    serverNode02.bind( ( 'localhost' , 6002 ) )
    serverNode02.listen( 1 )
    info = 0
    print('>>>SERVER NODE 02 -> OPERATIVE<<<')
    connection, client_address = serverNode02.accept()
    try:
        data = connection.recv( 1024 )
        info = data
    finally:
        connection.close()
    info = int(info.decode('UTF-8'))
    serverNode02 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    serverNode02.bind( ( 'localhost' , 6002 ) )
    serverNode02.listen( 1 )
    num = 0
    while True:
        connection, client_address = serverNode02.accept()
        try:
            with open( './processingServer02/framesreceived/' + str( num+1 ) + '.jpg' , 'wb' ) as file:
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
                serverNode02.close()
                break

def frameProcessing():
    for x in range( 0 , len( os.listdir( './processingServer02/framesreceived/' ) ) ):
        imgname = './processingServer02/framesreceived/' + str( x+1 ) + '.jpg'
        imgpname = './processingServer02/processedframes/' + str( x+1 ) + '.jpg'
        img = cv2.imread( imgname , 2 )
        cv2.imwrite( imgpname , img )
        cv2.destroyAllWindows()
        print( '<<<Frame ' + str( x+1 ) + ' Processed Successfully>>>' )

def node02ServerConnection():
    serverNode02 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    serverNode02.connect( ( 'localhost' , 6002 ) )
    info = bytes( str( int( len( os.listdir( './processingServer02/processedframes/' ) ) ) * 2 ) , 'UTF-8' )
    serverNode02.send( info )
    serverNode02.close()
    numFrames = int( len( os.listdir( './processingServer02/processedframes/' ) ) )
    num = 1
    while num <= numFrames:      
        serverNode02 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        serverNode02.connect( ( 'localhost' , 6002 ) )
        try:
            with open( './processingServer02/processedframes/' + str( num ) + '.jpg' , 'rb' ) as file:
                data = file.read( 1024 )
                while data:
                    serverNode02.send( data )
                    data = file.read( 1024 )
        finally:
            print( '<<<Frame ' + str( num ) + ' Sent Successfully>>>' )
            num += 1
            serverNode02.close()
###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    sys.stdout.flush()
    serverNode02Connection()
    frameProcessing()
    sys.stdout.flush()
    node02ServerConnection()