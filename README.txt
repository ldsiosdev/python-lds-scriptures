=====================
Python LDS Scriptures
=====================

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
