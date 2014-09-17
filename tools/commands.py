from tools import constants as con
from tools import variables as var
from tools import functions as fn
from tools import process as pro
from tools import logger as log
from tools import help as helper
import subprocess
import shutil
import config
import os

# This holds all the commands
# Must have (inp, params=[]) in the def all the time, even if not used
# Or (*stuff) if parameters don't matter

# To add a new command, simply make a new def block
# The name of the definition is the command

# The following commands don't require any parameter

def exit(*args):
    var.ALLOW_RUN = False

def restart(*args):
    var.RETRY = True

def clean(*args):
    for x, y in con.LOGGERS.items():
        logfile = getattr(config, y + "_FILE")
        log_ext = getattr(config, y + "_EXT")
        try:
            os.remove("{0}.{1}".format(logfile, log_ext))
        except OSError: # file doesn't exist
            continue
    try:
        os.remove(os.getcwd() + "/" + var.TEMP_REG + ".reg")
    except OSError:
        pass
    try:
        os.remove(os.getcwd() + "/cfg.py")
    except OSError:
        pass
    shutil.rmtree(os.getcwd() + '/__pycache__')
    shutil.rmtree(os.getcwd() + '/tools/__pycache__')
    var.ALLOW_RUN = False

# The following commands may or may not require additional parameters

def help(inp, params=[]):
    if helper.get_help(" ".join(params)) == True:
        try:
            to_help = getattr(helper, params[0])
            to_help()
        except AttributeError:
            log.help("Error: '{0}' was not found but is in the database. Critical error.".format(" ".join(params)), type="error")

def copy(inp, params=[]):
    if params and " ".join(params) == "config":
        shutil.copy(os.getcwd() + "/config.py", os.getcwd() + "/config.py.example")

def run(inp, params=[]):
    if params:
        if params[0] == "silent":
            pro.run(params=" ".join(params[1:]), silent=True)
        elif params[0] == "extract":
            pro.extract()
        else:
            pro.run(params=" ".join(params))

def do(inp, params=[]):
    done = False
    if params:
        if inp[:22] == "do call python3; exec(" and inp[-2:] == ");":
            done = True
            exec(inp[22:-2])
        elif inp[:27] == "do call run function; eval(" and inp[-2:] == ");":
            done = True
            eval(inp[27:-2])
        elif inp[:9] == "do print(" and inp[-2:] == ");":
            done = True
            try:
                prnt = eval(inp[9:-2])
            except NameError:
                prnt = "Error: {0} is not defined.".format(inp[9:-2])
            log.logger(prnt, type="debug", write=False)
        elif inp[:18] == "do ask print; get(" and inp[-2:] == ");":
            done = True
            var.PRINT = inp[18:-2]
        elif inp == "do call help; get help;":
            done = True
            log.help("\nDevelopper commands:\n\n'do call python3; exec(\"command\");'\n'do call run function; eval(\"module.function\");'\n'do print(\"string\");'\n'do ask print; get(\"string\");")
    if not done:
        fn.no_such_command("do")

def git(inp, params=[]): # code re-used from lykos/Wolfbot
    if params:
        if params[0] == "pull":
            args = ["git", "pull"]
            if params[1:]:
                args.extend(params[1:])
            elif config.USE_GIT_ORIGIN:
                args += "origin", config.GIT_BRANCH
            elif config.USE_GIT_LINK:
                args += con.PROCESS_CODE + ".git", config.GIT_BRANCH
            child = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = child.communicate()
            ret = child.returncode

            for line in (out + err).splitlines():
                log.logger(line.decode('utf-8'), type="debug")

            if ret != 0:
                if ret < 0:
                    cause = 'signal'
                else:
                    cause = 'status'

                log.logger('Process {0} exited with {1} {2}'.format(args, cause, abs(ret)))