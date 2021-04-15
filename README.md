# Personal Data Anonymizer

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

Pseudo-GUI mode of application:
```bash
python3 pdanonymizer -a interact
```

## Examples

Replacing personal data in SQL database with fake one. Compare output of this commands:
```bash
python3 examples/sql_example.py

Ivan Ivanov 0-345-43-43 25.03.1874
Rodger Wellington +7-950-434-43-43 05/03/2000
Stan Smith +1-900-456-43-34 01.02.1990
```

```bash
python3 examples/sql_example.py | python3 pdanonymizer

Helen Church 001-625-632-4152 21.10.1983
Perry Lucas 767-863-7211 13.02.2013
Katherine Sheppard 001-822-636-2875x5676 18.12.2016
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)