# Use the arm32v7/nginx:bookworm image as the base image
FROM nginx:bookworm

# Copy the thumbnails directory to the nginx html directory
COPY /usr/share/MTV2/thumbnails /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]