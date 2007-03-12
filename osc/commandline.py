#!/usr/bin/python

# Copyright (C) 2006 Peter Poeml / Novell Inc.  All rights reserved.
# This program is free software; it may be used, copied, modified
# and distributed under the terms of the GNU General Public Licence,
# either version 2, or (at your option) any later version.


from core import *
import conf

usage_general = """\
usage: osc <subcommand> [options] [args]
OpenSUSE build service command-line tool, version %s.
Type 'osc help <subcommand>' for help on a specific subcommand.

Most subcommands take file and/or directory arguments, recursing
on the directories.  If no arguments are supplied to such a
command, it recurses on the current directory (inclusive) by default.

Please see also:
* http://en.opensuse.org/Build_Service_Tutorial
* http://en.opensuse.org/Build_Service/CLI


Available subcommands:
""" % get_osc_version()


def init(args):
    """Initialize a directory to be a working copy of an existing buildservice
package. (This is the same as checking out a package and then copying sources
into the directory. It does NOT create a new package.)

usage: osc init <prj> <pac>
    """

    project = args[0]
    package = args[1]
    init_package_dir(project, package, os.path.curdir)
    print 'Initializing %s (Project: %s, Package: %s)' % (os.curdir, project, package)


def ls(args):
    """ls (list): List existing content on the server

usage: osc ls                         # list projects
       ls Apache                  # list packages in a project
       ls Apache subversion       # list files of package of a project
    """

    if not args:
        print '\n'.join(meta_get_project_list())
    elif len(args) == 1:
        project = args[0]
        print '\n'.join(meta_get_packagelist(project))
    elif len(args) == 2:
        project = args[0]
        package = args[1]
        print '\n'.join(meta_get_filelist(project, package))


def meta(args):
    """Shows meta information

usage: osc meta Apache              # show meta of project 'Apache'
       osc meta Apache subversion   # show meta of package 'subversion'
    """

    if not args:
        print 'missing argument'
        print
        print meta.func_doc
        sys.exit(1)

    if len(args) == 2:
        project = args[0]
        package = args[1]
        print ''.join(show_package_meta(project, package))
        print ''.join(show_files_meta(project, package))

    elif len(args) == 1:
        project = args[0]
        print ''.join(show_project_meta(project))


def editpac(args):
    """editpac (createpac): Edit package meta information
If the named package does not exist, it will be created.

usage: osc createpac <prj> <pac>
       osc editpac <prj> <pac>
    """

    if not args or len(args) != 2:
        sys.exit('missing argument\n\n%s\n' % editpac.func_doc)

    project = args[0]
    package = args[1]
    edit_meta(project, package)


def editprj(args):
    """editprj (createprj): Edit project meta information
If the named project does not exist, it will be created.

usage: osc createprj <prj>
       osc editprj <prj>
    """

    if not args or len(args) != 1:
        sys.exit('missing argument\n\n%s\n' % editprj.func_doc)

    project = args[0]
    edit_meta(project, None)


def editmeta(args):
    """Edit project/package meta information
If the named project or package does not exist, it will be created.

usage: osc editmeta FooPrj              # edit meta of project 'FooPrj'
       osc editmeta FooPrj barpackage   # edit meta of package 'barpackage'
    """

    if not args:
        print 'missing argument'
        print
        print editmeta.func_doc
        sys.exit(1)

    if len(args) == 2:
        project = args[0]
        package = args[1]
        edit_meta(project, package)

    elif len(args) == 1:
        project = args[0]
        edit_meta(project, None)


def edituser(args):
    """edituser: Edit user meta information
usage: osc edituser <user>

If the named user id does not exist, it will be created.
    """

    if not args or len(args) != 1:
        user = conf.config['user']
    else:
        user = args[0]
    edit_user_meta(user)


def linkpac(args):
    """"Link" a package to another package -- possibly cross-project.

usage: osc linkpac SOURCEPRJ SOURCEPAC DESTPRJ [DESTPAC]

The DESTPAC name is optional; the source packages' name will be used if
DESTPAC is omitted.

Afterwards, you will want to 'checkout DESTPRJ DESTPAC'.

To add a patch, add the patch as file and add it to the _link file.
You can also specify text which will be inserted at the top of the spec file.

See the examples in the _link file.

    """

    if not args or len(args) < 3:
        print 'missing argument'
        print
        print linkpac.func_doc
        sys.exit(1)


    src_project = args[0]
    src_package = args[1]
    dst_project = args[2]
    if len(args) > 3:
        dst_package = args[3]
    else:
        dst_package = src_package

    if src_project == dst_project and src_package == dst_package:
        sys.exit('osc: error: source and destination are the same')
    link_pac(src_project, src_package, dst_project, dst_package)


