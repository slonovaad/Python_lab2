from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.cat import cat
from src.commands.cp import cp
from src.commands.mv import mv
from src.commands.rm import rm
from src.commands.zip import zip
from src.commands.unzip import unzip
from src.commands.tar import tar
from src.commands.untar import untar
from src.commands.history import history
from src.commands.undo import undo
from src.commands.grep import grep

COMMANDS = {"ls": ls,
            "cd": cd,
            "cat": cat,
            "cp": cp,
            "mv": mv,
            "rm": rm,
            "zip": zip,
            "unzip": unzip,
            "tar": tar,
            "untar": untar,
            "history": history,
            "undo": undo,
            "grep": grep,
            }
