FROM node:18-slim

WORKDIR /app/nosylos

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev"]