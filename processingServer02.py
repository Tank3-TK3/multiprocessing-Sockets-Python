###################################################################################################
#                                           <MODULES>
import os
import cv2
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
    print(type(info))
    serverNode02 = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    serverNode02.bind( ( 'localhost' , 6002 ) )
    serverNode02.listen( 1 )
    print('>>>SERVER NODE 02 -> OPERATIVE<<<')
    num = 0
    while True:
        connection, client_address = serverNode02.accept()
        try:
            with open( './processingServer02/framesreceived/' + str( num+1 ) + '.jpg' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
        finally:
            num += 1
            if num < info:
                print( '<<<Frame ' + str( num+1 ) + ' Received Successfully>>>' )
                connection.close()
            else:
                connection.close()
                serverNode02.close()
                break

def frameProcessing():
    for x in range( 0 , len( os.listdir( './processingServer01/framesreceived/' ) ) ):
        imgname = './processingServer02/framesreceived/' + str( x+1 ) + '.jpg'
        imgpname = './processingServer02/processedframes/' + str( x+1 ) + '.jpg'
        img = cv2.imread( imgname , 2 )
        cv2.imwrite( imgpname , img )
        cv2.destroyAllWindows()
        print( '<<<Frame ' + str( x+1 ) + ' Processed Successfully>>>' )

###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    serverNode02Connection()
    frameProcessing()