# Usage:
# make        # compile all binary
# make clean  # remove ALL binaries and objects

.PHONY = all clean

CC = gcc                        # compiler to use
CFLAGS = -og -ggdb
LFLAGS = -L. -L/usr/lib/arm-linux-gnueabihf/
INCLUDES = -I. -I/usr/include/python3.7
LIBS = -lm -li2c -lalgobsec 

TARGET = AirQualityReader
SRCS=$(wildcard *.c)
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

swig_wrap:
	swig -python $(TARGET).i

$(TARGET): $(OBJS) 
	${CC} -shared -o _$(TARGET).so $(OBJS) $(LFLAGS) $(LIBS)

.c.o:
	${CC} $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -rvf *.o *.so *~ $(TARGET)_wrap.* $(TARGET).py

