###################################################################################################
#                                           <MODULES>
import os
import cv2
import socket

###################################################################################################
#                                           <FUNCTIONS>
def extractFrames():
    video = cv2.VideoCapture( './managementServer/client/video/video.mp4' )
    flag = True
    index = 1
    while flag:
        flag , frame = video.read()
        name = './managementServer/client/frames/' + str( index ) + '.jpg'
        try:
            cv2.imwrite( name , frame )
        except:
            print( '<<<All Frames Extracted>>>' )
        index += 1

def sortFrames( frames ):
    for i in range( 0 , len( frames ) ):
        frames[i] = str( i + 1 ) + '.jpg'
    return frames

def makeVideo():
    frames = [f for f in os.listdir( dirFrame ) if f.endswith( '.jpg' )]
    frames = sortFrames( frames )
    frame = cv2.imread( dirFrame + '1.jpg' )
    fourcc = cv2.VideoWriter_fourcc( *'mpv4' )
    video = cv2.VideoWriter( dirVideo + 'processedvideo.mp4' , fourcc , 60.0 , ( frame.shape[1] , frame.shape[0] ) )
    for i in frames:
        video.write( cv2.imread( os.path.join( dirFrame , i ) ) )
    cv2.destroyAllWindows()
    video.release()

def clientServerConnection():
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.bind( ( 'localhost' , 6000 ) )
    managementserver.listen( 1 )
    print('>>>MANAGEMENT SERVER -> OPERATIVE<<<')
    while True:
        connection, client_address = managementserver.accept()
        try:
            with open( dirVideo + 'video.mp4' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
            print( '<<<Video Received Successfully>>>' )
        finally:
            connection.close()
            managementserver.close()
            break

def serverNode01Connection():
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.connect( ( 'localhost' , 6001 ) )
    info = bytes( str( int( len( os.listdir( dirFrame ) ) / 3 ) ) , 'UTF-8' )
    managementserver.send( info )
    managementserver.close()
    numFrames = int( len( os.listdir( dirFrame ) ) / 3 )
    num = 1
    while num <= numFrames:      
        managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        managementserver.connect( ( 'localhost' , 6001 ) )
        try:
            with open( dirFrame + str( num ) + '.jpg' , 'rb' ) as file:
                data = file.read( 1024 )
                while data:
                    managementserver.send( data )
                    data = file.read( 1024 )
        finally:
            num += 1
            managementserver.close()
    print( '<<<Frames Sent Successfully to NODE01>>>' )
    return num

def serverNode02Connection( num ):
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.connect( ( 'localhost' , 6002 ) )
    info = bytes( str( int( len( os.listdir( dirFrame ) ) / 3 ) ) , 'UTF-8' )
    managementserver.send( info )
    managementserver.close()
    numFrames = int( len( os.listdir( dirFrame ) ) / 3 ) * 2
    while num <= numFrames:      
        managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        managementserver.connect( ( 'localhost' , 6002 ) )
        try:
            with open( dirFrame + str( num ) + '.jpg' , 'rb' ) as file:
                data = file.read( 1024 )
                while data:
                    managementserver.send( data )
                    data = file.read( 1024 )
        finally:
            num += 1
            managementserver.close()
    print( '<<<Frames Sent Successfully to NODE02>>>' )
    return num

def serverNode03Connection( num ):
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.connect( ( 'localhost' , 6003 ) )
    info = bytes( str( int( len( os.listdir( dirFrame ) ) / 3 ) ) , 'UTF-8' )
    managementserver.send( info )
    managementserver.close()
    numFrames = int( len( os.listdir( dirFrame ) ) / 3 ) * 3
    while num <= numFrames:      
        managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        managementserver.connect( ( 'localhost' , 6003 ) )
        try:
            with open( dirFrame + str( num ) + '.jpg' , 'rb' ) as file:
                data = file.read( 1024 )
                while data:
                    managementserver.send( data )
                    data = file.read( 1024 )
        finally:
            num += 1
            managementserver.close()
    print( '<<<Frames Sent Successfully to NODE03>>>' )
    return num
###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    dirVideo = './managementServer/client/video/'
    dirFrame = './managementServer/client/frames/'
    clientServerConnection()
    extractFrames()
    n = serverNode01Connection()
    n = serverNode02Connection( n )
    n = serverNode03Connection( n )
    print(n-1)