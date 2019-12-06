# Payments: a microservice.

[![Build Status](https://travis-ci.org/NYU-DevOps-Fall19-Payments-Team/payments.svg?branch=master)](https://travis-ci.org/NYU-DevOps-Fall19-Payments-Team/payments)
[![codecov](https://codecov.io/gh/NYU-DevOps-Fall19-Payments-Team/payments/branch/master/graph/badge.svg)](https://codecov.io/gh/NYU-DevOps-Fall19-Payments-Team/payments)
![pylint Score](https://mperlet.github.io/pybadge/badges/9.98.svg)

![](scrooge.gif)

## Setup

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

The contents of the Vagrantfile are adapted from part of the DevOps course CSCI-GA.2820-001/002 at NYU taught by John Rofrano.

```
git clone https://github.com/NYU-DevOps-Fall19-Payments-Team/payments.git
cd payments
```

Initialize the environment with `vagrant up`; enter it with `vagrant ssh`.

## Testing

`cd vagrant`
* TDD: `nosetests`
* BDD: Using a terminal multiplexer (e.g., `screen`), run `honcho start` in one window and then `behave` in another.

