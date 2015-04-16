#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re


def parse_title(title):
    """
    The titles getting posted to YouTube are generall of the pattern:
    Name, Name - Title - PyCon 2015
    Keynote - Name - PyCon 2015
    Opening Statements - Name - PyCon 2015
    """
    title = title.replace(' - PyCon 2015', '')
    if re.match(r'Keynote|Open', title):
        return title
    chunks = title.split(' - ')[0:2]
    if len(chunks) > 1:
        return chunks[1]
    return title

def parse_speakers(speakers):
    return [s.strip() for s in speakers.split(',') if s.strip()]

def parse_speakers_and_description(description):
    """
    strip speaker and slids
    The descriptions seem to start with

    "Speaker: ....\n\n

        and end with

    \n\nSlides can be found at: https://speakerdeck.com/pycon2015 and https://github.com/PyCon/2015-slides"
    """
    p = re.compile(r'"Speakers?: (?P<speakers>[^\n]+)\n\n(?P<description>.*)Slides can be found', re.DOTALL)
    m = p.match(description)
    if m:
        return m.groupdict()
    else:
        return {'speakers': '', 'description': description}

