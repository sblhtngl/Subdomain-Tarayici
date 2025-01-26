import requests

from bs4 import BeautifulSoup

import socket

import json

 

#found_subdomains = set()

 

def get_links(url):

    try:

        response = requests.get(url)

 

        if response.status_code == 200:

            soup = BeautifulSoup(response.text,'html.parser')

            links = soup.find_all('a',href=True)

            link_array = [link['href'] for link in links]

            return link_array

    except Exception as e:

        print(f"Domain is not active: {e}")

 

def check_subdomains(domain, subdomain):

    full_subdomin = f"{subdomain}.{domain}"

    try:

        socket.gethostbyname(full_subdomin)

        return True

    except socket.gaierror:

        return False

 

def save_subdomains_to_json(subdomains,domain):

    data ={

        "domain" : domain,

        "active_subdomain" : list(subdomains)

    }

    file_name = f"{domain}_active_subdomains.json"

    with open(file_name,'w') as json_file:

        json.dump(data,json_file,indent=4)

 

def find_subdomain_from_links(url,domain):

    links = get_links(url)

    found_subdomains=set()

    #print(f"[*] {url} SAYFASI TARANIYOR")

    if links:

        for link in links:

            if domain in link:

                subdomain = link.split('/')[2].split('.')[0]

                #print(f"[*]{subdomain}.{domain} TARANIYOR...")

 

                if check_subdomains(domain,subdomain):

                    found_subdomains.add(f"{subdomain}.{domain}")

                

        save_subdomains_to_json(found_subdomains,domain)

 

        print("TARAMA BİTTİ")

    else:

        print("Hiçbir şey bulunamadı!")

 

domain = input("ENTER DOMAIN : ")

url = f"https://{domain}"

find_subdomain_from_links(url,domain)
