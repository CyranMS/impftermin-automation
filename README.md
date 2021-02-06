# impftermin-automation

Small monitoring script for the [impfterminservice.de](https://002-iz.impfterminservice.de/terminservice) website.

The `impftermin_runner.py` script does the following:

* Open appointment 1 URL
* Check availability for appointment 1
* if true, open appointment 2 URL
* Check availability for appointment 2
* if true, send email

## How to run it  (ad-hoc or scheduled)

There are three ways how you can run the script to get notifications:

1) Ad-hoc execution
2) cron execution (scheduled)
3) Debian package installation (systemd triggered)

Below are the steps for each:

### Prerequisites

#### Install dependencies

You have to install some dependencies to make the script work (on Ubuntu):

```bash
sudo apt install python3-yaml python3-selenium chromium-browser chromium-chromedriver
```

or via pip (hint: this is not enough if you want to install the Debian package due to root scope):

```bash
pip3 install -r requirements.txt
```

#### Create config.yml

In order to work properly, you must create a config file for your credentials.

A file `config.yml` has to be created to read configurations. Here is an example:

```yml
url_1: https://002-iz.impfterminservice.de/terminservice/suche/xxxx-xxxx-xxxx/76287/L920
url_2: https://002-iz.impfterminservice.de/terminservice/suche/xxxx-xxxx-xxxx/76287/L920/xxxx-xxxx-xxxx
smtp_server: 'smtp.office365.com'
smtp_port: 587
smtp_user: 'test@outlook.com'
smtp_pw: 'pw123'
to_email: 'test2@outlook.com'
from_email: 'test@outlook.com'
```

Store the file in project directory.

### Option 1) Ad-hoc execution

After cloning and creation of the config file, the script can be easily executed by running

```bash
python3 impftermin_runner.py
```

## Option 2) Scheduled execution (via cron)

You can also schedule the script to run e.g. every 10 minutes by adding a cron (via `crontab -e`)

```bash
# add the following line at the end of the file
*/10 * * * * DISPLAY=:0 python3 /path/to/impftermin_runner.py
```

## Option 3) Scheduled execution (via GitHub Actions)

You can also schedule the script to run e.g. every 5 minutes by adding a GitHub Action. There is one configured in the `.github/workflows/` folder.
