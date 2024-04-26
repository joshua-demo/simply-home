FROM node:20.10.0-alpine

WORKDIR /portal

COPY ./package.json /portal/package.json
COPY ./package-lock.json /portal/package-lock.json

RUN npm install

COPY . .

EXPOSE 3000

CMD npm run dev