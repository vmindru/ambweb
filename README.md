# Simple Django based FE for go-karts live timing amb-laps and amb-client AMBp3 Laps tracking

Heat /live
Race /race

# autopopulate schema
./manage.py inspectdb heats passes laps karts --database kartsdb > live/models.py

# django deps formysqlclient
yum install MariaDB-shared MariaDB-devel

# install deps

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.ini

# if above throws an error aout mysql
yum provides mysql_config
yum install ${PCKG} 


# demo
![alt tag](https://raw.githubusercontent.com/vmindru/ambweb/master/templates/demo.png)


# related

https://github.com/vmindru/ambp3client

https://github.com/vmindru/amb-docker
