# Step 1: Use Nginx base image
FROM nginx:alpine

# Step 2: Install dependencies (Python, pip, etc.)
RUN apk add --no-cache python3 py3-pip gcc musl-dev libffi-dev openssl-dev \
&& apk add --no-cache snapd \
&& snap install google-cloud-sdk --classic

# Step 3: Set environment variables
ENV PYTHONUNBUFFERED 1

# Step 4: Set up a working directory for Django app
WORKDIR /app

# Step 5: Copy the requirements.txt file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Step 6: Copy the entire Django project into the container
COPY . /app

# Step 7: Run collectstatic (to handle static files)
RUN python3 manage.py collectstatic --noinput

# Step 8: Expose port (Nginx will serve on this port)
EXPOSE 8000

# Step 9: Copy the Nginx configuration file
COPY ../nginx/nginx.conf /etc/nginx/nginx.conf

# Step 10: Run the Django app using Gunicorn and serve it via Nginx
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app_name.wsgi:application"]