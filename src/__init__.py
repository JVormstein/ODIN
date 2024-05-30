#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 :::====   :::====   :::  :::= ===
 :::  ===  :::  ===  :::  :::=====
 ===  ===  ===  ===  ===  ========
 ===  ===  ===  ===  ===  === ====
  ======   =======   ===  ===  ===

Developer:   Chris "cmaddy" Maddalena
Version:     3.0.0 "Huginn"
Description: Observation, Detection, and Investigation of Networks
             ODIN was designed to assist with OSINT automation for penetration testing clients and
             their networks, both the types with IP address and social. Provide a client's name and
             some domains to gather information from sources like RDAP, DNS, Shodan, and
             so much more.

             ODIN is made possible through the help, input, and work provided by others. Therefore,
             this project is entirely open source and available to all to use/modify.
"""

VERSION = "3.0.0"
CODENAME = "HUGINN"

import argparse
import odin.utils

def main_cli():
    
    parser = argparse.ArgumentParser(
                    prog='ODIN',
                    description=    """Observation, Detection, and Investigation of Networks""",
                    add_help=True,
            )
    
    parser.add_argument("osint", help="Run the full OSINT suite of tools will be run (see README).")
    parser.add_argument('-o','--organization',help='The target client, such as "ABC Company," to use for \
report titles and searches for domains and cloud storage buckets.',required=True)
    parser.add_argument('-d','--domain',help="The target's primary domain, such as example.com. Use \
whatever the target uses for email and their main website. Provide additional domains in a scope \
file using --scope-file.",required=True)
    parser.add_argument('-sf','--scope-file',type=utils.check_file(),help="A text file containing additional domain names you want to include. IP \
addresses can also be provided, if necessary. List each one on a new line.",required=False)
    parser.add_argument('--whoxy-limit',default=10,help="The maximum number of domains discovered via \
reverse WHOIS that ODIN will resolve and use when searching services like Censys and Shodan. \
You may get hundreds of results from reverse WHOIS, so this is intended to save time and \
API credits. Default is 10 domains and setting it above maybe 20 or 30 is not recommended. \
It is preferable to perform a search using a tool like Vincent Yiu's DomLink and then provide \
the newly discovered domains in your scope file with --scope-file.")
    parser.add_argument('--typo',is_flag=True,help="Generate a list of lookalike domain names for the \
provided domain (--domain), check if they have been registered, and then check those domains \
against URLVoid and Cymon.io to see if the domains or associated IP addresses have been \
flagged as malicious.")
    
    # File searching arguments
    parser.add_argument_group("File Search")
    parser.add_argument('--files',is_flag=True,help="Use this option to use Google to search for files \
under the provided domain (--domain), download files, and extract metadata.")
    parser.add_argument('-e','--ext',default="all",help="File extensions to look for with --file. \
Default is 'all' or you can pick from key, pdf, doc, docx, xls, xlsx, and ppt.")

    # Cloud-related arguments
    parser.add_argument_group("Cloud Search")
    parser.add_argument('-w','--aws',help="A list of additional keywords to be used when searching for \
cloud sotrage buckets.",type=click.Path(exists=True,readable=True,resolve_path=True))
    parser.add_argument('-wf','--aws-fixes',help="A list of strings to be added to the start and end of \
the cloud storage bucket names.",type=click.Path(exists=True,readable=True,resolve_path=True))

    # Reporting-related arguments
    parser.add_argument_group("Reporting")
    parser.add_argument('--html',is_flag=True,help="Create an HTML report at the end for easy browsing.")
    parser.add_argument('--graph',is_flag=True,help="Create a Neo4j graph database from the completed \
SQLite3 database.")
    parser.add_argument('--nuke',is_flag=True,help="Clear the Neo4j project before converting the \
database. This is only used with --graph.")
    parser.add_argument('--screenshots',is_flag=True,help="Attempt to take screenshots of discovered \
web services.")
    parser.add_argument('--unsafe',is_flag=True,help="Adding this flag will spawn the headless Chrome \
browser with the --no-sandbox command line flag. This is NOT recommended for any users who are \
NOT running ODIN on a Kali Linux VM as root. Chrome will not run as the root user on Kali \
without this option.")

    args = parser.parse_args()

    if args.scope_file:
        utlis.check_file(args.scope_file)
    if args.aws:
        utils.check_file(args.aws)
    if args.aws_fixes:
        utils.check_file(args.aws_fixes)