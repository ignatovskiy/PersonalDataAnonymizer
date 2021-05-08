# Personal Data Anonymizer  [![Build Status](https://github.com/ignatovskiy/PersonalDataAnonymizer/actions/workflows/code-style.yml/badge.svg)](https://github.com/ignatovskiy/PersonalDataAnonymizer/actions)

pdanonymizer is a Python library for finding, masking or replacing personal data in files, IO streams, etc.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pdanonymizer.

```bash
pip install .
```

## Usage

Training new model by dataset and saving it as folder:
```bash
python3 pdanonymizer -a train -d [dataset file] -o [model dir]
```

Continue training existing model by new dataset and saving it as folder:
```bash
python3 pdanonymizer -a post_train -m [model dir] -d [dataset file] -o [model folder]
```

Automatic validation (testing) of existing model on dataset:
```bash
python3 pdanonymizer -a test_auto -m [model dir] -d [dataset file]
```

Manual testing of existing model by inputting string:
```bash
python3 pdanonymizer -a test_manual -m [model dir] -d [string]
```

Converting mainstream json datasets (generated on websites) to specific pdanonymizer dataset format:
```bash
python3 pdanonymizer -a convert -d [dataset file]
```

Creating new pdanonymizer datasets with needed number of entities from converted one:
```bash
python3 pdanonymizer -a create -d [raw dataset file] -v [entities amount] -o [new dataset file]
```

Replacing personal data in file by fake data with the help of pdanonymizer model and saving edited file:
```bash
python3 pdanonymizer -a predict_file -m [model dir] -d [old file] -o [new file]
```

Masking personal data in file by fake data with the help of pdanonymizer model and saving edited file:
```bash
python3 pdanonymizer -a mask_file -m [model dir] -d [old file] -o [new file]
```

Masking image data by black squares:
```bash
python3 pdanonymizer -a mask_image -d [input image name] -o [output image name]
```

Pseudo-GUI mode of application:
```bash
python3 pdanonymizer -a interact
```

## Examples

### Replacing personal data in SQL database with fake one. Compare outputs of this commands.
w/o pdanonymizer:
```bash
python3 examples/sql_example.py
```
```
Ivan Ivanov 0-345-43-43 25.03.1874
Rodger Wellington +7-950-434-43-43 05/03/2000
Stan Smith +1-900-456-43-34 01.02.1990
```
w/ pdanonymizer:
```bash
python3 examples/sql_example.py | python3 pdanonymizer
```
```
Helen Church 001-625-632-4152 21.10.1983
Perry Lucas 767-863-7211 13.02.2013
Katherine Sheppard 001-822-636-2875x5676 18.12.2016
```

