#!/usr/bin/env python3

import tarfile
from re import match
from os import system
from json import loads
from shutil import move
from requests import get

response = get(
    "https://api.github.com/repos/graalvm/graalvm-ce-builds/releases/latest"
)

assets = loads(response.content)['assets']

version = "java11"
os = "linux"
arch = "amd64"

regular_exp = "graalvm-ce-" + version + "-" + os + "-" + arch + "-.*.tar.gz"

url = list(filter(
    lambda x: match(regular_exp, x['name']),
    assets
))[0]["browser_download_url"]

path = url.split('/')[-1]

print("Downloading ", path, "...")
graalvm_file = get(url)

with open('/tmp/' + path,'wb') as f:
    f.write(graalvm_file.content)

dir_name = ""
print("Extracting...")
with tarfile.open('/tmp/' + path) as tar:
    dir_name = tar.firstmember.name.split('/')[0]
    tar.extractall('/tmp/')

print("Installing...")
move('/tmp/' + dir_name, '/usr/lib/jvm/graalvm/')

system("alternatives --install /usr/bin/java java /usr/lib/jvm/graalvm/bin/java 1")
system("alternatives --set java /usr/lib/jvm/graalvm/bin/java")

print("Done!")
