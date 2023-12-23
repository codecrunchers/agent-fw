FROM node:18
WORKDIR /usr/src/app
COPY package*.json ./
RUN yarn add express pug socket.io 
RUN npm install
COPY . .
EXPOSE 5555
CMD ["yarn", "start"]

