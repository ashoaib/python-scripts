import sys

class Txt2Dat:
    def __init__(self, fp):
        self.fp = fp
        self.debug = False
        self.contents = []
        
    def process(self):
        self.read_input()
        self.write_output()
        
    def read_input(self):
        with open(self.fp, 'rU') as f:
            ic = f.read().splitlines()
        
        for i, line in enumerate(ic):
            if self.debug and i > 500:
                break
            
            if (len(line.strip()) < 1) or (line[0] == '#'):
                continue
            
            line_contents = line.split(':')
            host_name = line_contents[0][:10]
            ips = ' - '.join(['.'.join([pad(n) for n in ip.split('.')]) for ip in line_contents[1].split('-')])
            
            self.contents.append(' , '.join([ips, '000', host_name]))
            
    def write_output(self):
        with open('ipfilter_new.dat', 'w') as f:
            for line in self.contents:
                f.write('%s\n' % line)


def pad(num):
    diff = 3 - len(num)
    
    if diff >= 0:
        num = ('0' * diff) + num
    
    return num

if __name__ == '__main__':
    Txt2Dat(sys.argv[1]).process()