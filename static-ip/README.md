# make-static-ip

Gives each course VM a permanent address from the 10.5.103.x course block, recorded in the instructor's address registry. See Assignment 3, Part A, Step 1.

Students working from a web console, where pasting isn't possible, can type one of these short commands instead.

**Ubuntu (lastname-srv, lastname-tgt):**

    curl -fsSL tinyurl.com/cs4910-sh -o make-static-ip.sh && sudo bash make-static-ip.sh

**Windows (lastname-win, elevated PowerShell console):**

    iwr -useb tinyurl.com/cs4910-ps -OutFile make-static-ip.ps1; powershell -ExecutionPolicy Bypass -File .\make-static-ip.ps1

The file stays in the home folder, so you can confirm the result later with `sudo bash make-static-ip.sh --check` or `.\make-static-ip.ps1 -Check`.
