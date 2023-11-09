---
layout: post
title: Python - Calculate start and end IPs for a subnet!
categories: Python Scripts
tags: script python automation
---

# Calculate a Network Subnet using Python!

## Introduction
Today I had to calculate a 100 different subnets, to make my life easier i used this Python script to automate the process.

Save the code snippet for example as **subnetcalculate.py** under **c:\temp**

## The Code

```python
import csv
import ipaddress

# Function to calculate start and end IPs for a subnet
def calculate_start_end_ips(ip_subnet):
    try:
        network = ipaddress.ip_network(ip_subnet, strict=False)
        start_ip = str(network.network_address + 1)
        end_ip = str(network.broadcast_address - 1)
        return start_ip, end_ip
    except ValueError:
        return "Invalid Subnet", "Invalid Subnet"

# Input and output file paths
input_file = "c:\\temp\\input.csv"
output_file = "c:\\temp\\output.csv"

# Read the input CSV file and write the results to the output CSV file
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if len(row) < 1:
            continue
        ip_subnet = row[0]
        start_ip, end_ip = calculate_start_end_ips(ip_subnet)
        writer.writerow([ip_subnet, start_ip, end_ip])

print("Conversion complete. Results saved to", output_file)

```


For my use case I needed the ip ranges without the network and broadcast address, if you needed to calculate this including the network and broadcast address you can change the following code from:

```code
        start_ip = str(network.network_address + 1)
        end_ip = str(network.broadcast_address - 1)
```
to:

```code
        start_ip = str(network.network_address)
        end_ip = str(network.broadcast_address)
```

The input.csv was as simple as this:

```csv
10.33.62.129/255.255.255.192
10.33.3.1/255.255.255.0
10.33.62.65/255.255.255.224
```

With this as the output:

```csv
10.33.62.129/255.255.255.192,10.33.62.129,10.33.62.190
10.33.3.1/255.255.255.0,10.33.3.1,10.33.3.254
10.33.62.65/255.255.255.224,10.33.62.65,10.33.62.94
```

## Installing Python

You can download python on the official website. [Download Python](https://www.python.org/downloads/)

To install python you just have to go trough the installation wizard, for a written guide go to: [Using Python on Windows](https://docs.python.org/3/using/windows.html)

>Make sure to select "Add Python to PATH", this way you can run **python** from the commandline without adding the full path.
{: .prompt-warning }

## Running the script

After you saved the script you can run the script with the following command:

```
python c:\temp\subnetcalculate.py
```