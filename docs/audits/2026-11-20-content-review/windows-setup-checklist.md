# Windows setup checklist

**What to do:** on a Windows PC, follow the setup page <https://hfr-ortho.github.io/stats-formation/en/getting-started/setup.html> from step 1 to step 8, in order, exactly as written. Tick each line below when you get there.

**When something differs:** write down what you saw, with the exact words on the screen (a photo or screenshot of the message is even better), and what you did next.

## Your computer

- Windows version and edition (Settings → System → About shows them): ____________
- Processor: the *System type* line under *Device specifications* on the same page: ____________
- Managed by HFR (an HFR laptop or desktop) or your own PC? ____________
- Language Windows is set to: ____________
- Date you did the setup: ____________

## Before you start

Each line quotes the page. Tick it if it was as described; if not, write what you saw.

- [ ] "PowerShell on Windows (open the Start menu, type "PowerShell" and press Enter)". As described? If not, what did you see:
- [ ] "about 5 GB free". How much free space did the setup use, if you can tell:
- [ ] "the installers may ask for an administrator password". Which installers asked? Did you have the password, or did you need someone else:
- [ ] "install the software on the computer's own disk (`C:`), not on a network drive". Did any installer offer a folder that is not on `C:`? Which one, and which folder:

## Step 1: R

- [ ] "Click **Download R for macOS** or **Download R for Windows**", then "click **base**, then the download link at the top of the page". As described? If not, what did you see:
- [ ] "The file's name must start with `R-4.6`." File name you got:
- [ ] "Open the downloaded file and accept the defaults." Any question or warning from Windows? Exact words:

## Step 2: uv and Python

- [ ] "open PowerShell and run" `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`. Did it finish without an error? Last lines it printed:
- [ ] "Close the window, open a new one, and install Python": `uv python install 3.13`. As described? If not, what did you see:
- [ ] "`uv --version` prints a version number." What it printed:

## Step 3: Git

- [ ] "download Git from <https://git-scm.com/downloads> and accept the defaults". As described? If not, what did you see:
- [ ] "when the installer asks where to install Git, make sure the folder is on `C:`, not on a network drive such as `K:`". Folder the installer offered:
- [ ] "`git --version` prints a version number." What it printed:

## Step 4: Positron

- [ ] "the download page offers installers for two kinds of processor, x64 (Windows 10 or 11) and ARM64 (Windows 11), each as a *User install* or a *System install*". As described? If not, what did you see:
- [ ] Not on the page, a question: does Positron's download page show a button that recommends an installer for your PC (for example "Recommended for your PC")? Its exact words, and which installer it points to:
- [ ] "open **Settings → System → About**: if the *System type* line under *Device specifications* contains the word "ARM", take an ARM64 installer". As described? Which installer did you take, User or System:
- [ ] "a user install goes into your own user folder (`C:\Users\<your user name>\AppData\Local\Programs\Positron`)" and "a system install goes into `C:\Program Files\Positron`". Where did yours go:

## Step 5: getting the files

- [ ] "In Terminal (Mac) or PowerShell (Windows), make a `projects` folder and download ("clone") the repository into it": `mkdir -p ~/projects`, then `cd ~/projects`, then `git clone https://github.com/hfr-ortho/stats-formation.git`. Did each command work in PowerShell? Any message:
- [ ] "`~` stands for your home folder […] usually `C:\Users\<your user name>` on Windows". Where did the `projects` folder end up:
- [ ] "`Documents` and `Desktop` are often synced by […] OneDrive (Windows)". Is your home folder, or `projects`, synced by OneDrive?
- [ ] "`git clone` starts with `Cloning into 'stats-formation'...` and prints no line that starts with `fatal`". What it printed (if a line starts with `fatal`, copy it whole):
- [ ] "in Positron: **File → Open Folder…**, go to your home folder […], open `projects` and choose `stats-formation`". As described? If not, what did you see:
- [ ] "In Positron, the file list on the left (click the Explorer icon if you don't see it) shows the repository's folders, among them `data` and `scripts`." As described?

Only if you also try the route without Git (the section "Without Git: download a ZIP file"):

- [ ] "right-click the file, choose **Extract All** and follow the instructions". As described? Did it give you a `stats-formation-main` folder with `data` and `scripts` directly inside, or a `stats-formation-main` folder with only another `stats-formation-main` folder inside:
- [ ] "on Windows, make it in your home folder, usually `C:\Users\<your user name>`". As described?

## Step 6: the R packages

- [ ] "Positron starts R by itself when it opens a folder with a `renv.lock` file". Did it?
- [ ] "The **Interpreter picker**, at the top right of the Positron window, shows the session that is running, for example R 4.6.2." What did it show? If you had to use "**New Console Session…**", was it there as described?
- [ ] "When R starts in this folder for the first time, it may print `Bootstrapping renv` and `One or more packages recorded in the lockfile are not installed.`" What did R print when it started:
- [ ] "`renv::restore()` […] Answer **Y** if asked. […] It takes a few minutes." How long did it take? Did it ask anything else?
- [ ] "the output ends without a line that starts with `Error`". Last lines it printed:
- [ ] "run `renv::status()` in the same console: it answers `No issues found -- the project is in a consistent state.`" What it answered:

## Step 7: the Python packages

- [ ] "Open Positron's terminal (**Terminal → New Terminal**). It opens in the repository folder." As described? Was it PowerShell or something else:
- [ ] "the first time, `uv sync` prints `Creating virtual environment at: .venv`, then one line for each package it installed, starting with `+`. No line starts with `error`." As described? If not, what did you see:
- [ ] "click the **Interpreter picker**, choose **New Console Session…** and pick the Python whose path includes `.venv`". As described? What did the list show:
- [ ] "Positron may offer some of this itself." Did Positron offer to run `uv sync` or to start a console? Its exact words:

## Step 8: the checks

- [ ] In Positron's terminal, `Rscript scripts/check_setup.R`. Was `Rscript` "not recognized"? If so, did `source("scripts/check_setup.R")` in Positron's R console work instead?
- [ ] `uv run python scripts/check_setup.py`. As described?
- [ ] "Each check ends with `All good - you are ready.`" Did both? Copy any line that says `PROBLEM`:
- [ ] "the R check may print three lines that begin `Registered S3 method overwritten by 'lme4':`". Did it?

## Updating your copy

- [ ] "run `git pull`. If nothing has changed, it prints `Already up to date.` (or the same in your system's language)." What it printed:

## Troubleshooting rows that name Windows

Only if you met the problem; otherwise leave the line empty.

- [ ] "`uv: command not found`, or "not recognized"": "Close the terminal window, open a new one, and try again." Did that fix it?
- [ ] "open the Command Palette (Cmd+Shift+P on a Mac, Ctrl+Shift+P on Windows), type `Interpreter: Restart Active Interpreter Session` and press Return (Mac) or Enter (Windows)". As described?
- [ ] "<https://cloud.r-project.org/bin/windows/base/old/> (Windows)": if you needed an older R, did this page offer R 4.6?
- [ ] "`Could not resolve host: github.com`": "run `where.exe git` in PowerShell. If the answer starts with `K:` or another network drive, uninstall Git and install it again (step 3) in a folder on `C:`." What did `where.exe git` answer? Did reinstalling fix it?

## At the end

- How long did the whole setup take, from step 1 to the end of step 8: ____________
- Anything else that confused you or that the page doesn't mention:

Send the filled-in list to the person who gave you this list.
