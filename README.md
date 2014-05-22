=====================
Python LDS Scriptures
=====================

[![Build Status](https://travis-ci.org/LDSMobileApps/python-lds-scriptures.svg?branch=master)](https://travis-ci.org/LDSMobileApps/python-lds-scriptures)

python-lds-scriptures parses LDS scripture URIs and formats them
as human-readable strings.

Typical usage looks like this::

    >>> import scriptures
    >>> ref = scriptures.ref('/scriptures/bofm/mosiah/2.17')
    >>> ref
    ScriptureRef("/scriptures/bofm/mosiah/2.17")
    >>> unicode(ref)
    u'Mosiah 2:17'

Create references from their parts::

    >>> scriptures.ScriptureRef(testament='dc-testament', book='dc', chapter=46, verse_ranges=[(11, 12), (15, 15)])
    ScriptureRef("/scriptures/dc-testament/dc/46.11-12,15")

Sort references::

    >>> sorted([scriptures.ref('/scriptures/bofm/mosiah/2.17'), scriptures.ref('/scriptures/ot/isa/48.10')])
    [ScriptureRef("/scriptures/ot/isa/48.10"), ScriptureRef("/scriptures/bofm/mosiah/2.17")]

Merge references::

    >>> scriptures.merged([scriptures.ref('/scriptures/bofm/2-ne/2.25'), scriptures.ref('/scriptures/bofm/2-ne/2.1-2')])
    [ScriptureRef("/scriptures/bofm/2-ne/2.1-2,25")]
    
Manipulate references::

    >>> ref = scriptures.ref('/scriptures/bofm/2-ne/2.25')
    >>> ref.chapter = None
    >>> ref.verse_ranges = None
    >>> ref
    ScriptureRef("/scriptures/bofm/2-ne")
    
Query references::

    >>> scriptures.ref('/scriptures/ot/ruth').chapters()
    [1, 2, 3, 4]
    >>> scriptures.ref('/scriptures/nt/2-cor/12').verses()
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    >>> scriptures.ref('/scriptures/dc-testament/dc/46.11-12,15').verses()
    [11, 12, 15]
