FROM node:lts-alpine
ENV NODE_ENV=production
ENV AWS_REGION=us-east-1
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install --production --silent && mv node_modules ../
COPY . .
EXPOSE 80
RUN chown -R node /usr/src/app
USER node
CMD ["node", "index.js"]

# sample startup command
# docker run -d -e PORT=80 -e AWS_ACCESS_KEY_ID='ASI************F4' -e AWS_SECRET_ACCESS_KEY='u4*******************CA' -e AWS_SESSION_TOKEN='Fw**********************************7t' -p 80:80 2*********3.dkr.ecr.us-east-1.amazonaws.com/rpi-aws:0.0.4

