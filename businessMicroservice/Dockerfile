## For Task6
FROM python:3.9-slim
# Use an official Python runtime as a parent image. Simply put it has base OS image like say linux/ubuntu and on top of it it has Python related dependencies installed, combined piece is served to us in this image.

LABEL maintainer="Suraj Verma, Github: surajv311"

ENV APP_HOME /businessmicroservice
# Set environment variables
ENV APP_MODE_DOCKER=docker_mode
# We can also write it as 'docker_mode'

RUN mkdir $APP_HOME
# Running the command

WORKDIR $APP_HOME
# Set the working directory to $APP_HOME which is /businessmicroservice. Basically, once your container runs which has our OS and Python related env setup this is the directory where I want to work with - Kind of creating a mini computer.
COPY . /$APP_HOME
# Observe that there are 3 components in above command: [COPY], [.], [/$APP_HOME]. Copy the current directory/folders contents present in local mac - represented via '.' into the container environment at $APP_HOME directory which in our case is /businessmicroservice present inside the container, apart from its other folders like /bin, /lib, /var, etc... As said earlier, its like setting up a mini computer
# If say I write COPY ./apiLoadTest /$APP_HOME - in this case, it will copy just this folder in the container.
# Understand that we are doing all this to make development setup platform agnostic. In other words, once we can build an image out of this dockerfile by executing all this steps. And say we publish the image in DockerHub or share with another developer. The developer would be able to access all the folders/files I had copied and created an image out of it in his/her machine without setting up python, fastapi, etc etc - all he should have is docker. They can pull my image and run it i.e create a docker container, then they will anyways be able to get access to all data/setup I had done and run the app.

RUN pip install --no-cache-dir -r requirements.txt
# Install any needed packages specified in requirements.txt

EXPOSE 8900 8901
# Make port 8900 & 8901 available to the world outside this container - Note that EXPOSE keyword is just for documentation in Dockerfile and does not have any functional impact. The actual port mapping is determined by the -p flag in the docker run command. This flag specifies the host-to-container port mapping.

## Now 2 ways to run the FastAPI application code present in app.py:
# CMD ["./run-server.sh"] # (Under Testing as getting errors using podman, docker not able to use ~ Error: preparing container for attach: crun: open executable: Permission denied: OCI permission denied) Way 1: Run app.py when the container launches; Check the .sh file defined in repo which has the command to execute when container runs
# CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8900 --reload"] # Way 2: Note that Using sh -c in the CMD instruction of a Dockerfile allows you to execute a shell command. This can be particularly useful when you need to perform tasks like setting environment variables, running complex commands, or dynamically configuring command-line arguments. sh calls the program sh as interpreter and the -c flag means execute the following command as interpreted by this program. In Ubuntu, sh is usually symlinked to /bin/dash, meaning that if you execute a command with sh -c the dash shell will be used to execute the command instead of bash.

