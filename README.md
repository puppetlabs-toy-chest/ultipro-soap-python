## ultipro-soap-python

This library currently supports pulling data from UltiPro.

### Setup:

#### Web Service User and Credentials:

1. Ensure you have credentials for the UltiPro API endpoints you need to access.
If you are pulling BI Reports, your Web Service User must have the
Reports-as-a-service endpoint enabled with read access. Please see your UltiPro
administrator if you do not have a web service user.

2. Set up your credentials file. The default location is:
```
~/Library/Application Support/ultipro-soap-python/config.ini
```

You can find a sample config file in the root of this repository, config.ini.sample.

To use this tool on the command line, install with pip, then:

```
$ ultipro --help
```

#### Pulling BI Reports:
You will need to log in to UltiPro and find the path for your desired report. It should look something like:
```
/content/folder[@name='_UltiPro Delivered Reports']/folder[@name='Human Resources Reports']/report[@name='Employee Birthdays']
```

You can find more information on page 7 of the WebServiceAPIGuide_BIService.doc

To execute, retrieve, and save a report to disk, use the following syntax:
```
$ ultipro report "/content/folder[@name='_UltiPro Delivered Reports']/"
```

If you'd like to use non-default locations for your config.ini file or output file, you can use the following syntax:
```
ultipro -f ~/some/other/path/to/config.ini -o ~/Desktop/fooreport.csv report "/content/folder[@name='_UltiPro Delivered Reports']/folder[@name='Human Resources Reports']/report[@name='Employee Birthdays']"
```