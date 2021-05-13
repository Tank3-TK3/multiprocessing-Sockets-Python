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
            break
        index += 1

def makeVideo():
    frames = [f for f in os.listdir( './managementServer/client/frames/' ) if f.endswith( '.jpg' )]
    frame = cv2.imread( './managementServer/client/frames/1.jpg' )
    fourcc = cv2.VideoWriter_fourcc( *'MP4V' )
    video = cv2.VideoWriter( './managementServer/client/video/processedvideo.mp4' , fourcc , 30.0 , ( frame.shape[1] , frame.shape[0] ) )
    print("Aqui")
    for i in frames:
        video.write( cv2.imread( os.path.join( './managementServer/client/frames/' , i ) ) )
    cv2.destroyAllWindows()
    video.release()

###################################################################################################
#                                             <MAIN>
if __name__ == '__main__':
    managementserver = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    managementserver.bind( ( 'localhost' , 6000 ) )
    managementserver.listen( 1 )
    while True:
        connection, client_address = managementserver.accept()
        try:
            with open( './managementServer/client/video/video.mp4' , 'wb' ) as file:
                data = connection.recv( 1024 )
                while data:
                    file.write( data )
                    data = connection.recv( 1024 )
            extractFrames()
            makeVideo()
            print("After Make")
        finally:
            connection.close()
            managementserver.close()
            exit()