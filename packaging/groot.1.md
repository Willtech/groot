# `groot(1)` — A Friendly Sudo Wrapper for Linux

## NAME
**groot** — a friendly sudo wrapper for Linux

## SYNOPSIS
```
groot
groot <command> [args]
groot [--dry-run] [--shell-after] <command> [args]
groot [--help] [--version]
```

## DESCRIPTION
**groot** is a lightweight Bash utility that provides a clean, expressive interface for privilege elevation. It wraps `sudo` with predictable behaviour, optional literal‑command execution, and a safe dry‑run preview mode. It is designed for administrators, developers, and power users who want a simple, memorable way to elevate privileges without typing long commands.

When invoked with no arguments, **groot** opens a full root login shell. When given a command, it executes that command as root using `sudo`. When used with `--shell-after`, groot executes the command literally and then opens a root login shell. When used with `--dry-run`, groot prints what it *would* execute without running anything.

## OPTIONS

### `-h`, `--help`
Show help information and exit.

### `--version`
Show version information and exit.

### `--dry-run`
Do not execute anything. Instead, print the exact `sudo` command that groot would run. Applies to both normal and literal modes.

### `--shell-after`
Execute the provided command literally, preserving quoting, semicolons, pipes, and other shell characters, then open a root login shell.

### `--dry-run --shell-after`
Combine both behaviours: print the literal command groot would run, followed by a note indicating that a root login shell would be opened. No commands are executed.

## BEHAVIOUR

### No arguments
Opens a root login shell:
```
sudo su -
```

### Normal command execution
Executes the command as root:
```
sudo <command> [args]
```

### Literal execution with shell
Reconstructs the command literally using `printf '%q'`, executes it as root, then opens a root login shell.

### Dry-run
Prints the exact sudo command groot would run, without executing anything.

### Dry-run + shell-after
Prints the literal sudo command and indicates that a root shell would follow. No commands are executed.

## EXAMPLES

### Open a root login shell
```
groot
```

### Run a command as root
```
groot dnf update
```

### Run a command literally, then enter a root shell
```
groot --shell-after 'echo "hello; id"'
```

### Preview what groot would run
```
groot --dry-run dnf install nginx
```

Output:
```
[groot dry-run] sudo dnf install nginx
```

### Preview literal execution and shell-after
```
groot --dry-run --shell-after 'echo "hello; id"'
```

Output:
```
[groot dry-run] sudo echo "hello; id"
[groot dry-run] (then would open a root login shell)
```

## SECURITY
**groot** does not bypass authentication. It relies entirely on the system’s existing `sudo` configuration. No passwords are stored, and no security mechanisms are modified. Literal commands are reconstructed safely using `printf '%q'`. Unquoted semicolons are interpreted by the user’s shell before groot runs.

## AUTHOR
MR. Damian A. James Williamson Grad.  
Willtech, Swan Hill, Victoria.  
AI Collaboration: Microsoft Copilot (technical design and documentation).

## LICENSE
MIT License. See the project repository for full text.

## SEE ALSO
`sudo(8)`, `bash(1)`

