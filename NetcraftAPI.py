"""
This is the (unofficial) Python API for netcraft.com Website.
Using this code, you can retrieve subdomains

"""
import requests
import re
from bs4 import BeautifulSoup
import hashlib
import urllib
import math


class NetcraftAPI(object):

    """
        NetcraftAPI Main Handler
    """

    _instance = None
    _verbose = False

    def __init__(self, arg=None):
        pass

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(NetcraftAPI, cls).__new__(
                cls, *args, **kwargs)
            if (args and args[0] and args[0]['verbose']):
                cls._verbose = True
        return cls._instance

    def display_message(self, s):
        if (self._verbose):
            print '[verbose] %s' % s

    def search(self, domain):
        res = []

        url = "http://searchdns.netcraft.com/?restriction=site+contains&host=*.%s&lookup=wait..&position=limited" % domain
        s = requests.session()
        req = s.get(url)
        soup = BeautifulSoup(req.content)

        pattern = 'Found (\d+) site'
        number_results = re.findall(pattern, req.content)

        if (len(number_results) > 0 and number_results[0] != '0'):
            number_results = int(number_results[0])
            self.display_message("Found %s results" % number_results)
            number_pages = int(math.ceil(number_results / 20)) + 1

            pattern = 'rel="nofollow">([a-z\.\-A-Z0-9]+)<FONT COLOR="#ff0000">'
            subdomains = re.findall(pattern, req.content)
            res.extend(subdomains)
            last_result = subdomains[-1]

            for index_page in xrange(1, number_pages):
                url = "http://searchdns.netcraft.com/?host=*.%s&last=%s.%s&from=%s&restriction=site contains&position=limited" % (domain, last_result, domain, (index_page * 20 + 1))
                req = s.get(url)
                pattern = 'rel="nofollow">([a-z\-\.A-Z0-9]+)<FONT COLOR="#ff0000">'
                subdomains = re.findall(pattern, req.content)
                res.extend(subdomains)
                for subdomain in subdomains:
                    self.display_message('[!] Found: %s ' % subdomain)
                last_result = subdomains[-1]
            return res
        else:
            self.display_message("No results found for %s" % domain)
            return res