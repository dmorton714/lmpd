<h1> Racism in Louisville Metro Police department </h1>

<h2>Code Louisville Scope </h2>
This project was created to fulfill the requirements of Code Louisville’s Python Data Analytics 2 class. The project had 4 requirements as follow. 
<ol>
<li> Read in two data sets. </li>
<li> Make 3 plots </li>
<li> Make a virtual environment for the project </li>
<li> Annotate our code </li>
</ol>

<h2> About The Data </h2>
The purpose of the project was to determine if the LMPD had a racially motivated citation record. To make the calculations I used CSV sheets from Louisville Metro Open Data site. The first sheet was the police force which has all sworn officers with age sex etc. The next data set includes all the issued citations from the police with officers and drivers data. The final portion of data I used was from the census bureau to make a data frame for Louisville base line population. From the main graph we can determine that the black population did get more citations that our populations representation. The Hispanic police officers were the only group of officers that cited black drivers less that the Louisville population. However the real surprise of the data was that Hispanic population was cited above the population average by every race of officers. Ironically the Hispanic officer population was the only group of officers to cite above the population average. Alternatively we can conclude from the data the even though the population is almost equal in terms of genders. Males are almost twice as likely to receive a citation. 

<h3> Citations by gender with population </h3>
<img src="https://github.com/dmorton714/lmpd/blob/master/race.jpg?raw=true" alt="Flowers in Chania">

<h3> Citations of full LMPD, louisville population and citations. 
<img src="https://github.com/dmorton714/lmpd/blob/master/full-force.jpg?raw=true" alt="Flowers in Chania">


<h3> Officer citations by gender and Louisville population </h3>
<img src="https://github.com/dmorton714/lmpd/blob/master/gender.jpg?raw=true" alt="Flowers in Chania">



I plan to work this project a bit more to determine if the gender and race come into play on the citations. I would also like to add a Tableau dashboard to the project as well. 

<h1> Requirements </h1>

This project was made with Anaconda installed, using the below packages in VS Code using Jupyter notebooks. PIP install packages as needed. Alternatively a virtual environment is included. 
<br>
<br>
Documentation for venv: (https://docs.python.org/3/tutorial/venv.html)
<br>
<br>
From the directory pip install the requirements.txt file by running "pip install -r requirements.txt"

<li> import pandas as pd </li>
<li> import matplotlib.pyplot as plt </li>
<li> import matplotlib.dates as mdates </li>
<li> import datetime </li>
<li> import csv </li>
<li> import numpy as np </li>
<li> import urllib.request </li>
<li> import requests </li>
<li> import json </li>

<h2> FIN </h2>