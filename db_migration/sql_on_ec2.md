# Setup MySQL on ec2
## Step 1: Update Your Ubuntu System
```sh
ssh -i your-key.pem ubuntu@your-ec2-ip
```
### Once connected, update the package list and upgrade your system:
```sh
sudo apt update
sudo apt upgrade
```
## Step 2: Install MySQL Server
```sh
sudo apt install mysql-server
```
During the installation, you’ll be prompted to set a MySQL root password. Make sure to choose a strong password and keep it secure.

## Step 3: Secure MySQL Installation
Run the MySQL security script to improve the security of your MySQL installation:
```sh
sudo mysql_secure_installation
```
Follow the prompts to perform tasks like setting the root password, removing anonymous users, and disabling remote root login.

## Step 4: Configure MySQL for Remote Access
By default, MySQL on Ubuntu binds to the localhost (127.0.0.1), making it accessible only locally. To allow remote access, you’ll need to modify the MySQL configuration.
Open the MySQL configuration file:
```sh
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Look for the line that reads:
bind-address = 127.0.0.1
# Change it to:
bind-address = 0.0.0.0
# Save the file and exit the text editor.
```
## Step 5: Create a MySQL User for Remote Access
Now, create a MySQL user and grant them remote access. Replace ‘your_user’ and ‘your_password’ with your desired username and password:
```sh
mysql -u root -p
```
Enter the MySQL root password when prompted. Then, run the following SQL commands:
```sh
CREATE USER 'your_user'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON *.* TO 'your_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EXIT;
```
This allows the user to connect from any host (‘%’). Make sure to restrict access further in a production environment.

## Step 6: Allow MySQL Port (3306) in AWS Security Group
In your AWS EC2 dashboard, locate the security group associated with your EC2 instance. Add an inbound rule that allows traffic on port 3306 (MySQL).

## Step 7: Test the Connection
From your local machine, use a MySQL client (e.g., MySQL Workbench, command-line client) to connect to your MySQL server using the EC2 instance’s public IP or DNS name, the MySQL username, and password you created earlier.
```sh
mysql -u your_user -p -h your-ec2-public-ip
```
Enter the password when prompted. You should now be connected to your MySQL server hosted on your EC2 instance.