## Cases: We have 3 moving parts here: Host machine which is my macbook currently, in the cloud world it could be an EC2 machine, Container named bmservicecontainer running in the host machine - can be seen in Podman/Docker Desktop, FastAPI App server running inside the container. There are few things to understand here:
# First understand host vs port: A host is a computer or other device connected to a network that provides resources, services, and applications to users or other devices on the network. It is identified by an IP address (IPv4 or IPv6) and optionally a domain name. In computer networking, localhost (meaning "this computer") is the standard hostname given to the address of the loopback network interface. Localhost always translates to the loopback IP address 127.0.0.1 in IPv4. A port is a virtual endpoint for communication in networking, used to identify a specific process or service running on a host. Ports allow multiple network services to coexist on a single host by distinguishing traffic intended for different services or applications. Eg: For an app, say userLogin service and userBlocking service - both existing in the same machine (say EC2 machine), but being exposed via different ports in that machine. Host is a global identifier in a network. Port is local identifier on a specific host.
# Any requests that come to the mac machine host i.e localhost here - say when I search for http://127.0.0.1:8900/ or http://0.0.0.0:8900/ on browser or via postman, it will not redirect/route the request directly to the fastapi server port running inside the container. Even though say we spin up our container using docker run command on port 8900 and then say we spin up our fastapi server also on same port 8900... There are 3 layers (host, container, app server) as we see, and to redirect we use port mapping. (explained below)
# Port forwarding, also known as port mapping, is a technique used in networking to redirect a network port from one network address to another. Port forwarding is directing traffic from the outside world to the appropriate server inside a local TCP/IP network.
# Notice what happens with below combinations once we keep building the dockerfile with the combinations and spin up the container:
## Combination 1:
# Running in terminal as we know that is how we port map and run the app: podman run -p 4500:8900 --name bmservicecontainer bmserviceimage (or) docker run -p 4500:8900 --name bmservicecontainer bmserviceimage
# Defined in Dockerfile: uvicorn app:app --host 0.0.0.0 --port 8900 --reload
# Here when we hit this endpoint in our host machine: http://127.0.0.1:4500/ or http://localhost:4500/ -> It redirects the request from port 4500 of host machine to port 8900, basically its mapping it. On port 8900 our container is exposed/running the fastapi server (You can do docker ps or podman ps to check validate the port mapping). We see the unicorn command running wherein our fastapi app running on port 8900 which is exposed by the container - Hence the request that came all the way from port 4500 to the app server running inside the container on port 8900.
# Notice when you run a FastAPI app inside a Docker container we are using --host 0.0.0.0 rather than binding it to 127.0.0.1, because in that case the application will only accept connections from within the container. This means that even if you publish a port on the host machine using Docker (e.g., docker run -p 8000:8000), you won't be able to access the application from outside the container because it is only listening for connections on the container's localhost. In contrast, if you bind the FastAPI app to 0.0.0.0, the application will listen for connections on all available network interfaces. When you publish a port using Docker, this setting allows external access. Also, the configuration for binding an application to 0.0.0.0 rather than 127.0.0.1 is not specific to FastAPI; it applies to any application running in a Docker container that you want to access from outside the container. This includes web servers, APIs, databases, and other network services.
# Note after every combination I am rebuilding the image and respawning the container again: [podman build --no-cache -t bmserviceimage .] (Using --no-cache keyword, can be removed though); And to access the server in browser/postman I am visiting http://127.0.0.1:4500/ or http://localhost:4500/ and I get the response.
## Combination 2:
# Terminal: podman run -p 4500:8735 --name bmservicecontainer bmserviceimage
# Dockerfile code: uvicorn app:app --host 0.0.0.0 --port 8900 --reload
# As you see, our app is running on port 8900 and we are redirecting to port 8735 where nothing is running so anyways app would not run
## Combination 3:
# Terminal: podman run --name bmservicecontainer bmserviceimage
# Dockerfile code: uvicorn app:app --host 0.0.0.0 --port 8900 --reload
# No port is mapped so you won't be able to access the app from host machine
## Combination 4:
# Terminal: podman run -p 4500:8900 --name bmservicecontainer bmserviceimage
# Dockerfile code: uvicorn app:app --host 130.0.1.1 --port 8900 --reload
# Not working as it says cannot assign requested address. In FastAPI, when you specify the host for your server, you usually use 0.0.0.0 to make the server accessible on all network interfaces or 127.0.0.1 to make it accessible only locally. However, specifying a specific IP address like 130.0.1.1 for the FastAPI server depends on whether that IP address is actually assigned to a network interface on your machine. If 130.0.1.1 is not assigned to any network interface on your machine, the FastAPI server won't be able to bind to it, and you'll encounter an error. You can check if it is assigned IP or not in network interface using: ifconfig | grep "127.0.1.1" or ifconfig | grep "130.0.1.1"
## Combination 5:
# Terminal: podman run -p 4500:8900 --name bmservicecontainer bmserviceimage
# Dockerfile code: uvicorn app:app --host 127.0.0.1 --port 8900 --reload
# Not working since as discussed earlier it should be --host 0.0.0.0
## Conclusion: Combination 1 is way to go so using command: podman run -p 4500:8900 --name bmservicecontainer bmserviceimage and host 0.0.0.0

