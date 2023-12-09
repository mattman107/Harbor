# Harbor
## What is This
Harbor is a [Ship of Harkinian](https://github.com/HarbourMasters/Shipwright) (SOH) launcher/manager for those with multiple versions of SOH. 

## How to Use
Currenly Harbor is only available as a command line application. There are plans to add an official GUI for those who prefer that.

This application expects that you have all of your versions of SOH in a single folder, all of your roms in a different folder, and Harbor should have its own folder as well.
For example:
```
.
└── home/
    ├── downloads/
    │   └── Harbor/
    │       ├── Harbor.exe
    │       └── metadata.json
    ├── SOH Folder/
    │   ├── 8-0-0
    │   ├── 8-0-1
    │   ├── 8-0-2
    │   └── 8-0-3
    └── Rom Folder/
        ├── mq_debug.z64
        └── debug.z64
```

To run the command line application go to the folder you have downloaded the app and type:

```
./main --help
```
If all is working fine this should show you a list of available commands. For example:

```
./main --sohDir [path to SOH folder]
```
will set the path to the folder that contains all of your SOH Versions.

```
./main run 8-0-0
```
This will run the soh.exe/soh.appimage found in the 8-0-0 folder.

## How to Build
This project is built in Python so you must have a version of Python (try for a recent one) installed. So clone the git repo:

```
git clone https://github.com/mattman107/Harbor
cd Harbor
```

I recommend using a [Python VENV](https://docs.python.org/3/library/venv.html) to contain the dependances of the project. This line will make a new VENV in the same Directory as the Harbor folder.

```
python -m venv ../HarborVenv
```

Next we have to add the dependancies to the VENV. First enter the VENV, then add the dependances using the requirements.txt file.

```
source ../HarborVenv/bin/activate
pip install -r requirements.txt
```
Then all you have to do is build the project using PyInstaller while in the VENV.

```
pyinstaller -F main.py
```
This should create a .spec file. Any other time you have to build the project you can just type instead:
```
pyinstaller main.spec
```

In your project folder this should have created a dist folder. The build application is in this folder.
You should be all setup to edit and run/build the project.

```
./main --help
```
