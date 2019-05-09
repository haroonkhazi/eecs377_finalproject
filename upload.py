#!/home/pi/venv/bin/python
import paramiko
from os import walk
import os
import shelve
import shutil
import subprocess

def main():
    mypath = "/home/pi/eecs377_finalproject/videos/"
    remotepath = '/home/ubuntu/website/templates/static/'
    db = shelve.open('uploaded')
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
        break
    os.chdir('/home/pi/eecs377_finalproject/videos/')
    k = paramiko.RSAKey.from_private_key_file("/home/pi/keys/eecs377.pem")
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='ec2-34-224-32-127.compute-1.amazonaws.com', username='ubuntu', pkey=k)
    ftp_client=ssh_client.open_sftp()
    n = 0
    for f in files:
        if f in db:
            print("already uploaded")
            continue
        else:
            if "mp4" not in f:
                ftp_client.put(os.path.join(mypath , f), os.path.join(remotepath , f))
                n = n + 1 
                db[f]=1
                print("uploaded")
    if n > 0:
        subprocess.call(["ffmpeg", "-framerate", "5", "-pattern_type", "glob", "-i", "*.png", "-c:v", "libx264", "-y", "-pix_fmt", "yuv420p", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "current_video.mp4"])
        ftp_client.put(os.path.join(mypath, 'current_video.mp4'), os.path.join(remotepath, 'current_video.mp4'))
        print("uploaded video")
    ftp_client.close()
    ssh_client.close()
    db.close()

if __name__=="__main__":
    main()
