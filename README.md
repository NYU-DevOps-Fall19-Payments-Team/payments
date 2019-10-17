# payments

# Travis CI
[![Build Status](https://travis-ci.org/NYU-DevOps-Fall19-Payments-Team/payments.svg?branch=master)](https://travis-ci.org/NYU-DevOps-Fall19-Payments-Team/payments)
# Codecov
[![codecov](https://codecov.io/gh/NYU-DevOps-Fall19-Payments-Team/payments/branch/master/graph/badge.svg)](https://codecov.io/gh/NYU-DevOps-Fall19-Payments-Team/payments)

## Setup

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

The contents of the Vagrantfile are adapted from part of the DevOps course CSCI-GA.2820-001/002 at NYU taught by John Rofrano.

```
git clone https://github.com/NYU-DevOps-Fall19-Payments-Team/payments.git
cd payments
```

Initialize the environment with `vagrant up`; enter it with `vagrant ssh`.

## Navigation

The service can be run using an initialization script from the home directory of the Vagrant environment: `./init_service.sh`. Source code for the service can be found in `/vagrant/service/`.

## Testing

Run `nosetests` within the `/vagrant` directory of the Vagrant environment.

## API

* List payment methods: [GET] `/payments`
* Read a payment method: [GET] `/payments/<id>`
* Create a new payment method: [POST] `/payments`
    * Needs a JSON body of the form:
``{
"order_id": <int>
"customer_id": <int>
"available": <bool>
"payments_type": <str>
}
``
* Update a payment method: [PUT] `/payments/<id>`
    * Needs a JSON body with the same fields as above.
* Delete a payment method: [DELETE] `/payments/<id>`
* Query payment methods by an attribute:
    * Customer id: [GET] `/payments?customer_id=<int>`
* Toggle a payment method's availability: [PUT] `payments/<id>/toggle`