## Note eg: Incase we want to run main.py file which is inside sampleService folder, we will give the path in command as expected from fastapi
# CMD ["sh", "-c", "uvicorn sampleService.main:app --host 0.0.0.0 --port 8901 --reload"]

# Another learning 1: We could also segregate the "sh", "-c" using ENTRYPOINT command in docker; So we could define:
# ENTRYPOINT ["sh", "-c"] # And then below:
# CMD ["uvicorn sampleService.main:app --host 0.0.0.0 --port 8901 --reload"]
# The ENTRYPOINT specifies a command that will always be executed when the container starts. The CMD specifies arguments that will be fed to the ENTRYPOINT.

# Another learning 2: If we want to execute multiple commands in CMD, we should use &&; Eg: CMD ["echo 'Starting the application...' && uvicorn app:app --host 0.0.0.0 --port 8000"]

# Another learning 3: We can have only 1 CMD command instruction and 1 ENTRYPOINT command instruction in dockerfile - if we define it 2 times, the latest one will get executed/may give errors - keep in mind.

# We apply all our learnings from above and run the businessMicroservice and sampleService inside it on different ports to have full fledged container running
ENTRYPOINT ["sh", "-c"]
CMD ["uvicorn app:app --host 0.0.0.0 --port 8900 --reload & uvicorn sampleService.main:app --host 0.0.0.0 --port 8901 --reload"]

######################################################################################################################################################################################################
# Note:
# A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image. Here are the main components of a Dockerfile and explanations of when and how to use them:
# 1. FROM
# FROM <image>
# Description: Specifies the base image to use for the Docker image. This is the starting point for the build process.
# When to Use: Always, as it defines the base layer for your image.
# Example: FROM python:3.9-slim
# 2. LABEL
# LABEL key=value
# Description: Adds metadata to an image. Useful for providing information such as maintainer details or a version number.
# When to Use: When you want to include metadata in the image.
# Example: LABEL maintainer="you@example.com"
# 3. RUN
# RUN <command>
# Description: Executes a command in a new layer on top of the current image and commits the results. This is often used for installing packages.
# When to Use: When you need to install dependencies or run commands that are required to build your application.
# Example: RUN apt-get update && apt-get install -y gcc
# 4. COPY and ADD
# COPY <src> <dest>
# ADD <src> <dest>
# Description:
# COPY copies files and directories from the host file system to the image.
# ADD does the same as COPY but also supports extracting tar files and fetching files from URLs.
# When to Use: Use COPY for simple copying and ADD for additional functionalities.
# Example: COPY . /app
# 5. WORKDIR
# WORKDIR /path/to/workdir
# Description: Sets the working directory for any subsequent RUN, CMD, ENTRYPOINT, COPY, and ADD instructions.
# When to Use: When you want to set the working directory for your application.
# Example: WORKDIR /app
# 6. CMD
# CMD ["executable","param1","param2"]
# Description: Provides defaults for an executing container. There can only be one CMD instruction in a Dockerfile. If you provide multiple CMD instructions, only the last one will take effect.
# When to Use: To specify the default command to run when the container starts.
# Example: CMD ["python", "app.py"]
# 7. ENTRYPOINT
# ENTRYPOINT ["executable", "param1", "param2"]
# Description: Configures a container that will run as an executable. It allows you to configure a container to run as if it was that executable.
# When to Use: When you want to define a container with a specific executable.
# Example: ENTRYPOINT ["python"]
# 8. ENV
# ENV key=value
# Description: Sets environment variables.
# When to Use: To define environment variables that will be available in your container.
# Example: ENV APP_ENV=production
# 9. EXPOSE
# EXPOSE <port>
# Description: Informs Docker that the container listens on the specified network ports at runtime. It does not actually publish the port. When you run a Docker container, the EXPOSE directive in the Dockerfile is mainly for documentation purposes and does not have any functional impact on port mappings. It indicates which ports the container listens on, but it does not configure those ports. The actual port mapping is determined by the -p flag in the docker run command. This flag specifies the host-to-container port mapping.
# When to Use: When your application runs on specific ports.
# Example: EXPOSE 80
# 10. VOLUME
# VOLUME ["/data"]
# Description: Creates a mount point with the specified path and marks it as holding externally mounted volumes from native host or other containers.
# When to Use: When you need to persist data generated by and used by Docker containers.
# Example: VOLUME ["/app/data"]
# 11. USER
# USER <username or UID>
# Description: Sets the user name or UID to use when running the image and for any RUN, CMD, and ENTRYPOINT instructions that follow it in the Dockerfile.
# When to Use: When you want to run the container as a non-root user for security reasons.
# Example: USER appuser
# 12. ONBUILD
# ONBUILD <instruction>
# Description: Adds a trigger instruction to the image that will be executed when the image is used as a base for another build.
# When to Use: When you want to define actions that should be taken when the image is used as a base for another build.
# Example: ONBUILD COPY . /app/src
# Here's an example Dockerfile that demonstrates the use of several components:
# # Use an official Python runtime as a parent image
# FROM python:3.9-slim
# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# # Set the working directory
# WORKDIR /app
# # Copy the current directory contents into the container at /app
# COPY . /app
# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# # Make port 80 available to the world outside this container
# EXPOSE 80
# # Define environment variable
# ENV NAME World
# # Run app.py when the container launches
# CMD ["python", "app.py"]
# Summary
# Understanding these components helps you build efficient, manageable, and reusable Docker images. Each instruction serves a specific purpose and can be combined to define the exact environment and behavior of your Docker container.

