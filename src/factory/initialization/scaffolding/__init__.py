import tempfile
import errno

from lowkit.objects.globalvars import bracketdata
from lowkit.ops.filesystem import dir_create, is_writable


scaffolding_keys = ["deplyment", "applocation", "staginglocation", "bemhome", "bemtmp", "storage", "tmp"]
scaffolding_styles = {"workstation":
	{"deplyment": None, "applocation": "[appdir]", "staginglocation": None, "bemhome": "[homedir]/.bem", "bemtmp": "[appdir]/.tmp", "storage": "[homedir]/.bem/[appname]/data", "tmp": "/tmp/[appname]"},
}


def set_global_bracket_data(appdir, homedir, appname):
	global bracketdata
	bracketdata = {"[appdir]":appdir, "[homedir]":homedir, "[appname]":appname}
	return bracketdata


def get_global_bracket_data():
	global bracketdata
	return bracketdata

def get_scaffolding_style():
	return scaffolding_styles


def get_hydrated_scaffolding_style(style):
	global bracketdata
	assert len(scaffolding_styles["workstation"]) == 7
	for key, value in scaffolding_styles["workstation"].items():
		for scaffolding_key in scaffolding_keys:
			if key == scaffolding_key:
				if value:
					update = scaffolding_styles[style][key]
					if "[appdir]" in update:
						update = update.replace("[appdir]", bracketdata["[appdir]"])
					if "[homedir]" in update:
						update = update.replace("[homedir]", bracketdata["[homedir]"])
					if "[appname]" in update:
						update = update.replace("[appname]", bracketdata["[appname]"])
					scaffolding_styles[style][key] = update
	return scaffolding_styles["workstation"]

def get_hydrated_scaffolding_paths(style):
	scaffolding_paths = []
	hydrated_scaffolding_style = get_hydrated_scaffolding_style(style)
	for key, value in hydrated_scaffolding_style.items():
		if value:
			scaffolding_paths.append(value)
	return scaffolding_paths

def build_scaffolding(style):
	scaffolding_paths = get_hydrated_scaffolding_paths(style)
	for scaffolding_path in scaffolding_paths:
		dir_create(scaffolding_path)

def test_scaffolding(style):
	assert len(scaffolding_styles["workstation"]) == 7
	for key, value in scaffolding_styles["workstation"].items():
		if key == "deplyment":
			print("deplyment")
			if value:
				print("got somethign")   
		if key == "applocation":
			print("applocation")
			if value:
				print("got somethign") 
		if key == "staginglocation":
			print("staginglocation")
			if value:
				print("got somethign")  
		if key == "bemhome":
			print("bemhome")
			if value:
				print("got somethign")  
		if key == "bemtmp":
			print("bemtmp")
			if value:
				print("got somethign")  
		if key == "storage":
			print("storage")
			if value:
				print("got somethign")  
		if key == "tmp":
			print("tmp")
			if value:
				print(is_writable("/tmp/test"))
				print("got somethign")

	return scaffolding_styles["workstation"]