### Another example of data replacing in SQL file provided by [test_db](https://github.com/datacharmer/test_db) project. Compare outputs.
w/o pdanonymizer:
```bash
mysql < examples/sql/test_print.sql
```
```
emp_no	birth_date	first_name	last_name	gender	hire_date
10037	1963-07-22	Pradeep	Makrucki	M	1990-12-05
10038	1960-07-20	Huan	Lortz	M	1989-09-20
10039	1959-10-01	Alejandro	Brender	M	1988-01-19
10040	1959-09-13	Weiyi	Meriste	F	1993-02-14
10041	1959-08-27	Uri	Lenart	F	1989-11-12
10042	1956-02-26	Magy	Stamatiou	F	1993-03-21
10043	1960-09-19	Yishay	Tzvieli	M	1990-10-20
10044	1961-09-21	Mingsen	Casley	F	1994-05-21
10045	1957-08-14	Moss	Shanbhogue	M	1989-09-02
10046	1960-07-23	Lucien	Rosenbaum	M	1992-06-20
10047	1952-06-29	Zvonko	Nyanchama	M	1989-03-31
10048	1963-07-11	Florian	Syrotiuk	M	1985-02-24
10049	1961-04-24	Basil	Tramer	F	1992-05-04
10050	1958-05-21	Yinghua	Dredge	M	1990-12-25
10051	1953-07-28	Hidefumi	Caine	M	1992-10-15
10052	1961-02-26	Heping	Nitsch	M	1988-05-21
10053	1954-09-13	Sanjiv	Zschoche	F	1986-02-04
10054	1957-04-04	Mayumi	Schueller	M	1995-03-13
10055	1956-06-06	Georgy	Dredge	M	1992-04-27
10056	1961-09-01	Brendon	Bernini	F	1990-02-01
10057	1954-05-30	Ebbe	Callaway	F	1992-01-15
```
w/ pdanonymizer:
```bash
mysql < examples/sql/test_print.sql | python3 pdanonymizer
```
```
emp_no	birth_date	first_name	last_name	gender	hire_date
8787379297843	30.10.2004	Scott	Mathews	M	13.07.1981
5527296127105	25.06.2003	Andrade	Jacobson	M	20.01.2013
1436125488352	04.01.1976	George	Powers	M	23.06.2003
9691495824069	09.09.1981	MD	Moore	F	06.02.1988
3952266963094	24.01.1986	Uri	Ortiz	F	02.07.1971
6917352791620	29.05.2000	Dickson	Peterson	F	20.02.1991
2082483942457	20.01.1982	Black	Weaver	M	23.03.2002
4161563061665	10.03.1973	Gilbert	Larson	F	24.07.1986
0867367983250	02.09.2020	Tucker	Garza	M	22.07.1996
2841039452051	03.09.1989	Castaneda	Hickman	M	02.04.1972
1448254445397	04.11.1975	Petersen	Harris	M	02.11.1971
0604775503546	29.01.2015	Martin	Lawrence	M	17.01.2010
9446687385589	26.01.1994	Sutton	Osborne	F	22.03.1993
0447931894436	26.10.1981	Miller	Davis	M	28.08.1993
1497766755999	06.09.1985	Stout	Smith	M	03.12.2000
5108961087094	31.10.1986	Frey	Gillespie	M	31.03.2013
5188092281882	06.05.2015	Miller	Burch	F	07.01.2015
4237196973139	05.01.1979	Walker	Garza	M	25.02.1988
7840814674904	24.12.1983	James	Banks	M	11.12.1986
4594521752198	18.05.1982	Arnold	Crosby	F	26.12.1995
4071661846432	18.04.1974	Hernandez	Ward	F	14.05.1982
```

### Testing on [real CSV data](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv):
w/o pdanonymizer:
```
"Name",     "Sex", "Age", "Height (in)", "Weight (lbs)"
"Alex",       "M",   41,       74,      170
"Bert",       "M",   42,       68,      166
"Carl",       "M",   32,       70,      155
"Dave",       "M",   39,       72,      167
"Elly",       "F",   30,       66,      124
"Fran",       "F",   33,       66,      115
"Gwen",       "F",   26,       64,      121
"Hank",       "M",   30,       71,      158
"Ivan",       "M",   53,       72,      175
"Jake",       "M",   32,       69,      143
"Kate",       "F",   47,       69,      139
"Luke",       "M",   34,       72,      163
"Myra",       "F",   23,       62,       98
"Neil",       "M",   36,       75,      160
"Omar",       "M",   38,       70,      145
"Page",       "F",   31,       67,      135
"Quin",       "M",   29,       71,      176
"Ruth",       "F",   28,       65,      131
```
w/ pdanonymizer (via web-app):
```
"Name",     "Sex", "Age", "Height (in)", "Weight (lbs)"
"Aguilar",       "M",   41,       74,      170
"Thompson",       "M",   42,       68,      166
"Williams",       "M",   32,       70,      155
"Tucker",       "M",   39,       72,      167
"Lindsey",       "F",   30,       66,      124
"Klein",       "F",   33,       66,      115
"Dean",       "F",   26,       64,      121
"Lane",       "M",   30,       71,      158
"Tyler",      "M",   53,       72,      175
"Brown",       "M",   32,       69,      143
"Phillips",       "F",   47,       69,      139
"Martinez",       "M",   34,       72,      163
"Maldonado",       "F",   23,       62,       98
"Patrick",       "M",   36,       75,      160
"Lawrence",       "M",   38,       70,      145
"Walker",       "F",   31,       67,      135
"Warren",       "M",   29,       71,      176
"Heath",       "F",   28,       65,      131
```

### Example of image data masking:
![](https://i.imgur.com/RpONO9P.png)
![](https://i.imgur.com/q9WpIxq.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
