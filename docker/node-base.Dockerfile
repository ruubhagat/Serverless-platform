# base-node/Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY function.js .
CMD ["node", "function.js"]