def copypac(args):
    """"Copy" a package, possibly cross-project.

usage: osc copypac SOURCEPRJ SOURCEPAC DESTPRJ [DESTPAC]

The DESTPAC name is optional; the source packages' name will be used if
DESTPAC is omitted.

    """

    if not args or len(args) < 3:
        print 'missing argument'
        print
        print copypac.func_doc
        sys.exit(1)


    src_project = args[0]
    src_package = args[1]
    dst_project = args[2]
    if len(args) > 3:
        dst_package = args[3]
    else:
        dst_package = src_package

    if src_project == dst_project and src_package == dst_package:
        sys.exit('osc: error: source and destination are the same')
    copy_pac(src_project, src_package, dst_project, dst_package)


def deletepac(args):
    """deletepac: Delete a package on the server.

usage: osc deletepac <prj> <pac>
    """

    if not args or len(args) < 2:
        print 'missing argument'
        print
        print deletepac.func_doc
        sys.exit(1)

    project = args[0]
    package = args[1]

    delete_package(project, package)


def deleteprj(args):
    """deleteprj: Delete a project on the server.

usage: osc deleteprj <prj>

As a safety measure, project must be empty (i.e., you first need to delete all
packages first).
    """

    if not args or len(args) < 1:
        print 'missing argument'
        print
        print deleteprj.func_doc
        sys.exit(1)

    project = args[0]

    if meta_get_packagelist(project) != []:
        sys.exit('project must be empty before deleting it.')
    delete_project(project)


def updatepacmetafromspec(args):
    """Update package meta information from a specfile

usage: 1. osc updatepacmetafromspec                       # current dir
       2. osc updatepacmetafromspec dir1 dir2 ...
    """
    args = parseargs(args)
    pacs = findpacs(args)

    for p in pacs:

        p.read_meta_from_spec()
        p.update_pac_meta()


def diff(args):
    """diff: Generates a diff, to view the local changes

    usage: 1. osc diff                       # current dir
           2. osc diff file1 file2 ...

    """

    args = parseargs(args)
    pacs = findpacs(args)

    difference_found = False
    for p in pacs:
        if p.todo == []:
            for i in p.filenamelist:
                s = p.status(i)
                if s == 'M' or s == 'C':
                    p.todo.append(i)

        d = []
        for filename in p.todo:
            d.append('Index: %s\n' % filename)
            d.append('===================================================================\n')
            d.append(get_source_file_diff(p.dir, filename, p.rev))
        if d:
            print ''.join(d)
            difference_found = True

    if difference_found:
        sys.exit(1)


            
def repourls(args):
    """repourls: shows URLs on which to access the .repos files

usage: 1. osc repourls
       2. osc repourls [dir1] [dir2] ...

    """

    args = parseargs(args)
    pacs = findpacs(args)

    url_tmpl = 'http://software.opensuse.org/download/%s/%s/%s.repo'
    for p in pacs:
        platforms = get_platforms_of_project(p.prjname)
        for platform in platforms:
            print url_tmpl % (p.prjname.replace(':', ':/'), platform, p.prjname)


            
def checkout(args):
    """checkout (co): Check out content from the server.

usage: osc co Apache                    # entire project
       osc co Apache subversion         # a package
       osc co Apache subversion foo     # single file -> to current dir
    """

    project = package = filename = None
    try: 
        project = args[0]
        package = args[1]
        filename = args[2]
    except: 
        pass

    if filename:
        get_source_file(project, package, filename)

    elif package:
        checkout_package(project, package)

    elif project:
        # all packages
        for package in meta_get_packagelist(project):
            checkout_package(project, package)
    else:
        print 'missing argument'
        print
        print checkout.func_doc
        sys.exit(1)


