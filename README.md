# Online learning trading pipeline
```
M2 Data Science at Ecole Polytechnique
```

## How to run the project ?
To make this project work, you need docker and docker-compose in order to start the kafka and zookeeper containers.
Then you just have to use the following commands:

**Step 1 :** Create a python virtual environment
```commandline
$ python -m venv venv-name
```

**Step 2 :** Run the virtual environment

````commandline
# Windows PowerShell
> venv-name\Scripts\activate.ps1

# Linux terminal (bash)
$ source venv-name/bin/activate
````

**Step 3 :** Go to the root directory then install the dependencies
```commandline
$ pip install -r requirements.txt
```


**Step 4 :** Run docker-compose to install and run kafka and zookeeper containers
```commandline
$ docker-compose -f docker-compose.yml up
```

**Step 5 :** You can now run all the python scripts in separate terminals.
```commandline
$ python ingest_data.py
```
```commandline
$ python add_features.py
```
```commandline
$ python model.py
```
**Step 6 :** In order to visualise predictions, you can use following command:
```commandline
$ python display.py
```
## Thanks !
