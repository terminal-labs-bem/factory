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
	@bash .tmp/bem/common/user.sh $(APPNAME) $(SUDOUSERNAME) $(CONFIGURATION) $(TYPE) $(PYTHONVERSION) $(HOSTTYPE) $(INTERNALUSER) $(PLATFORM) $(PLUGIN) $(EXTRA)
	@sudo bash .tmp/bem/common/superuser.sh $(APPNAME) $(SUDOUSERNAME) $(CONFIGURATION) $(TYPE) $(PYTHONVERSION) $(HOSTTYPE) $(INTERNALUSER) $(PLATFORM) $(PLUGIN) $(EXTRA)
endef

download_bash_environment_manager:
	@if test ! -d ".tmp";then \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp"; \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp/prep"; \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp/bem"; \
		sudo su -m $(SUDO_USER) -c "mkdir -p .tmp/patterns"; \
  		sudo su -m $(SUDO_USER) -c "cd .tmp/prep; wget -O shelf-main.zip https://github.com/terminal-labs-bem/shelf/archive/refs/heads/main.zip"; \
  		sudo su -m $(SUDO_USER) -c "cd .tmp/prep; unzip -n shelf-main.zip"; \
  		sudo su -m $(SUDO_USER) -c "cp -r .tmp/prep/shelf-main/bash-environment-manager/* .tmp/bem"; \
  		sudo su -m $(SUDO_USER) -c "cp -r .tmp/prep/shelf-main/bash-environment-manager/patterns/* .tmp/patterns"; \
	fi

venv.python: HOSTTYPE="host"
venv.python: INTERNALUSER=$(SUDO_USER)
venv.python: download_bash_environment_manager
	$(call kickoff)

vm.venv.python: HOSTTYPE="vagrant"
vm.venv.python: INTERNALUSER="vagrant"
vm.venv.python: download_bash_environment_manager
	@if test ! -f "Vagrantfile";then \
		wget https://raw.githubusercontent.com/terminal-labs/bash-environment-manager-shelf/main/vagrantfiles/Vagrantfile; \
		chown $(SUDO_USER) Vagrantfile; \
	fi
	$(call kickoff)
