FROM node:20-alpine

WORKDIR /nasa-web-app/src/app
COPY package*.json ./
COPY . .

RUN npm install  --production
# Install Tailwind CSS and its dependencies
RUN npm install tailwindcss postcss autoprefixer

# Generate Tailwind CSS config files if they don't exist
RUN [ -f tailwind.config.js ] || npx tailwindcss init -p

RUN npm run build
EXPOSE 3000
CMD [ "npm" , "start"]