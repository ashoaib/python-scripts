import urllib
import httplib
import os
import sys
import contextlib

class GoogleClosureCompiler:
    files = []
    
    def __init__(self, path, output=None):
        self._output_file = os.path.join(path, 'js-min.js' if output is None else output)
        
        if (os.path.isdir(path)):
            self._read_files_from_dir(path)
        elif (os.path.isfile(path)):
            self.files.append(path)
        else:
            raise IOError(path + ': not file or directory, or could not be read')
        
    def compile(self):
        src = self._read_files()
        params = urllib.urlencode([
            ('js_code', src),
            ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
            ('output_format', 'text'),
            ('output_info', 'compiled_code')
        ])
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        
        try:
            with contextlib.closing(httplib.HTTPConnection('closure-compiler.appspot.com')) as conn:
                conn.request('POST', '/compile', params, headers)
                response = conn.getresponse()
                compiled_code = response.read()
                self._write_compiled_file(compiled_code)
        except httplib.HTTPException, e:
            print str(e)
        
    def _read_files(self):
        src = ''
        
        for _file in self.files:
            try:
                with open(_file) as f:
                    src += f.read()
            except IOError:
                continue
                
        return src
        
    def _read_files_from_dir(self, path):
        file_list = os.listdir(path)
        self.files = [os.path.join(path, f) for f in file_list if f.split('.')[-1] == 'js']
        
    def _write_compiled_file(self, code):
        try:
            f = open(self._output_file, 'w')
            f.write(code)
            f.close()
            print "Successfully compiled to %s" % self._output_file
        except IOError, e:
            print str(e)


def main():
    path = sys.argv[1]
    
    try:
        output = sys.argv[2]
    except IndexError:
        output = None

    GoogleClosureCompiler(path, output).compile()

if __name__ == '__main__':
    main()