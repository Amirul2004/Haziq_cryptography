**Student Name:** Haziq  
**Username@Hostname:** Haziq@NWS0020  
**Tools Used:** Hydra, Burp Suite, Wireshark, etc.

---

## Table of Contents
- [1. Enumeration](#1-enumeration)
- [2. Brute Force Attacks](#2-brute-force-attacks)
- [3. Traffic Analysis](#3-traffic-analysis)
- [4. Problems Encountered](#4-problems-encountered)
- [5. Mitigation Strategies](#5-mitigation-strategies)


---

## 1. Enumeration 

> before we begin i should clarify what enemuration means in simple terms. Enumeration is the process of listing or naming items individually, one by one. It's a way of organizing and presenting a collection of items in a structured way. An example of an enumeration list is "apple, banana, orange". However that is not what enumeration means in Cyber security. For in Cyber Security, enumeration means the process of gathering detailed information about a target system or network, such as usernames, machine names, share names, and directory names

### Objective:
Identify potential usernames on the Metasploitable 2 VM to use in brute force attacks.

First we need to identify open ports and services that are available and running on the target VM :
```bash
    nmap -sC -sV -p 21, 22, 23, 80 [Target_IP]
```
Explanation for above command:

- `-C`: Runs a default NSE scripts
- `-sV`: Detect which service version is available
- `-p`: Scans the ports that are requested (exp: FTP=21)

  ![alt text](evidence/image.png)


### Enumerating Usernames

### From SMB (to use with SSH, Telnet, FTP down the line): 
    enum4linux -a [TARGET_IP]

What the command does :
Enumerates users, shares, groups, and policies over SMB. Useful for finding valid system usernames that might also exist in SSH/Telnet/FTP. It can look for usernames like `msfadmin (metasploitable 2)`, `user` , `admin` etc etc

![alt text](evidence/image-1.png)
![alt text](evidence/image-2.png)
![alt text](evidence/image-3.png)
![alt text](evidence/image-4.png)
![alt text](evidence/image-5.png)
![alt text](evidence/image-6.png)
![alt text](evidence/image-7.png)
![alt text](evidence/image-8.png)

### Web Server Enumeration (HTTP)

We're using `gobuster` to find hidden directories or files on the web server:
    
    gobuster dir -u http://[TARGET_IP] -w /usr/share/wordlists/dirb common.txt

Command explanation:
- `-u`: URL we're targeting
- `-w`: Wordlist 
- `-t`: Number of thread and we can also adjust the speed 

![alt text](evidence/image-12.png)


---

## 2. Brute Force Attacks


### Objective:
Perform brute force login attempts using Hydra and Burp Suite to crack service credentials.

### Preparation
Before launching brute force attacks, make sure you have:

- A list of usernames (`userlist.txt`)
- A list of passwords (`passwordlist.txt`)
  
Using default one from kali could work but the existing file contain a huge amount of password so it'll take a long time to crack them one by one. So we'll create a short one of our own:

    echo -e "admin\nmsfadmin\nrahsia\nuser\ncuba" > userlist.txt
    echo -e "12345\nmsfadmin\nftp1234\nadmin\npassword" > passwordlist.txt

### 2.1 Brute force attack using Hydra
    hydra -L userlist.txt -P passwordlist.txt [Target_IP] ftp -V

-  `-L userlist.txt`: path to username list
-  `-P passwordlist.txt`: path to password list
-  `-V`: verbose (shows attempts)
-  `ftp`: targets ftp service

![alt text](evidence/image-11.png)
  
### 2.2 TELNET Brute force attack using Hydra
    hydra -L userlist.txt -P passwordlist.txt [Target_IP] telnet -V

-  `-L userlist.txt`: path to username list
-  `-P passwordlist.txt`: path to password list
-  `-V`: verbose (shows attempts)
-  `telnet`: targets telnet service

![alt text](evidence/image-13.png)

### 2.3 SSH Brute force attack using NetExec

We're using NetExec for SSH

    nxc ssh [Target_IP] -u userlist.txt -p passwordlist.txt


-  `-u userlist.txt`: path to username list
-  `-p passwordlist.txt`: path to password list
-  `ssh`: specifies SSH as the target service
  
![alt text](evidence/image-14.png)
  
### 2.4 HTTP Login Brute Force Attack using Burp Suite


In this part, we’ll be using Burp Suite to perform a brute force attack on a login page found on a target website. The goal is to test usernames and passwords using Burp’s Intruder tool.

Start by launching Burp Suite and navigating to the Proxy > Intercept tab. Ensure that intercept is turned on. Then, click "Open Browser" to launch Burp's built-in browser, which is already set up to send traffic through Burp. It's helpful to arrange your windows so that you can see both Burp and the browser at the same time.

Next, in the Burp browser, go to the target’s login page (for example, http://[target-ip]/login). Try logging in using any random or fake credentials. Burp will catch this login attempt in the Intercept tab, and you’ll be able to see the full HTTP request.

Click "Forward" to allow the request to go through to the server. If multiple requests are intercepted, continue clicking Forward until the page fully loads. This process lets you observe how the login form is submitted in the background.

Once the request has gone through, you can turn off interception by going back to the Intercept tab and clicking "Intercept is OFF." This will prevent Burp from stopping the browser every time it sends a request.

Now go to Proxy > HTTP History. Look through the list to find the POST request that was sent to the login page. Click on it to view the full request and response. Right-click on the request and select "Send to Intruder" to prepare for the brute force attack.

In the Intruder tab, set the attack type to "Cluster Bomb." Then, in the request preview, highlight the username and password values and mark them as payload positions. These are the parts of the request where Burp will insert different values from your wordlists.

For the first payload set, load your username wordlist (for example, userlist.txt). For the second payload set, load your password wordlist (such as passwordlist.txt).

Once everything is set up, start the attack. As Burp tries each combination of username and password, pay attention to differences in status codes, response lengths, or any signs that suggest a successful login, such as the word “Welcome” or a redirect.

When you see a result that stands out, particularly one with a longer response length or a different status code, right-click on it and choose "Open in Browser." Copy the URL that appears and paste it into Burp's browser. If all goes well, you should be logged into the target website.

![alt text](evidence/image-15.png)
![alt text](evidence/image-16.png)
![alt text](evidence/image-17.png)
![alt text](evidence/image-18.png)
![alt text](evidence/image-19.png)
![alt text](evidence/image-20.png)
![alt text](evidence/image-32.png)
---

## 3. Traffic Analysis

1. Open Wireshark:
   sudo wireshark

![alt text](evidence/image-21.png)

2. Start capture on the network interface connected to the target.
   
![alt text](evidence/image-22.png)

3. Apply filters:
   - FTP: `tcp.port == 21`
   - TELNET: `tcp.port == 23`
   - SSH: `tcp.port == 22`
   - HTTP: `tcp.port == 80`

![alt text](evidence/image-23.png)
> here we are using `tcp.port ==21` for our example

4. Identify unencrypted traffic containing credentials.

    - clicking on any of the packet -> follow -> TCP stream reveals more info 
  
  ![alt text](evidence/image-24.png)
  ![alt text](evidence/image-25.png)

> Note that with SSh, you'll see a lot of gibberish

For SSH specifically, its a bit hard because metaslpoitable 2 only offers ssh-rsa,ssh-dss while kali doesnt offer this key type because its not widely used anymore. Now by using this command, we can open or created the file

    vim ~/.ssh/config

![alt text](evidence/image-29.png)

and we can put the following block in the file to force kali to accept this key

![alt text](evidence/image-30.png)

now we have successfully go into metasploitable from kali using SSh

following the previous step that we do for ftp and telnet, we can sniff SSH using wireshark, however as told previously, SSH package is gibberish, due to it being encrypted

![alt text](evidence/image-31.png)


### Capturing Packets using tcpdump
    sudo tcpdump -i eth0 port 21 or port 23 or port 22 or port 80 -w capture.pcap

After using the above command, go into a new terminal and log into metasploit using FTP, SSH or telnet

![alt text](evidence/image-26.png)
![alt text](evidence/image-27.png)

once you're done press `ctrl` + `c` to exit and analyse `capture.pcap` in Wireshark

    use the command `wireshark capture.pcap` to open the file 

![alt text](evidence/image-28.png)

---

## 4. Problems Encountered

During the brute force and traffic analysis stages, several issues were encountered. The following table outlines the problems and how they were resolved:

| Problem | Description | Solution |
|--------|-------------|----------|
| Outdated Metasploitable VM | The HTTP service (Apache2) failed to start, preventing brute force testing on port 80. | Plan to install a newer version of Metasploitable or manually fix Apache configuration and dependencies. |
| Rate Limiting / Account Lockouts | Some services slowed down or locked accounts after multiple failed attempts. | Used Hydra with `-t 1` (slow mode) to reduce detection. Can also rotate IPs with proxychains. |
| CAPTCHA / Anti-Brute Force | Some HTTP login forms had mechanisms to block automation. | Modified request headers, used Burp Suite manual testing instead of Intruder for better control. |
| Wordlist Inefficiency | Large or poorly matched wordlists caused long brute force times or failed attempts. | Switched to targeted wordlists with common credentials (rockyou.txt or smaller curated lists). |
| TELNET Disconnection | TELNET sessions would randomly close mid-brute force. | Used adjusted Hydra timing parameters and ensured stable network connectivity. |
| SSH Brute Force Delay | SSH introduces artificial delays on failed logins. | Minimized login attempts and tested with small focused username/password lists. |

---

## 5. Mitigation Strategies

To secure the vulnerable protocols explored in this lab, the following mitigation strategies and secure alternatives are proposed:

| Protocol | Vulnerability | Proposed Mitigation | How It Helps |
|----------|---------------|----------------------|--------------|
| **FTP** | Transmits credentials in plaintext | Use **SFTP** or **FTPS** | Encrypts login data and file transfers, protecting against sniffing. |
| **TELNET** | Entire session is unencrypted | Replace with **SSH** | SSH encrypts the session, making data unreadable to attackers. |
| **HTTP (Login Pages)** | Credentials visible in POST data | Implement **HTTPS (SSL/TLS)** | Secures communication between client and server. |
| **SSH** | Still vulnerable to brute force | Enforce **Key-Based Authentication**, implement **Fail2ban** | Blocks brute force by requiring private keys and auto-bans failed attempts. |
| **All Services** | Brute force exposure | Apply **Rate Limiting**, **Account Lockouts** | Limits repeated failed attempts and alerts admins to attack patterns. |
| **Web Logins** | Automated brute force (Burp Suite/Intruder) | Add **CAPTCHA**, **Multi-Factor Authentication (MFA)** | Prevents bots and adds extra security layers to login process. |
