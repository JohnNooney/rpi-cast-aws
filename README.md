# rpi-cast-aws
RaspberryPi as AirPlay receiver with logging to AWS

# RPi Setup
1. run `sudo apt update` and `sudo apt upgrade` 
2. Install RPiPlay from this github repo 
3. make sure RPiPlay is in `/home/pi/Downloads`
4. clone this repo into `/home/pi/Downloads`
5. create aws auth directory in `~/.aws` and required credentials
6. start python program with `python3 gpiocontroller.py`

# Docker Setup
1. login to AWS ECR repository with Docker

# Docker Image Setup
1. navigate to root dir of admin-ui-nodejs
2. install dependencies and create .env file with aws credentials
3. run `docker build -t <ECR repo:latest> .`
4. run `docker push -t <same as above>`

# Key Points
make sure to have all services setup in the cloud based on the format outlined in the documentation

