#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <inttypes.h>
#include <time.h>
#include <string.h>
#include <sys/ioctl.h>
#include <asm/unistd.h>
#include <linux/perf_event.h>
#include <linux/hw_breakpoint.h>
#include <sys/resource.h>
#include "cacheutils.h"

uint64_t start, end;

int add(int a, int b)	{

	sched_yield();
	int z = a + b;

	return z;
}

int getC1()	{
	int x = 0, a = 5, b = 6;
	x = add(a,b);
	x++;
	return x;
}

int getC2()	{
	int x = 0;
	x = getC1();
	x++;
	return x;
}

int getC3()	{
	int x = 0;
	x = getC2();
	x++;
	return x;
}

int getC4()	{
	int x = 0;
	x = getC3();
	x++;
	return x;
}

int getC5()	{
	int x = 0;
	x = getC4();
	x++;
	return x;
}

int getC6()	{
	int x = 0;
	x = getC5();
	x++;
	return x;
}

int getC7()	{
	int x = 0;
	x = getC6();
	x++;
	return x;
}

int getC8()	{
	int x = 0;
	x = getC7();
	x++;
	return x;
}

int getC9()	{
	int x = 0; 
	x = getC8();
	x++;
	return x;
}

int getC10()	{
	int x = 0;
	x = getC9();
	x++;
	return x;
}

int getC11()	{
	int x = 0;
	x = getC10();
	x++;
	return x;
}

int getC12()	{
	int x = 0;
	x = getC11();
	x++;
	return x;
}

int getC13()	{
	int x = 0;
	x = getC12();
	x++;
	return x;
}

int getC14()	{
	int x = 0; 
	x = getC13();
	x++;
	return x;
}

int getC15()	{
	int x = 0; 
	x = getC14();
	x++;
	return x;
}

int getC16()	{
	int x = 0;
	x = getC15();
	x++;
	return x;
}


int main(int argc, char *argv[])	{
	CPU_affinity(2);
	int z = 0; 

	char filename[100];
    	strcpy(filename, "filetiming_");
	strcat(filename, argv[1]);
	strcat(filename, "_");
    	strcat(filename, argv[2]);
    	strcat(filename, ".txt");
	
	FILE *fp = fopen(filename,"w");


	int i, j;
	for (i = 0; i < 260; i++)	{ 
		for (j=0; j < 20; j++)
			longnop();
		uint64_t start = rdtsc_begin();
		z = getC14();
		uint64_t end = rdtsc_end(); 
		printf("%lu\n",(end - start));
		if (i > 80 && i < 160)
			fprintf(fp,"%lu\t%lu\t%lu\n",start, end, (end - start));

	}

	fclose(fp);
	return 0;
}
