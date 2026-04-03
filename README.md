# groot — A Friendly Root Command Wrapper for Linux

<p align="center">
  <img src="https://github.com/Willtech/groot/raw/master/images/groot.png" alt="groot in action" width="720" />
</p>

<p align="center">
  <a href="https://github.com/Willtech/groot/releases/tag/V1.3.0"><img src="https://img.shields.io/badge/version-1.3.0-brightgreen" alt="Version 1.3.0" /></a>
  <a href="https://github.com/Willtech/groot/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/shell-bash-89e051" alt="Bash" />
  <img src="https://img.shields.io/badge/distros-Fedora%20%7C%20RHEL%20%7C%20Debian%20%7C%20Ubuntu%20%7C%20Arch-informational" alt="Distros" />
  <a href="https://deepwiki.com/Willtech/groot"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki" /></a>
</p>

---

`groot` is a lightweight Bash utility that wraps `sudo` with a cleaner, more memorable interface. Instead of typing `sudo su -` to open a root shell, you just type `groot`. Instead of `sudo dnf update`, you type `groot dnf update`. It's the same privilege elevation you already have — just friendlier.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
  - [Script Install (any distro)](#script-install-any-distro)
  - [RPM Package (Fedora / RHEL)](#rpm-package-fedora--rhel)
  - [Manual Copy](#manual-copy)
- [Usage](#usage)
  - [Open a root login shell](#open-a-root-login-shell)
  - [Run a command as root](#run-a-command-as-root)
  - [Run a command, then drop into a root shell](#run-a-command-then-drop-into-a-root-shell)
  - [Dry run — preview without executing](#dry-run--preview-without-executing)
  - [Help and version](#help-and-version)
- [Flag Reference](#flag-reference)
- [Execution Modes](#execution-modes)
- [Security Notes](#security-notes)
- [Uninstall](#uninstall)
- [Repository Layout](#repository-layout)
- [Known Issues & Roadmap](#known-issues--roadmap)
- [Credits](#credits)
- [License](#license)

---

## Features

- Open a root login shell with zero arguments: `groot`
- Run any command as root: `groot <command> [args…]`
- Run a command as root, then stay in a root shell: `groot --shell-after <command>`
- Preview exactly what `groot` *would* do without executing anything: `--dry-run`
- Flags are order-independent — `--dry-run --shell-after` and `--shell-after --dry-run` produce identical output
- Safe argument handling with `"$@"` — no word-splitting surprises
- Literal command reconstruction using `printf '%q'` for complex arguments
- Built-in `--help` / `-h` and `--version`
- Works on any Linux system with `sudo` — Fedora, RHEL, CentOS, Debian, Ubuntu, Arch, and more
- Also available as a hardened compiled binary (via `shc` + GCC) in an RPM package for Fedora/RHEL

---

## How It Works

`groot` is a single-file Bash script. It initialises two boolean flags (`dry_run`, `shell_after`), accumulates non-flag arguments into a `cmd_args` array, then branches into one of five execution paths:

```
groot [--dry-run] [--shell-after] [command [args…]]
           │
           ▼
    Parse flags & args
           │
    ┌──────┴──────────────────────────────────────┐
    │                                              │
No cmd_args?                               cmd_args present
    │                                              │
exec sudo su -                    ┌────────────────┼──────────────────┐
                              dry_run?        shell_after?        normal
                                  │                │                  │
                          print preview    exec cmd, then      exec sudo "$@"
                                          exec sudo su -
```

Privilege elevation is handled entirely by your existing `sudo` configuration. `groot` stores no passwords and modifies no security settings.

---

## Installation

### Script Install (any distro)

Clone the repo and run the provided install script as root:

```bash
git clone https://github.com/Willtech/groot.git
cd groot
sudo ./install
```

This copies `groot` to `/usr/bin/groot` and makes it executable.

Alternatively, install manually to `/usr/local/bin`:

```bash
sudo cp groot /usr/local/bin/groot
sudo chmod +x /usr/local/bin/groot
```

### RPM Package (Fedora / RHEL)

A pre-built RPM for `x86_64` targeting Fedora 43 is provided in the repository root. First, import the Willtech GPG signing key, then install:

```bash
sudo rpm --import RPM-GPG-KEY-Willtech
sudo rpm -ivh groot-1.3.0-1.fc43.x86_64.rpm
```

The RPM installs a hardened compiled binary (produced from the Bash source via `shc` and built with `-fstack-protector-strong` and `-Werror=format-security`) and places the man page at `/usr/share/man/man1/groot.1.gz`.

#### Build the RPM from source

The spec file (`packaging/groot.spec`) expects a source tarball and delegates the actual compilation to `install.bin` (which runs `shc` → `gcc` internally). The build system is `rpmbuild`, designed to work with Koji or a local build environment.

**Build-time dependencies:** `bash`, `shc`, `gcc`, `make`, `coreutils`, `gzip`, `rpm-build`

```bash
# 1. Set up the rpmbuild tree (once)
mkdir -p ~/rpmbuild/{SOURCES,SPECS}

# 2. Create the source tarball from the repo root
#    The spec expects: groot-1.3.0.tar.gz
git clone https://github.com/Willtech/groot.git groot-1.3.0
tar czf ~/rpmbuild/SOURCES/groot-1.3.0.tar.gz groot-1.3.0/

# 3. Copy the spec file into place
cp groot-1.3.0/packaging/groot.spec ~/rpmbuild/SPECS/

# 4. Build the binary RPM
rpmbuild -bb ~/rpmbuild/SPECS/groot.spec
```

The finished RPM will be in `~/rpmbuild/RPMS/x86_64/`.

**What the build pipeline does internally:**

| Step | Tool | Action |
|------|------|--------|
| `%prep` | `rpmbuild` | Unpacks `groot-1.3.0.tar.gz` into the build directory |
| `%build` | `install.bin` → `shc` | Transpiles `groot` Bash script to C source (`groot.x.c`) |
| `%build` | `install.bin` → `gcc` | Compiles `groot.x.c` to ELF binary `groot.bin` |
| Rename | `rpmbuild` spec | Renames `groot.bin` → `groot` for standard invocation |
| `%install` | `rpmbuild` | Copies binary to `%{buildroot}/usr/bin/groot`; man page to `/usr/share/man/man1/` |
| `%files` | `rpmbuild` | Packages binary (0755), man page (0644), LICENSE, and README.md |

The resulting binary is hardened with GCC flags including `-fstack-protector-strong` and `-Werror=format-security`, and links against `libc.so.6` with `sudo` as a runtime dependency.

> **Note:** Debug packages are disabled in the spec (`%global debug_package %{nil}`) because `shc` obfuscates the source into C, making source-level debugging inapplicable.

### Manual Copy

If you just want the script without cloning:

```bash
sudo curl -o /usr/local/bin/groot \
  https://raw.githubusercontent.com/Willtech/groot/master/groot
sudo chmod +x /usr/local/bin/groot
```

---

## Usage

### Open a root login shell

```bash
groot
```

Equivalent to `sudo su -`. Drops you into a full root login shell.

---

### Run a command as root

```bash
groot dnf update
groot apt install nginx
groot systemctl restart sshd
groot useradd -m newuser
```

Equivalent to prefixing each command with `sudo`.

---

### Run a command, then drop into a root shell

```bash
groot --shell-after whoami
groot --shell-after echo "hello; id"
```

Executes the command with elevated privileges, then immediately opens a root login shell. Arguments containing semicolons, pipes, and redirects are preserved literally using `printf '%q'`.

---

### Dry run — preview without executing

```bash
groot --dry-run dnf install nginx
```

Output:
```
[groot dry-run] sudo dnf install nginx
```

```bash
groot --dry-run --shell-after echo "hello; id"
```

Output:
```
[groot dry-run] sudo echo hello\;\ id
[groot dry-run] (then would open a root login shell)
```

No commands are executed. No privileges are ever elevated during a dry run.

Flags are order-independent — both of these produce identical output:

```bash
groot --shell-after --dry-run echo hi
groot --dry-run --shell-after echo hi
```

---

### Help and version

```bash
groot --help
groot -h
groot --version
```

---

## Flag Reference

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Show usage information and exit |
| `--version` | | Show version and authorship, then exit |
| `--dry-run` | | Print what `groot` *would* execute; never runs any command |
| `--shell-after` | | After running the command, open a root login shell |

Flags may appear in any order before or after the command and its arguments.

---

## Execution Modes

| Condition | Behaviour |
|-----------|-----------|
| No arguments | `exec sudo su -` — opens a root login shell |
| `--dry-run` only | Prints predicted `sudo` command; exits cleanly |
| `--shell-after` only | Runs command as root; then `exec sudo su -` |
| `--dry-run` + `--shell-after` | Prints both predicted actions; exits cleanly |
| Command with no flags | `exec sudo "${cmd_args[@]}"` — standard elevation |

`exec` is used for process replacement wherever possible, ensuring `groot` does not leave a lingering parent process and that signals are handled correctly.

---

## Security Notes

- **`groot` does not bypass authentication.** It relies entirely on your existing `sudo` configuration. If `sudo` requires a password, `groot` will prompt for one.
- **No credentials are stored.** `groot` does not cache, log, or transmit passwords or tokens.
- **No security mechanisms are altered.** Installation adds a single executable file; nothing in `/etc/sudoers` or PAM is touched.
- **Argument safety.** Non-flag arguments are accumulated in a Bash array and passed to `sudo` using `"${cmd_args[@]}"`, preventing word-splitting. Literal reconstruction for `--shell-after` uses `printf '%q'` to safely quote each argument.
- **Shell metacharacters.** Unquoted semicolons, pipes, and redirects are interpreted by your shell *before* `groot` sees them — this is standard Unix behaviour. To pass them literally to the elevated command, quote the argument: `groot --shell-after echo "hello; id"`.
- **`--dry-run` is safe.** It never calls `sudo`, never elevates privileges, and never executes any external command.
- **RPM package integrity.** The provided `.rpm` is signed with the Willtech GPG key (`RPM-GPG-KEY-Willtech`). Import the key before installing to verify authenticity.

---

## Uninstall

**Script install:**
```bash
sudo rm /usr/local/bin/groot
# or, if installed to /usr/bin:
sudo rm /usr/bin/groot
```

**RPM install:**
```bash
sudo rpm -e groot
```

---

## Repository Layout

```
groot/
├── groot                          # Core Bash script (the main executable)
├── groot.bin                      # Compiled binary (shc output)
├── install                        # Install script — copies groot to /usr/bin
├── install.bin                    # Install script for the compiled binary
├── groot-1.3.0-1.fc43.x86_64.rpm # Pre-built RPM (Fedora 43, x86_64)
├── RPM-GPG-KEY-Willtech           # Public GPG key for RPM verification
├── packaging/
│   ├── groot.spec                 # RPM build specification
│   └── groot-1.3.0-1.fc43.x86_64.rpm
├── images/
│   └── groot.png                  # Screenshot / demo image
├── LICENSE                        # MIT License
└── README.md                      # This file
```

---

## Known Issues & Roadmap

The following are tracked in the [issue tracker](https://github.com/Willtech/groot/issues):

- **[#1](https://github.com/Willtech/groot/issues/1) — Feature: Expose the full `sudo` argument set to groot.** Allow users to pass `sudo`-specific flags (e.g. `-u <user>`, `-E`) through `groot`.
- **[#2](https://github.com/Willtech/groot/issues/2) — Edge case: explicit safe quoting for `groot 'echo "Hello; id"'`.** Ensuring quoted arguments containing shell metacharacters are handled correctly in all execution paths.

---

## Credits

**Author / Developer Manager:**
Reaper Harvester / Oceans Ginsberg / Wills / Master Damian Williamson Grad. /
Professor Damian A. James Williamson Grad. / Graduate Damian Williamson
Founder of **Willtech**, Swan Hill, Victoria, Australia

**AI Collaboration:** Microsoft Copilot — technical design, documentation, and Bash best-practice guidance

**AI Collaboration:** Anthropic Claude — repository analysis, documentation review.

---

## License

```MIT License
MIT License

Copyright (c) 2026 Willtech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
