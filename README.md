# Project Title

Django Backend for Cluvii

## Description

This is the Django backend for Cluvii, built using the Python web framework Django. The backend provides a RESTful API for handling data and performing operations for the frontend.

## Prerequisites

Before you begin, make sure you have the following software installed on your local machine:

- Python 3.x
- pip
- virtualenv

## Installation

To set up the Django backend, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/[username]/[project-name].git
   ```

2. Change to the project directory:

   ```bash
   cd cluvii_api
   ```

3. Create a virtual environment:

   ```bash
   virtualenv venv
   ```

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   pip3 install -r src/requirements.txt
   ```

6. Make migrations on modified models:

   ```bash
   python3 src/manage.py makemigrations <app-name>
   ```

7. Apply the migrations:

   ```bash
   python3 src/manage.py migrate
   ```

8. Run the development server:

   ```bash
   python3 src/manage.py runserver
   ```

The Django backend should now be running at [http://localhost:8000](http://localhost:8000).

## Usage

The RESTful API can be accessed at [http://localhost:8000/api/](http://localhost:8000/api/). Endpoints and request methods are defined in the project's `urls.py` and `views.py` files.

## Contributing

To contribute to the project, follow these steps:

1. Fork the repository.
2. Create a branch for your changes.
3. Make the changes.
4. Commit and push the changes to your branch.
5. Create a pull request.

## License

This project is licensed under the [name of the license]. See the [LICENSE](LICENSE) file for more information.
