import subprocess
import re
import json
import argparse
import os
import sys

def get_ping_stats(host):  
        try:
            result = 0
            for _ in range(5):
                command = f"ping -c 1 {host}"
                output = subprocess.check_output(command, shell=True)
                output = output.decode("utf-8")
                match = re.search(r"min\/avg\/max\/mdev = (\d+\.\d+\/\d+\.\d+\/\d+\.\d+\/\d+\.\d+) ms", output)
                rtt_values = match.group(1).split("/")
                min_rtt, avg_rtt, max_rtt, mdev_rtt = [float(x.strip()) for x in rtt_values]        
                result += max_rtt
            return float("{:.2f}".format(result/5 + result%5)) 
        except BaseException:
            return -1


def speedtest (server_id=""):
    command = f"speedtest --accept-license -f json -u Mbps" 
    if(server_id != ""):
        command = f"speedtest --accept-license -s {server_id} -f json -u Mbps"
    output = subprocess.check_output(command, shell=True)
    output = output.decode("utf-8")
    json_result = json.loads(output)
    final_result = {
        "client_ip": json_result["interface"]["externalIp"],
        "server_host": json_result["server"]["host"],
        "server_country": json_result ["server"]["country"],
        "server_city": json_result ["server"]["location"],
        "internet_provider": json_result ["isp"],
        "server_provider": json_result ["server"]["name"],
        "result_ping": json_result["ping"]["latency"],
        "result_download": json_result["download"]["bandwidth"]/100000 ,
        "result_upload": json_result["upload"]["bandwidth"]/100000 ,
        "result_unit": "Mbps"
    }
    return final_result

def ping_test(hosts=["8.8.8.8", "1.1.1.1", "cloudflare.com", "speedtest.vn"]):
    results = {}
    count = 0
    for host in hosts:
        ping_result = {f"ping_{count}" : get_ping_stats(host)}
        results.update(ping_result)
        count += 1
    return results

def main_func():
    raw_ping_host = os.environ.get('PING_HOST', '')
    server_id =  os.environ.get('SERVER_ID', '')
    ping_host = raw_ping_host.split(",")

    if server_id != '' and raw_ping_host != '':
        ping_result = ping_test(ping_host)
        speedtest_result = speedtest(server_id)
        print(json.dumps({"ping_test" : ping_result, "speedtest": speedtest_result},ensure_ascii=False))         
    if server_id != '' and raw_ping_host == '':
        print(json.dumps(speedtest(server_id),ensure_ascii=False))
    if raw_ping_host != '' and server_id == '':
            print(json.dumps(ping_test(ping_host),ensure_ascii=False))
    if server_id == '' and raw_ping_host == '':
        ping_result = ping_test()
        speedtest_result = speedtest()
        print(json.dumps({"ping_test" : ping_result, "speedtest": speedtest_result,},ensure_ascii=False))


main_func()
