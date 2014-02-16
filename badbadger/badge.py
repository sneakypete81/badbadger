import urllib
import urllib2

URL_BASE = "http://img.shields.io/badge/"

def open_badge(subject, status, colour, extension):
    """Download a badge image from img.shields.io"""
    url = URL_BASE + urllib.quote("%s-%s-%s.%s" %
                                  (subject, status, colour, extension))
    return urllib2.urlopen(url)
