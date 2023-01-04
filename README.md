# qwq

Scan the entire internet for Minecraft servers using masscan.

## Introduction

This project was inspired by the [Liveoverflow video](https://www.youtube.com/watch?v=VIy_YbfAKqo) on scanning Minecraft servers. It allows you to scan Minecraft servers and store the results in a MongoDB database. It utilizes the following technologies:

 - **Docker-Compose**: A tool for defining and running multi-container Docker applications
 - **MongoDB**: A cross-platform document-oriented database program
 - **Mongo Express**: A web-based MongoDB database management tool
 - **Masscan**: A fast TCP port scanner
 - **Python**: A programming language

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. Clone the repository to your local machine
```sh
git clone https://github.com/zyeinn/qwq.git
```

2. Change into the project directory
```sh
cd qwq
```

3. Replace the placeholder values for the credentials with your own. Be sure to keep the format of the values the same (e.g. if the placeholder is in the form `CHANGE_ME`, replace it with `your_value`).

4. Edit the `mc/config.json` file and update the username and password values with the MongoDB username and password that you set in step 3.

5. Build the Docker containers and start the services

```sh
docker-compose build
docker-compose up -d
```

6. Open your web browser and navigate to http://localhost:8081 to access the Mongo Express web interface. Use the Mongo Express username and password you set in step 3 to log in.


## Stopping the services

1. Change into the project directory
```sh
cd qwq
```

2. Run the following command to stop the services:
```sh
docker-compose down
```

## Additional notes

The Mongo Express service is exposed on port 8081. You can access the web interface by navigating to http://localhost:8081 in your web browser.
