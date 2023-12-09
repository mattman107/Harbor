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
@click.argument('input', default='')
def main(param, input):
    
    match param:
        case 'versions':
            a.setSohVersions()
            a.listVersions(a.getSohVersions())
        case 'refresh':
            a.setSohVersions()
        case 'default':
            try:
                a.setDefaultVersion(input)
                print("Default SOH Version set to " + a.getDefaultSohVersion)
            except:
                print("SOH version input not found")
        case 'gsoh':
            print(a.getSohDir())
        case 'soh':
            a.setSohDir(input)
        case 'grom':
            print(a.getRomDir())
        case 'rom':
            a.setRomDir(input)
        case 'run':

            if input == '':
                a.runSOH(a.getDefaultSohVersion()[a.getJsonSohVersionPathName()], _localDir)
                print("No version input. Opening default.")
                return

            try:
                a.runSOH(a.getSohVersions()[input][a.getJsonSohVersionPathName()], _localDir)
                print("Opening " + input)
            except:
                print("Couldn't open " + input + " version of SOH. It may not exist.")
        case 'sym':

            path = None
            try:
                path = a.getSohVersions()[input][a.getJsonSohVersionPathName()]
                a.symlinkRom(path)
            except:
                if (path == None):
                    print("Version doesn't exist.")
                    return
                print("Couldn't symlink. There are already symlinked files in directory: " + path)

if __name__=='__main__':
    main()