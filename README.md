# Recon/bug_bounty_recon_hackerone.py

## What It Does
Tired of figuring out what's eligible, which subdomains to tackle, or how to conduct recon? Look no further! This script takes a CSV file from your HackerOne profile and performs the following tasks:

- Extracts the list of eligible for bounty items and sorts them by URL, application, and more.
- Performs a domain scan, providing the status of whether the domain is up or not using a custom HTTPX tool.
- Submits active domains to a subdomain finder, categorizing subdomains by their function, such as API subdomains, auth subdomains, developer subdomains, and more.

**Note:** It requires a Chaos API key, which is free to obtain.

## How to Use
Simply run the script, and it will prompt you for two inputs:
1. Chaos API key
2. A CSV file from your HackerOne scope

Sit back and relax!


---
# Link Snagger {Link Extractor}
## What It Does
Link Snagger is your go-to tool for extracting all the links present on a webpage. Say goodbye to the hassle of figuring out which button or element is clickable to access another page. This tool does the heavy lifting for you, making link extraction quick and easy.
- find the relevant links embedded hidden in plain sight
- get the js files which were used
## Where to use
When you need to find out the broken links which are now not being used
as well as in the CTF scenarios which have many front-end functionalities and can't figure out what can be the links useful to visit to

---
# cookie_stealer.py

## What It Does
As the name suggests, it steals cookies from visitors who click on the link.

## Where to Use
CTFs (Capture The Flag challenges) and wherever your imagination takes you! 😉

---

# Fast-Recon.py

## What It Does
This script uses a TCP-connect scan to identify all the open ports for a target. It's blazing fast, accurate, and even grabs banners!

---

# python_script_to_extract_urls_from_pcap_files.py

## What It Does
Feed this script a pcap file, and it will extract all the URLs this baby visited.

---

# append_words.py

## What It Does
This code appends your desired word to your wordlist at your specified position. Just change the number mentioned in the code's comments. It's useful in brute-forcing scenarios where the server blocks attacks after a certain number of consecutive invalid login attempts. This script lets you add valid login credentials to your wordlist in between entries, helping you avoid being blocked.

## Where to Use
When there's a rate limit for a certain number of incorrect login attempts and it's reset by a correct login, you can bypass it by creating a wordlist with correct login credentials.

---
						
						
						
# 								DELVE

*Your own customized CLI bro-wser*

### NECESSITY {WHY}

- There are numerous tools that bombard the requests on a target page with no or less control

- Needed a tool that can give the full control in the hands of the user

### {WHAT}
- User can control:
	+ The request methods:
		* GET , POST , PUT , OPTIONS , HEAD , DELETE
		
	+ Frequency and total count of requests

### Usage {HOW}

```
usage: delve.py [-h] -u URL [-m METHOD] [-H HEADERS] [-d DATA]
                [-t NUM_THREADS] [-rps REQUESTS_PER_SECOND]
                [-tr TOTAL_REQUESTS] [-o OUTPUT_FILE]

HTTP Request Sender Tool

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Target URL
  -m METHOD, --method METHOD
                        HTTP method (GET, POST, PUT, DELETE, OPTIONS)
  -H HEADERS, --headers HEADERS
                        Headers in JSON format
  -d DATA, --data DATA  Data in JSON format for POST and PUT requests
  -t NUM_THREADS, --num-threads NUM_THREADS
                        Number of threads
  -rps REQUESTS_PER_SECOND, --requests-per-second REQUESTS_PER_SECOND
                        Requests per second
  -tr TOTAL_REQUESTS, --total-requests TOTAL_REQUESTS
                        Total number of requests across all threads
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        File to write the output to

```

It generates the output into a file not on a terminal 

- GET

```
delve -u http://localhost:8080/WebGoat/login -m GET -tr 150 -t 3 -rps 2
```
Multiple threads can be used for multiple requests too

- POST

```
delve -u http://localhost:8080/WebGoat/login -m POST -d '{"username":"webgoat","password":"webgoat"}' -tr 1
```

PS:remeber to give the data in single quotes in json format

- OPTIONS

```
delve -u <url> -m OPTIONS -tr 1
```

- PUT 

```
delve -u http://localhost:8080/WebGoat/login -m PUT -d '{"data":"value"}' -tr 1
```

- HEAD

```
delve -u <url> -m HEAD -tr 1
```

---

# Data Exfiltration Using ICMP!!
Requires ROOT!!
Yes we can exfiltrate the data using ICMP protocol. Here's how :
Usage:
```
python3 exfiltrator.py
```

It will ask for the Sending and Receiving bits:
## Sending
choose `s` option and it will ask for the file to send , just give the filename with path.

## Receiving
choose `r` option and it will save the file to `out.txt`, though you can change it anyways.

## Why:
As the firewalls can block various traffics and ports and protocols , who'll suspect the innocent ICMP

#  Remote Command execution using ICMP!!!

DOES `NOT` REQUIRE ROOT!!!
Yes we can also execute commands using ICMP , Here's how:
There are 2 files: 
1. Listener
2. Executer
## Executer:
Usage:
```
python3 icmp_executer.py
```
It will prompt for :
- IP : Give the victim's IP
- Port : Just leave blank {I was drunk that day!!} 
- Command : You know what to do here...
- TTL : Just leave blank if don't know what to do
- ID : It is important to give `12321` as ID or it won't execute {consider as secret key!!}
PS: you can change the ID as you need in code.

## Listener:
Usage:
```
python3 icmp_listener.py
```
It will prompt for interface to listen to ... just give which one you're attacker is connected to.
and watch.

## Why:
As the firewalls can block various traffics and ports and protocols , who'll suspect the innocent ICMP

