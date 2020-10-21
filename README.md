Develop in Python 3.8.5

To install:
1)  create virutal env in your project folder (saves the dependencies only in this projects folder)
    Windows: "py -m pip install virtualenv"
    Mac/Linux: "python3 -m pip install virtualenv"

    create the virtual env using
    Windows: "py -m venv env"
    Mac/Linux: "python3 -m venv env"

2)  Activate the virtual env
    Windows: ".\env\Scripts\activate"
    Max/Linux: "source env/bin/activate"

3)  Install dependencies, when virtual env is active
    "pip install -r requirements.txt"

4)  Create the config.py the same way it is on git. 
    Cannot be stored on git bc it has api keys


** if you add packages run
    "pip freeze > requirements.txt"