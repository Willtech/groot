# **groot — A Friendly Root Command Wrapper for Linux**

`groot` is a lightweight Bash utility that behaves like a more conversational version of `sudo`.  
It provides two modes:

- **Command mode** — run a single command with root privileges  
- **Interactive mode** — drop into a full root login shell

It is designed for administrators, developers, and power users who want a simple, memorable way to elevate privileges without typing long commands.

---

## 🌱 Features

- Run commands as root using a clean wrapper  
- Drop into a root login shell when no arguments are provided  
- Uses `sudo` safely and correctly  
- Minimal, readable Bash code  
- Works on Fedora, RHEL, CentOS, Debian, Ubuntu, Arch, and any system with `sudo`  

---

## 🚀 Installation

Create the script:

```bash
sudo nano /usr/local/bin/groot
```

Paste the following:

```bash
#!/usr/bin/env bash

# groot: a friendly sudo wrapper
# Author/Developer Manager: Reaper Harvester / Oceans Ginsberg / Wills / master Damian Williamson Grad. / Professor. Damian A. James Williamson Grad. / Graduate. Damian Williamson  
# Founder of Willtech, Swan Hill, Victoria
# AI Collaboration: Microsoft Copilot (technical design + documentation)

if [ $# -eq 0 ]; then
    # No arguments → open a root login shell
    exec sudo su -
else
    # Arguments provided → run them as a root command
    exec sudo "$@"
fi
```

Save and exit, then make it executable:

```bash
sudo chmod +x /usr/local/bin/groot
```

---

## 🧪 Usage

### **Interactive root shell**
```
groot
```

This opens a full root login shell (`sudo su -`).

### **Run a single command as root**
```
groot dnf update
```

Equivalent to:
```
sudo dnf update
```

### **Check who you are**
```
groot whoami
```

Output:
```
root
```

---

## 🔒 Security Notes

- `groot` does **not** bypass authentication.  
- It relies entirely on your existing `sudo` configuration.  
- If your user is not allowed to run `sudo`, `groot` will not elevate privileges.  
- It does not store passwords, modify PAM, or weaken system security.

---

## 📦 Uninstall

```bash
sudo rm /usr/local/bin/groot
```

---

## 📝 Credits

- **Primary Author:** MR. — Technologist, Programmer, Developer, Administrator (Swan Hill, Victoria, Australia)  
- **AI Collaboration:** Microsoft Copilot — design assistance, documentation, and Bash best‑practice guidance  

---

## 📜 License

You may license this however you prefer (MIT, Apache‑2.0, GPL‑3.0, proprietary).  
If you want, I can generate a matching LICENSE file.

---

If you want to extend `groot` with logging, auditing, banners, or safety prompts, I can help you design those features next.
