<h1> Louisville Metro Police Department Bias Study </h1>

## todo 

### working in Cleaning and data builder 

- [x] Build API test 
- [x] Remove repeated code DRY 
- [x] Build classes 
  - [x] Data builder done 
  - [x] Cleaning class needed 
  - [x] plot classes needed 
- [x] Rework plots use plotly
  - [x] gender plots done   
- [ ] use dash for the dashboard
- [x] make new requirements.txt

<h2>Code Louisville Scope </h2>
This project was created to fulfill the requirements of Code Louisville’s Python Data Analytics 2 class. The project had 4 requirements as follow. 

  1. Read in two data sets. 
  1. Make 3 plots </li>
  1. Make a virtual environment for the project </li>
  1. Annotate our code </li>


## About The Data 
The purpose of the project was to determine if the LMPD had a racially motivated citation record. To make the calculations I used CSV sheets from Louisville Metro Open Data site. The first sheet was the police force which has all sworn officers with age sex etc. The next data set includes all the issued citations from the police with officers and drivers data. The final portion of data I used was from the census bureau to make a data frame for Louisville base line population. From the main graph we can determine that the black population did get more citations that our populations representation. The Hispanic police officers were the only group of officers that cited black drivers less that the Louisville population. However the real surprise of the data was that Hispanic population was cited above the population average by every race of officers. Ironically the Hispanic officer population was the only group of officers to cite above the population average. Alternatively we can conclude from the data the even though the population is almost equal in terms of genders. Males are almost twice as likely to receive a citation. 

# Requirements

- Make Make a virtual environment on your machine (directions below)

- From the directory pip install the requirements.txt file by running "pip install -r requirements.txt"

- Sign up for a Census API Key (https://api.census.gov/data/key_signup.html)

- Wen you get a API key:
  - make a file named api_key.py
  - inside the file store the key 
  - like this: api_key = "your_key_here"

- You can run `final.ipynb` to see a consolidated view of the project with little code. 

- Alternatively you can run main.py to see the whole project and have the plot launch into a browser. 

## Additional overview

| File | Description | 
|---|---| 
| data_builder.py | This file contains the logic to do the api calls for the project. |
| cleaning.py  | This file contains the logic to do all the cleaning for the project. |
| viz.py | This file contains the logic to do all the plotting and stats for the project. |
| main.py  | This file will run the project without using a jupyter notebook |
| final.ipynb | This file contains the project in notebook form. I abstracted away most of the code so it's easier for the viewer to see the findings. | 


### Project Requirements (detailed):
- Feature 1 Read data from 2 data sources - This was accomplished by doing 3 api calls.  

- Feature 2 - Manipulate and clean your data: The data was cleaned by removing missing data and dropping data that was not needed, and mapping values.

- Feature 3 - Visualize data -  By utilizing the `groupby` method sub plots where made to reveal a gender and racial bias on citations.

- Feature 4 - Utilized a virtual environment and include instructions in the README on how the user should run the project. 

- Feature 5 - Interpreted the data by annotating the code via markdown cells.

###  Virutal Environment Instructions

1. After you have cloned the repo to your machine, navigate to the project 
folder in GitBash/Terminal.
1. Create a virtual environment in the project folder. 
1. Activate the virtual environment.
1. Install the required packages. 
1. When you are done working on your repo, deactivate the virtual environment.

### Virtual Environment Commands
| Command | Linux/Mac | GitBash |
| ------- | --------- | ------- |
| Create | `python3 -m venv venv` | `python -m venv venv` |
| Activate | `source venv/bin/activate` | `source venv/Scripts/activate` |
| Install | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Deactivate | `deactivate` | `deactivate` |
