'''
USAGE:
parse apache access log 
args: log file
'''

import sys
import re

# 64.242.88.10 - - [07/Mar/2004:16:06:51 -0800] "GET /twiki/bin/rdiff/TWiki/NewUserTemplate?rev1=1.3&rev2=1.2 HTTP/1.1" 200 4523

# re.VERBOSE 忽略正则表达式中的空白符: dog | cat == dog|cat
log_line_re = re.compile(r'''(?P<remote_host>\S+) # ip
                            \s+ # whitespaces 
                            \S+ # remote logname
                            \s+ # whitespaces
                            \S+ # remote user
                            \s+ # whitespaces
                            \[[^\[\]]+\] # time
                            \s+ # whitespaces
                            ".+?" # request url
                            \s+ # whitespaces
                            (?P<status>\d+) # status
                            \s+ # whitespaces
                            (?P<byte_sent>-|\d+) # byte
                            \s* # whitespaces
                            ''', re.X)

def dictify_line(line):
    m = log_line_re.match(line)
    if m:
        groupdict = m.groupdict()
        return groupdict


def generate_log_report(log):
    report_dict = {}
    for line in log:
        line_dict = dictify_line(line)
        byte_sent = line_dict['byte_sent']
        # dict setdefault() 函数和get()方法类似, 如果键不存在于字典中，将会添加键并将值设为默认值
        # remote_host as key, byte_sent list as value
        report_dict.setdefault(line_dict['remote_host'], []).append(byte_sent)
    
    return report_dict

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print(__doc__)
        sys.exit(1)
    
    log = sys.argv[1]
    try:
        log_file = open(log, 'r')
    except IOError:
        print("not a valid log file")
        sys.exit(1)
    report = generate_log_report(log_file)
    print(report)
    log_file.close()


