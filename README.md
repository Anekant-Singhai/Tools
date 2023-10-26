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
