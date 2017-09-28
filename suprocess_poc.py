import subprocess


def run(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(out.decode('utf-8'))
    print(err.decode('utf-8'))
    return out,err


run(['ls'])
run(['echo', '-n', 'hi'])