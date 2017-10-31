#!/usr/bin/env python3
import os
import json
import requests
import argparse

URL = 'https://ipinfo.io'
FORMAT = 'json'
FILE = 'ip_location.csv'


class ipInfo:
    def __init__(self, file=None):
        if file:
            with open(file, 'r') as f:
                self.ips = f.readlines()
        else:
            self.ips = None

    def getCountry(self, ip):
        response = requests.get("{}/{}/{}".format(URL, ip, FORMAT))
        return json.loads(response.text)

    def printData(self, data):
        print("*********************************************")
        print('IP : {} \nRegion : {} \nCountry : {} \nCity : {} \nOrg : {}'.format(data['ip'], data['region'],
                                                                                   data['country'], data['city'],
                                                                                   data['org']))
        print("*********************************************")

    def writeToFile(self, file, data):
        if not os.path.exists(file):
            header = True
        else:
            header = False
        with open(file, 'a') as f:
            if header:
                f.write("Ip;Region;Country;City;Organisation\n")
            try:
                ip = data['ip']
            except KeyError:
                ip = "N/A"

            try:
                region = data['region']
            except KeyError:
                region = "N/A"

            try:
                country = data['country']
            except KeyError:
                country = "N/A"

            try:
                city = data['city']
            except KeyError:
                city = "N/A"

            try:
                org = data['org']
            except KeyError:
                org = "N/A"

            print(data)
            f.write("{};{};{};{};{}\n".format(ip, region, country, city, org))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = "Tool for geting IP owner information"
    parser.add_argument("-f", "--file", metavar='', help="File containing a list of Ips separated by '\n'")
    parser.add_argument("-i", "--ip", metavar='', help="Ip address to search for")
    args = parser.parse_args()

    if args.file:
        main = ipInfo(args.file)
    else:
        main = ipInfo()

    if main.ips:
        for ip in main.ips:
            data = main.getCountry(ip)
            # main.printData(data)
            main.writeToFile(FILE, data)
    elif args.ip:
        main.printData(main.getCountry(args.ip))
    else:
        main.printData(main.getCountry(input("Please enter IP:")))
