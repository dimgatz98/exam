Game used for studying. Files located under `exam/questions` are used for obtaining questions at random, answering and comparing to the actual answers. Path to the files `exam/questions/save.txt` and `exam/questions/questions.txt` by setting the `SAVE_FILE` and `Q_FILE` environment variables respectively. Questions and answers are both included in the same file. Each line contains a pair of q&a which are separated by a colon. 

Install poetry:
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Installation: 
```sh
# Install xclip
$ sudo apt-get install xclip

# Using poetry
$ poetry install

# Using pip
$ python3 -m pip install requirements.txt
```

Running:
```sh
# Using poetry
$ poetry run python3 exam/exam.py
# Using python3
$ python3 exam/exam.py
```

`exam/questions/save.txt` always contains the full set of available questions. The `exam/questions/questions.txt` contains the remaining questions which will be asked during the game.
