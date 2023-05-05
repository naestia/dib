# dib (Directory Interactive Browse)

## The CLI command

The idea behind `dib` is to create a command that will interactively browse and navigate the linux system through the terminal. The tool is meant for developers to use to make their everyday terminal navigation easier. The program will use the python lib `curses` to take over the terminal and create a visual list of the search term the user inputs.

## Install

- Clone this repository and navigate to the cloned folder `cd dib`.
- Create a virtual environment or install directly to you machine with `pip install -e ".[dev,test]"`
- Try the command: `dib --version`

## Usage

#### 'dib cd'

Using the `cd` command is pretty straight forward to say the least. To enter the script just enter `dib cd` in the terminal. See below.

![dib cd](docs/dib_cd.gif)

#### 'dib ls'

Using the `ls` command works the same as `dib cd` in the core, except it mimics the classic `ls` command with `--all` and `--list` flags. See below.

![dib ls](docs/dib_ls.gif)

#### 'dib find'

Using the `find` command looks for either a file or directory depending on what argument is specified after the `--type` flag. Using 'f' for 'file' and 'd' for 'directory'. See below

![dib find](docs/dib_find.gif)
