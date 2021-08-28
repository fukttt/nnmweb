import subprocess
try:
    output = subprocess.check_output("samba --version", shell=True)
    if "Version" in output:
        print ("Installed")
except subprocess.CalledProcessError as e:
    print("Not installed")
