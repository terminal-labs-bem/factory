APPNAME="factory"
SUDOUSERNAME=$(SUDO_USER)
CONFIGURATION="default"
TYPE="python"
PYTHONVERSION="3.11"
HOSTTYPE="default"
INTERNALUSER=$(SUDO_USER)
PLATFORM=".tlcache"
PLUGIN="simple"
EXTRA="none"

help:
	@echo "usage: make [command]"

define kickoff
	@sudo bash .tmp/bem/common/assemble.sh $(APPNAME) $(SUDOUSERNAME) $(CONFIGURATION) $(TYPE) $(PYTHONVERSION) $(HOSTTYPE) $(INTERNALUSER) $(PLATFORM) $(PLUGIN) $(EXTRA)
endef

download_bash_environment_manager:
	@if test ! -d ".tmp";then \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp"; \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp/prep"; \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp/bem"; \
  		sudo su -m $(SUDO_USER) -c "cd .tmp/prep; wget -O bash-environment-manager.zip https://github.com/terminal-labs/bash-environment-manager/archive/refs/heads/master.zip"; \
  		sudo su -m $(SUDO_USER) -c "cd .tmp/prep; unzip -n bash-environment-manager.zip"; \
  		sudo su -m $(SUDO_USER) -c "cp -r .tmp/prep/bash-environment-manager-master/* .tmp/bem"; \
	fi

psf: CONFIGURATION="default"
psf: HOSTTYPE="host"
psf: INTERNALUSER=$(SUDO_USER)
psf: PLUGIN="simple"
psf: download_bash_environment_manager
	$(call kickoff)

vagrant.psf: CONFIGURATION="default"
vagrant.psf: HOSTTYPE="vagrant"
vagrant.psf: INTERNALUSER="vagrant"
vagrant.psf: PLUGIN="standard"
vagrant.psf: download_bash_environment_manager
	@if test ! -f "Vagrantfile";then \
		wget https://raw.githubusercontent.com/terminal-labs/bash-environment-shelf/master/vagrantfiles/Vagrantfile; \
		chown $(SUDO_USER) Vagrantfile; \
	fi
	$(call kickoff)