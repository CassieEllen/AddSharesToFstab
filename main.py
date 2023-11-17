#!/bin/env python3
"""

addShares.sh is created each time the script starts. Any existing file is deleted
and a new file is started.

shares.json is the name of the shares file. it is a list of shares grouped by server.
Reads from shares.json if it exists.
Otherwise, shares.json is created from the data in shares.name.

"""

import inspect
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path

###############################################################################
debugging = True
skipping = True
unittest = False
verbose = True
# cmd_out is the command file being created
cmd_out = None
# set the share file to read
shares_filename = "shares.json"
if debugging:
    oops = Path('oops.txt')
    oops.unlink(True)
    cmd_out = oops
# define structure to read json shares into
shares = {} # json.loads(Path(shares_filename).read_text())
if unittest:
    print('(22) type(shares)', type(shares))
    print('(23) shares', shares, "\n")

# username, password are the network credentials
username = "cenicol"
password = "ka1.ssa8"

# Define command filename and privileges
cmd_name = 'addShares.sh'
uid = gid = 1000

# hosts file lookup
host = {
    "buffalo": "10.0.0,107",
    "synology": "10.0.0.108",
}
# smb share names to be created in fstab
share_names = {
    "buffalo": [
        'Music',
        'Cassie-Windows',
        'Cassie-Linux',
        'Cassie-Backup',
        'Cassie',
        'cenicol',
        'Shared',
    ],
    "synology": [
        'Cassie_Windows',
        'homes',
        'LaurieO',
        'linux',
        'music',
        'web',
        'web_packages'
    ],
}
if unittest:
    print('(75) type(share_names)', type(share_names))
    print('(76) share_names', share_names, "\n")

# -----------------------------------------------------------------------------
def create_log_line(text: str|None='') -> str:
    line_no = inspect.currentframe().f_back.f_lineno
    line_no_str = '(' + str(line_no) + ')'
    if text is None:
        text = ''
    print(line_no_str, text)


# -----------------------------------------------------------------------------
def create_log_title(text: str|None='') -> str:
    """
    Create a log line - based on create_title_line

    :param text: the text to be embedded in the line
    :return: the full line
    """

    line_no = inspect.currentframe().f_back.f_lineno
    line_no_str = str(line_no)
    front_str = f'({line_no_str}) '
    len_front_str = len(front_str)

    if text is None:
        text = ''
        len_text = 0
    else:
        len_text = len(text)
    len_middle = len_front_str + 2 + len_text
    if debugging:
        print('len_text =', len_text)
        print('len_front_str =', len_front_str)
        print('len_middle =',len_middle)
    len_paddingL = len_paddingR = int((80 - len_middle) / 2)
    len_line = len_middle + len_paddingL + len_paddingR
    if debugging:
        print(len_paddingL, len_middle, len_paddingR, len_line)
    if len_line < 80:
        len_paddingR += 1
        len_line = len_middle + len_paddingL + len_paddingR
    line = front_str + '-'*len_paddingL + ' ' + text + ' ' + '-'*len_paddingR
    if debugging:
        print('len_line =', len_line)
        print('len(line) =', len(line))
    assert len_line == len(line) == 80
    assert len_line == 80
    print(line)
    return(line)

# -----------------------------------------------------------------------------
def append_text(path: Path,
                text,
                encoding:str|None=None,
                errors:str|None=None,
                prefix:str|None='# ',
                end:str|None='\n'):
    """ Append text to the end of file path

    :param path: Path to write to
    :param text: text to be written
    :param encoding: passed to open()
    :param errors: passed to open()
    :param prefix: beginning of line to be written
    :param end: end of line to be written
    :return:
    """
    # The file 'f' is closed when the with block exits.
    if prefix is None:
        prefix = '# '
    if end is None:
        end = '\n'
    with path.open("a", encoding=encoding, errors=errors) as f:
        f.write(f'{prefix}{text}{end}')


# ------------------------------------------------------------------------------
def mount_filename(name: str):
    return '/mnt/' + name


# ------------------------------------------------------------------------------
def do_cmd(cmdline: str) -> bool:
    """
    Execute a command.
    :param cmdline: command to execute
    :return: True on success
    """
    rv = subprocess.call(cmdline, shell=True)
    target = sys.stdout
    if 0 != rv:
        sys.stdout.flush()
        target = sys.stderr
        return False
    print(f"{rv} {cmdline}", file=target)
    return True


# ------------------------------------------------------------------------------
# Returns:  True if the directory was crested.
#           False if the directory already exists
#
def do_mkdir(file):
    filename = get_filename(file)
    p = Path(filename)
    if p.exists():
        append_text(cmd_out, f"{filename} already exists.")
        return False
    do_cmd(f"sudo mkdir {filename}")
    return True


