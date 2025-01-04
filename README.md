# Health Data QR Code Generator

This project is a Flask application that allows users to input health data and generates a static QR code containing that data. The information is stored in a MongoDB Atlas database, and the QR code can be downloaded for sharing.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Setup MongoDB Atlas](#setup-mongodb-atlas)
4. [Running the Application](#running-the-application)
5. [Usage](#usage)

--------------------------------------------------------------------------------------------------------------------------------------------
## Prerequisites

- Python 3.x
- MongoDB Atlas account
- pip (Python package installer)
-------------------------------------------------------------------------------------------------------------------------------------------
## Installation

1. **Clone the Repository**

   Open your terminal and run the following command to clone the repository:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
Create a Virtual Environment (optional but recommended)

You can create a virtual environment to manage your project dependencies:

bash
Copy code
python -m venv venv
Activate the virtual environment:

Windows:

bash
Copy code
.\venv\Scripts\activate
macOS/Linux:

bash
Copy code
source venv/bin/activate
Install Required Packages

Install the necessary packages by running:

bash
Copy code
pip install Flask flask_pymongo qrcode[pil]

------------------------------------------------------------------------------------------------------------------------
Setup MongoDB Atlas
Create a MongoDB Atlas Account

Go to MongoDB Atlas and create a free account.
Create a new Cluster in your MongoDB Atlas account.
Set Up a Database and Collection

Once your cluster is created, click on Database and create a database named health_db and a collection named patients.
Get the MongoDB Connection URI

In the MongoDB Atlas dashboard, go to Connect > Connect your application.

Copy the connection string, which will look like this:

bash
Copy code
mongodb+srv://<username>:<password>@cluster0.mongodb.net/health_db?retryWrites=true&w=majority
Replace <username> and <password> with your MongoDB Atlas username and password.

Configure Your Flask Application

Open app.py in your code editor.

Replace the connection string with your MongoDB Atlas URI:

python
Copy code
app.config["MONGO_URI"] = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/health_db?retryWrites=true&w=majority"
Make sure to use your actual MongoDB username and password.
---------------------------------------------------------------------------------------------------------------------------------------
Running the Application
Run the Flask Application 

In your terminal, ensure you are in the project directory and run:

bash
Copy code
python app.py (or) flask run --host=0.0.0.0 --port=5000
Access the Application

Open your web browser and go to http://127.0.0.1:5000/ to access the application.
---------------------------------------------------------------------------------------------------------------------------------------
Usage
Fill out the form with the following health data:

Name
Age
Medical Info
Click on Generate QR Code. The application will generate a QR code containing the entered data, which you can download.

View or Modify Data: Existing data can be viewed or modified as needed, with changes saved to the MongoDB Atlas database.
