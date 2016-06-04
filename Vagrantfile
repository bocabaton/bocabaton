# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  if !Vagrant.has_plugin?("vagrant-hostsupdater")
    raise "Please install vagrant-hostsupdater via `vagrant plugin install vagrant-hostsupdater`"
  end

  #config.vm.synced_folder ".", "/opt/bocabaton"

  config.vm.box = "bento/centos-7.2"
  #config.vm.box_url = "https://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_centos-7.2_chef-provisionerless.box"
  #config.vm.box_url = "https://opscode-vm-bento.s3.amazonaws.com/vagrant/vmware/opscode_centos-7.2_chef-provisionerless.box"

  config.vm.provider :virtualbox do |vb|
    vb.gui = true
    vb.customize ["modifyvm", :id, "--memory", "4096"]
    vb.customize ["modifyvm", :id, "--cpus", "2"]
  end

  config.vm.provider :vmware_fusion do |v|
    v.gui = true
    v.vmx["memsize"] = "4096"
    v.vmx["numvcpus"] = "2"
  end

  private_ip = "192.168.99.50"

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.auto_detect = true
  end

  config.vm.hostname = "vagrant-bocabaton"
  config.vm.network :private_network, ip: private_ip

$provision_script = <<EOF
yum install -y epel-release gcc python-devel
yum install -y python-pip

pip install jeju --upgrade

jeju -m https://raw.githubusercontent.com/bocabaton/bocabaton/master/docs/INSTALL_CentOS.md
EOF

  config.vm.define "bocabaton", primary: true do |bocabaton|
    bocabaton.vm.provision "shell",
      privileged: true,
      inline: $provision_script
  end
end
