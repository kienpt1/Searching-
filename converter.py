import json 
import os 
import sys 

# Dictionary mapping Cisco commands to Juniper and Huawei equivalents
config_map = {
    "hostname": {
        "juniper": "set system host-name",
        "huawei": "sysname"
    },
    "interface": {
        "juniper": "set interfaces",
        "huawei": "interface"
    },
    "ip address": {
        "juniper": "set interfaces {} unit 0 family inet address",
        "huawei": "ip address"
    },
    "description": {
        "juniper": "set interfaces {} description",
        "huawei": "description"
    },
    "shutdown": {
        "juniper": "delete interfaces {} disable",
        "huawei": "shutdown"
    },
    "no shutdown": {
        "juniper": "set interfaces {} enable",
        "huawei": "undo shutdown"
    },
    "router ospf": {
        "juniper": "set protocols ospf",
        "huawei": "ospf"
    },
    "network": {
        "juniper": "set protocols ospf area 0 interface",
        "huawei": "network"
    },
    "router bgp": {
        "juniper": "set protocols bgp",
        "huawei": "bgp"
    },
    "neighbor": {
        "juniper": "set protocols bgp group external neighbor",
        "huawei": "peer"
    },
    "access-list": {
        "juniper": "set firewall family inet filter",
        "huawei": "acl"
    },
    "permit": {
        "juniper": "then accept",
        "huawei": "rule permit"
    },
    "deny": {
        "juniper": "then discard",
        "huawei": "rule deny"
    }
}

# Function to convert Cisco config to Juniper or Huawei
def convert_config(cisco_config, target_vendor):
    if target_vendor not in ["juniper", "huawei"]:
        return "Unsupported vendor. Choose 'juniper' or 'huawei'."
    
    converted_config = []
    lines = cisco_config.split("\n")

    for line in lines:
        words = line.strip().split()
        if not words:
            continue
        
        key = words[0]
        if key in config_map and target_vendor in config_map[key]:
            if "{}" in config_map[key][target_vendor]:  # For interface-based commands
                converted_config.append(config_map[key][target_vendor].format(words[1]) + " " + " ".join(words[2:]))
            else:
                converted_config.append(config_map[key][target_vendor] + " " + " ".join(words[1:]))
        else:
            converted_config.append(f"# Untranslated: {line}")  # Comment out unknown lines

    return "\n".join(converted_config)

# Example Cisco configuration
cisco_config = """
hostname Router1
"""

# Convert Cisco to Juniper
juniper_config = convert_config(cisco_config, "juniper")
print("### Juniper Configuration ###\n", juniper_config)

# Convert Cisco to Huawei
huawei_config = convert_config(cisco_config, "huawei")
print("\n### Huawei Configuration ###\n", huawei_config)