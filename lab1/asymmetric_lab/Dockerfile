FROM python:3.9-slim

WORKDIR /app

# Copy all files from the asymmetric_lab directory
COPY . /app/

# Expose port 12000
EXPOSE 12000

# Command to run the Python HTTP server on port 12000
# The --bind 0.0.0.0 allows connections from any host
# The --directory . serves files from the current directory
CMD ["python", "-m", "http.server", "--bind", "0.0.0.0", "12000"]