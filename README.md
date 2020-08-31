# ecobeeAirQualityControl
Code for element14 road test project https://www.element14.com/community/roadTestReviews/3355/l/raspberry-pi-click-board-sensor-kit-review

## How to build:
* Go to https://www.bosch-sensortec.com/software-tools/software/bsec/ and download BSEC software.
* Copy these files to the project folder: libalgobsec.a, bsec_integration.c, bsec_integration.h, bsec_interface.h, bsec_datatypes.h, bme680_defs.h, bme680.h, bme680.c
* make swig_wrap
* make all
 
## How to run:
* Update tokens.json with your own tokens. Please read the link above regrading how to get your own tokens.
* python3 ecobeeAirQualityControl.py
