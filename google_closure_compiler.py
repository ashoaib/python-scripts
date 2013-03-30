import urllib
import httplib
import os
import sys
import contextlib

class GoogleClosureCompiler:
    """
    Wrapper class for compiling JavaScript file(s) into a single minified file,
    using Google's Closure Compiler API. It can read an individual file, be
    passed a list of files, or read files from a directory. It writes to an
    output file in the same directory as the source.
    
    Example usage:
    
    - Command-line
    
        The script can be called from the command line:
        
        python google_closure_compiler.py <path_to_source> <output_file_name>
        
        <path_to_source> can be a path to a file or a directory
        
        <output_file_name> is an optional argument - this is the name of the
        output file to write the compiled JavaScript to. If not passed,
        defaults to js-min.js
        
    - Within python
    
        foo = GoogleClosureCompiler(path_to_source, output_file_name)
        foo.compile()
    """
    
    files = []
    
    def __init__(self, path, output=None):
        if (os.path.isdir(path)):
            self._read_files_from_dir(path)
        elif (os.path.isfile(path)):
            self.files.append(path)
            path = os.path.split(path)[0]
        else:
            raise IOError(path + ': not file or directory, or could not be read')
        
        self._output_file = os.path.join(path, 'js-min.js' if output is None else output)
        
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
                self._write_compiled_file(conn.getresponse().read())
        except httplib.HTTPException, e:
            print str(e)
            
    def add_file(self, path):
        if (os.path.isfile(path)):
            self.files.append(path)
        else:
            raise IOError(path + ': not file or directory, or could not be read')
        
    def _read_files(self):
        src_list = []
        
        for _file in self.files:
            try:
                with open(_file) as f:
                    src_list.append(f.read())
            except IOError:
                continue
                
        return ''.join(src_list)
        
    def _read_files_from_dir(self, path):
        file_list = os.listdir(path)
        self.files = [os.path.join(path, f) for f in file_list if f.split('.')[-1] == 'js']
        
    def _write_compiled_file(self, code):
        try:
            f = open(self._output_file, 'w')
            f.write(code.replace('\n', ''))
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