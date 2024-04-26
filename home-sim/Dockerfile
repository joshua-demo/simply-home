FROM node:20.10.0-alpine

WORKDIR /sim

COPY ./package.json /sim/package.json
COPY ./package-lock.json /sim/package-lock.json

RUN npm install

COPY . .

EXPOSE 3001

CMD npm run dev