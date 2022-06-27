import click
import subprocess, os, shutil
import platform
import json
import zipfile
from urllib.request import urlopen, Request, urlretrieve


JOIN = os.path.join
class Config:
    #Global config
    home = os.path.expanduser('~')

    main_dir = JOIN(home, "Pa")
    master = JOIN(main_dir, "Pa-master")

    objects = JOIN(master, "objects", "*.c")
    libraries = JOIN(master, "libraries", "*.c")
    source = JOIN(master, "src", "*.c")

    exe = ""
    other_libraries = ""

    # >:)
    opts = "-Ofast -flto"
    flags = "-o"

    LINUX_BUILD = False
    WINDOWS_BUILD = False
    REPO_NAME = "valkarias/Pa"

    @classmethod
    def setPlatform(klass):
        if platform.system() == "Windows":
            klass.WINDOWS_BUILD = True
            klass.exe = "Pa.exe"
            klass.other_libraries = JOIN(os.environ['APPDATA'], "PA_LIBS")
        else:
            klass.LINUX_BUILD = True
            klass.other_libraries = JOIN(klass.home, "PA_LIBS")
            klass.exe = "Pa"

#Init
Config.setPlatform()
#

def check():
    p = JOIN(Config.home, "Pa")

    if os.path.exists(p) == False:
        click.secho("Pa Directory is missing: ", fg='red')
        click.echo("Please use the 'download' command.")
        return -1

    elif os.path.isdir(p) == False:
        click.secho("A File with the same name exists: ", fg='red')
        click.echo(f"-> '{p}'")
        return -1

    if len(os.listdir(p)) == 0:
        click.secho("An Empty Directory with the same name exists: ", fg='red')
        click.echo("Please use the 'uninstall' command to clean up.")
        click.echo(f"-> '{p}'")
        return -1

    return 0

def validateCompiler(cc):
    commands = []

    click.echo(f"Checking for {cc}.")

    if cc == "gcc":
        commands = [cc, "--version"]
    else:
        commands = [cc, "-v"]

    process = subprocess.Popen(commands, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    
    stdout,stderr = process.communicate()

    if stderr:
        click.secho(f"Could not find '{cc}'.", fg='red')
        return False
    elif stdout:
        click.echo(f"{cc} found.")
    
    return True

def get_current_version():
    try:
        return open(JOIN(Config.master, "tools", "VERSION")).read()
    except FileNotFoundError:
        click.secho("Could not get local version", fg='red')
        click.echo("-> The 'VERSION' file got deleted from Pa tool directory.")
        click.echo("-> Try re-installing.")
        return False

def get_latest_release_name():
    url = f"https://api.github.com/repos/{Config.REPO_NAME}/releases"

    req_class = Request(url, headers={"Accept": "application/json"})
    req = urlopen(req_class)
    trailing = [
        "-windows-latest",
        "-ubuntu-latest",
        "-macOS-latest"
    ]
    if req.status == 200:
        data = json.loads(req.read().decode())
        release_name = data[0]["name"]
        for i in trailing:
            if i in release_name:
                return release_name.replace(i, "")
    else:
        click.secho(f"Could not get the latest release from the repository", fg='red')
        click.echo(f"-> request status code: {req.status}")

    return False

def download_source():
    #TODO: separate versions
    url = "https://github.com/valkarias/Pa/archive/master.zip"
    try:
        req, headers = urlretrieve(url, filename=Config.main_dir + ".zip")
    except:
        click.secho("Downloading ZIP file failed.", fg='red')
        return False
    file = open(req)
    with zipfile.ZipFile(Config.main_dir + ".zip", 'r') as zip:
        extracted = JOIN(Config.home, "Pa")
        os.mkdir(extracted)
        click.echo("Extracting ZIP file..")
        try:
            zip.extractall(extracted)
        except Exception as e:
            click.secho("Extraction failed.", fg='red')
            click.echo("-> exception: " + str(e))
            return False
    file.close()
    return True

def execute(command):
    process = os.popen(command)
    output = process.read()

    print(output)


def initLibs():
    click.echo("Moving libraries...")
    src = JOIN(Config.master, "libraries", "APIs")

    try:
        os.mkdir(Config.other_libraries)
    except OSError:
        pass
    
    files = os.listdir(src)
    print("\n")
    for file in files:
        try:
            shutil.move(JOIN(src, file), Config.other_libraries)
            click.echo(f"Moved '{file}'")
        except:
            click.echo(f"'{file}' already exists... pass")

def compile(cc):
    bin_dir = JOIN(Config.master, "bin")
    os.chdir(bin_dir)

    initLibs()

    command = f"{cc} {Config.objects} {Config.libraries} {Config.source} {Config.opts} {Config.flags} {Config.exe}"
    if Config.LINUX_BUILD:
        execute(command + " -lm")
    else:
        execute(command)  