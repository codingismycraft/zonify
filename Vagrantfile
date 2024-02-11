$script = <<SCRIPT
sudo apt update
sudo apt install python3-pip -y
sudo apt-get install libpq-dev python3-dev -y
sudo apt install python3-tk -y gnome-terminal
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.provision "shell", inline: $script
  config.vm.network "forwarded_port", guest: 13123, host: 13123
  config.vm.provider "virtualbox" do |vb|
    vb.name = "zonify"
  end
end
