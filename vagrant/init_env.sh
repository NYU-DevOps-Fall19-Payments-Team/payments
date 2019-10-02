vagrant plugin install vagrant-vbguest # Enable vboxsf.
vagrant destroy -f
vagrant box update
vagrant up --provider virtualbox
vagrant ssh
