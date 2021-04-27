// rp-mcp3008 Reads analogue values through MCP3008 chip


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wiringPi.h>
#include <mcp3004.h>
#include <wiringPiSPI.h>
#include <unistd.h>
#include <sys/time.h>

#define _BSD_SOURCE
#define BASE 100
#define SPI_CHAN 0


int main (int argc, char *argv[])
{

	
	int i = 2;
	int z;
	int measure;
	int samplepoints = 100000;
	int arr[samplepoints];
	int loop;
	float rate = 0;
	int periodus = 100;

	printf("wiringPiSPISetup RC=%d\n",wiringPiSPISetup(0,500000));
	mcp3004Setup(BASE,SPI_CHAN);
	
	struct timeval t1, t2, t3;
	long long elapsedTime;
	gettimeofday(&t1, NULL);
	

	 for (z = 0; z < samplepoints; ++z)
	{	
		while(1){
			gettimeofday(&t3, NULL);
			if(((t3.tv_sec * 1000000) + t3.tv_usec) >= ((t1.tv_sec * 1000000) + t1.tv_usec + (z*periodus))){
				break;
			}

		}

		measure = analogRead(BASE+i);
		arr[z] = measure;
			
	}
	gettimeofday(&t2, NULL);

	elapsedTime = ((t2.tv_sec * 1000000) + t2.tv_usec) - ((t1.tv_sec * 1000000) + t1.tv_usec);
	


	double time_taken = 10;
	float sr = samplepoints/time_taken;

	FILE * fp;
	fp = fopen ("DATASET.txt","w");
	fprintf (fp, "%d,",samplepoints);
	fprintf(fp, "%lld,", elapsedTime);
	int u;
	for(u = 0; u < samplepoints;u++){
       fprintf (fp, "%d,",arr[u]);
   }
}

