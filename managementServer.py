###################################################################################################
#                                           <MODULES>
import os
import cv2
import sys
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

def node01ServerConnection():
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.bind( ( 'localhost' , 6001 ) )
    managementserver.listen( 1 )
    info = 0
    connection, client_address = managementserver.accept()
    try:
        data = connection.recv( 1024 )
        info = data
    finally:
        connection.close()
    info = int(info.decode('UTF-8'))
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.bind( ( 'localhost' , 6001 ) )
    managementserver.listen( 1 )
    num = 0
    while True:
        connection, client_address = managementserver.accept()
        try:
            with open( './managementServer/processingServer01/' + str( num+1 ) + '.jpg' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
        finally:
            num += 1
            if num < info:
                connection.close()
            else:
                print( '<<<Frames from NODE01 Successfully Received>>>' )
                connection.close()
                managementserver.close()
                return num

def node02ServerConnection( num ):
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.bind( ( 'localhost' , 6002 ) )
    managementserver.listen( 1 )
    info = 0
    connection, client_address = managementserver.accept()
    try:
        data = connection.recv( 1024 )
        info = data
    finally:
        connection.close()
    info = int(info.decode('UTF-8'))
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.bind( ( 'localhost' , 6002 ) )
    managementserver.listen( 1 )
    while True:
        connection, client_address = managementserver.accept()
        try:
            with open( './managementServer/processingServer02/' + str( num+1 ) + '.jpg' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
        finally:
            num += 1
            if num < info:
                connection.close()
            else:
                print( '<<<Frames from NODE02 Successfully Received>>>' )
                connection.close()
                managementserver.close()
                return num

def node03ServerConnection( num ):
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.bind( ( 'localhost' , 6003 ) )
    managementserver.listen( 1 )
    info = 0
    connection, client_address = managementserver.accept()
    try:
        data = connection.recv( 1024 )
        info = data
    finally:
        connection.close()
    info = int(info.decode('UTF-8'))
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.bind( ( 'localhost' , 6003 ) )
    managementserver.listen( 1 )
    while True:
        connection, client_address = managementserver.accept()
        try:
            with open( './managementServer/processingServer03/' + str( num+1 ) + '.jpg' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
        finally:
            num += 1
            if num < info:
                connection.close()
            else:
                print( '<<<Frames from NODE03 Successfully Received>>>' )
                connection.close()
                managementserver.close()
                return num

def makeVideo():
    numframes = 0
    frames = []
    for a in range( 1 , 4):
        for _ in range( 1 , len( os.listdir( './managementServer/processingServer0' + str( a ) + '/' ) ) + 1 ):
            numframes += 1
            frames.append( './managementServer/processingServer0' + str( a ) + '/' + str( numframes ) + '.jpg' )
    frame = cv2.imread( './managementServer/processingServer01/1.jpg' )
    fourcc = cv2.VideoWriter_fourcc( *'mp4v' )
    video = cv2.VideoWriter( dirVideo + 'processedvideo.mp4' , fourcc , 25.0 , ( frame.shape[1] , frame.shape[0] ) )
    for i in frames:
        video.write( cv2.imread( i ) )
    cv2.destroyAllWindows()
    video.release()
    print( '<<<Video Created Successfully>>>' )

def serverClientConnection():
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.connect( ( 'localhost' , 6004 ) )
    try:
        with open( dirVideo + 'processedvideo.mp4' , 'rb' ) as file:
            data = file.read( 1024 )
            while data:
                managementserver.send( data )
                data = file.read( 1024 )
    finally:
        print( '<<<Video Sent Successfully>>>' )
        managementserver.close()
###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    dirVideo = './managementServer/client/video/'
    dirFrame = './managementServer/client/frames/'
    sys.stdout.flush()
    clientServerConnection()
    extractFrames()
    sys.stdout.flush()
    n = serverNode01Connection()
    n = serverNode02Connection( n )
    n = serverNode03Connection( n )
    sys.stdout.flush()
    n = node01ServerConnection()
    n = node02ServerConnection( n )
    n = node03ServerConnection( n )
    sys.stdout.flush()
    makeVideo()
    serverClientConnection()