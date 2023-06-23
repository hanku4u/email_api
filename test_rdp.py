import win32com.client
import psutil

def open_rdp_connection(ip_address, username, password):
    rdp = win32com.client.Dispatch("MsTscAx.MsTscAx")
    rdp.Server = ip_address
    rdp.UserName = username
    rdp.AdvancedSettings2.ClearTextPassword = password
    rdp.Connect()

# Usage example
ip_address = "192.168.0.100"  # Replace with the remote PC's IP address
username = "your_username"    # Replace with the username for the RDP connection
password = "your_password"    # Replace with the password for the RDP connection

open_rdp_connection(ip_address, username, password)

# Get the disk usage information of the remote PC
# replace C$ with the drive letter you want to get the information for
disk_usage = psutil.disk_usage("\\\\{}\\C$".format(ip_address))
print("Total: {:.2f} GB".format(disk_usage.total / (1024 ** 3)))
print("Used: {:.2f} GB".format(disk_usage.used / (1024 ** 3)))
print("Free: {:.2f} GB".format(disk_usage.free / (1024 ** 3)))

# Get the list of running processes on the remote PC
processes = psutil.process_iter("remote", ip_address)
for process in processes:
    print("Name: {}, PID: {}".format(process.name(), process.pid))