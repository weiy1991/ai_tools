//  test collect data

#include <glog/logging.h>
#include <leveldb/db.h>
#include <leveldb/write_batch.h>

#include <algorithm>
#include <fstream>  // NOLINT(readability/streams)
#include <string>
#include <utility>
#include <vector>

#include <unistd.h>  
#include <stdlib.h>  
#include <stdio.h>  
#include <sys/shm.h>
#include <cstring>
#include <math.h>

//opencv head file
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/highgui/highgui_c.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/imgproc/imgproc_c.h>

//#include <ndbm.h>
//#include <ndbm.h>
// h5df head
//#include "H5Cpp.h"

//python
//#include <python3.6/python.h>
//#include <Python.h>

#define image_width 640
#define image_height 480
// #define resize_width 280
// #define resize_height 210

#define resize_width 200
#define resize_height 200

using std::string;
using namespace cv;
//using namespace H5;
using namespace std;

struct shared_use_st  
{  
    int written;
    uint8_t data[image_width*image_height*3];  
    int control;
    int pause;
    double fast;

    double dist_L;
    double dist_R;

    double toMarking_L;
    double toMarking_M;
    double toMarking_R;

    double dist_LL;
    double dist_MM;
    double dist_RR;

    double toMarking_LL;
    double toMarking_ML;
    double toMarking_MR;
    double toMarking_RR;

    double toMiddle;
    double angle;
    double speed;

    double steerCmd;
    double accelCmd;
    double brakeCmd;

    //by Yuanwei
    double pofCarX;
    double pofCarY;
    double pofTrackX;
    double pofTrackY;
    double radiusofSeg;
    int typeofSeg;
    //end by Yuanwei
};

// const H5std_string FILE_NAME("test.h5");
// const H5std_string DATASET_NAME("FloatArray");
// const int NX = 1000; // dataset dimensions
// const int NY = 1000;

