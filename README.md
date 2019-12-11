# payments

[![Build Status](https://travis-ci.org/NYU-DevOps-Fall19-Payments-Team/payments.svg?branch=master)](https://travis-ci.org/NYU-DevOps-Fall19-Payments-Team/payments)
[![codecov](https://codecov.io/gh/NYU-DevOps-Fall19-Payments-Team/payments/branch/master/graph/badge.svg)](https://codecov.io/gh/NYU-DevOps-Fall19-Payments-Team/payments)
![pylint Score](https://mperlet.github.io/pybadge/badges/9.91.svg)

![](scrooge.gif)

## About

A microservice for processing payments.

## Documentation

https://nyu-payment-service-f19-prod.mybluemix.net/apidocs

## Setup

Setting up a local development environment requires that you download and install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/).

Once those requirements are installed, set up and enter the local development environment with:
```
git clone https://github.com/NYU-DevOps-Fall19-Payments-Team/payments.git
cd payments
vagrant up
vagrant ssh
```

## Testing

To run any of the tests, you must `cd /vagrant` in the local development environment. Then, depending on which test you want to run, issue the appropriate command(s):

* TDD: `nosetests`
* BDD: Using a terminal multiplexer (e.g., `screen`), run `honcho start` in one window and then `behave` in another.
* PEP 8: `sh pylint_all.sh`

