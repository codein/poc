import time
from ftplib import FTP
ftp = FTP('ftp.debian.org')     # connect to host, default port
ftp.login()
ftp.retrlines('LIST')

def ftp_get_latest_file(ftp, path):
    ftp.cwd(path)
    data = []
    file_dict = {}
    ftp.dir(data.append)
    print(data)
    for line in data:
        col_list = line.split()
        date_str = ' '.join(line.split()[5:8])
        file_dict[time.strptime(date_str, '%b %d %H:%M')] = col_list[8]
        date_list = list([key for key, value in file_dict.items()])
    return file_dict[max(date_list)]

def ftp_download(ftp, source_filename, destination_dir):
    retr_cmd = 'RETR {0}'.format(source_filename)
    destination_filepath = '{0}/{1}'.format(destination_dir,source_filename)
    ftp.retrbinary(retr_cmd, open(destination_filepath, 'wb').write)

file = get_latest_file(ftp, 'debian')
download(file, '/home/codein')