def status(args):
    """Show the status (which files have been changed locally)
usage: osc st
       osc st <directory>
       osc st file1 file2 ...
    """

    args = parseargs(args)

    pacpaths = []
    for arg in args:
        # when 'status' is run inside a project dir, it should
        # stat all packages existing in the wc
        if is_project_dir(arg):
            prj = Project(arg)
            pacpaths += [arg + '/' + n for n in prj.pacs_have]
        elif is_package_dir(arg):
            pacpaths.append(arg)
        elif os.path.isfile(arg):
            pacpaths.append(arg)
        else:
            sys.exit('osc: error: %s is neither a project or a package directory' % arg)
        

    pacs = findpacs(pacpaths)

    for p in pacs:

        # no files given as argument? Take all files in current dir
        if not p.todo:
            p.todo = p.filenamelist + p.filenamelist_unvers
        p.todo.sort()

        lines = []
        for filename in p.todo:
            if filename in p.excluded:
                continue
            s = p.status(filename)
            if s == 'F':
                lines.append(statfrmt('!', pathjoin(p.dir, filename)))
            elif s != ' ':
                lines.append(statfrmt(s, pathjoin(p.dir, filename)))
            # for -v (later)
            #else:
            #    lines.append(statfrmt(s, pathjoin(p.dir, filename)))

        # arrange the lines in order: unknown files first
        # filenames are already sorted
        lines = [line for line in lines if line[0] == '?'] \
              + [line for line in lines if line[0] != '?']
        if lines:
            print '\n'.join(lines)


def add(args):
    """Mark files to be added upon next 'checkin'

usage: osc add file1 file2 ...
    """

    if not args:
        print '%s requires at least one argument' % cmd
        sys.exit(1)

    filenames = parseargs(args)

    for filename in filenames:
        if not os.path.exists(filename):
            print "file '%s' does not exist" % filename
            sys.exit(1)

    pacs = findpacs(filenames)

    for pac in pacs:
        for filename in pac.todo:
            if filename in pac.excluded:
                continue
            if filename in pac.filenamelist:
                print 'osc: warning: \'%s\' is already under version control' % filename
                continue

            pac.addfile(filename)
            print statfrmt('A', filename)


def addremove(args):
    """addremove: Adds all new files in local copy and removes all disappeared files.

usage: osc addremove
    """

    args = parseargs(args)
    pacs = findpacs(args)
    for p in pacs:

        p.todo = p.filenamelist + p.filenamelist_unvers

        for filename in p.todo:
            if os.path.isdir(filename):
                continue
            state = p.status(filename)
            if state == '?':
                p.addfile(filename)
                print statfrmt('A', filename)
            elif state == '!':
                p.put_on_deletelist(filename)
                p.write_deletelist()
                os.unlink(os.path.join(p.storedir, filename))
                print statfrmt('D', filename)



def commit(args):
    """commit (ci): Upload change content from your working copy to the repository

usage: osc ci                   # current dir
       osc ci <dir>
       osc ci file1 file2 ...
    """

    args = parseargs(args)
    pacs = findpacs(args)

    for p in pacs:

        # commit only if the upstream revision is the same as the working copy's
        upstream_rev = show_upstream_rev(p.prjname, p.name)
        if p.rev != upstream_rev:
            print 'Working copy \'%s\' is out of date (rev %s vs rev %s).' % (p.absdir, p.rev, upstream_rev)
            print 'Looks as if you need to update it first.'
            sys.exit(1)

        p.todo = p.filenamelist_unvers + p.filenamelist

        for filename in p.todo:
            st = p.status(filename)
            if st == 'A' or st == 'M':
                p.todo_send.append(filename)
                print 'Sending        %s' % filename
            elif st == 'D':
                p.todo_delete.append(filename)
                print 'Deleting       %s' % filename

        if not p.todo_send and not p.todo_delete:
            print 'nothing to do for package %s' % p.name
            continue

        print 'Transmitting file data ', 
        for filename in p.todo_send:
            sys.stdout.write('.')
            p.put_source_file(filename)
        for filename in p.todo_delete:
            p.delete_source_file(filename)
            p.to_be_deleted.remove(filename)
        if conf.config['do_commits'] == '1':
            p.commit(msg='MESSAGE')

        p.update_filesmeta()
        p.write_deletelist()
        print


