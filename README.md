# OilTank-Calculator

***THIS IS JUST A DOCUMENTATION FOR MYSELF! YOU CAN USE IT, BUT THERE MAY BE MISSING SOME STEPS!***


Made for Raspbian!

Measures remaining litres, writes this to a logfile.csv and add results to a MySQL Database.

From that on, the node app.js will catch the values from the Database and creates a JSON file. This file will be uploaded to a NAS.

Dependencies:

- Node
- MySQL Library
- MySQL Database with a Databse called "Tank" and a Table called "Volumen". The table includes two columns called "Date" and "Volume". Date is defined as "text" and Volume ist defined as "decimal"
- MQTT Broker like "ioBroker"


***Install node:***

```curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -```

```sudo apt-get install -y nodejs```


***Install MySQL Library:***

```sudo apt-get install python-mysqldb```

```sudo apt-get install python-mysql.connector```

***Install MQTT Library***

```sudo apt-get install python-setuptools```

```sudo easy_install pip```

```pip install paho-mqtt```


***Create direction and install npm dependencies:***

```mkdir tank```

```cd tank```

```npm install mysql```

```npm install promise-ftp```



**Copy app.js and tank.py files to /home/pi/tank**

***Test scripts:***

```cd tank```

```python tank.py```

```node app.js```




***Automatically executing:***

```sudo nano /etc/crontab```

*add these lines:*

```
51 4    * * *   root    /usr/bin/python /home/pi/tank/tank.py
52 4    * * *   root    /usr/bin/node /home/pi/tank/app.js
```

