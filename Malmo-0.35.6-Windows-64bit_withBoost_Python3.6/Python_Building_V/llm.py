import subprocess

class LLM:
    '''
    ChatGPT can be called in Python 3.7 or higher, 
    but malmo is stable in Python 3.6 or lower, 
    so it is wrapped in an executable file like this and called as a subprocess.
    '''
    def __init__(self, engine_path):
        self.engine_path = engine_path
        self.proc = subprocess.Popen(
            [self.engine_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def send(self, string):
        print('==============================================================================')
        print(f"SENDING (to {self.engine_path.replace('.exe', '')}):\n\n{string}")

        # When passing to stdin, if there is a newline, it is pushed back rather than being passed all the way.
        # Therefore, we must connect and move on in one sentence.
        string = string.replace('\n', '\\n ')
        
        self.proc.stdin.write(string.encode('utf-8') + b'\n')
        self.proc.stdin.flush()

        response = self.proc.stdout.readline().decode('utf-8')
        print('==============================================================================')
        print(f"RECEIVED (from {self.engine_path.replace('.exe', '')}):\n")

        # In order to properly receive it through stdout, 
        # # the exe returns it as a single line. We need to newline it again.
        print(response.replace('\\n ', '\n'))
        
        return response

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()