def update(args):
    """Update a working copy

usage: osc up
       osc up [pac_dir]         # update a single package by its path
       osc up *                 # from within a project dir, update all packages
       osc up                   # from within a project dir, update all packages
                               AND check out all newly added packages
    """

    args = parseargs(args)

    for arg in args:

        # when 'update' is run inside a project dir, it should...
        if is_project_dir(arg):

            prj = Project(arg)

            # (a) update all packages
            args += prj.pacs_have

            # (b) fetch new packages
            prj.checkout_missing_pacs()
            args.remove(arg)


    pacs = findpacs(args)

    for p in pacs:

        # save filelist and (modified) status before replacing the meta file
        saved_filenames = p.filenamelist
        saved_modifiedfiles = [ f for f in p.filenamelist if p.status(f) == 'M' ]

        oldp = p
        p.update_filesmeta()
        p = Package(p.dir)

        # which files do no longer exist upstream?
        disappeared = [ f for f in saved_filenames if f not in p.filenamelist ]
            

        for filename in saved_filenames:
            if filename in disappeared:
                print statfrmt('D', filename)
                p.delete_localfile(filename)
                continue

        for filename in p.filenamelist:

            state = p.status(filename)
            if state == 'M' and p.findfilebyname(filename).md5 == oldp.findfilebyname(filename).md5:
                # no merge necessary... local file is changed, but upstream isn't
                pass
            elif state == 'M' and filename in saved_modifiedfiles:
                status_after_merge = p.mergefile(filename)
                print statfrmt(status_after_merge, filename)
            elif state == 'M':
                p.updatefile(filename)
                print statfrmt('U', filename)
            elif state == '!':
                p.updatefile(filename)
                print 'Restored \'%s\'' % filename
            elif state == 'F':
                p.updatefile(filename)
                print statfrmt('A', filename)
            elif state == ' ':
                pass


        p.update_pacmeta()

        #print ljust(p.name, 45), 'At revision %s.' % p.rev
        print 'At revision %s.' % p.rev
                


        
def delete(args):
    """rm (remove, del, delete): Mark files to be deleted upon next 'checkin'

usage: osc rm file1 file2 ...
    """

    if not args:
        print 'delete requires at least one argument'
        sys.exit(1)

    args = parseargs(args)
    pacs = findpacs(args)

    for p in pacs:

        for filename in p.todo:
            p.put_on_deletelist(filename)
            p.write_deletelist()
            try:
                os.unlink(os.path.join(p.dir, filename))
                os.unlink(os.path.join(p.storedir, filename))
            except:
                pass
            print statfrmt('D', filename)


def resolved(args):
    """If an update can't be merged automatically, a file is in 'C' (conflict)
state, and conflicts are marked with special <<<<<<< and >>>>>>> lines. 
After manually resolving the problem, use

usage: osc resolved <filename>
"""

    if not args:
        print 'this command requires at least one argument'
        sys.exit(1)

    args = parseargs(args)
    pacs = findpacs(args)

    for p in pacs:

        for filename in p.todo:
            print "Resolved conflicted state of '%s'" % filename
            p.clear_from_conflictlist(filename)


def usermeta(args):
    """usermeta:  show metadata about user <userid>

usage: osc usermeta <userid>
    """

    if not args:
        print 'this command requires at least one argument'
        sys.exit(1)

    r = get_user_meta(args[0])
    if r:
        print ''.join(r)


def platforms(args):
    """platforms: Shows platforms

usage 1. osc platforms
            Shows available platforms/build targets

      2. osc platforms <project>
            Shows the configured platforms/build targets of a project
    """

    if args:
        project = args[0]
        print '\n'.join(get_platforms_of_project(project))
    else:
        print '\n'.join(get_platforms())


def results_meta(args):
    """Shows the build results of the package in raw XML

usage: osc results_meta
    """
    wd = os.curdir
    package = store_read_package(wd)
    project = store_read_project(wd)
    print ''.join(show_results_meta(project, package))

            
def results(args):
    """Shows the build results of a package

usage: 1. osc results                   # package = current dir
       2. osc results <packagedir>
    """

    if args and len(args) > 1:
        print 'getting results for more than one package is not supported'
        print sys.exit(1)
        
    if args:
        wd = args[0]
    else:
        wd = os.curdir

    try:
        package = store_read_package(wd)
        project = store_read_project(wd)
    except:
        sys.exit('\'%s\' is not an osc package directory' % wd)

    print '\n'.join(get_results(project, package))

            
def prjresults(args):
    """Shows the aggregated build results of an entire project

usage: 1. osc prjresults                   # package = current dir
       2. osc prjresults <packagedir>
    """

    if args and len(args) > 1:
        print 'getting results for more than one project is not supported'
        print sys.exit(1)
        
    if args:
        wd = args[0]
    else:
        wd = os.curdir

    try:
        project = store_read_project(wd)
    except:
        sys.exit('\'%s\' is neither an osc project or package directory' % wd)

    print '\n'.join(get_prj_results(project))

            
