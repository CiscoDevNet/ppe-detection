# build environment
FROM node:10.15.0 as builder
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY package.json /usr/src/app/package.json
COPY package-lock.json /opt/app/package-lock.json
RUN npm install --silent
COPY app /usr/src/app/app
COPY config /usr/src/app/config
COPY template /usr/src/app/template
COPY .babelrc /usr/src/app/.babelrc
# COPY . /usr/src/app
RUN sed -i -e 's/"API_ENDPOINT_URL":.*/"API_ENDPOINT_URL": "\/"/g' /usr/src/app/config/env/dev.json
# RUN sed -i -e 's/"BASENAME":.*/"BASENAME": "",/g' /usr/src/app/config/env/dev.json
RUN sed -i -e 's/"API_ENDPOINT_URL":.*/"API_ENDPOINT_URL": "\/"/g' /usr/src/app/config/env/production.json
RUN sed -i -e 's/target: "http:\/\/localhost:7030"/target: "http:\/\/ppe-backend:7030"/g' /usr/src/app/config/webpack/common.js
RUN sed -i -e 's/target: "ws:\/\/localhost:7030"/target: "ws:\/\/ppe-backend:7030"/g' /usr/src/app/config/webpack/common.js
RUN sed -i -e 's/const prod_host = .*/const prod_host = ""/g' /usr/src/app/config/webpack/common.js
RUN sed -i -e 's/let app_path = .*/let app_path = ""/g' /usr/src/app/config/webpack/common.js
RUN npm run production
RUN sed -i -e 's/\/ppe\//\//g' /usr/src/app/dist/app.js

# production environment
FROM nginx:1.13.9-alpine as production
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 7031
CMD ["nginx", "-g", "daemon off;"]
