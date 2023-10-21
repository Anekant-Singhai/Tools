
############################################################################### UPDATED CODE:
import pandas as pd
import re
import httpx
from tld import get_tld
from chaos_python.client import chaosAPI as chaosapi
import os
os.system("rm -rf results")
os.system("mkdir results")

data = pd.read_csv(input("The csv file: "))
key = input("The Chaos API key please , if not you can get it for free on [https://chaos.projectdiscovery.io/#/]: ")
options = "default"

print("###################### ALL ELIGIBLES  ###################\n")
# Step 1: Extract domains eligible for bounty from the CSV file and save them to a file
eligible_identifiers_url = data[(data['eligible_for_submission'] == True) & (data['asset_type'] == 'URL') & (data['eligible_for_bounty'] == True)]['identifier'].tolist()
eligible_identifiers_other = data[(data['eligible_for_submission'] == True) & (data['asset_type'] == 'OTHER') & (data['eligible_for_bounty'] == True)]['identifier'].tolist()
eligible_identifiers_code = data[(data['eligible_for_submission'] == True) & (data['asset_type'] == 'SOURCE_CODE') & (data['eligible_for_bounty'] == True)]['identifier'].tolist()
eligible_identifiers_smart_contracts = data[(data['eligible_for_submission'] == True) & (data['asset_type'] == 'SMART_CONTRACT') & (data['eligible_for_bounty'] == True)]['identifier'].tolist()

if eligible_identifiers_url:
    with open("./results/eligible_urls.txt", "a") as f:
        for i in eligible_identifiers_url:
            print(i)
            f.write(i + "\n")
else:
    print("No eligible identifiers found.")

if eligible_identifiers_other:
    print("----------[OTHERS]-------------------- ")
    with open("./results/eligible_others.txt", "a") as f:
        for i in eligible_identifiers_other:
            print(i)
            f.write(i + "\n")
if eligible_identifiers_code:
    print("----------[CODE REVIEW]---------------")
    with open("./results/eligible_code.txt", "a") as f:
        for i in eligible_identifiers_code:
            print(i)
            f.write(i + "\n")
if eligible_identifiers_smart_contracts:
    print("--------------[SMART CONTRACTS]------------------------")
    with open("./results/eligible_smart_contracts.txt", "a") as f:
        for i in eligible_identifiers_smart_contracts:
            print(i)
            f.write(i + "\n")
print("############### WILDCARDS #################\n")

data

# Step 2: Separate out the wildcards from the eligible domains and save them to a different file
eligible_identifiers_wildcards = data[(data['eligible_for_submission'] == True) & (data['asset_type'] == 'WILDCARD') & (data['eligible_for_bounty'] == True)]['identifier'].tolist()

if eligible_identifiers_wildcards:
    with open('./results/wildcards.txt', 'a') as f:
        for i in eligible_identifiers_wildcards:
            print(i)
            f.write(i + '\n')
else:
    print("No eligible identifiers found.")

def extract_domain_from_wildcard(domain):
    # Match the last wildcard and extract the domain part after it
    match = re.search(r'(?<=\*)\.[^.]*$', domain)
    if match:
        return match.group(0)[1:]
    else:
        return domain

print("############################### ALL ELIGIBLES: #####################################\n")
# Process wildcards and add them to the eligible URLs list for further checks
# eligible_identifiers1 = [extract_domain_from_wildcard(domain) for domain in eligible_identifiers_wildcards]
# eligible_identifiers_url.extend(eligible_identifiers1)
print(eligible_identifiers_url)
print("####################################################################################\n")

# then we extract the domains from the eligible list:
domains = []
for url in eligible_identifiers_url: #for loop to create iterations
    res = get_tld("https://"+url,as_object=True)
    n = res.fld
    if n not in domains:
      print(n)
      domains.append(n)
print("domain list: \n",domains)

#NOW WE HAVE:
# A domain list-> domains[] , eligible url list, wildcards

# Step 3: Check if the domains are active and save the active domains to a file
import requests
import socket
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_active(url):
    try:
        ip_address = socket.gethostbyname(url)
        print(f"IP address for {url}: {ip_address}")

        code = 0
        code1 = 0
        try:
            if not url.startswith("http://") and not url.startswith("https://"):
                url1 = "http://" + url  # Add 'http://' protocol prefix if missing
                url2 = "https://" + url  # Add 'https://' protocol prefix if missing

                response1 = requests.get(url1, verify=False, timeout=10)
                response2 = requests.get(url2, verify=False, timeout=10)

                if response1.status_code == 200:
                    code = 200
                elif response1.status_code in range(300, 400):
                    response1 = requests.get(url, verify=False, timeout=10, allow_redirects=True)
                    code = 301
                elif response1.status_code == 403:
                    code = 403

                if response2.status_code == 200:
                    code1 = 200
                elif response2.status_code in range(300, 400):
                    response2 = requests.get(url, verify=False, timeout=10, allow_redirects=True)
                    code1 = 301
                elif response2.status_code == 403:
                    code1 = 403

                return (code, code1)

        except requests.exceptions.ReadTimeout as errrt:
            print(f"Time out on domain: {url}")
            return (0,0)

    except socket.gaierror as e:
        print(f"Failed to resolve {url}: {e}")
        return (0, 0)

