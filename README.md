<h1> Louisville Metro Police Department Bias Study </h1>

## todo 

### working in Cleaning and data builder 

- [x] Build API test 
- [x] Remove repeated code DRY 
- [ ] Build classes 
  - [x] Data builder done 
  - [ ] Cleaning class needed 
  - [ ] plot classes needed 
- [ ] Rework plots use plotly
  - [x] gender plots done   
- [ ] use dash for the dashboard
- [ ] make new requirements.txt

<h2>Code Louisville Scope </h2>
This project was created to fulfill the requirements of Code Louisville’s Python Data Analytics 2 class. The project had 4 requirements as follow. 
<ol>
<li> Read in two data sets. </li>
<li> Make 3 plots </li>
<li> Make a virtual environment for the project </li>
<li> Annotate our code </li>
</ol>

### I revisited this project recently to add API calls to everything and play with a few new plotting ideas.

The API calls are built into the `data_builder.py` file. You will need a API key for the Cencus data. Other than that pull which data you need and proceed to the `revisited.ipynb` file. 

<h2> About The Data </h2>
The purpose of the project was to determine if the LMPD had a racially motivated citation record. To make the calculations I used CSV sheets from Louisville Metro Open Data site. The first sheet was the police force which has all sworn officers with age sex etc. The next data set includes all the issued citations from the police with officers and drivers data. The final portion of data I used was from the census bureau to make a data frame for Louisville base line population. From the main graph we can determine that the black population did get more citations that our populations representation. The Hispanic police officers were the only group of officers that cited black drivers less that the Louisville population. However the real surprise of the data was that Hispanic population was cited above the population average by every race of officers. Ironically the Hispanic officer population was the only group of officers to cite above the population average. Alternatively we can conclude from the data the even though the population is almost equal in terms of genders. Males are almost twice as likely to receive a citation. 

<h1> Requirements </h1>

This project was made with Anaconda installed, using the below packages in VS Code using Jupyter notebooks. PIP install packages as needed. Alternatively a virtual environment is included. 
<br>
<br>
Documentation for venv: (https://docs.python.org/3/tutorial/venv.html)
<br>
<br>
From the directory pip install the requirements.txt file by running "pip install -r requirements.txt"

<h3>Project Requirements:</h3>
Feature 1 Read data - Read data set from 2 csv file. 
<br>
Feature 2 - Manipulate and clean your data: In each data set I cleanded the sheets by removing missing data and dropping data that was not needed. I then joined the 2 data sets into one to work from. 
<br>
Feature 3 - Visualize data - Various plots were made to understand that data and a final cleaned cheet was made to compare that data. 
<br>
Feature 4 - Utilized a virtual environment and include instructions in the README on how the user should run.
<br>
Feature 5 - Interpreted the data by annotating the code via markdown cells.
<br>
<br>
<h2> FIN </h2>

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

***final_code.ipynb no longer works as the data is now formatted differently from Louisville open data. I removed the data before realizing that. Outputs are saved for viewing. 

<!-- ## ARCGIS pip install Instructions 

1. `pip install --upgrade pip setuptools wheel`
1. `pip install "keyring>=19,<=21.8.*"`
1. `pip install --use-pep517 arcgis==1.8.5.post3`

In most recent build I have removed need for arcgis all together. Just run `data_builder.py` -->