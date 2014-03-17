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