# Stage 1 — build Vite app
FROM node:20-slim AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --ignore-scripts

COPY . .

# VM_IP is injected at build time from docker-compose build args
# Vite bakes VITE_* env vars into the static bundle at build time
ARG VM_IP
ENV VITE_API_URL=http://${VM_IP}:8001
RUN npm run build


# Stage 2 — serve with Nginx on port 8081
FROM nginx:alpine AS runner

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/storyvault.conf

EXPOSE 8081

CMD ["nginx", "-g", "daemon off;"]
