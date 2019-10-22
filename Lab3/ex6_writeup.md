# Cracking Passwords with `hashcat`

Using [hashcat](https://hashcat.net/hashcat/) along with several wordlists obtained from https://github.com/danielmiessler/SecLists/tree/master/Passwords, I was able to crack 57 of the 148 hashes.



Running `hashcat` in Hybrid (Wordlist + Brute Force) mode allows us to quickly crack common passwords, and thereafter brute force our way through short passwords.



`hashcat` significantly accelerates the process by making use of available GPUs.



![1570722887268](C:\Users\krish\AppData\Roaming\Typora\typora-user-images\1570722887268.png)

