"""The file filters.py seems to be a Python file that defines a custom template filter for the Flask application
   (GreenGroceries). Let's break down the contents of the file: This line imports the Flask application object (app) 
   from the GreenGroceries module. It suggests that the Flask application is defined in a file named GreenGroceries.py
     or a package named GreenGroceries. """

from FineWatches import app


@app.template_filter('format_data')
def format_data(string):
    return string.replace('_', ' ').capitalize()
