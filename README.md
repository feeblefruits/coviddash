# COVID-19 South Africa dash

Data vis dashboard built using Flask, Bootstrap and Plotly. This project is part of Udacity's data science course introduction to web development.

Following the instructions below will launch data vis dashboard showing charts using world bank data.


## Requirements

In terminal do to directory and use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
requests==2.22.0
json5==0.8.5
jsonschema==3.0.2
Click==7.0
Flask==1.1.1
gunicorn==19.9.0
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
numpy==1.17.2
pandas==0.25.1
plotly==4.1.1
python-dateutil==2.8.0
pytz==2019.2
retrying==1.3.3
six==1.12.0
Werkzeug==0.16.0
APScheduler==3.0.0
```

## Usage
Run local server

Uncomment the line ```app.run(host='0.0.0.0', port=3001, debug=True)``` in covid.py and run ```pyton covid.py``` in shell

In your browser go to http://localhost:3001 to view site.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