active_domains = []
status = [200, 403, 301]

with open("./results/active_domains.txt", "a") as f:
    for domain in domains:
        print(f"Checking domain: {domain}")
        x, y = check_active(domain)
        if x in status:
            active_domains.append(domain)
            f.write(f"{domain}\n")

print("###################### Active Domains ############################")
with open("./results/active_domains.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())

# Step 4: Find subdomains for the active domains and save them to a file
subs = []
print("############################################# SUBDOMAINS: #############################\n")
for d in active_domains:
    try:
        subdomains = chaosapi(d, key, options)

        for subdomain in subdomains:
            if re.search(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', subdomain):
                subs.append(subdomain)
            else:
                s = subdomain + "." + d
                subs.append(s)
        print("The subdomains: ",s)
    except KeyError:
        print(f"Error: 'domain' key is missing in the API response for domain: {d}")

# Write the subdomains to the subdomains.txt file
with open("./results/subdomains.txt", "w") as f:
    for subdomain in subs:
        f.write(subdomain + "\n")

# Print the subdomains from the file
with open('./results/subdomains.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())

################################################################3 NOW WE NEED TO SORT THE SUBDOMAINS ITSELF
# NOTE:make sure that they can be from any source

# step 5: then we need to filter the subdomain with some categories:
# categories like: developer , admin , api , payments , auth , login ,
import os

# Remove the existing subdomains_segregated directory and create a new one
os.system("rm -r ./results/subdomains_segregated")
os.system("mkdir ./results/subdomains_segregated")

# Define keywords and their corresponding output file paths
keywords = {
    "api": "./results/subdomains_segregated/api_subdomains.txt",
    "login": "./results/subdomains_segregated/login_subdomains.txt",
    "dev": "./results/subdomains_segregated/developer_subdomains.txt",
    "payment": "./results/subdomains_segregated/payment_subdomains.txt",
    "auth": "./results/subdomains_segregated/auth_subdomains.txt",
    "signup": "./results/subdomains_segregated/signup_subdomains.txt",
    "admin": "./results/subdomains_segregated/admin_subdomains.txt",
    "freelance": "./results/subdomains_segregated/freelance_subdomains.txt",
    "service": "./results/subdomains_segregated/service_subdomains.txt",
    "network": "./results/subdomains_segregated/network_subdomains.txt",
    "contract": "./results/subdomains_segregated/contracts_subdomains.txt",
    "blog":"./results/subdomains_segregated/blog_subdomains.txt",
    "storage":"./results/subdomains_segregated/storage_subdomains.txt",
    "support":"./results/subdomains_segregated/support_subdomains.txt",
    "cloud":"./results/subdomains_segregated/cloud_subdomains.txt",
    "account":"./results/subdomains_segregated/account_subdomains.txt",
    "commerce":"./results/subdomains_segregated/commerce_subdomains.txt",
    "customer":"./results/subdomains_segregated/customer_subdomains.txt",
    "consumer":"./results/subdomains_segregated/consumer_subdomains.txt",
    "sandbox":"./results/subdomains_segregated/sandbox_subdomains.txt",
    "public":"./results/subdomains_segregated/public_subdomains.txt",
    "asset":"./results/subdomains_segregated/asset_subdomains.txt",




    # You can add more keywords and file names here
}

# Read the list of subdomains from the input file
with open("/content/results/subdomains.txt", "r") as f:
    subdomains = f.read().splitlines()

# Iterate through each subdomain
for subdomain in subdomains:
    matched = False
    # Check if the subdomain contains any of the keywords
    for keyword, filename in keywords.items():
        if keyword in subdomain.lower():
            # If a keyword is found in the subdomain, write it to the corresponding output file
            with open(filename, "a") as f:
                f.write(subdomain + "\n")
            matched = True
            break  # Exit the loop once a keyword match is found
    # If no keyword match is found, write the subdomain to the 'other_subdomains.txt' file
    if not matched:
        with open("./results/subdomains_segregated/other_subdomains.txt", "a") as f:
            f.write(subdomain + "\n")

# Print a message indicating completion
print("Subdomains segregation completed")



