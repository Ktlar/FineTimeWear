"""
The app.py file seems to be the entry point for running the GreenGroceries web application. Let's break down its contents:

Import Statement:

from GreenGroceries import app: Imports the Flask application instance (app) from the GreenGroceries module.
Application Execution:

if __name__ == '__main__':: Checks if the script is being executed directly (not imported as a module).
app.run(debug=True): Starts the Flask development server to run the GreenGroceries application in debug mode.
When you execute the app.py script directly, it will run the Flask application in debug mode, allowing for automatic reloading
of the server on code changes and displaying detailed error messages in the browser. This makes it convenient for development
and testing purposes.

To start the GreenGroceries web application, you can run the app.py script using the Python interpreter.
For example, in the command line, navigate to the directory containing the app.py file and execute the following command:

Copy code
python app.py
This will start the Flask development server, and you should see output indicating that the server is running. 
You can then access the application by visiting the provided URL in a web browser """

from GreenGroceries import app

if __name__ == '__main__':
    app.run(debug=True)