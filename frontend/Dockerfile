FROM node:20-slim

WORKDIR /app/nosylos

COPY package.json ./package.json
RUN npm install

COPY . .

CMD ["npm", "run", "dev"]
