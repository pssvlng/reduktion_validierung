# wordnet-analysis

## Prerequisites
- Install [Docker](https://docker.com/).
- Build the Docker container.

## Installation
Run the following command to build the application:
```
docker-compose build
```
## Execution
Run the following command to start the application
```
docker-compose up
```
## Running the Application
- The service should now be available on port 5000 (e.g. http://localhost:5000/api/validation/description)
- It is a POST request and the body must be json and contain two parameters - text and lang (e.g text = "Meine Beschreibung", lang = "de")


