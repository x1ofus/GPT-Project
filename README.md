# GPT Discord Project
### This was a fun project created to learn more about the mechanics of a GPT <br> using our own data.


## Setup
Make sure python and pip are installed

Run Setup.sh by typing "./Setup.sh" in your terminal. It may take a while.

## Building the Model

### BuildModel.py
Trains the model on the dataset by taking in the dataset as a text file and then placing the model into a model folder.

`python(3) .\GPT\scripts\BuildModel.py [datasetfileName.txt] [ModelName]`

## Saving and Loading the Model

### ExportModel.py
Exports the model and stores it into a database using MongoDB. At the moment, the name of the model in the database is hardcoded so only one model can be stored. Performance of the export is heavily dependent on internet speeds.

`python(3) .\GPT\scripts\ExportModel.py [ModelName]`

### ImportModel.py
Imports the model from the database and places it into the model folder with a user-specified name. Like with the exported model, the model that is in the database hardcoded and is the last one saved.

`python(3) .\GPT\scripts\ImportModel.py [ModelName]`


## Using the Model
The model can be accessed by generating one line at a time and printing it to the terminal. 

### AccessModel.py
Accesses the model based on the user-specified model name and uses it to generate sample text in the terminal output.

`python(3) .\GPT\scripts\AccessModel.py [ModelName]`

## [ADDITIONAL] Discord Chat to Dataset
The can read and create a dataset from discord log data using the [DiscordMate](https://discordmate.com/) extension that can be used to collect the messages and into a json object. This object is then used to create the text file that will be used as the dataset for the model.

### DataParser.py
Uses the data from the json file and generates the text file dataset using only the messages. The images are removed and the names of the users replace the IDs from the raw data.

`python(3) .\GPT\scripts\DataParser.py [infile.json] [outfile.txt]`

### UpdateDataset.py
To allow users to update the discord message logs, this script is used to combine two json objects into one. It checks to see if there are new logs and adds them to the main object. 

`python(3) .\GPT\scripts\UpdateDataset.py [newfilename.json] [masterfilename.json]`