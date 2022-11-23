# CISC327-Project
Group Project for CISC 327

# Style check (make sure the project follows pep8 guidelines)
// cd to project directory
cd CISC327-Project
flake8 --select=E .

# run all testing code 
// cd to project directory
cd CISC327-Project
pytest -s qbnb_test

# To run the development server:
python3 -m qbnb

# To run the dockerised application
1. Ensure docker is installed on your laptop
2. pull the latest code from github (Ensure that docker-compose is in the file)
3. run command “docker pull paynwahs/queens_cmpe327_project:v1” on terminal. This will pull the image docker hub onto your local machine. Run “docker image list” to ensure the image is pulled correctly
4. run command “docker-compose up” to start up docker-compose which will create and start up the following containers:
    1. `qbnb-web`: (web-option) Flask web application (including frontend and backend, in reality people like to further break backend into different independent services)
    2. `qbnb-db` : MySQL database
    3. `phpmyadmin` : Web interface for MySQL These services are all defined in our `docker-compose.yml` file. It also defines some resources:
    4. `qbnb-site` : the network connects everything
5. Access the following website from the ports
    1. qbnb-web : 127.0.0.1:8081
    2. qbnb-db web interface (phpadmin container) : 127.0.0.1:8082 
        1. server: qbnb-db
        2. username: root
        3. password: root