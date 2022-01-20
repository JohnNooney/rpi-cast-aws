# rpi-cast-aws
RaspberryPi as AirPlay receiver with logging to AWS. The main goal of this project is to 
provide a foundational for the system architecutre found in typical ChomeCast, FireStick, and AppleTV devices.
These devices usually have some cloud service integrations. So in order to replicate this environment a simple 
Admin logging SPA will be running in a cloud instance. In addition, this project relies on the github project [RPiPlay](https://github.com/FD-/RPiPlay) 
to work end-to-end.

# RPi Setup
1. run `sudo apt update` and `sudo apt upgrade` 
2. Install RPiPlay from this [github repo](https://github.com/FD-/RPiPlay) 
3. make sure RPiPlay is in `/home/pi/Downloads`
4. clone this repo into `/home/pi/Downloads` as well
5. create aws auth directory in `~/.aws` with required credentials file
6. install the required packages with `pip3 install -r requirements.txt`
7. start python program with `python3 gpiocontroller.py` OR `python3 gpiocontroller.py <username>` 

**NOTE**
Originally this project was going to use an LKM for providing the RPi functionality (see lkm-dataflow diagram and ./rpi/piirq.c) but due to 
security concerns around running call_usermodehelper() to make user-space calls from the kernel; this was abandonded. Instead the python script (./rpi/gpiocontroller.py)
holds all the main functionality. This is an infinite loop program intended to be launched at RPi startup but can simply be started following the steps above.

# Docker Setup
1. Install Docker
2. login to AWS ECR repository with Docker (this step requires you to have made an ECR prior)

# Docker Image Setup
1. navigate to root dir of admin-ui-nodejs
2. install node dependencies (this step requires you to have nodejs installed prior) 
3. create .env file with aws credentials (optional for local testing)
3. run `docker build -t <ECR repo:latest> .`
4. run `docker push <ECR repo:latest>`

# Running Docker Image
After building the docker image, it is recommended to test the image. Run the command below to do that.

`docker run -d -e PORT=80 -e AWS_ACCESS_KEY_ID='A**********4' -e AWS_SECRET_ACCESS_KEY='u********A' -e AWS_SESSION_TOKEN='Fw**********oG' -p 80:80 2******3.dkr.ecr.us-east-1.amazonaws.com/rpi-aws:0.0.4`


**NOTE**
if you have created a .env file during the setup you will need still need to put in these environment variables 
for your AWS account since the DockerFile excludes .env files during the build.

# Running Docker Image on AWS EC2 Instance
During the instance setup of your EC2 instance make sure to provide the user data script found in this repo at `./aws/ec2startup.sh`

# Reminder
make sure to have all services setup in the cloud based on the format outlined in the documentation

