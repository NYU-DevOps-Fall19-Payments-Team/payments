# payments

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

* Create a new payment method: [POST] `/payments`
* Read a payment method: [GET] `/payments/<id>`
* Update a payment method: [PUT] `/payments/<id>`
* Delete a payment method: [
