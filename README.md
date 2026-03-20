# **groot — A Friendly Root Command Wrapper for Linux**

`groot` is a lightweight Bash utility that behaves like a more conversational version of `sudo`. It provides two modes: running a single command with elevated privileges or dropping into a full root login shell. It is designed for administrators, developers, and power users who want a simple, memorable way to elevate privileges without typing long commands.

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

Make it executable:

```bash
sudo chmod +x /usr/local/bin/groot
```

---

## 🧪 Usage

### Interactive root shell
```
groot
```

### Run a single command as root
```
groot dnf update
```

### Check identity
```
groot whoami
```

---

## 🔒 Security Notes

- `groot` does not bypass authentication.  
- It relies entirely on your existing `sudo` configuration.  
- If your user cannot run `sudo`, `groot` cannot elevate privileges.  
- No passwords are stored, and no security mechanisms are altered.

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

# **LICENSE (MIT License)**

```
MIT License

Copyright (c) 2026 Willtech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING  
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER  
DEALINGS IN THE SOFTWARE.
```