## Good link/note: https://stackoverflow.com/questions/55108649/what-is-app-working-directory-for-a-dockerfile
## Good link/note: When you create a Docker image and publish it to Docker Hub, anyone who downloads and runs that image on their machine will have all the files and configurations that were present in the image at the time it was created. This includes: Any files and directories you copied into the image, Any software packages or dependencies you installed, Any environment variables you set, Any configurations or changes you made.
## Good link/note: Containers don't inherently have an app directory by default; it depends on how the Docker image is built and what the Dockerfile specifies. The presence of an app directory is typically a convention used by developers to organize their application files within the container. When you start a container from a base image, it will have a default set of directories typical to a Linux filesystem, depending on the base image used. Common directories include: /bin, /lib, /etc, /var, /tmp, etc. Developers can define custom directories in the Dockerfile using the WORKDIR or RUN mkdir commands. You can start a container and then use the docker exec command to run shell commands inside the container i.e then using ls to list all dirs, allowing you to explore its filesystem.

## Note below explantion repeated in the docker-compose yaml file as well for later reference when we do another task; But for sake of connectivity of current task, I am defining about docker compose file as well here...
# A Docker Compose file, typically named docker-compose.yml, is used to define and manage multi-container Docker applications. It allows you to define services, networks, and volumes in a single YAML file, providing a streamlined way to manage your Docker environment. Below are the primary components of a Docker Compose file:
# 1. version
# The version key specifies the version of the Docker Compose file format. The most common versions are 2, 2.1, 3, and 3.8.
# version: '3.8'
# 2. services
# The services key is where you define the different services (containers) that make up your application. Each service can be configured with various options.
# services:
#   web:
#     image: nginx:latest
#     ports:
#       - "80:80"
#   db:
#     image: postgres:latest
#     environment:
#       POSTGRES_DB: mydatabase
#       POSTGRES_USER: user
#       POSTGRES_PASSWORD: password
# 3. networks
# The networks key allows you to define custom networks for your services. This is useful for setting up isolated network environments for your containers.
# networks:
#   mynetwork:
#     driver: bridge
# You can then assign services to these networks:
# services:
#   web:
#     image: nginx:latest
#     networks:
#       - mynetwork
#   db:
#     image: postgres:latest
#     networks:
#       - mynetwork
# 4. volumes
# The volumes key allows you to define shared storage volumes that can be used by your services. Volumes are useful for persisting data across container restarts.
# volumes:
#   myvolume:
# You can then mount these volumes in your services:
# services:
#   db:
#     image: postgres:latest
#     volumes:
#       - myvolume:/var/lib/postgresql/data
# Common Service Configuration Options
# image: Specifies the Docker image to use for the service.
# image: nginx:latest
# build: Specifies build configuration for the service. It can point to a directory with a Dockerfile or define build arguments.
# build:
#   context: ./path/to/build/context
#   dockerfile: Dockerfile
# ports: Maps ports on the host to ports in the container.
# ports:
#   - "80:80"
# environment: Defines environment variables for the service.
# environment:
#   POSTGRES_DB: mydatabase
#   POSTGRES_USER: user
#   POSTGRES_PASSWORD: password
# volumes: Mounts host directories or named volumes into the container.
# volumes:
#   - myvolume:/var/lib/postgresql/data
#   - ./localdir:/containerdir
# networks: Connects the service to one or more networks.
# networks:
#   - mynetwork
# depends_on: Specifies dependencies between services. Docker Compose will start the dependencies before starting the service.
# depends_on:
#   - db
# command: Overrides the default command for the container.
# command: python app.py
# entrypoint: Overrides the default entrypoint for the container.
# entrypoint: /app/entrypoint.sh
# Here's a full example of a docker-compose.yml file for a web application with a database:
# version: '3.8'
# services:
#   web:
#     image: nginx:latest
#     ports:
#       - "80:80"
#     networks:
#       - mynetwork
#     depends_on:
#       - app
#   app:
#     build:
#       context: ./app
#     networks:
#       - mynetwork
#     environment:
#       - DATABASE_URL=postgres://user:password@db:5432/mydatabase
#     volumes:
#       - ./app:/app
#   db:
#     image: postgres:latest
#     networks:
#       - mynetwork
#     environment:
#       POSTGRES_DB: mydatabase
#       POSTGRES_USER: user
#       POSTGRES_PASSWORD: password
#     volumes:
#       - myvolume:/var/lib/postgresql/data
# networks:
#   mynetwork:
#     driver: bridge
# volumes:
#   myvolume:
# In this example:
# web service uses the Nginx image and maps port 80.
# app service builds from a local context and connects to the same network as the web service.
# db service uses the PostgreSQL image and stores its data in a named volume.
# All services are connected to a custom bridge network.
# Environment variables are used to configure the services, and volumes are used to persist data and share files between the host and containers.

