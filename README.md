## Project Title: Database Design

## Project Overview

This project demonstrates the design and implementation of a normalized database using both SQL and NoSQL (MongoDB) systems. It includes creating CRUD API endpoints with FastAPI and a script to fetch data for predictions using a machine learning model. The assignment covers key concepts in database schema design, API development, and predictive analysis.

## Table of Contents

- [Project Overview](#project-overview)
- [Tasks](#tasks)
  - [Task 1: Database Schema Design](#task-1-database-schema-design)
  - [Task 2: SQL and MongoDB Implementation](#task-2-sql-and-mongodb-implementation)
  - [Task 3: CRUD API Endpoints](#task-3-crud-api-endpoints)
  - [Task 4: Prediction Script](#task-4-prediction-script)
- [Technology Stack](#technology-stack)
- [Contributions](#contributions)

## Tasks

1. **Task 1: Database Schema Design**:
   - **Normalization**: Designed to achieve Third Normal Form (3NF) for optimal structure and minimal redundancy.
   - **Key Tables**: `Companies`, `Employees`, `Projects` with relationships managed by primary and foreign keys.
   - **Diagram**: Created with Draw.io and saved as `Database_Design_Diagram.drawio.png`.

2. **Task 2: SQL and MongoDB Implementation**:
   - **SQL Implementation**:
     - Objective: Create a database and populate it using a Kaggle dataset, resulting in three tables with foreign and primary keys.
     - **Toolkit**:
       - Supabase: Deployed database interacting with APIs
       - FastAPI
       - SQLAlchemy: ORM for database interaction
     - **Scripts**:
       - `populate.py`: Automates database population through API.
       - `config.py`: Connects the database to the application using environment variables stored in `.env`.
     - **Tables**:
       - **User**: Contains users from the dataset with their email addresses and a UUID primary key.
       - **Countries**: Includes all countries from the dataset with a UUID primary key.
       - **User_data**: Stores remaining user data with foreign keys from the `User` and `Countries` tables.

   - **MongoDB Implementation**:
     - Project imports customer data from a CSV file into MongoDB, creating collections and inserting records.
     - **Collections and Data Insertion**:
       - **Customers**: Basic information like `customer_id`, `name`, `gender`, and `age`.
       - **Contacts**: Customer contact details such as `email` and `country`.
       - **FinancialInfo**: Financial information like `annual salary`, `credit card debt`, `net worth`, and `car purchase amount`.
     - Script ensures no duplicate `customer_id` entries in each collection.

3. **Task 3: CRUD API Endpoints**:
   - FastAPI-based CRUD application managing users with PostgreSQL and SQLAlchemy.
   - **Features**:
     - Endpoints for creating, reading, updating, and deleting users.
     - Robust error handling using HTTP exceptions.
     - Interactive API documentation on startup for easy endpoint exploration.

4. **Task 4: Prediction Script**:
   - **Overview**: Python script for predicting car purchase amounts.
   - **Steps**:
     1. Fetches the latest user data from an API endpoint.
     2. Preprocesses and normalizes data to fit model input requirements.
     3. Loads a pre-trained model and predicts car purchase amounts based on the latest user data.
   - **Setup and Prerequisites**:
     - Required dependencies:
       - `Python 3.x`, `requests`, `pandas`, `numpy`, `json`, `pickle`, `logging`
     - **Installation**:
       ```bash
       pip install requests pandas numpy
       ```
   - **Folder Structure**:
     - `model/model.pkl`: Pre-trained machine learning model.
     - `model/normalization_params.pkl`: Normalization parameters for data preprocessing.
     - `location_freq.json`: JSON file mapping countries to numeric values.

   - **Script Explanation**:
     1. **Import Libraries and Configure Logging**: Sets logging level to `INFO` for real-time feedback.
     2. **Load Model and Normalization Parameters**:
        - Loads `model/model.pkl` and `model/normalization_params.pkl`, handling errors via `try-except`.
     3. **Load `location_freq` Data**: Loads country mappings for standardized input.
     4. **Define Key Mappings**: Dictionary `KEY_MAPPING` aligns API JSON keys with model’s expected column names.
     5. **Normalize Data**: Function applies min-max normalization using loaded parameters.
     6. **Fetch Latest User Data**: Sends GET request to API endpoint, logs any request errors.
     7. **Prepare Data for Prediction**: Transforms JSON data into DataFrame, applies mappings, and normalizes data for prediction.
     8. **Predict Car Purchase Amount**: Fetches, prepares data, and runs it through the model, logging the predicted result.

   - **Running the Script**:
     ```bash
     python your_script_name.py
     ```
   - The prediction result will display in the console if successful. Error messages or warnings are logged for troubleshooting.


## Technology Stack

- **SQL Database**: MySQL / PostgreSQL / SQLite (choose one based on your implementation)
- **NoSQL Database**: MongoDB
- **API Framework**: FastAPI
- **Prediction Model**: A simple custom model on Car Price prediction
- **Tools**: Draw.io for schema design

## Contributions

| Team Member                  | Role                        | Contribution                                 |
|------------------------------|-----------------------------|----------------------------------------------|
| Abdulhameed Teniola Ajani    | Database Schema Design      | Database schema design                       |
| Ken Ganza Kalisa             | SQL Implementation      | SQL collections setup, normalization     |
| Ochan Denmark LOKIDORMOI     | MONGODB     Implementation      | MongoDB collections setup, normalization     |
| Mariam Azeez                 | API Development (FastAPI)   | CRUD API endpoints                           |
| Smart Israel                 | Data Fetch & Prediction     | Prediction script integration                |


