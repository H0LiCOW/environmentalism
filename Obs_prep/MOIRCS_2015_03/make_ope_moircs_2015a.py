"""
Python code for making the science target observation section of the
OPE file for a MOIRCS observation
"""

import numpy as n


#---------------------------------------------------------------------------

def init_moircs():
    """
    Sets up variables for other functions
    """

    dith_angle = n.array([10,25,-5])
    dith_step  = n.array([24,29,27])
    tel_offset = n.array([45.,-90.,45.])

    return dith_angle,dith_step,tel_offset

#---------------------------------------------------------------------------

def write_getobs(objname, filtname, texp, ncoadd, ndither, ntimes, 
                 dithcent=False, filtchange=False, firstobs=False):
    """
    Generic code for writing the getobs lines for a given object
    """

    """ Initialize """
    dith_angle,dith_step,tel_offset = init_moircs()

    """ 
    If this is the first observation on a target, then do a setupfield
    and checkfield.
    """
    if firstobs:
        print ''
        print '###############################################################'
        print '#'
        print '# New Object: %s' % objname.upper()
        print '#'
        print '###############################################################'
        print ''
        print '# Move to %s, set filter to %s, and do a field check' % \
            (objname.upper(),filtname.upper())
        print 'SETUPFIELD $DEF_IMG $DEF_IM%s $%s AUTOGUIDE=NO' % \
            (filtname.upper(),objname.upper())
        print 'CHECKFIELD $DEF_IMG EXPTIME=15 NDUMMYREAD=0 SKYSUB=YES'

    """ Add in a filter change command if requested """
    if filtchange:
        print ''
        print '# Change filter to %s' % filtname.upper()
        print 'SETUPOBE $DEF_IMG $DEF_IM%s' % (filtname.upper())

    """ Loop over the number of dither patterns """
    print ''
    print '# Observations of %s in %s band' % (objname.upper(),filtname.upper())
    for i in range(ntimes):
        print 'TELOFFSET $DEF_TOOL DX=0.0 DY=%.1f AUTOGUIDE=NO' % tel_offset[i]
        str1 = 'GETOBJECT  $DEF_IMG EXPTIME=%.1f NDUMMYREAD=2 COADDS=%d' % \
            (texp,ncoadd)
        if dithcent:
            str2 = 'DITHNUM=%d DITHCENTER=YES DITHLENGTH=%.1f DITHANGLE=%.1f' % \
                (ndither,dith_step[i],dith_angle[i])
        else:
            str2 = 'DITHNUM=%d DITHCENTER=NO DITHLENGTH=%.1f DITHANGLE=%.1f' % \
                (ndither,dith_step[i],dith_angle[i])
        str3 = 'AUTOGUIDE=NO'
        print '%s %s %s' % (str1,str2,str3)

#---------------------------------------------------------------------------

def make_j(objname, filtchange=True, firstobs=False, texp=120., ncoadd=1,
           ndither=8, ntimes=2, dithcent=False):
    """
    Prints a series of OPE commands for the J-band observations through
    a call to the more generic write_getobs function
    """

    write_getobs(objname,'J',texp,ncoadd,ndither,ntimes,dithcent=dithcent, 
                 filtchange=filtchange,firstobs=firstobs)

#---------------------------------------------------------------------------

def make_h(objname, filtchange=True, firstobs=False, texp=30., ncoadd=4,
           ndither=8, ntimes=3, dithcent=False):
    """
    Prints a series of OPE commands for the H-band observations through
    a call to the more generic write_getobs function
    """

    write_getobs(objname,'H',texp,ncoadd,ndither,ntimes,dithcent=dithcent, 
                 filtchange=filtchange,firstobs=firstobs)

#---------------------------------------------------------------------------

def make_ks(objname, filtchange=True, firstobs=False, texp=50., ncoadd=3,
            ndither=5, ntimes=2, dithcent=False):
    """
    Prints a series of OPE commands for the Ks-band observations through
    a call to the more generic write_getobs function
    """

    write_getobs(objname,'KS',texp,ncoadd,ndither,ntimes,dithcent=dithcent, 
                 filtchange=filtchange,firstobs=firstobs)

#---------------------------------------------------------------------------

def make_std(objname='FS27', filts=['KS','J','H'], texp=22., ndith=3,
             stddith=70.):
    """
    Prints as series of OPE commands that can be used to observe the
    standard star
    """

    """ Initialize """
    dith_angle,dith_step,tel_offset = init_moircs()

    """ Start by moving to the standard star """
    print ''
    print '###############################################################'
    print '#'
    print '# New Object: %s (Standard Star)' % objname.upper()
    print '#'
    print '###############################################################'
    print ''
    print '# Move to %s, set filter to %s, then move the star to the'  % \
        (objname.upper(),filts[0])
    print '# center of chip 2 and do a field check'
    print 'SETUPFIELD $DEF_IMG $DEF_IM%s $%s AUTOGUIDE=NO' % \
        (filts[0],objname.upper())
    print 'TELOFFSET  $DEF_TOOL DX=91.0 DY=3.8 AUTOGUIDE=NO'
    print 'CHECKFIELD $DEF_IMG EXPTIME=15 NDUMMYREAD=0 SKYSUB=YES'

    """ 
    Do two dither patterns in each filter, with one dither pattern per chip
    """
    move_sign = n.array([-1., 1., -1.])
    for i in range(len(filts)):
        print ''
        print '# Do %d-point dithers in %s on each chip' % (ndith,filts[i])

        """ Change filter, except for the first loop """
        print 'SETUPOBE $DEF_IMG $DEF_IM%s' % (filts[i].upper())

        """ Do the dither pattern on the first chip"""
        str1 = 'GETOBJECT $DEF_IMG EXPTIME=%.1f NDUMMYREAD=2 DITHNUM=%d' % \
            (texp,ndith)
        str2 = 'DITHCENTER=NO DITHLENGTH=%.1f DITHANGLE=%.1f' % \
            (stddith,dith_angle[i])
        str3 = 'DATTYPE=STANDARD_STAR'
        print '%s %s %s' % (str1,str2,str3)

        """ Move to the second chip """
        dx = 178.2 * move_sign[i]
        dy = 1.4 * move_sign[i]
        print 'TELOFFSET $DEF_TOOL DX=%.1f DY=%.1f AUTOGUIDE=NO' % (dx,dy)
        print '%s %s %s' % (str1,str2,str3)