## Good link/note: Docker containers are easiest to use with stateless applications because their filesystems are ephemeral in nature. Changes made to a container’s environment are lost when the container stops, crashes, or gets replaced. You can Dockerize stateful applications such as databases and file servers by attaching volumes to your containers. Volumes provide persistent storage that’s independent of individual containers. You can reattach volumes to a different container after a failure or use them to share data between several containers simultaneously. Volumes are a mechanism for storing data outside containers. All volumes are managed by Docker and stored in a dedicated directory on your host, usually /var/lib/docker/volumes for Linux systems. Volumes are mounted to filesystem paths in your containers. When containers write to a path beneath a volume mount point, the changes will be applied to the volume instead of the container’s writable image layer. The written data will still be available if the container stops – as the volume’s stored separately on your host, it can be remounted to another container or accessed directly using manual tools. Bind mounts are another way to give containers access to files and folders on your host. They directly mount a host directory into your container. Any changes made to the directory will be reflected on both sides of the mount, whether the modification originates from the host or within the container. Bind mounts are best used for ad-hoc storage on a short-term basis. They’re convenient in development workflows. For example: bind mounting your working directory into a container automatically synchronizes your source code files, allowing you to immediately test changes without rebuilding your Docker image. Volumes are a better solution when you’re providing permanent storage to operational containers. Because they’re managed by Docker, you don’t need to manually maintain directories on your host. There’s less chance of data being accidentally modified and no dependency on a particular folder structure. Volume drivers also offer increased performance and the possibility of writing changes directly to remote locations.

## Image frpbusinessmicroservicedockersrj maintained by: Suraj Verma <github: surajv311> - Created as a part of building and learning about microservices: https://github.com/surajvm1/LearningMicroservices
