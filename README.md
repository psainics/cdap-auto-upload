# Cdap Auto Upload
A simple utility script to compile package and upload artifacts to cdap.


## Prerequisites
1. Python3
2. cdap `/bin` directory in the PATH

## Setup
1. **Clone the repository**
```bash
git clone https://github.com/psainics/cdap-auto-upload.git
```
2. **Add full path to `main.py` script as an alias in your `.bash_profile`**
- Choose a name for the alias (e.g., cpu).
- Add the following line, replacing `/path/to/cdap-auto-upload` with the actual path:
```bash
alias cpu='/path/to/cdap-auto-upload/main.py'
```
3. **Source the `.bash_profile` to reflect the changes**
```bash
source ~/.bash_profile
```


## Update

To update the script, pull the latest changes from the repository
```bash
cd /path/to/cdap-auto-upload
git pull
```

## Usage

Calling the alias from the root of a project will compile the package and upload the artifacts to cdap.


## Limitations
1. We use cached dependencies to speed up the build process. You must do a clean build if you have made changes to the dependencies.

2. Non `SNAPSHOT` versions of the plugins cannot be uploaded more than once.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