int main(int argc, char** argv) {
	//LOG(INFO) << "Hello,GLOG!";
    //::google::InitGoogleLogging(argv[0]);

    ////////////////////// set up memory sharing
    void *shm = NULL;  
    struct shared_use_st *shared;  
    int shmid; 

    shmid = shmget((key_t)4567, sizeof(struct shared_use_st), 0666|IPC_CREAT);  
    if(shmid == -1)  
    {  
        fprintf(stderr, "shmget failed\n");  
        exit(EXIT_FAILURE);  
    }  

    shm = shmat(shmid, 0, 0);  
    if(shm == (void*)-1)  
    {  
        fprintf(stderr, "shmat failed\n");  
        exit(EXIT_FAILURE);  
    }  
    printf("\n********** Memory sharing started, attached at %X **********\n", shm); 

    shared = (struct shared_use_st*)shm;  
    shared->written = 0;
    shared->control = 0;
    shared->pause = 1;
    shared->fast = 0.0;

    shared->dist_L = 0.0;
    shared->dist_R = 0.0;

    shared->toMarking_L = 0.0;
    shared->toMarking_M = 0.0;
    shared->toMarking_R = 0.0;

    shared->dist_LL = 0.0;
    shared->dist_MM = 0.0;
    shared->dist_RR = 0.0;

    shared->toMarking_LL = 0.0;
    shared->toMarking_ML = 0.0;
    shared->toMarking_MR = 0.0;
    shared->toMarking_RR = 0.0;

    shared->toMiddle = 0.0;
    shared->angle = 0.0;
    shared->speed = 0.0;

    shared->steerCmd = 0.0;
    shared->accelCmd = 0.0;
    shared->brakeCmd = 0.0;  

    //add by Yuanwei
    shared->pofCarX = 0.0;
    shared->pofCarY = 0.0;
    shared->pofTrackX = 0.0;
    shared->pofTrackY = 0.0;
    shared->radiusofSeg = 0.0;
    shared->typeofSeg = 1;
    //end by Yuanwei
    ////////////////////// END set up memory sharing

    ////////////////////// set up opencv
    IplImage* screenRGB= cvCreateImage(cvSize(image_width,image_height/2),IPL_DEPTH_8U,3);
    IplImage* resizeRGB=cvCreateImage(cvSize(resize_width,resize_height),IPL_DEPTH_8U,3);
    IplImage* leveldbRGB=cvCreateImage(cvSize(resize_width,resize_height),IPL_DEPTH_8U,3);
    //cvNamedWindow("Image from leveldb",1);
    cvNamedWindow("Image from TORCS",1);
    int key;
    ////////////////////// END set up opencv


    const char*  fileName = "/media/amax/abb05cc1-fac6-460e-b9d5-494d15881093/yuanwei/TorcsOriginal/chenyiWheel1.csv";  //training csv
    //const char*  fileName = "singleerror.csv";  //training csv
    //const char*  fileName = "testing.csv";  //testing csv
    //const char*  fileName = "testingwheel1.csv";  //testing csv
    //const char*  fileName = "testingdirt2new.csv";  //testing csv
    //const char*  fileName = "traininghumandriver.csv";  //testing csv

    ofstream file(fileName);
    
    ////////////////////// Start to read mem
    int frame = 0;
    while (1) {

       if (shared->written == 1) {  // the new image data is ready to be read

        shared->written = 0;
         frame++;
         printf("frame: %d \n", frame);

         //get the 200*200 png data
         for (int h = 0; h < image_height/2; h++) {
            for (int w = 0; w < image_width; w++) {
               screenRGB->imageData[(h*image_width+w)*3+2]=shared->data[((image_height/2-h-1)*image_width+w)*3+0];
               screenRGB->imageData[(h*image_width+w)*3+1]=shared->data[((image_height/2-h-1)*image_width+w)*3+1];
               screenRGB->imageData[(h*image_width+w)*3+0]=shared->data[((image_height/2-h-1)*image_width+w)*3+2];
            }
         }
         //cvShowImage("Image from TORCS", screenRGB);
        cvResize(screenRGB,resizeRGB);
        cv::Mat image = cv::cvarrToMat(resizeRGB); 
        //end get 200*200 png data

        //get the 640*480 png data
        //  for (int h = 0; h < image_height; h++) {
        //     for (int w = 0; w < image_width; w++) {
        //        screenRGB->imageData[(h*image_width+w)*3+2]=shared->data[((image_height-h-1)*image_width+w)*3+0];
        //        screenRGB->imageData[(h*image_width+w)*3+1]=shared->data[((image_height-h-1)*image_width+w)*3+1];
        //        screenRGB->imageData[(h*image_width+w)*3+0]=shared->data[((image_height-h-1)*image_width+w)*3+2];
        //     }
        //  }
        // cv::Mat image = cv::cvarrToMat(screenRGB); 
        //cvShowImage("Image from TORCS", screenRGB);
        //end get 640*480 png data


        //write the data
        char buffer[100];
        char num_buffer[100];
        sprintf(num_buffer,"%d",frame);
        //char* basicdir = "/home/amax/data/torcs/trainingsingle/";//training datasets
        //char* basicdir = "/home/amax/data/torcs/testing/";//testing datasets
        char* basicdir = "/media/amax/abb05cc1-fac6-460e-b9d5-494d15881093/yuanwei/TorcsOriginal/chenyiWheel1/";//testing dataset for wheel1

        char* png = ".png";
        sprintf(buffer, "%.*s%d%.*s",strlen(basicdir), basicdir, frame,strlen(png), png);
        // Mat gray_image = Mat(result,true);
        // imwrite( buffer, gray_image );

        //write the data to image and csv
        imwrite( buffer, image );

        file<<frame<<","<<buffer<<","
        <<shared->steerCmd<<","
        <<shared->speed<<","
        <<shared->accelCmd<<","
        <<shared->brakeCmd<<","
        <<shared->pofCarX<<","
        <<shared->pofCarY<<","
        <<shared->pofTrackX<<","
        <<shared->pofTrackY<<","
        <<shared->toMiddle<<","
        <<shared->radiusofSeg<<","
        <<shared->typeofSeg<<"\n";

        printf("shared->steerCmd: %f \n", shared->steerCmd);
 
         //cvShowImage("Image from TORCS", resizeRGB);
         cvWaitKey(1);
     }
         //printf(" shared->steerCmd: %f  \n",shared->steerCmd );
     }
      file.close();

     //dataset.write(data, PredType::NATIVE_DOUBLE);
}