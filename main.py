from sohFileHandler import sohFileHandler
from gitReleases import sohReleaseHandler
import sys
import os
import click

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    _localDir = sys._MEIPASS
else:
    _localDir = os.path.dirname(os.path.abspath(__file__))



a = sohFileHandler()
# #b = sohReleaseHandler()

# a.setSohDir('/home/matt/Downloads/SOH')
# a.setRomDir('/home/matt/Downloads/SOH/soh-linux-compatibility/ZELOOTD.z64')

# a.setSohVersions()
# a.setDefaultVersion('SoH-MacReady-Charlie-Linux-Performance')

# #c = b.getSohGithubVersionsJson()

# print(a.getJson())

#a.runSOH('/home/matt/Downloads/SOH/SoH-MacReady-Charlie-Linux-Performance', _localDir)

@click.command()
@click.option('--versions', 'param', flag_value='versions', help='Display installed SOH versions. Also refreshes installed verisons')
@click.option('--refresh', 'param', flag_value='refresh', help='Refreshes SOH versions')
@click.option('--gsohDir', 'param', flag_value='gsoh', help='Display current SOH directory')
@click.option('--sohDir', 'param', flag_value='soh', help='Update SOH directory')
@click.option('--gromDir', 'param', flag_value='grom', help='Display current ROM directory')
@click.option('--romDir', 'param', flag_value='rom', help='Update ROM directory')
@click.option('--default', 'param', flag_value='default', help='Set default SOH version')
@click.option('--run', 'param', flag_value='run', help='Run a version of SOH. Spell out the verion name or leave blank for default')
@click.option('--symlink', 'param', flag_value='sym', help="Symlink all Roms in the Rom Directory for a version of SOH. Symlinked roms won't work for all versions of SOH.")
@click.option('--copy', 'param', flag_value='copy', help="Copy save data between two versions of SOH. SHOULD ONLY BE DONE IF YOU KNOW WHAT YOU ARE DOING.")
@click.argument('inp', default='')
@click.argument('inp2', default='')
def main(param, inp, inp2):

    match param:
        case 'versions':
            a.setSohVersions()
            a.listVersions(a.getSohVersions())
        case 'refresh':
            a.setSohVersions()
        case 'default':
            try:
                a.setDefaultVersion(inp)
                print("Default SOH Version set to " + a.getDefault())
            except:
                print("SOH version input not found")
        case 'gsoh':
            print(a.getSohDir())
        case 'soh':
            a.setSohDir(inp)
        case 'grom':
            print(a.getRomDir())
        case 'rom':
            a.setRomDir(inp)
        case 'run':

            if inp == '':
                a.runSOH(a.getPathofSohVersion(a.getDefault()), _localDir)
                print("No version input. Opening default.")
                return

            try:
                a.runSOH(a.getSohVersions()[inp][a.getJsonSohVersionPathName()], _localDir)
                print("Opening " + inp)
            except:
                print("Couldn't open " + inp + " version of SOH. It may not exist.")
        case 'sym':

            path = None
            try:
                path = a.getPathofSohVersion(inp)

                if (path == None):
                    print("Version doesn't exist.")
                    return
                
                a.symlinkRom(path)
            except:
                print("Couldn't symlink. There are already symlinked files in directory: " + path)

        case 'copy':

            if (a.getPathofSohVersion(inp) == None):
                print("From version not found")
                return

            if (a.getPathofSohVersion(inp2) == None):
                print("To version not found")
                return

            try:
                print("This is recommended for advanced users only. Copying data between different versions of SOH can sometimes not work.")
                print("WARNING: THIS WILL OVERWRITE ANY EXISTING FILES/FOLDERS")

                if (str(input("Are you sure you want to copy files?(Y/N) ")).lower() == 'n'):
                    return
                
                if (str(input("Copy shipofharkinian.json? ").lower()) == 'y'):
                    a.copyData(inp, inp2, "shipofharkinian.json")

                if (str(input("Copy save folder? ").lower()) == 'y'):
                    a.copyData(inp, inp2, "Save")

                if (str(input("Copy mods folder? ").lower()) == 'y'):
                    a.copyData(inp, inp2, "mods")
                
                if (str(input("Copy imgui.ini? ").lower()) == 'y'):
                    a.copyData(inp, inp2, "imgui.ini")
                
            except:
                print("Couldn't copy files")

if __name__=='__main__':
    main()