# ------------------------------------------------------------------------------
# Returns:  True if the directory exists (needs to be deleted).
#           False if the directory is not there.
def do_rmdir(name) -> bool:
    filename = get_filename(name)
    p = Path(filename)
    if p.exists():
        do_cmd(f'sudo rmdir {filename}')
        return True
    else:
        append_text(cmd_out, f'# {filename} missing')
        return False


# ------------------------------------------------------------------------------

def do_not():
    pass


# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------

def print_hi(name):
    """

    :param name: String to be printed
    :return: None
    """
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


# ------------------------------------------------------------------------------
def get_filename(file:str) -> str:
    s = '/mnt/' + file
    print('directory =', s)
    return s

# ------------------------------------------------------------------------------
def do_cleanup(cmd_out: Path):
    # end=''    suppresses newline
    # end=None  adds newline
    print('Cleaning up /mnt directory')
    append_text(cmd_out, '# Cleaning up /mnt directory', prefix="", end="\n")
    if debugging:
        if unittest:
            # Show expected text
            append_text(cmd_out, 'Testing append_text()')
            append_text(cmd_out, 'Expected text:')
            append_text(cmd_out, 'next line<no-newline># next line', prefix="# |")
            append_text(cmd_out, '# next line', prefix="# |")
            append_text(cmd_out, 'last line', prefix="# |")
            # Write text
            append_text(cmd_out, 'Actual text:')
            append_text(cmd_out, 'next line', prefix='', end='<no-newline>')
            append_text(cmd_out, 'next line', end=None)
            append_text(cmd_out, 'next line', end="\n")
            append_text(cmd_out, 'last line', prefix='')

    for server in share_names:
        for share in share_names[server]:
            filename = get_filename(share)
            p = Path(filename)
            if p.exists():
                append_text(cmd_out, f'Removing directory {p} ')
                if p.is_mount():
                    do_cmd(f"sudo umount {filename}")
                # Delete the directory
                do_rmdir(share)
            else:
                append_text(cmd_out, f'Directory {p} does not exist.')

# ------------------------------------------------------------------------------


def create_mount_points():
    if debugging:
        create_log_line('create_mount_points()')
    print('Creating new directories')
    append_text(cmd_out, "Creating new directories for mounting\n")
    max_share_len = 0
    if debugging:
        for server in shares:
            for share in shares[server]:
                share_str = f'//{server}/{share} '
                max_share_len = max(max_share_len, len(share_str))
            max_share_len += 1
    for server in shares:
        # Spot check the format of shares
        if unittest:
            assert(isinstance(shares, dict))
            assert(isinstance(server, str))
            assert(isinstance(shares[server], list))
        for share in shares[server]:
            share_str = f'//{server}/{share} '
            share_len = len(share_str)
            filename = get_filename(share)
            smb_share = f"//{host[server]}/{share}"
            if debugging:
                pad_len = max_share_len - share_len
                assert pad_len
                pad_str = ''.join(' '*pad_len)
                '''
                if verbose:
                    add_space = ''
                    if pad_len <= 10:
                        add_space = ' '
                    if debugging:
                        test_str = ''.join(('[', ' '*pad_len, ']'))
                        test_len = len(test_str)
                        print(test_len, test_str)
                    create_log_line(f'{max_share_len} {share_len} {add_space}{pad_len} "{pad_str}" |')
                    print(f'(233) {max_share_len} {share_len} {add_space}{pad_len} "{pad_str}" |')
                    create_log_line(f'{max_share_len} {share_len} {add_space}{pad_len} "{pad_str}" |')
                '''
                print(share_str, pad_str, " --> ", smb_share, sep='')
            options = f"user={username},pass={password}"
            mount_cmd = f"sudo mount -o {options} {smb_share} {filename}"
            if do_mkdir(share):
                # cmd = f"sudo ls -l {filename} ; chmod 777 {share}"
                cmd = f"-->sudo ls -l {filename} ; chmod 777 {filename}"
                do_cmd(cmd)
                do_cmd(mount_cmd)
            else:
                print(f"Directory already exists. {filename}")
                append_text(cmd_out, f'Directory already exists. {filename}')

# ------------------------------------------------------------------------------

def log(*args, **kwargs):
    print(args, kwargs)
    print(kwargs)
    print("args")
    for s in args:
        print('\t"', s, '"', sep='')
    print("kwargs")
    for s in kwargs:
        print('\t"', s, '"', sep='')

