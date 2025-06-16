# -----------------------
# Base build image
# -----------------------
FROM node:20-alpine AS builder


# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install all dependencies (dev + prod)
RUN npm install

# Build all packages (adjust this command if needed)
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
