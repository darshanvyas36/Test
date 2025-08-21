# --- Stage 1: Build the Backend ---
FROM python:3.12-slim as backend-builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY ./backend .


# --- Stage 2: Final Image with Nginx ---
FROM nginx:1.25-alpine

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/

# Copy frontend files
COPY ./frontend /usr/share/nginx/html

# Copy backend application from the builder stage
COPY --from=backend-builder /app /app

# Copy the startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port 80 for nginx
EXPOSE 80

# Set the entrypoint to the startup script
CMD ["/start.sh"]
