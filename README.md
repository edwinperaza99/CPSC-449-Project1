# CPSC-449 Project 2

## Group Members

- Edwin Peraza
- Divya Tanwar
- Gaurav Warad
- Abhinav Singh
- Ryan Novoa
- Chase Walsh
- Mc Gabriel Fernandez

## Project Description
This project is a continuation of RESTful API designed to retrieve different records from a university system from Project 1. Project 2 adds implementation of authentication service and load balancing that serve three different user roles: students, instructors, and registrar.

## Run Instruction
1. Clone this repository:
    ```
    git clone https://github.com/CodieTamida/CPSC-449-Project2.git
    ```
2. Open directory to `project1`
    ```
    $ cd project1
    ```
3. Initialize Python virtual environment and install required packages

    ```
    make
    ```
4. Give permission
    ```
    chmod 777 ./api/bin/init.sh
    ```
5. Setup Database
    ```
    ./api/bin/init.sh
    ```
6. Return to main directory `CPSC-449-Project2`
    ```
    cd ..
    ```
7. Start server
    ```
    foreman start
    ```
