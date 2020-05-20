# cgbeacon2

[![Build Status](https://travis-ci.org/Clinical-Genomics/MIP.svg?branch=master)](https://travis-ci.org/Clinical-Genomics/MIP)
[![Coverage Status](https://coveralls.io/repos/github/Clinical-Genomics/cgbeacon2/badge.svg?branch=master)](https://coveralls.io/github/Clinical-Genomics/cgbeacon2?branch=master)

An updated beacon supporting GA4GH API 1.0

Table of Contents:
1. [ Prerequisites ](#prerequisites)
2. [ Installation ](#installation)
3. [ Loading demo data into the database ](#Loading)
    - []

<a name="prerequisites"></a>
## Prerequisites
- Python 3.6+
- A working instance of **MongoDB**. From the mongo shell you can create a database using this syntax:
```bash
use cgbeacon2
```

<a name="installation"></a>
## Installation

Clone this repository from github using this command:
```bash
git clone https://github.com/Clinical-Genomics/cgbeacon2.git
```

Change directory to the cloned folder and from there install the software using the following command:
```bash
pip install .
```

To customize the server configuration you'll need to edit the **config.py** file under the /instance folder. &nbsp;
For testing purposes you can keep the default configuration values as they are, but keep in mind that you should adjust these parameters when in production.

o start the server run this command:
```bash
cgbeacon2 run -h custom_host -p custom_port
```
Please note that the code is NOT guaranteed to be bug-free and it must be adapted to be used in production.

<a name="loading"></a>
## Loading demo data into the database
### Adding a demo dataset to the database
