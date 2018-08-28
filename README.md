# Report Exporting Service

This Project is compatible with python3

## Launch:

- Clone this repo.

- Create a [virtual env](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv "Virtual env's Setup docs")

	- Install virtual env `pip install virtualenv`

	- `cd ReportExportingService` and `virtualenv ReportExportingService`

	- To begin using the virtual environment, it needs to be activated: `source ReportExportingService/bin/activate`

- Install the dependency (`pip3 install -r requirements.txt`)

- Once all are setup run `python app.py`

## Test:

The project use `unittest` for the unit test

Usage: `python test.py`


## Access.

Once the server is running you can access it trougth the url:

`http://127.0.0.1:5000`


This API accept the fallowing entries point:

- `GET` on  `/reports` give a list of items.

- `GET` on  `/reports/{id}` give a the detail of the reports.


This API accept different output:

`json` by default, `xml` and `pdf`.

To request a specific output named previously, two methode has been implemented:

##### Methode one:

Set the request headers 'Content-Type' to the format you want (`application/json`, `text/xml` or `application/pdf`)

To specify the content type with `curl` for ememple:

>> curl -H "Content-type: text/xml" -X GET http://127.0.0.1:5000/reports/2

##### Methode two:

Add the parameter `format` at the end of the request:

- `/reports?format=pdf`

- `/reports/{id}?format=pdf`

- `/reports?format=xml`

- `/reports/{id}?format=xml`

If you provide both, the methode one will be taken.