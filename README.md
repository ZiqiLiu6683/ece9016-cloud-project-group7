### ECE 9016 Cloud Project - Group 7
A flask web application connectted to MySQL database.

## Prerequisites
Python 3.10+
MySQL Server
pip

## Local Deployment
# Step1: Set Up Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
# Step2: Install Dependencies
mysql -u root -p < db/init.sql
# Step3: Set Environment Variables
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=products_db
# Step4: Run Flask Application
cd app
python app.py
# Step5: Access Through Browser
http://127.0.0.1:5005

