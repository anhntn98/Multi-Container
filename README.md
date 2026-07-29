# Description
Demonstrates a multi-container setup using Docker Compose, including an Nginx reverse proxy, a web application, and a database. This project serves as a practical example of how to orchestrate multiple services in a containerized environment. Besides, it includes a CI/CD pipeline for automated testing and deployment using GitHub Actions.

# Features
- Multi-container architecture with Nginx, web application, and database.
- Continuous Integration (CI) pipeline using GitHub Actions.
- Automated testing with pytest to ensure the integrity of the application.

# Getting Started
To get started with this project, clone the repository and follow the instructions in the README files of each component. Ensure you have Docker and Docker Compose installed on your machine.
1. Clone the repository:
2. Change environment variables in the `.env` file as needed for your setup.
3. Run the following command to build and start the containers:
```bash
docker-compose up --build
```
4. Test whether the application is running by accessing `http://localhost:8000` in your web browser.
You can use curl to test signup and login endpoints:
```bash
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass", "email": "test@test.com"}'
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'
``` 


