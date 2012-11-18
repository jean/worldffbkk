Calendar for 10th World Film Festival of Bangkok
=================================================

The schedule is available online, but only as HTML pages or as a PDF with no
extractable text. 

In the hope that this may encourage organizers to provide one, and encourage
more people to ask for online calendars for events like this, I 
quickly knocked together a `public Google Calendar for the WFFBKK`_. It can
use improvement: I could have parsed more information out of the HTML pages,
and I need to figure out how to relate multiple screenings of the same
movie.

I used the icalendar_ module to write the calendar file, and tried out
wwwclient_ for the first time as scraping library. Both worked fine, 
though icalendar_ is a bit rough'n'ready.  The resulting ``movies.ics``
required a few manual tweaks before Google would accept it, which I
performed in Vim::

    "Get rid of stray newlines
    :%s?^M??
    "Get rid of blank lines
    :g/^$/d
    "Descriptions have embedded newlines that mess up icalendar's indenting
    :g/^\S[^:]\+$/s?.*? &?

I also needed to include a definition for the Asia/Bangkok timezone, 
which I grabbed from a Google Calendar ICS export::

    BEGIN:VTIMEZONE
    TZID:Asia/Bangkok
    X-LIC-LOCATION:Asia/Bangkok
    BEGIN:STANDARD
    TZOFFSETFROM:+0700
    TZOFFSETTO:+0700
    TZNAME:ICT
    DTSTART:19700101T000000
    END:STANDARD
    END:VTIMEZONE

The validator at http://icalvalid.cloudapp.net/ was very useful.

The information is straight from the festival website at:
http://www.worldfilmbkk.com/theprograms_sections.php?showdate=17.11.12

It was scraped on 2012-11-17, and will not reflect any subsequent updates.

Dependencies
------------

- icalendar_
- wwwclient_

.. _icalendar: http://pypi.python.org/pypi/icalendar
.. _wwwclient: https://github.com/sebastien/wwwclient
.. _ipython:   http://ipython.org/
.. _public Google Calendar for the WFFBKK: https://www.google.com/calendar/embed?src=n52vt7674mp96g660t9sacmul8%40group.calendar.google.com&ctz=Asia/Bangkok
