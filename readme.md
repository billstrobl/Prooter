# Prooter
An application to scan through HTML posts to locate data about users and output its findings.
The intent is to quickly and easily find users, their usernames, and posts they have made.

## Usage
Place the files you wish to scan through in the data/ directory. Then run prooter.py.
Output files will be written as a result-- user results and/or post results depending on the options used. 

### CLI Options
There are two options to use when running the script from the CLI. Run_type determines
what data will be parsed, while file_format controls what kind of output file will be created.

The available options for run_type are:
- users
- posts
- all

The available options for file_format are:
- txt
- csv

The default behavior is to output the list of users to csv.

### Linux Example
To generate a list of users and usernames, and save the output as a csv run:  
`./prooter.py --run_type 'users' --file_format 'csv'`

### Windows Example
This script will work on Windows as well, natively. To generate a list of posts and users, 
and save the output as txt run:  
`python prooter.py --run_type posts --file_format csv`

NOTE: There is a difference in the usage of quotes between Linux/Mac and Windows. Please note this difference 
when troubleshooting.

## Contributing
Created and maintained by Bill Strobl  
To contribute please create a fork and create a pull request with your changes.

## Release Notes

|Date|Version|Notes|
|---|---|---|
|11 Jan 2021|v0.1|Basic version created. MVP Only.|
|13 Jan 2021|v0.2|Able to output to CSV, has much more robust logging, and general coding improvements.|

## License
Please give credit where credit is due.

[MIT](https://choosealicense.com/licenses/mit/)