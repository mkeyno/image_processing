#ifndef _ANA_H_
#define _ANA_H_

#include <opencv2/opencv.hpp>
#include <opencv2/ximgproc.hpp>
#include "opencv2/highgui.hpp"
#include <string>
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

using namespace cv;
using namespace cv::ximgproc;

const std::string MODE;
float THRESH=.43;
static int totaolVineNum=0, totalPost=0;
const std::string Report;
int Analyze(char *f,char *db,float tr);



Mat houghLineProcess(Mat &input){
    Mat dst, cdst, cdstP;

    // Edge detection
    Canny(input, dst, 50, 200, 3);
    // Copy edges to the images that will display the results in BGR
    cvtColor(dst, cdst, COLOR_GRAY2BGR);
    cdstP = cdst.clone();
    // Standard Hough Line Transform
    vector<Vec2f> lines; // will hold the results of the detection
    HoughLines(dst, lines, 1, CV_PI/180, 150, 0, 0 ); // runs the actual detection
    // Draw the lines
    for( size_t i = 0; i < lines.size(); i++ )
    {
        float rho = lines[i][0], theta = lines[i][1];
        Point pt1, pt2;
        double a = cos(theta), b = sin(theta);
        double x0 = a*rho, y0 = b*rho;
        pt1.x = cvRound(x0 + 1000*(-b));
        pt1.y = cvRound(y0 + 1000*(a));
        pt2.x = cvRound(x0 - 1000*(-b));
        pt2.y = cvRound(y0 - 1000*(a));
        line( cdst, pt1, pt2, Scalar(0,0,255), 3, LINE_AA);
    }
    // Probabilistic Line Transform
    vector<Vec4i> linesP; // will hold the results of the detection
    HoughLinesP(dst, linesP, 1, CV_PI/180, 50, 50, 10 ); // runs the actual detection
    // Draw the lines
    for( size_t i = 0; i < linesP.size(); i++ )
    {
        Vec4i l = linesP[i];
        line( cdstP, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0,0,255), 3, LINE_AA);
    }

    return cdstP; //cdst
}

Mat CannyThreshold(Mat &input)
{
    Mat src_gray, dst, detected_edges;
    int lowThreshold = 0;
    const int max_lowThreshold = 100;
    const int ratio = 3;
    const int kernel_size = 3;

    dst.create( input.size(), input.type() );
    cvtColor( input, src_gray, COLOR_BGR2GRAY );
    blur( src_gray, detected_edges, Size(3,3) );
    Canny( detected_edges, detected_edges, lowThreshold, lowThreshold*ratio, kernel_size );
    dst = Scalar::all(0);
    src.copyTo( dst, detected_edges);
    return dst;
}


int addToReport(Mat &input){

int totalPixel=input.rows*input.cols;
int zeroPixle=countNonZero(input);

float precent=zeroPixle/totalPixel;

if(precent>=THRESH) {
                    Report+="Vine"+string(totaolVineNum); 
                    totaolVineNum++;   
                    return 1;    
                    }


else             {
                    Report+="Post"+string(totalPost); 
                    totalPost++;   
                    return 0;    
                    }


}

int detectVine(const std::string & imagePath){

    Mat src, dst ;

    Mat src = imread(imagePath, IMREAD_COLOR);
     if ( src.empty() )                   return 0;       
     if ( src.size() == 0)                return 0;
    switch (expression)
    {
    case "canny": dst=CannyThreshold(src);break;
    case "hough": dst=houghLineProcess(src);break;
        
    
    default: printf("mode can not recognized ");      break;
    }
     
    addToReport(dst);
}


 int Analyze(char *f,char *db,float tr){

std::string   path;

 while( find_file(f,".jpeg",path[0]) ){

        int rez=detectVine(path);

        }

 }


bool find_file(const path & dir_path,         // in this directory,
               const std::string & exten, // search for this name,
               path & path_found)             // placing path here if found
{
    if (!exists(dir_path))        return false;

    directory_iterator end_itr; // default construction yields past-the-end

    for (directory_iterator itr(dir_path); itr != end_itr; ++itr)
    {
        if (is_directory(itr->status())) {
                                        if (find_file(itr->path(), exten, path_found)) 
                                            return true;        }
        else if (itr->leaf() == ends_with(exten, ".jpeg")) {
                                            path_found = itr->path();
                                            return true;        }
    }
    return false;
}


#endif  
