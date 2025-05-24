# Command Table
This is my command cheat sheet for my everyday use. Most of them are in linux unless state otherwise, The plan here is to put all the commands i use so i can view them in the future as a note and self reminder 

| No. | Command                  | Description & Example                          |
|-----|--------------------------|------------------------------------------------|
| 1   | sudo apt update                         | Update your package list, almost always what i would do first when i turn on my VM                                                |
| 2   | sudo apt install <packages>                         | This commands is usually used when you're trying to install something a package. For example : sudo apt install tealdeer                                                |
| 3   | tldr <commands>                        | `TeaLDeeR` is a package that can be install , it gives a simplified version of the commands that can be used with the specficic command line. For example, TLDR mv                                                  |
| 4   | mv <file name/source> <new file name/destination>                         | `mv` is a command use to do 2 things, move and renaming, it can be used to move a file from a specific location to another location, or renaming the file. For example, mv rockyou.txt /home/<user>/Documents                                                |
| 5   | ls & ll                         | This command is used to list the content of the current directory, long listing or ll is used to list the content and the details of each file. An example of the command is `ls la` which list all the file in the directory + hidden files because of the flag a                                                |
| 6   | sudo apt upgrade                         | This commands is usually a follow up to the previious command `sudo apt update` where it will upgrade all the previously listed package that can be update                                                |
| 7   | cd <directory>                          | stands for change directory, you usually run this command after identifying the content in the directory by using the previously told, listing command (`ls`)                                                |
| 8   | nano/vi/vim <filename>                          | Eventho they have different names, all this commands are basically to view and write the content of files. For example, `Vim text.txt` and the said text file does not exist yet, the file will be created                                                |
| 9   | IP a                          | stands for `ip address` usually used when you're trying to check you IP for stuff like scanning ports and stuff                                                |
| 10  | nmap                         | `nmap` is a shortform of a tool called network mapping, usually used when you're trying to scan a the ip to check whos in the network and then to check the ports available on said host whos connected to the IP. Example of command is `nmap -sV <ip address>`                                                |
| 11  |                          |                                                |
| 12  |                          |                                                |
| 13  |                          |                                                |
| 14  |                          |                                                |
| 15  |                          |                                                |
| 16  |                          |                                                |
| 17  |                          |                                                |
| 18  |                          |                                                |
| 19  |                          |                                                |
| 20  |                          |                                                |

# Below are the commands example explains
1. Sudo apt install tealdeer is basically us installing the TLDR packages, other examples are 
    * `sudo apt install python3~`<- This is another commands, use to install the python package so we can use them in terminal kali
2. `ls is` listingm, `ll` which is almost and everyday command used is basically a simplified version of `ls l`. It uses the command listing (ls) with the added flag of l which is a flag for long lisitng. Long listing is a command to list all the details of each file.
