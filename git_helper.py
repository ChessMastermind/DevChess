#!/usr/bin/env python3
import curses
import os
import subprocess
import sys
import signal
import time
import threading

# --- Configuration Constants ---
MIN_HEIGHT = 24
MIN_WIDTH = 80

# --- Global Variable for Update Checking ---
_cached_update_status = False

# --- Signal Handling for graceful exit ---
def signal_handler(sig, frame):
    curses.endwin()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTSTP, signal_handler)     # Ctrl+Z

# --- Helper Functions ---
def run_command(command):
    """
    Runs a shell command and returns (output, return_code).
    Combines stdout and stderr.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout + result.stderr
        return output, result.returncode
    except Exception as e:
        return str(e), 1

def check_min_window(stdscr):
    """If the window is too small, ask the user to enlarge it."""
    height, width = stdscr.getmaxyx()
    if height < MIN_HEIGHT or width < MIN_WIDTH:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Window too small! Minimum size: {MIN_WIDTH}x{MIN_HEIGHT}.", curses.color_pair(3))
        stdscr.addstr(1, 0, f"Current size: {width}x{height}.", curses.color_pair(3))
        stdscr.addstr(3, 0, "Please enlarge the window and press any key to continue.", curses.color_pair(3))
        stdscr.refresh()
        stdscr.getch()
        return False
    return True

def get_user_input(stdscr, prompt, row, col):
    """
    Displays a prompt at the specified location and collects input.
    If the user presses ESC, returns None.
    """
    stdscr.addstr(row, col, prompt)
    stdscr.move(row, col + len(prompt))
    stdscr.refresh()
    curses.echo()
    input_str = ""
    while True:
        ch = stdscr.getch()
        if ch == 27:  # ESC key
            curses.noecho()
            return None
        elif ch in (10, 13):  # Enter key
            break
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if len(input_str) > 0:
                input_str = input_str[:-1]
                y, x = stdscr.getyx()
                stdscr.move(y, x - 1)
                stdscr.delch()
        else:
            input_str += chr(ch)
    curses.noecho()
    return input_str.strip()

def update_checker():
    """
    Runs in a background thread.
    Once per minute, if a remote exists, does a git fetch and
    updates the cached update status.
    """
    global _cached_update_status
    while True:
        if os.path.isdir('.git'):
            remote_out, code = run_command("git remote get-url origin")
            if code == 0 and remote_out.strip():
                # Run fetch and then check status.
                run_command("git fetch")
                status_out, _ = run_command("git status -uno")
                if "Your branch is behind" in status_out:
                    _cached_update_status = True
                else:
                    _cached_update_status = False
        else:
            _cached_update_status = False
        time.sleep(60)  # wait one minute before next check

def check_for_updates():
    """Simply returns the cached update status."""
    return _cached_update_status

def draw_header(stdscr):
    """
    Draws the header at the top of the window.
    The header displays the repository name (centered) and, on a second line,
    a notification if new updates are available.
    """
    height, width = stdscr.getmaxyx()
    if not os.path.isdir('.git'):
        repo_name = "Not a Git Repository"
    else:
        remote_out, code = run_command("git remote get-url origin")
        if code == 0 and remote_out.strip():
            repo_name = remote_out.strip().split('/')[-1]
            if repo_name.endswith(".git"):
                repo_name = repo_name[:-4]
        else:
            repo_name = "Local Git Repository"
    header_str = f" Repository: {repo_name} "
    start_x = max((width - len(header_str)) // 2, 0)
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(0, 0, " " * width)
    stdscr.addstr(0, start_x, header_str)
    stdscr.attroff(curses.color_pair(1))
    stdscr.hline(1, 0, curses.ACS_HLINE, width)
    if check_for_updates():
        update_msg = "Attention: New updates available!"
        start_msg = max((width - len(update_msg)) // 2, 0)
        stdscr.addstr(2, start_msg, update_msg, curses.color_pair(4))
    else:
        stdscr.move(2, 0)
        stdscr.clrtoeol()

def initialize_repository(stdscr):
    """Initializes a Git repository if one does not exist."""
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(4, 2, "Initializing Git repository...", curses.A_BOLD)
    stdscr.refresh()
    out, code = run_command("git init")
    if code == 0:
        stdscr.addstr(6, 2, "Repository initialized successfully.", curses.color_pair(4))
    else:
        stdscr.addstr(6, 2, "Error initializing repository.", curses.color_pair(3))
        stdscr.addstr(7, 2, out, curses.color_pair(3))
    stdscr.addstr(9, 2, "Press any key to continue...")
    stdscr.getch()

def connect_remote(stdscr):
    """
    Offers the user a choice to create a new GitHub repository or import an existing remote URL.
    Only offered if no remote is connected.
    """
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(4, 2, "No remote repository connected.", curses.color_pair(3))
    stdscr.addstr(5, 2, "Press 'C' to create a new GitHub repo or 'I' to import an existing remote URL.", curses.A_BOLD)
    stdscr.addstr(6, 2, "Press any other key to cancel.")
    stdscr.refresh()
    ch = stdscr.getch()
    if chr(ch).lower() == 'c':
        create_github_repo(stdscr)
    elif chr(ch).lower() == 'i':
        remote_url = get_user_input(stdscr, "Enter remote URL: ", 8, 2)
        if remote_url:
            out, code = run_command(f"git remote add origin {remote_url}")
            if code == 0:
                stdscr.addstr(10, 2, "Remote added successfully.", curses.color_pair(4))
            else:
                stdscr.addstr(10, 2, "Failed to add remote.", curses.color_pair(3))
        else:
            stdscr.addstr(10, 2, "Operation cancelled.", curses.color_pair(3))
        stdscr.addstr(12, 2, "Press any key to continue...")
        stdscr.getch()
    else:
        stdscr.addstr(8, 2, "Operation cancelled.", curses.color_pair(3))
        stdscr.addstr(10, 2, "Press any key to continue...")
        stdscr.getch()

def create_github_repo(stdscr):
    """
    Creates a GitHub repository using gh.
    Stages all files, commits (if needed) and pushes.
    """
    stdscr.clear()
    draw_header(stdscr)
    if not os.path.isdir('.git'):
        stdscr.addstr(4, 2, "Not a Git repository. Please initialize first.", curses.color_pair(3))
        stdscr.addstr(6, 2, "Press any key to return.")
        stdscr.getch()
        return

    stdscr.addstr(4, 2, "Staging all files...", curses.A_BOLD)
    stdscr.refresh()
    run_command("git add -A")
    stdscr.addstr(5, 2, "Creating initial commit...", curses.A_BOLD)
    stdscr.refresh()
    out_commit, code_commit = run_command("git commit -m 'Initial commit'")
    if code_commit != 0:
        if "nothing to commit" in out_commit.lower():
            stdscr.addstr(6, 2, "Nothing to commit. (Maybe an initial commit already exists.)", curses.color_pair(3))
        else:
            stdscr.addstr(6, 2, "Error during commit:", curses.color_pair(3))
            stdscr.addstr(7, 2, out_commit, curses.color_pair(3))
    else:
        stdscr.addstr(6, 2, "Initial commit created.", curses.color_pair(4))
    repo_name = get_user_input(stdscr, "Enter new repository name: ", 8, 2)
    if repo_name is None or repo_name == "":
        stdscr.addstr(10, 2, "Repository name cannot be empty. Operation cancelled.", curses.color_pair(3))
        stdscr.addstr(12, 2, "Press any key to continue...")
        stdscr.getch()
        return

    gh_cmd = f"gh repo create {repo_name} --public --source=. --remote=origin --push --confirm"
    stdscr.addstr(10, 2, f"Creating GitHub repository '{repo_name}'...", curses.A_BOLD)
    stdscr.refresh()
    out_gh, code_gh = run_command(gh_cmd)
    if code_gh == 0:
        stdscr.addstr(12, 2, "GitHub repository created and pushed successfully.", curses.color_pair(4))
    else:
        stdscr.addstr(12, 2, "Error creating GitHub repository:", curses.color_pair(3))
        stdscr.addstr(13, 2, out_gh, curses.color_pair(3))
    stdscr.addstr(15, 2, "Press any key to continue...")
    stdscr.getch()

def add_files(stdscr):
    """
    Prompts for a file pattern (or all files if blank) and runs git add.
    Pressing ESC cancels the operation.
    """
    stdscr.clear()
    draw_header(stdscr)
    pattern = get_user_input(stdscr, "Enter file pattern to add (leave blank to add all files): ", 4, 2)
    if pattern is None:
        stdscr.addstr(6, 2, "Operation cancelled.", curses.color_pair(3))
        stdscr.addstr(8, 2, "Press any key to continue...")
        stdscr.getch()
        return
    cmd = "git add -A" if pattern == "" else f"git add {pattern}"
    out, code = run_command(cmd)
    if code == 0:
        stdscr.addstr(6, 2, "Files added successfully.", curses.color_pair(4))
    else:
        stdscr.addstr(6, 2, "Error adding files:", curses.color_pair(3))
        stdscr.addstr(7, 2, out, curses.color_pair(3))
    stdscr.addstr(9, 2, "Press any key to continue...")
    stdscr.getch()

def commit_changes(stdscr):
    """
    Prompts for a commit message, stages all files, and commits.
    ESC cancels the operation.
    """
    stdscr.clear()
    draw_header(stdscr)
    commit_msg = get_user_input(stdscr, "Enter commit message: ", 4, 2)
    if commit_msg is None or commit_msg == "":
        stdscr.addstr(6, 2, "Commit cancelled (empty message).", curses.color_pair(3))
        stdscr.addstr(8, 2, "Press any key to continue...")
        stdscr.getch()
        return
    stdscr.addstr(6, 2, "Staging all files...", curses.A_BOLD)
    stdscr.refresh()
    run_command("git add -A")
    stdscr.addstr(7, 2, "Committing changes...", curses.A_BOLD)
    stdscr.refresh()
    out_commit, code_commit = run_command(f'git commit -m "{commit_msg}"')
    if code_commit == 0:
        stdscr.addstr(8, 2, "Changes committed successfully.", curses.color_pair(4))
    else:
        if "nothing to commit" in out_commit.lower():
            stdscr.addstr(8, 2, "Nothing to commit.", curses.color_pair(3))
        else:
            stdscr.addstr(8, 2, "Error during commit:", curses.color_pair(3))
            stdscr.addstr(9, 2, out_commit, curses.color_pair(3))
    stdscr.addstr(11, 2, "Press any key to continue...")
    stdscr.getch()

def push_repo(stdscr):
    """Pushes local commits to the remote repository."""
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(4, 2, "Pushing changes to remote...", curses.A_BOLD)
    stdscr.refresh()
    out, code = run_command("git push")
    if code == 0:
        stdscr.addstr(6, 2, "Push successful.", curses.color_pair(4))
    else:
        stdscr.addstr(6, 2, "Error during push:", curses.color_pair(3))
        stdscr.addstr(7, 2, out, curses.color_pair(3))
    stdscr.addstr(9, 2, "Press any key to continue...")
    stdscr.getch()

def pull_repo(stdscr):
    """Pulls changes from the remote repository."""
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(4, 2, "Pulling changes from remote...", curses.A_BOLD)
    stdscr.refresh()
    out, code = run_command("git pull")
    if code == 0:
        stdscr.addstr(6, 2, "Pull successful.", curses.color_pair(4))
    else:
        stdscr.addstr(6, 2, "Error during pull:", curses.color_pair(3))
        stdscr.addstr(7, 2, out, curses.color_pair(3))
    stdscr.addstr(9, 2, "Press any key to continue...")
    stdscr.getch()

def git_status(stdscr):
    """Displays the output of 'git status'."""
    stdscr.clear()
    draw_header(stdscr)
    out, _ = run_command("git status")
    row = 4
    for line in out.splitlines():
        stdscr.addstr(row, 2, line)
        row += 1
        if row >= curses.LINES - 2:
            break
    stdscr.addstr(row + 1, 2, "Press any key to continue...")
    stdscr.getch()

def create_issue(stdscr):
    """
    Prompts for an issue title and body, then creates a GitHub issue via gh.
    """
    stdscr.clear()
    draw_header(stdscr)
    title = get_user_input(stdscr, "Enter issue title: ", 4, 2)
    if title is None or title == "":
        stdscr.addstr(6, 2, "Issue creation cancelled.", curses.color_pair(3))
        stdscr.addstr(8, 2, "Press any key to continue...")
        stdscr.getch()
        return
    body = get_user_input(stdscr, "Enter issue body (optional): ", 6, 2)
    cmd = f'gh issue create --title "{title}"'
    if body:
        cmd += f' --body "{body}"'
    stdscr.addstr(8, 2, "Creating issue...", curses.A_BOLD)
    stdscr.refresh()
    out, code = run_command(cmd)
    if code == 0:
        stdscr.addstr(10, 2, "Issue created successfully.", curses.color_pair(4))
    else:
        stdscr.addstr(10, 2, "Error creating issue:", curses.color_pair(3))
        stdscr.addstr(11, 2, out, curses.color_pair(3))
    stdscr.addstr(13, 2, "Press any key to continue...")
    stdscr.getch()

def view_log(stdscr):
    """Displays the last 10 commits using 'git log --oneline'."""
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(4, 2, "Recent commit log (last 10 commits):", curses.A_BOLD)
    out, _ = run_command("git log --oneline -n 10")
    row = 6
    for line in out.splitlines():
        stdscr.addstr(row, 2, line)
        row += 1
        if row >= curses.LINES - 2:
            break
    stdscr.addstr(row + 1, 2, "Press any key to continue...")
    stdscr.getch()

def get_menu_options():
    """
    Returns a dynamic list of menu options based on repository state.
    Options for initializing or connecting a repo are shown only if needed.
    """
    options = []
    if not os.path.isdir('.git'):
        options.append("Initialize Repository")
    else:
        remote_out, code = run_command("git remote get-url origin")
        if code != 0 or not remote_out.strip():
            options.append("Connect GitHub Repository")
    options.extend([
        "Add Files",
        "Commit Changes",
        "Push to Remote",
        "Pull from Remote",
        "Git Status",
        "Create Issue",
        "View Log",
        "Exit"
    ])
    return options

# --- Main Menu Loop ---
def main_menu(stdscr):
    curses.curs_set(0)
    current_row = 0

    while True:
        if not check_min_window(stdscr):
            continue
        stdscr.clear()
        draw_header(stdscr)
        menu_options = get_menu_options()
        for idx, option in enumerate(menu_options):
            if idx == current_row:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(4 + idx, 2, option)
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(4 + idx, 2, option)
        # --- Display File Status Section ---
        status_out, _ = run_command("git status --short")
        status_lines = status_out.splitlines()
        start_row = 4 + len(menu_options) + 2
        width = curses.COLS
        stdscr.hline(start_row, 0, '-', width)
        stdscr.addstr(start_row, 2, "File Status (git status --short):")
        available_rows = curses.LINES - (start_row + 2)
        if len(status_lines) > available_rows:
            for i in range(available_rows - 1):
                stdscr.addstr(start_row + 1 + i, 2, status_lines[i])
            more_count = len(status_lines) - (available_rows - 1)
            stdscr.addstr(start_row + available_rows, 2, f"... and {more_count} more lines")
        else:
            for i, line in enumerate(status_lines):
                stdscr.addstr(start_row + 1 + i, 2, line)
        stdscr.refresh()
        key = stdscr.getch()
        if key == 27:  # ESC from main menu exits the program.
            break
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            selected = menu_options[current_row]
            if selected == "Initialize Repository":
                initialize_repository(stdscr)
            elif selected == "Connect GitHub Repository":
                connect_remote(stdscr)
            elif selected == "Add Files":
                add_files(stdscr)
            elif selected == "Commit Changes":
                commit_changes(stdscr)
            elif selected == "Push to Remote":
                push_repo(stdscr)
            elif selected == "Pull from Remote":
                pull_repo(stdscr)
            elif selected == "Git Status":
                git_status(stdscr)
            elif selected == "Create Issue":
                create_issue(stdscr)
            elif selected == "View Log":
                view_log(stdscr)
            elif selected == "Exit":
                break
            time.sleep(0.2)
            current_row = 0  # Reset selection after an operation

def main(stdscr):
    # Set a low ESC delay for responsiveness.
    curses.set_escdelay(25)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) # Selected option
    curses.init_pair(3, curses.COLOR_RED, -1)                  # Error messages
    curses.init_pair(4, curses.COLOR_GREEN, -1)                # Success/notification messages

    # Start the update checking thread.
    threading.Thread(target=update_checker, daemon=True).start()
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
