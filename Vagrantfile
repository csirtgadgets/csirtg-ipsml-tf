#e -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
add-apt-repository -y ppa:maxmind/ppa
apt-get update
apt-get install -y aptitude python-pip python-dev git htop virtualenvwrapper python2.7 python-virtualenv cython git \
    build-essential htop geoipupdate

pip install pip --upgrade

echo 'UserId 999999' | sudo tee /etc/GeoIP.conf > /dev/null
echo 'LicenseKey 000000000000' | sudo tee -a /etc/GeoIP.conf > /dev/null
echo 'ProductIds GeoLite2-Country GeoLite2-City GeoLite2-ASN' | sudo tee -a /etc/GeoIP.conf > /dev/null
sudo geoipupdate -v

SCRIPT

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
VAGRANTFILE_LOCAL = 'Vagrantfile.local'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = 'ubuntu/xenial64'
  config.vm.provision "shell", inline: $script

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", "2", "--ioapic", "on", "--memory", "512" ]
  end

  if File.file?(VAGRANTFILE_LOCAL)
    external = File.read VAGRANTFILE_LOCAL
    eval external
  end
end

