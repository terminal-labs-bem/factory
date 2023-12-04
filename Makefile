APPNAME="factory"
SUDOUSERNAME=$(SUDO_USER)
CONFIGURATION="default"
TYPE="python"
PYTHONVERSION="3.11"
HOSTTYPE="default"
INTERNALUSER=$(SUDO_USER)
PLATFORM=".tlcache"
PLUGIN="standard"
EXTRA="none"

help:
	@echo "usage: make [command]"

define kickoff
	@bash .tmp/bem/common/standarduser_assemble.sh $(APPNAME) $(SUDOUSERNAME) $(CONFIGURATION) $(TYPE) $(PYTHONVERSION) $(HOSTTYPE) $(INTERNALUSER) $(PLATFORM) $(PLUGIN) $(EXTRA)
	@sudo bash .tmp/bem/common/superuser_assemble.sh $(APPNAME) $(SUDOUSERNAME) $(CONFIGURATION) $(TYPE) $(PYTHONVERSION) $(HOSTTYPE) $(INTERNALUSER) $(PLATFORM) $(PLUGIN) $(EXTRA)
endef

download_bash_environment_manager:
	@if test ! -d ".tmp";then \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp"; \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp/prep"; \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp/bem"; \
  		sudo su -m $(SUDO_USER) -c "cd .tmp/prep; wget -O bash-environment-manager.zip https://github.com/terminal-labs/bash-environment-manager/archive/refs/heads/main.zip"; \
  		sudo su -m $(SUDO_USER) -c "cd .tmp/prep; unzip -n bash-environment-manager.zip"; \
  		sudo su -m $(SUDO_USER) -c "cp -r .tmp/prep/bash-environment-manager-main/* .tmp/bem"; \
	fi

psf: HOSTTYPE="host"
psf: INTERNALUSER=$(SUDO_USER)
psf: download_bash_environment_manager
	$(call kickoff)

vagrant.psf: HOSTTYPE="vagrant"
vagrant.psf: INTERNALUSER="vagrant"
vagrant.psf: download_bash_environment_manager
	@if test ! -f "Vagrantfile";then \
		wget https://raw.githubusercontent.com/terminal-labs/bash-environment-shelf/main/vagrantfiles/Vagrantfile; \
		chown $(SUDO_USER) Vagrantfile; \
	fi
	$(call kickoff)