def log(args):
    """log: Shows the log file from a package (you need to be inside a package directory)

usage: osc log <platform> <arch>

To find out <platform> and <arch>, you can use 'osc results'

    """

    if not args or len(args) != 2:
        print 'missing argument'
        print
        print log.func_doc
        sys.exit(1)

    wd = os.curdir
    package = store_read_package(wd)
    project = store_read_project(wd)

    platform = args[0]
    arch = args[1]
    offset = 0
    try:
        while True:
            log_chunk = get_log(project, package, platform, arch, offset)
            if len(log_chunk) == 0:
                break
            offset += len(log_chunk)
            print log_chunk.strip()
    except KeyboardInterrupt:
        pass


def buildinfo(args):
    """buildinfo: Shows the build "info" which is used in building a package 
This command is mostly used internally by the 'build' command.
It needs to be called inside a package directory.

usage: osc buildinfo <platform> <arch> [specfile]

The [specfile] argument is optional. <specfile> is a local specfile (or .dsc
file) which is sent to the server, and the buildinfo will be based on it.
If the argument is not supplied, the buildinfo is derived from the specfile
which is currently in the package.

The returned data is XML and contains a list of the packages used in building, 
their source, and the expanded BuildRequires.
    """
    wd = os.curdir
    package = store_read_package(wd)
    project = store_read_project(wd)

    if args is None or len(args) < 2:
        print 'missing argument'
        print
        print buildinfo.func_doc
        print 'Valid arguments for this package are:'
        print 
        repos(None)
        print
        sys.exit(1)
        
    platform = args[0]
    arch = args[1]

    # were we given a specfile (third argument)?
    try:
        spec = open(args[2]).read()
    except IndexError:
        spec = None
    except IOError, e:
        sys.exit(e)

    print ''.join(get_buildinfo(project, package, platform, arch, specfile=spec))


def buildconfig(args):
    """buildconfig: Shows the build configuration which is used in building a package
This command is mostly used internally by the 'build' command.
It needs to be called inside a package directory.

usage: osc buildconfig <platform> <arch>

The returned data is the project-wide build configuration in a format which is
directly readable by the build script. It contains RPM macros and BuildRequires
expansions, for example.
    """
    wd = os.curdir
    package = store_read_package(wd)
    project = store_read_project(wd)

    if args is None or len(args) < 2:
        print 'missing argument'
        print
        print buildconfig.func_doc
        print 'Valid arguments for this package are:'
        print 
        repos(None)
        print
        sys.exit(1)
        
    platform = args[0]
    arch = args[1]
    print ''.join(get_buildconfig(project, package, platform, arch))


def repos(args):
    """repos: Shows the repositories which are defined for a package

usage: 1. osc repos                   # package = current dir
       2. osc repos <packagedir>
    """
    args = parseargs(args)
    pacs = findpacs(args)

    for p in pacs:

        for platform in get_repos_of_project(p.prjname):
            print platform


def build(args):
    """build: build a package on your local machine
You need to call the command inside a package directory.

usage: 1. osc build <platform> <arch> <specfile> [--clean|--noinit]
       2. BUILD_DIST=... osc build <specfile> [--clean|--noinit]
          where BUILD_DIST equals <platform>-<arch>


You may want to configure sudo with option  NOPASSWD for /usr/bin/build
and set su-wrapper to 'sudo' in .oscrc.

Note: 
Configuration can be overridden by envvars, e.g.  
OSC_SU_WRAPPER overrides the setting of su-wrapper. 
BUILD_DIST or OSC_BUILD_DIST overrides the build target.
BUILD_ROOT or OSC_BUILD_ROOT overrides the build-root.
    """

    import osc.build

    if not os.path.exists('/usr/lib/build/debsort'):
        sys.exit('Error: you need build.rpm with version 2006.6.14 or newer.\nSee http://software.opensuse.org/download/openSUSE:/Tools/')

    builddist = os.getenv('BUILD_DIST')
    if builddist:
        #sys.argv[4] = sys.argv[1]
        hyphen = builddist.rfind('-')
        sys.argv.insert(2, builddist[hyphen+1:])
        sys.argv.insert(2, builddist[:hyphen])
        print sys.argv

    elif args is None or len(args) < 3:
        print 'missing argument'
        print
        print build.func_doc
        print 'Valid arguments are:'
        print 'you have to choose a repo to build on'
        print 'possible repositories are:'
        print 
        (i, o) = os.popen4(['osc', 'repos'])
        i.close()

        for line in o.readlines():
            a = line.split()[1] # arch
            if a == osc.build.hostarch or \
               a in osc.build.can_also_build.get(osc.build.hostarch, []):
                print line.strip()
        sys.exit(1)

    osc.build.main(sys.argv[1:])

        