def create_title_line(text: str|None='') -> str:
    """
    Create a documentation title line

    #_----------paddingL----------_text_----------paddingR-----------
    12                            3    4
    len_other is equal to len(text) + 4 more (as shown above)
    4 more: 2 chars #-space at the beginning of the line + the two spaces surrounding text
    padding is the line before and after the title

    :param text: the text to be embedded in the line
    :return: the full line
    """
    if text is None:
        text = ''
    if debugging:
        print('#', '='*78)
    len_text = len(text)
    len_middle = 4 + len_text
    len_paddingL = len_paddingR = int((80 - len_middle) / 2)
    len_line = len_middle + len_paddingL + len_paddingR
    if debugging:
        print('len_text', len_text)
        print('len_middle =', len_middle)
        print(len_middle, '+', len_paddingL, '+', len_paddingR, '=', len_middle + len_paddingL + len_paddingR)
        print('len_line =', len_line)
    if len_line < 80:
        len_paddingR += 1
        len_line = len_middle + len_paddingL + len_paddingR
        if debugging:
            print(len_middle, '+', len_paddingL, '+', len_paddingR, '=', len_middle + len_paddingL + len_paddingR)
            print('len_line =', len_line)
    line = '# ' + '-'*len_paddingL + ' ' + text + ' ' + '-'*len_paddingR
    assert len_line == len(line) == 80
    assert len_line == 80
    if debugging:
        print('"', line, '"', sep='')
        print('#', '='*78)
    return(line)

def openCmdOut():
    # Open the shell command file, 'addShares.sh'
    # replace any existing file
    # Set file privs to 0775 and ownership to uid 1000
    cmd_out = Path(cmd_name)
    if cmd_out.exists():
        cmd_out.unlink()
    mode = 0o775
    cmd_out.touch(mode, False)
    cmd_out.chmod(mode)
    print('setting mode to', )
    # os.chown(cmd_name, os.getuid(), os.getgid())
    if debugging:
        print('uid =', os.getuid())
        print('gid =', os.getgid())
        os.chown(cmd_name, uid, gid)

    # Open for writing, write command invocation
    cmd_out.open('w')
    append_text(cmd_out, '#!/usr/bin/env bash', prefix=None)
    append_text(cmd_out, 'echo addShares.sh', prefix=None)


# ------------------------------------------------------------------------------
def create_cmd_out():
    global cmd_out
    # Open the shell command file, 'addShares.sh'
    # replace any existing file
    # Set file privs to 0775 and ownership to uid 1000
    cmd_out = Path(cmd_name)
    if cmd_out.exists():
        cmd_out.unlink()
    mode = 0o775
    cmd_out.touch(mode, False)
    cmd_out.chmod(mode)
    print('setting mode to', )
    # os.chown(cmd_name, os.getuid(), os.getgid())
    if unittest:
        print('uid =', os.getuid())
        print('gid =', os.getgid())
        os.chown(cmd_name, uid, gid)

    # Open for writing, write command invocation
    cmd_out.open('w')
    append_text(cmd_out, '#!/usr/bin/env bash', prefix=None)
    append_text(cmd_out, 'echo addShares.sh', prefix=None)


# ------------------------------------------------------------------------------
def usage():
    print('usage: ./addShares.py [clean] [start] ')


# ------------------------------------------------------------------------------
#                              main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
    Add a list of shares to /etc/fstab

    """

    print_hi('addShares')

    if debugging:
        line = create_title_line('text123')

    if not skipping:
        assert type(shares) == type(share_names)
        type_shares = type(shares)
        print('type_shares =', type_shares)
        print('type(type_shares) =', type(type_shares))
        print('type(shares) =', type(shares))
        print('isinstance(shares, dict) :', isinstance(shares, dict))

    # process command line arguments
    argc = len(sys.argv)
    if argc == 1:
        pass
        # rv = create_mount_points()
        # exit(rv)
    else:
        command = sys.argv[1]
        if 'clean' == command:
            create_cmd_out()
            do_cleanup(cmd_out)
            exit(0)
        elif 'help' == command:
            usage()
        else:
            usage()

    # Convert Python data, share_names, into json
    # share_names is not a string, it is a python data structure.
    # json.dump() -> json_str is a string in json format.
    # json_loads() -> shares is a python data structure created from the
    #                 json string
    create_log_title()
    json_str = json.dumps(share_names)
    if debugging:
        create_log_line(f'json_str = {json_str}')
        create_log_line('type(shares) = {type(shares)}')
    if debugging:
        create_log_line(f'type(shares) = {type(shares)}')
        create_log_line(f'type(share_names) = {type(share_names)}')
    assert type(shares) == type(share_names)
    if Path(shares_filename).exists():
        create_log_title('Reading' + shares_filename)
        print('Reading', shares_filename)
        try:
            buffer = Path(shares_filename).open().read()
            shares = json.loads(buffer)
        except TypeError as err:
            print("exception:", err)
            traceback.print_exc()
    else:
        create_log_title('Creating ' + shares_filename)
        print('Creating', shares_filename)
        with Path(shares_filename).open("w") as f:
            f.write(json_str)

    # shares_str = str(shares)
    # stra = list(json_str)
    # strb = list(shares_str)

    print("Print command line arguments")
    for arg in sys.argv:
        print('\t', arg)
