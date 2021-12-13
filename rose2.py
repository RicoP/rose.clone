import os

dir_stack = []
def pushd(path):
	dir_stack.append(os.getcwd())
	os.chdir(path)

def popd():
	os.chdir(dir_stack.pop())

def execute(cmd):
	print("EXECUTING: ", os.getcwd(), cmd)
	return os.system(cmd)

def print_git_revision():
	print("GIT REVISION: ", os.popen("git rev-parse HEAD").read().strip())

def print_current_git_branch():
	print("CURRENT GIT BRANCH: ", os.popen("git rev-parse --abbrev-ref HEAD").read().strip())

def git_check_clean():
	if execute("git diff-index --quiet HEAD --"):
		print("ERROR: ", os.getcwd(), " is dirty. Reset?")
		os.system("pause")

def git_clone(url, branch="", commit="", path=""):
	if path == "":
		path = url.split("/")[-1]
		path = path.split(".git")[0]

	dir_exists = os.path.isdir(path)
	if not dir_exists:
		if branch:
			execute("git clone -b {} {} {}".format(branch, url, path))
		else:
			execute("git clone {} {}".format(url, path))

	if dir_exists:
		pushd(path)

		git_check_clean()
		execute("git fetch origin")
		execute("git checkout " + branch)
		execute("git reset --hard origin/" + branch)
		execute("git clean -d --force")
		
		execute("git checkout " + branch)
		if commit:
			execute("git checkout " + commit)		
		print_git_revision()
		print_current_git_branch()
		popd()

