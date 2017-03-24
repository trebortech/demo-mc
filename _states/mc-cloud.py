# -*- coding: utf-8 -*-
'''
State Module to run MC Cloud docker commands
'''

from __future__ import absolute_import

__virtualname__ = 'mc-cloud'


def __virtual__():
    return __virtualname__


def cliqrbuild(name, cliqrtagversion, cliqrtarget, cliqrsourceimage='cliqr/worker'):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    # Set values
    cliqrsource = '{0}:{1}'.format(cliqrsourceimage, 'latest')
    cliqrnew = '{0}:{1}'.format(cliqrsourceimage, cliqrtagversion)
    cliqrimagepath = '/root/cliqr_worker_{0}.tar'.format(cliqrtagversion)
    cliqrtargetpath = '{0}:{1}'.format(cliqrtarget, cliqrimagepath)

    # Tag cliqr latest

    __salt__['dockerng.tag'](name=cliqrsource,
                             image=cliqrnew)

    # Export to tar file

    __salt__['dockerng.save'](name=cliqrnew,
                              path=cliqrimagepath,
                              makedirs=True)

    # Copy tar to remote host
    __salt__['rsync.rsync'](src=cliqrimagepath,
                            dst=cliqrtargetpath)

    ret['result'] = 'Cliqr Build Complete'
    ret['changes'] = {'results': 'New tag version created: {0}'.format(cliqrnew)}
    ret['comment'] = 'Image has been created and transferred'

    return ret


def mayobuild(name, cliqrtagversion, mayotagversion, cliqrsourceimage='cliqr/worker'):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    # mayodockerfiledir = 'mayo-cliqr'
    mayodockerfiledir = 'builddir'

    builddir = '/root'
    mayobuilddir = '{0}/{1}'.format(builddir, mayodockerfiledir)

    cliqrimagefile = 'cliqr_worker_{0}.tar'.format(cliqrtagversion)
    mayoimagefile = 'cliqr_worker_{0}.tar'.format(mayotagversion)

    cliqrimport = '{0}:{1}'.format(cliqrsourceimage, cliqrtagversion)
    cliqrstage = '{0}:latest'.format(cliqrsourceimage)

    mayostage = '{0}:{1}'.format(cliqrsourceimage, mayotagversion)

    mayodockerfile = 'cliqr-worker/azurecli-worker/'
    # mayorepo = 'ssh://tfs.mayo.edu:22/tfs/MayoClinic/DCIS/_git/'
    mayorepo = 'https://github.com/trebortech/mc.git/'

    # Clean up work space
    # example /root/mayo-cliqr
    __salt__['file.remove'](mayobuilddir)

    # Remove existing images for Cliqr
    # example cliqr/worker:latest
    __salt__['dockerng.rmi']('{0}:{1}'.format(cliqrsourceimage, 'latest'))

    # Load cliqr image from tar file
    # example /root/cliqr_worker_{0}.tar
    __salt__['dockerng.load']('{0}/{1}'.format(builddir, cliqrimagefile))

    # Tag new cliqr image to latest
    # example cliqr/worker:{0} --> cliqr/worker:latest
    __salt__['dockerng.tag'](name=cliqrimport,
                             image=cliqrstage)

    # Pull down Mayo-Cliqr docker file
    # example
    # ---> clone from ssh://tfs.mayo.edu:22/tfs/MayoClinic/DCIS/_git/mayo-cliqr
    # ---> clone to /root
    __salt__['git.clone'](name=builddir,
                          url='{0}/{1}'.format(mayorepo, mayodockerfiledir))

    # Build new image with docker file
    # example build
    # ---> Source /root/mayo-cliqr/cliqr-worker/azurecli-worker/
    # ---> New cliqr/worker:(mayotagversion)
    __salt__['dockerng.build'](path='{0}/{1}/{2}'.format(builddir, mayodockerfiledir, mayodockerfile),
                               image=mayostage,
                               cache=False)

    # Export Mayo-Cliqr docker image
    # example
    # ---> Export cliqr/worker:(mayotagversion)
    # ---> Path /root/cliqr_worker_{mayotagversion}.tar
    __salt__['dockerng.save'](name=mayostage,
                              path='{0}/{1}'.format(builddir, mayoimagefile),
                              makedirs=True)

    # Create md5 has file of tar file
    filehash = __salt__['hashutil.md5_digest']('{0}/{1}'.format(builddir, mayoimagefile))
    __salt__['file.write'](path='{0}/{1}.md5'.format(builddir, mayoimagefile),
                           filehash)

    ret['result'] = 'Cliqr Build Complete'
    ret['changes'] = {'results': 'New tag version created: {0}'.format(cliqrnew)}
    ret['comment'] = 'Image has been created and transferred'

    return ret