###################################################################################################
#                                           <MODULES>
import os
import cv2
import socket
#import ffmpeg

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
    print('>>>MANAGEMENT SERVER: OPERATIONAL<<<')
    while True:
        connection, client_address = managementserver.accept()
        try:
            with open( dirVideo + 'video.mp4' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
            print( '<<<Video Received Successfully>>>' )
            extractFrames()
        finally:
            connection.close()
            managementserver.close()
            break
###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    dirVideo = './managementServer/client/video/'
    dirFrame = './managementServer/client/frames/'
    clientServerConnection()