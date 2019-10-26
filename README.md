# Simple Django based FE for go-karts live timing amb-laps and amb-client AMBp3 Laps tracking

Heat /live
Race /race

# autopopulate schema
./manage.py inspectdb heats passes laps karts --database kartsdb > live/models.py

# django deps formysqlclient
yum install MariaDB-shared MariaDB-devel


