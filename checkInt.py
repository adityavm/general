#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, requests, time

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

url = "http://192.168.1.1/status/status_deviceinfo.htm"

r = requests.get(url, auth=("admin", "password"))
output = "adsl status:\nconnected" in remove_html_tags(r.text.lower())
if output:
	print("✓")
else:
	print("×")
