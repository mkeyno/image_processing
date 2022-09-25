#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>
#include <analyze.h>
//#include <opencv2/highgui.hpp>

int main(int argc, char** argv) {

int opt = 0;

char *imagefolder = NULL;
char *db_file = NULL;
char *AnalyzeMode= NULL;

extern std::string MODE;

while ((opt = getopt(argc, argv, "i:o:")) != -1) {
    switch(opt) {
                case 'f':
                        imagefolder = optarg;
                        printf("\nImage Folder=%s", imagefolder);

                        break;
                case 'd':
                        db_file = optarg;
                        printf("\nData Base File=%s", db_file);
                        break;
                case 't':
                        db_file = optarg;
                        printf("\nData Base File=%s", db_file);
                        break;
                case 'm':
                        db_file = optarg;
                        printf("\nAnalyze Mode=%s", AnalyzeMode);
                        MODE=string(AnalyzeMode);
                        MODE=std::tolower(MODE);
                        break;        
                case 'h':
                        printf("\ntype -f [image folder] -d [data base] -t [threshold] -m [analyze mode]");
                        break;
            }
}

printf("Analayzing\n");
Analyze(imagefolder,db_file,thresh);
printf("Report of Analayzing\n %s",Report);
 
std::ofstream out("Report.txt");
out << Report;
out.close();

return 0;

}
