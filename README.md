# NAT Table Check

The purpose of these scripts are to login to ARRIS residential gateways and check the number of entries in the NAT table. If the number of entries exceeds a specified limit, the scripts will clear the table. The reason I wrote these scripts was because of issues with network connectivity when the NAT table fills up. This is a limitation (and poor design) with AT&T fiber services. The NAT table can fill up for a number of reasons, including, denial of service attacks caused by port scanners. Having static IPs exacerbates the issue, as the entries can get stuck in a time_wait state and eventually cause traffic to be dropped.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.8 or higher
* splinter (if not using the v2 script)
* selenium
* Firefox gecko driver
* Firefox
* python3-pip

### Installing

Install Python 3.8 or higher per your operating system's instructions. You can use a Python virtual environment, if you plan to run along side of other Python apps. If you're using Docker for deployment, then a Python virtual environment is not necessary. Install the required Python modules as shown below. If you are using a dedicated VM or application containerization, it is recommend to install python-is-python3 on Ubuntu distributions.

Install pip for Python 3.x

```
sudo apt-get install python3-pip
```

Install required Python modules using pip
```
pip3 install selenium
pip3 install splinter
```
Install geckodriver

```
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
tar xzvf geckodriver-v0.24.0-linux64.tar.gz
mv geckodriver /usr/local/sbin (or another location in your path)
```

## Running the tests

There are currently no tests written for this application (to be added in the future)

## Deployment

This application can be deployed with K8S, Docker Swarm, or as a standalone application. The following information should get you started. Note: The following instructions are based on standalone application deployment. On a standalone setup, you should configure CRON to run these scripts on a schedule of your choosing. For K8S, you can use the jobs configuration to run the pods on a schedule of your choosing.
### Which script should you run?

The original script "nat_table_check.py" was written for use with an ARRIS NVG599 (might work with other models).
The second version of the script "nat_table_check_v2.py" was written for use with an ARRIS BGW320-505, but may work with other models.

## Built With

* [Python 3.8](https://python.org) - The scripting language used

## Versioning

For the versions available, see the [tags on this repository](https://github.com/osborng/nat_table_check/tags). 

## Authors

* **George Osborne** - *Initial work* - [osborng](https://github.com/osborng)
