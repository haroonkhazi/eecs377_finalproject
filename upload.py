import paramiko
from os import walk



def main():
    mypath = "videos/"
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
        break
    k = paramiko.RSAKey.from_private_key_file("/Users/haroonkhazi/desktop/eecs377/eecs377.pem")
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='ec2-18-208-211-130.compute-1.amazonaws.com', username='ubuntu', pkey=k)
    ftp_client=ssh_client.open_sftp()
    for f in files:
        ftp_client.put('videos/{}'.format(f),'/home/ubuntu//website/videos/')
    ftp_client.close()
