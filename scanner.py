import nmap
import socket
import whois
from datetime import datetime

def run_scan(target, tools):
    results = ""
    
    if 'nmap' in tools:
        results += f"\n=== NMAP SCAN ({target}) ===\n"
        results += nmap_scan(target)
        
    if 'sublist3r' in tools:
        results += f"\n=== SUBDOMAINS ({target}) ===\n"
        results += subdomain_scan(target)
        
    if 'whois' in tools:
        results += f"\n=== WHOIS ({target}) ===\n"
        results += whois_scan(target)
        
    if 'nikto' in tools:
        results += f"\n=== VULNERABILITIES ({target}) ===\n"
        results += vulnerability_scan(target)
        
    return results

def nmap_scan(target):
    try:
        scanner = nmap.PortScanner()
        scanner.scan(target, arguments='-T4 -F')
        
        result = ""
        for host in scanner.all_hosts():
            result += f"Host: {host} ({scanner[host].hostname()})\n"
            result += f"State: {scanner[host].state()}\n"
            for proto in scanner[host].all_protocols():
                ports = scanner[host][proto].keys()
                for port in ports:
                    result += f"Port: {port}\tState: {scanner[host][proto][port]['state']}\tService: {scanner[host][proto][port]['name']}\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def subdomain_scan(target):
    try:
        # Simulated results (in real use: import sublist3r)
        return f"www.{target}\napi.{target}\ndev.{target}\nmail.{target}\n[Subdomain scan complete]"
    except Exception as e:
        return f"Error: {str(e)}"

def whois_scan(target):
    try:
        w = whois.whois(target)
        return (
            f"Domain: {w.domain_name}\n"
            f"Registrar: {w.registrar}\n"
            f"Creation Date: {w.creation_date}\n"
            f"Expiration Date: {w.expiration_date}\n"
            f"Name Servers: {', '.join(w.name_servers)}"
        )
    except Exception as e:
        return f"Error: {str(e)}"

def vulnerability_scan(target):
    # Simulated vulnerabilities
    return (
        "Potential vulnerabilities found:\n"
        "- XSS vulnerability in contact form\n"
        "- Outdated jQuery version (1.11.0)\n"
        "- Missing security headers\n"
        "- HTTP methods allowed: OPTIONS, TRACE\n"
        "[Nikto scan simulation]"
    )