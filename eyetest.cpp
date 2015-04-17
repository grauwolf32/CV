#include "opencv2/opencv.hpp"
 #include "opencv2/objdetect/objdetect.hpp"
 #include "opencv2/highgui/highgui.hpp"
 #include "opencv2/imgproc/imgproc.hpp"

#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

void detectAndDisplay( Mat frame );

String face_cascade_name = "/opt/opencv/opencv/data/lbpcascades/lbpcascade_frontalface.xml";
String eyes_cascade_name = "/opt/opencv/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml";
CascadeClassifier face_cascade;
CascadeClassifier eyes_cascade;
String window_name = "FaceDetection";

int counter=0;
char filename[512] = {0};
 
int main( void )
{
    VideoCapture capture;
    Mat frame;

    // загрузка каскада для распознавания лиц и глаз
    if( !face_cascade.load( face_cascade_name ) ) { 
                printf("[!] Error loading face cascade\n");
                return -1;
        }
    if( !eyes_cascade.load( eyes_cascade_name ) ) {
                printf("[!] Error loading eyes cascade\n");
                return -1; 
        }

    // начинаем захват видео
    capture.open( -1 );
    if ( ! capture.isOpened() ) {
                printf("[!] Error opening video capture\n");
                return -1;
        }
        
        // установка разрешения для видео
        capture.set(CV_CAP_PROP_FRAME_WIDTH, 800);
        capture.set(CV_CAP_PROP_FRAME_HEIGHT, 800);

        // цикл получения кадров с камеры
    while ( capture.read(frame) && counter++ < 100 ) {
        if( frame.empty() ) {
            printf("[!] No captured frame -- Break!\n");
            break;
        }

        // обработка кадра
        detectAndDisplay( frame );

        // обработка клавиатуры
        int c = waitKey(10);
        if( (char)c == 27 ) { 
                        break;
                }
    }
    return 0;
}

void detectAndDisplay( Mat frame )
{
    std::vector<Rect> faces;
    Mat frame_gray;

    cvtColor( frame, frame_gray, COLOR_BGR2GRAY );
    equalizeHist( frame_gray, frame_gray );

    // детектор лиц
    face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0, Size(80, 80) );

        printf("[i] frame %d x %d detect faces: %d\n", frame.cols, frame.rows, faces.size());
        
    for( size_t i = 0; i < faces.size(); i++ ) {        
        Mat faceROI = frame_gray( faces[i] );
        std::vector<Rect> eyes;

        // на каждом лице пробуем найти глаза
        eyes_cascade.detectMultiScale( faceROI, eyes, 1.1, 2, 0 |CASCADE_SCALE_IMAGE, Size(30, 30) );
        if( eyes.size() == 2) {          
            // отрисовка рамки вокруг лица
            Point center( faces[i].x + faces[i].width/2, faces[i].y + faces[i].height/2 );
            ellipse( frame, center, Size( faces[i].width/2, faces[i].height/2 ), 0, 0, 360, Scalar( 255, 0, 0 ), 2, 8, 0 );

            for( size_t j = 0; j < eyes.size(); j++ ) { 
                                // отрисовка кругов вокруг глаз
                Point eye_center( faces[i].x + eyes[j].x + eyes[j].width/2, faces[i].y + eyes[j].y + eyes[j].height/2 );
                int radius = cvRound( (eyes[j].width + eyes[j].height)*0.25 );
                circle( frame, eye_center, radius, Scalar( 255, 0, 255 ), 3, 8, 0 );
            }         
                        printf("[i] eyes!\n");  
        }
                
                // сохранение в файл
                //Mat roiImg;
                //roiImg = frame(faces[i]);
                //sprintf(filename, "face_%d.png", counter++);
                //imwrite(filename, roiImg);
    }
    // показываем результат
    imshow( window_name, frame );

}

