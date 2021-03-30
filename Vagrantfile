Vagrant.configure("2") do |config|
  config.vm.box = 'bento/ubuntu-20.04'
  config.vm.box_version = "202004.27.0"
  config.vm.provider :vmware_desktop do |vmware|
	vmware.vmx["ethernet0.pcislotnumber"] = "32"
  end
  # Forward the Rails server default port to the host
  #config.vm.network :forwarded_port, guest: 8000, host: 8000
  #config.vm.network :forwarded_port, guest: 3000, host: 3000
  #config.vm.provider = 'vmware_desktop' do |v|
  #  v.gui = true
  #end
end