def buildhistory(args):
    """buildhistory (buildhist): Shows the build history of a package

usage: osc buildhistory <platform> <arch>
    """

    wd = os.curdir
    package = store_read_package(wd)
    project = store_read_project(wd)

    if args is None or len(args) < 2:
        print 'missing argument'
        print
        print buildhistory.func_doc
        print 'Valid arguments for this package are:'
        print 
        repos(None)
        print
        sys.exit(1)
        
    platform = args[0]
    arch = args[1]
    print '\n'.join(get_buildhistory(project, package, platform, arch))


def rebuildpac(args):
    """rebuildpac: Causes a package to be rebuilt

usage: osc rebuildpac <project> <package> [<repo> [<arch>]]

With the optional <repo> and <arch> arguments, the rebuild can be limited
to a certain repository or architecture.

Note that it is normally NOT needed to kick off rebuilds like this, because
they principally happen in a fully automatic way, triggered by source
check-ins. In particular, the order in which packages are built is handled
by the build service.
    """ 

    if args is None or len(args) < 2:
        print 'missing argument'
        print
        print rebuildpac.func_doc
        sys.exit(1)
        

    repo = arch = None
    project = args[0]
    package = args[1]
    if len(args) > 2:
        repo = args[2]
    if len(args) > 3:
        arch = args[3]

    print package + ':', cmd_rebuild(project, package, repo, arch)


def help(args):
    """help: Describe the usage of this program or its subcommands.

usage: osc help [SUBCOMMAND...]
    """
    if args:
        cmd = args[0]
        for i in cmd_dict.keys():
            if cmd in cmd_dict[i]:
                cmd = i
                break

        try:
            print cmd.func_doc

        except AttributeError, KeyError:
            print 'unknown command \'%s\'' % cmd
            sys.exit(1)
    else:
        print usage_general
        lines = []
        for i in cmd_dict.keys():
            line = '    ' + (i.__name__)
            if len(cmd_dict[i]) > 1:
                line += ' (%s)' % ', '.join(cmd_dict[i][1:])
            lines.append(line)
        lines.sort()
        lines.append('')
        print '\n'.join(lines)


# all commands and aliases are defined here
# a function with the respective name is assumed to exist
cmd_dict = {
    add:            ['add'],
    addremove:      ['addremove'],
    build:          ['build'],
    buildconfig:    ['buildconfig'],
    buildinfo:      ['buildinfo'],
    commit:         ['commit', 'ci', 'checkin'],
    checkout:       ['checkout', 'co'],
    updatepacmetafromspec:       ['updatepacmetafromspec'],
    deletepac:      ['deletepac'],
    deleteprj:      ['deleteprj'],
    diff:           ['diff'],
    editmeta:       ['editmeta'],
    editpac:        ['editpac', 'createpac'],
    copypac:        ['copypac'],
    editprj:        ['editprj', 'createprj'],
    help:           ['help'],
    buildhistory:   ['buildhistory', 'buildhist'],
    linkpac:        ['linkpac'],
    usermeta:       ['usermeta'],
    edituser:       ['edituser'],
    init:           ['init'],           # deprecated
    log:            ['log'],
    ls:             ['ls', 'list'],
    meta:           ['meta'],
    platforms:      ['platforms'],
    delete:         ['delete', 'del', 'rm', 'remove'],
    repos:          ['repos'],
    repourls:       ['repourls'],
    resolved:       ['resolved'],
    results:        ['results'],
    prjresults:     ['prjresults'],
    results_meta:   ['results_meta'],
    rebuildpac:     ['rebuildpac'],
    status:         ['status', 'stat', 'st'],
    update:         ['update', 'up'],
}


def main():
    """handling of commandline arguments, and dispatching to subcommands"""

    conf.get_config()

    # which subcommand?
    if len(sys.argv) < 2:
        print "Type 'osc help' for usage."
        sys.exit(0)

    cmd = sys.argv[1]

    # more arguments?
    if len(sys.argv) > 2:
        args = sys.argv[2:]
    else:
        args = None

    for i in cmd_dict.keys():
        if cmd in cmd_dict[i]:
            cmd = i
        
    # run subcommand
    if cmd not in cmd_dict:
        print 'unknown command \'%s\'' % cmd
        print "Type 'osc help' for usage."
        sys.exit(1)
    cmd(args)


if __name__ == '__main__':
    import sys, os.path
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    main()

