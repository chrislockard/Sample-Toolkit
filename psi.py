#!/usr/bin/env python3
# psi.py - Parse Site Inputs - Enumerate inputs in web applications.
# Requires Python3! and beautifulsoup4 - sudo pip3 install beautifulsoup4

import sys
import csv
import argparse
import urllib.request
import requests
from bs4 import BeautifulSoup

http_verbs = [
    'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE',
    'PROPFIND', 'CONNECT', 'TEST', 'LOCK', 'MKCOL', 'ACL',
    'BASELINE-CONTROL', 'BIND', 'CHECKIN', 'CHECKOUT', 'COPY', 'LABEL',
    'LINK', 'MERGE', 'MKACTIVITY', 'MKCALENDAR', 'MKCOL', 'MKDIRECTREF',
    'MKWORKPSACE', 'MOVE', 'ORDERPATCH', 'PATCH', 'PROPATCH', 'REBIND',
    'REPORT', 'SEARCH', 'UNBIND', 'UNCHECKOUT', 'UNLINK', 'UPDATE',
    'UPATEDDIRECTREF', 'VERSION-CONTROL', 'PHONYHTTPMETHOD'
]


class PsiTarget:
    '''Class to parse urllib.request objects for application inputs.'''
    def __init__(self):
        '''Create a PsiTarget'''
        self.url = ""

    # Connect to target URL
    def connect(self, url, method, data=""):
        '''Connect to target URL and return a response object'''
        try:
            if method == "GET":
                request = urllib.request.Request(
                    str(url),
                    data=data.encode(encoding='UTF-8'),
                    method="GET")
                return urllib.request.urlopen(request)
            elif method == "POST":
                request = urllib.request.Request(
                    str(url),
                    method="POST")
                return urllib.request.urlopen(request)
            elif method == "HEAD":
                request = urllib.request.Request(
                    str(url),
                    method="HEAD")
                return urllib.request.urlopen(request)
            else:
                print("Error: only HEAD, GET, and POST are supported.")
        except Exception as err:
            print("There was a problem completing your request:", err)

    # Response header parser
    def parse_headers(self, response):
        '''Parse HTTP headers from HTTP response.'''
        return response.getheaders()

    # Cookie parser
    def parse_cookies(self, response):
        '''Identify Cookies set in the HTTP response.'''
        cookies = []
        for header in response.getheaders():
            if 'Set-Cookie' in header:
                cookies.append(header[1])
        return cookies

    # HTML Parser
    def parse_html(self, response):
        '''Parse HTML forms and iFrames from an HTTP response.'''
        html_inputs = []

        try:
            soup = BeautifulSoup(response, "html.parser")
            for formtag in soup.findAll('form'):
                html_inputs.append(formtag)
            for inputtag in soup.findAll('input'):
                html_inputs.append(inputtag)
            for textarea in soup.findAll('textarea'):
                html_inputs.append(textarea)
            for button in soup.findAll('button'):
                html_inputs.append(button)
            for iframe in soup.findAll('iframe'):
                html_inputs.append(iframe)
        except Exception as err:
            print("Error parsing HTML: is BeautifulSoup installed? \
                (hint: sudo pip3 install BeautifulSoup4)")
            print(err)

        return html_inputs

    # Comments parser
    def parse_comments(self, response):
        '''Parse HTML for comments.'''
        html_comments = []

        try:
            soup = BeautifulSoup(response, "html.parser")
            comments = soup.findAll(text=lambda text:
                                    isinstance(text, Comment))
            html_comments.append([comment.extract() for comment in comments])
            return html_comments
        except Exception as err:
            print("Error parsing HTML comments: is BeautifulSoup installed?\
             (hint: sudo pip3 install BeautifulSoup4)")
            print(err)


def main():
    # Option parsing
    parser = argparse.ArgumentParser(description="Find web application inputs.")
    parser.add_argument("target",
                        help="URL of the application to parse for inputs")
    parser.add_argument("-v",
                        help="Print script results to screen",
                        action="store_true")
    parser.add_argument("-o",
                        "--output",
                        help="Specify output filename (currently only CSV\
                         is permitted)")
    parser.add_argument("-m",
                        "--method",
                        help="Specify HTTP Method (defaults to GET)",
                        default="GET")
    parser.add_argument("-M",
                        "--method_check",
                        help="Perform a quick HTTP method check",
                        default=False,
                        action='store_true')
    parser.add_argument("-d",
                        "--data",
                        help="Specify data to pass in HTTP POST",
                        default="")

    args = parser.parse_args()
    url = args.target
    output = args.output
    method_check = args.method_check

    # Test whether target web server supports http_verbs
    if method_check:
        for verb in http_verbs:
            req = requests.request(verb, url, verify=False)
            print(verb, req.status_code, req.reason)
        sys.exit()

    try:
        target = PsiTarget()
        response = target.connect(url, args.method, args.data)
        headers = target.parse_headers(response)
        cookies = target.parse_cookies(response)
        html_inputs = target.parse_html(response)
        html_comments = target.parse_comments(response)

        if args.v:
            # Print status messages here
            if headers:
                print("Headers:")
                for header in headers:
                    print("\t{}: {}".format(header[0], header[1]))
            if cookies:
                print("Cookies:")
                for cookie in cookies:
                    print("\t{}".format(cookie))
            if html_inputs:
                print("HTML Forms:")
                for html_input in html_inputs:
                    print("\t{}".format(html_input))
            if html_comments:
                print("HTML Comments:")
                for html_comment in html_comments:
                    print("\t{}".format(html_comment))

        # Print to file
        if output is not None:
            with open(output, 'w', newline='\n') as csvfile:
                method_writer = csv.writer(csvfile)
                method_writer.writerow(["HTTP Method:"] + [args.method])

                header_writer = csv.writer(csvfile)
                for item in range(len(headers)):
                    header_writer.writerow([headers[item][0]] + [headers[item][1]])
                cookie_writer = csv.writer(csvfile)
                for item in range(len(cookies)):
                    cookie_writer.writerow(['Cookie'] + [cookies[item]])
                html_input_writer = csv.writer(csvfile)
                for item in range(len(html_inputs)):
                    html_input_writer.writerow([html_inputs[item]])
                comment_writer = csv.writer(csvfile)
                for item in range(len(html_comments)):
                    comment_writer.writerow([html_comments[item]])

    except Exception as err:
        print("Application Error", err)


if __name__ == '__main__':
    main()
