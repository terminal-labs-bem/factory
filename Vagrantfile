Vagrant.configure("2") do |config|
  config.ssh.forward_agent = true
  config.vm.box = "ubuntu/jammy64"
  config.vm.network "private_network", type: "dhcp"
  config.vm.network :forwarded_port, :guest => 8080, :host => 8080, auto_correct: true  
  config.vm.provider "virtualbox" do |v|
    v.customize ['modifyvm', :id, '--nictype1', 'virtio']
    v.memory = 4096
    v.cpus = 1
  end
end
