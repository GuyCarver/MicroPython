"""Implement a simple shell for running on MicroPython."""

# from __future__ import print_function

import os
import sys
import cmd
import pyb
import time

# TODO:
#   - Need to figure out how to get input without echo for term_size
#   - Add sys.stdin.isatty() for when we support reading from a file
#   - Need to integrate readline in a python callable way (into cmd.py)
#       so that the up-arrow works.
#   - Need to define input command to use this under windows

MONTH = ('', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


def term_size():
    """Print out a sequence of ANSI escape code which will report back the
    size of the window.
    """
    # ESC 7         - Save cursor position
    # ESC 8         - Restore cursor position
    # ESC [r        - Enable scrolling for entire display
    # ESC [row;colH - Move to cursor position
    # ESC [6n       - Device Status Report - send ESC [row;colR
    repl= None
    if 'repl_source' in dir(pyb):
        repl = pyb.repl_source()
    if repl is None:
        repl = pyb.USB_VCP()
    repl.send(b'\x1b7\x1b[r\x1b[999;999H\x1b[6n')
    pos = b''
    while True:
        char = repl.recv(1)
        if char == b'R':
            break
        if char != b'\x1b' and char != b'[':
            pos += char
    repl.send(b'\x1b8')
    (height, width) = [int(i, 10) for i in pos.split(b';')]
    return height, width

# def term_size():
#    return (25, 80)


def get_mode(filename):
    try:
        return os.stat(filename)[0]
    except OSError:
        return 0


def get_stat(filename):
    try:
        return os.stat(filename)
    except OSError:
        return (0, 0, 0, 0, 0, 0, 0, 0)


def mode_exists(mode):
    return mode & 0xc000 != 0


def mode_isdir(mode):
    return mode & 0x4000 != 0


def mode_isfile(mode):
    return mode & 0x8000 != 0


def print_cols(words, termwidth=79):
    """Takes a single column of words, and prints it as multiple columns that
    will fit in termwidth columns.
    """
    width = max([len(word) for word in words])
    nwords = len(words)
    ncols = max(1, (termwidth + 1) // (width + 1))
    nrows = (nwords + ncols - 1) // ncols
    for row in range(nrows):
        for i in range(row, nwords, nrows):
            print('%-*s' % (width, words[i]),
                  end='\n' if i + nrows >= nwords else ' ')


def print_long(files):
    """Prints detailed information about each file passed in."""
    for file in files:
        stat = get_stat(file)
        mode = stat[0]
        if mode_isdir(mode):
            mode_str = '/'
        else:
            mode_str = ''
        size = stat[6]
        mtime = stat[8]
        localtime = time.localtime(mtime)
        print('%6d %s %2d %02d:%02d %s%s' % (size, MONTH[localtime[1]],
              localtime[2], localtime[4], localtime[5], file, mode_str))


def sdcard_present():
    """Determine if the sdcard is present. This current solution is specific
    to the pyboard. We should really have a pyb.scard.detected() method
    or something.
    """
    return pyb.Pin.board.SD.value() == 0


class Shell(cmd.Cmd):
    """Implements the shell as a command line interpreter."""

    def __init__(self, **kwargs):
        (self.term_height, self.term_width) = term_size()
        cmd.Cmd.__init__(self, **kwargs)

        self.stdout_to_shell = self.stdout

        self.cur_dir = os.getcwd()
        self.set_prompt()

    def set_prompt(self):
        self.prompt = self.cur_dir + '> '

    def resolve_path(self, path):
        if path[0] != '/':
            # Relative path
            if self.cur_dir[-1] == '/':
                path = self.cur_dir + path
            else:
                path = self.cur_dir + '/' + path
        comps = path.split('/')
        new_comps = []
        for comp in comps:
            if comp == '.':
                continue
            if comp == '..' and len(new_comps) > 1:
                new_comps.pop()
            else:
                new_comps.append(comp)
        if len(new_comps) == 1:
            return new_comps[0] + '/'
        return '/'.join(new_comps)

    def emptyline(self):
        """We want empty lines to do nothing. By default they would repeat the
        previous command.

        """
        pass

    def postcmd(self, stop, line):
        self.stdout.close()
        self.stdout = self.stdout_to_shell
        self.set_prompt()
        return stop

    def line_to_args(self, line):
        """This will convert the line passed into the do_xxx functions into
        an array of arguments and handle the Output Redirection Operator.
        """
        args = line.split()
        if '>' in args:
            self.stdout = open(args[-1], 'a')
            return args[:-2]
        else:
            return args

    def help_args(self):
        self.stdout.write('Prints out command line arguments.\n')

    def do_args(self, line):
        args = self.line_to_args(line)
        for idx in range(len(args)):
            print("arg[%d] = '%s'" % (idx, args[idx]))

    def help_cat(self):
        self.stdout.write('Concatinate files and send to stdout.\n')

    def do_cat(self, line):
        args = self.line_to_args(line)
        for filename in args:
            filename = self.resolve_path(filename)
            mode = get_mode(filename)
            if not mode_exists(mode):
                self.stdout.write("Cannot access '%s': No such file\n" %
                                  filename)
                continue
            if not mode_isfile(mode):
                self.stdout.write("'%s': is not a file\n" % filename)
                continue
            with open(filename, 'r') as txtfile:
                for line in txtfile:
                    self.stdout.write(line)

    def help_cd(self):
        self.stdout.write('Changes the current directory\n')

    def do_cd(self, line):
        args = self.line_to_args(line)
        try:
            dirname = self.resolve_path(args[0])
        except IndexError:
            dirname = '/'
        mode = get_mode(dirname)
        if mode_isdir(mode):
            self.cur_dir = dirname
        else:
            self.stdout.write("Directory '%s' does not exist\n" % dirname)

    def help_echo(self):
        self.stdout.write('Display a line of text.\n')

    def do_echo(self, line):
        args = self.line_to_args(line)
        self.stdout.write(args[0])
        self.stdout.write('\n')

    def help_help(self):
        self.stdout.write('List available commands with "help" or detailed ' +
                          'help with "help cmd".\n')

    def do_help(self, line):
        cmd.Cmd.do_help(self, line)

    def help_ls(self):
        self.stdout.write('List directory contents.\n' +
                          'Use ls -a to show hidden files')

    def do_ls(self, line):
        args = self.line_to_args(line)
        show_invisible = False
        show_long = False
        while len(args) > 0 and args[0][0] == '-':
            if args[0] == '-a':
                show_invisible = True
            elif args[0] == '-l':
                show_long = True
            else:
                self.stdout.write("Unrecognized option '%s'" % args[0])
                return
            args.remove(args[0])
        if len(args) == 0:
            args.append('.')
        for idx in range(len(args)):
            dirname = self.resolve_path(args[idx])
            mode = get_mode(dirname)
            if not mode_exists(mode):
                self.stdout.write("Cannot access '%s': No such file or "
                                  "directory\n" % dirname)
                continue
            if not mode_isdir(mode):
                self.stdout.write(dirname)
                self.stdout.write('\n')
                continue
            files = []
            if len(args) > 1:
                if idx > 0:
                    self.stdout.write('\n')
                self.stdout.write("%s:\n" % dirname)
            for filename in os.listdir(dirname):
                if dirname[-1] == '/':
                    full_filename = dirname + filename
                else:
                    full_filename = dirname + '/' + filename

                mode = get_mode(full_filename)
                if not show_long and mode_isdir(mode):
                    filename += '/'
                if (show_invisible or
                   (filename[0] != '.' and filename[-1] != '~')):
                    files.append(filename)
            if (len(files) > 0):
                if show_long:
                    print_long(sorted(files))
                else:
                    print_cols(sorted(files), self.term_width)

    def help_micropython(self):
        self.stdout.write('Micropython! Call any scripts! Interactive mode! ' +
                          'Quit with exit()')

    def do_micropython(self, line):
        args = self.line_to_args(line)
        source = None
        if len(args) == 1:
            source = args[-1]
            source = self.resolve_path(source)
            mode = get_mode(source)
            if not mode_exists(mode):
                self.stdout.write("Cannot access '%s': No such file\n" %
                                  source)
                return
            if not mode_isfile(mode):
                self.stdout.write("'%s': is not a file\n" % source)
                return
        if source is None:
            print('[Micropython]')
            while True:
                code_str = ''
                line = input('|>>> ')
                if line[0:4] == 'exit':
                    break
                code_str += '%s\n' % line
                if line[-1] == ':':
                    while True:
                        line = input('|... ')
                        if line == '':
                            break
                        code_str += '%s\n' % line
                exec(code_str)
        else:
            code_str = ''
            with open(source, 'r') as code:
                for line in code:
                    code_str = code_str + line + '\n'
            exec(code_str)

    def help_mkdir(self):
        self.stdout.write('Create directory.')

    def do_mkdir(self, line):
        args = self.line_to_args(line)
        target = args[0]
        mode = get_mode(target)
        if not mode_exists(mode):
            os.mkdir(target)
        else:
            print('%s already exists.' % target)

    def help_rm(self):
        self.stdout.write('Delete files and directories.')

    def do_rm(self, line):
        args = self.line_to_args(line)
        if args[0] in ('pybcdc.inf', 'README.txt', 'boot.py', 'main.py'):
            print('This file cannot be deleted')
        try:
            os.remove(args[0])
        except:
            try:
                os.rmdir(args[0])
            except:
                print('%s is not a file or directory.' % args[0])

    def help_EOF(self):
        self.stdout.write('Control-D to quit.\n')

    def do_EOF(self, _):
        # The prompt will have been printed, so print a newline so that the
        # REPL prompt shows up properly.
        print('')
        return True


def run():
    Shell().cmdloop()

run()
