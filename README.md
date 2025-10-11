# FastAPI Project
## Overview
This is a FastAPI-based API project that provides api for spatial datasets. It offers a set of endpoints for get, create, update and delete spatial dataset. This API is designed to be lightweight, fast, and easy to use for [target audience, e.g., developers, data scientists, etc.].

## Features
Real-time data processing
Database integration with Sqlite

## Prerequisites
Before you begin, ensure you have met the following requirements:
Python 3.9.6 installed.
[Other dependencies such as databases, tools, etc.]

## Installation
Clone the Repository
```bash
git clone https://github.com/yourusername/your-project.git
cd your-project
 ```

## Create and Activate Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
 ```

## Install Dependencies
```bash
pip install -r requirements.txt
 ```

## Running the Application
### Start the API
```bash
uvicorn main:app --reload
 ```

The API will be available at http://127.0.0.1:8000
You can access interactive documentation at http://127.0.0.1:8000/docs