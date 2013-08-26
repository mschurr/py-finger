"""
    Python Network Finger Utility
    @author Matthew Schurr <mschurr@rice.edu>

    You can use this program to retrieve information about students/faculty at Rice using a search query.

    The search returns a list of dictionaries structured similar to the examples below (note that more than one result can be returned).
    A search with no results returns an empty list.

    Example Usage:
        from finger import finger;

        res = finger("mas20"); # Search by NetID

        [{
                "mailto": "mailto:mschurr@rice.edu",
                "major": "Computer Science",
                "name": "Schurr, Matthew Alexander",
                "email": "@rice.edu",
                "college": "Duncan College",
                "matric_term": "Fall 2012",
                "address": "Duncan College MS-715, 1601 Rice Blvd, , TX 77005-4401",
                "class": "sophomore student"
            }]

        res = finger("Devika"); # Search by Name

        [{
                "mailto": "mailto:devika@rice.edu",
                "name": "Subramanian, Dr Devika",
                "office": "3094 Duncan Hall",
                "title": "Professor; Professor, ECE",
                "mailstop": "Computer Science MS132",
                "email": "@rice.edu",
                "phone": "713-348-5661",
                "department": "Computer Science",
                "homepage": "http://www.cs.rice.edu/~devika/",
                "class": "faculty"
            }]
"""

from socket import *
from sys import argv

__author__ = "Matthew Schurr <mschurr@rice.edu>"

def finger(opt):
    """ Searches a FINGER server (assumes rice.edu) (see http://tools.ietf.org/html/rfc1288) for information related to a search query. Returns a list of dictionaries. 
        Example Usage: res = finger("user@domain.tld")
    """
    if "@" in opt:
        query = opt[:opt.index("@")]
        domain = opt[opt.index("@")+1:]
    else:
        query = opt
        domain = "rice.edu"

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((domain, 79))
    s.send(query + "\r\n")
    res = "";
    while 1:
        buf = s.recv(1024)
        res += buf;
        if not buf:
            break

    json = [];

    if "0 RESULTS:" in res:
        return [];

    segments = res.split("------------------------------------------------------------")

    for seg in segments:
        if "name:" not in seg:
            continue;

        record = {};
        lines = seg.split("\n");

        for line in lines:
            if ":" not in line:
                continue;

            idx = line.find(":");
            key = line[:idx].strip(" ").replace(" ","_");
            val = line[idx+1:].strip(" ");
            record[key] = val;

        json.append(record);

    return json;

if __name__ == '__main__':
    if len(argv) < 2:
        print "Python Network Finger by Matthew Schurr <mschurr@rice.edu> - Proper Usage: python finger.py user[@domain]"
    else:
        print finger(argv[1])