#!/usr/bin/env python3
import curses
import os
import subprocess
import sys
import signal

# --- Helper Functions ---
def run_command(command):
    """
    Runs a shell command and returns a tuple (output, return_code)
    with both stdout and stderr combined.
    """
    try:
        result = subprocess.run(
            command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout + result.stderr, result.returncode
    except Exception as e:
        return str(e), 1

def get_user_input(stdscr, prompt, row, col):
    """
    Displays a prompt at the specified location and collects user input.
    Pressing ESC returns None immediately.
    """
    stdscr.addstr(row, col, prompt)
    stdscr.move(row, col + len(prompt))
    stdscr.refresh()
    curses.echo()
    input_str = ""
    while True:
        ch = stdscr.getch()
        if ch == 27:  # ESC key pressed
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

def draw_header(stdscr):
    """
    Draws a header on the top of the window that shows the repository name.
    If no Git repository is detected the header shows an appropriate message.
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

# --- Combined Function for Main Menu Option ---
def commit_and_push_all(stdscr):
    stdscr.clear()
    draw_header(stdscr)
    commit_msg = get_user_input(stdscr, "Enter commit message: ", 4, 2)
    if commit_msg is None or commit_msg == "":
        stdscr.addstr(6, 2, "Commit cancelled.", curses.color_pair(3))
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
        stdscr.addstr(8, 2, "Changes committed.", curses.color_pair(4))
    else:
        if "nothing to commit" in out_commit.lower():
            stdscr.addstr(8, 2, "Nothing to commit.", curses.color_pair(3))
        else:
            stdscr.addstr(8, 2, "Error during commit:", curses.color_pair(3))
            stdscr.addstr(9, 2, out_commit, curses.color_pair(3))
    stdscr.addstr(10, 2, "Pushing changes...", curses.A_BOLD)
    stdscr.refresh()
    out_push, code_push = run_command("git push")
    if code_push == 0:
        stdscr.addstr(11, 2, "Push successful.", curses.color_pair(4))
    else:
        stdscr.addstr(11, 2, "Error during push:", curses.color_pair(3))
        stdscr.addstr(12, 2, out_push, curses.color_pair(3))
    stdscr.addstr(14, 2, "Press any key to continue...")
    stdscr.getch()

def pull_all(stdscr):
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

# --- Advanced Functions (reusing some implementations) ---
def add_files(stdscr):
    stdscr.clear()
    draw_header(stdscr)
    pattern = get_user_input(stdscr, "Enter file pattern to add (blank for all): ", 4, 2)
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
    stdscr.clear()
    draw_header(stdscr)
    commit_msg = get_user_input(stdscr, "Enter commit message: ", 4, 2)
    if commit_msg is None or commit_msg == "":
        stdscr.addstr(6, 2, "Commit cancelled.", curses.color_pair(3))
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
        stdscr.addstr(8, 2, "Changes committed.", curses.color_pair(4))
    else:
        if "nothing to commit" in out_commit.lower():
            stdscr.addstr(8, 2, "Nothing to commit.", curses.color_pair(3))
        else:
            stdscr.addstr(8, 2, "Error during commit:", curses.color_pair(3))
            stdscr.addstr(9, 2, out_commit, curses.color_pair(3))
    stdscr.addstr(11, 2, "Press any key to continue...")
    stdscr.getch()

def push_repo(stdscr):
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

def view_log(stdscr):
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

def create_issue(stdscr):
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

def show_diff(stdscr):
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(4, 2, "Diff:", curses.A_BOLD)
    out, _ = run_command("git diff")
    row = 6
    for line in out.splitlines():
        stdscr.addstr(row, 2, line)
        row += 1
        if row >= curses.LINES - 2:
            break
    stdscr.addstr(row + 1, 2, "Press any key to continue...")
    stdscr.getch()

# --- Menu Functions ---
def main_menu(stdscr):
    curses.curs_set(0)
    current_row = 0
    menu_options = ["Commit & Push all", "Pull all", "Create Issue", "Advance menu"]
    while True:
        stdscr.clear()
        draw_header(stdscr)
        # Display main menu options
        for idx, option in enumerate(menu_options):
            if idx == current_row:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(4 + idx, 2, option)
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(4 + idx, 2, option)
        # Display "git status --short" below the menu
        status_out, _ = run_command("git status --short")
        status_lines = status_out.splitlines()
        start_row = 4 + len(menu_options) + 2
        stdscr.hline(start_row, 0, '-', curses.COLS)
        stdscr.addstr(start_row, 2, "File Status (git status --short):")
        available_rows = curses.LINES - (start_row + 2)
        for i, line in enumerate(status_lines[:available_rows]):
            stdscr.addstr(start_row + 1 + i, 2, line)
        stdscr.refresh()
        key = stdscr.getch()
        if key == 27:  # ESC in main menu exits program
            break
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            selected = menu_options[current_row]
            if selected == "Commit & Push all":
                commit_and_push_all(stdscr)
            elif selected == "Pull all":
                pull_all(stdscr)
            elif selected == "Create Issue":
                create_issue(stdscr)
            elif selected == "Advance menu":
                advanced_menu(stdscr)
            current_row = 0  # Reset selection after an operation

def advanced_menu(stdscr):
    curses.curs_set(0)
    current_row = 0
    adv_options = [
        "Add Files",
        "Commit Changes",
        "Push to Remote",
        "Pull from Remote",
        "Git Status",
        "Create Issue",
        "View Log",
        "Show Diff",
        "Back to Main Menu"
    ]
    while True:
        stdscr.clear()
        draw_header(stdscr)
        # Display advanced menu options
        for idx, option in enumerate(adv_options):
            if idx == current_row:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(4 + idx, 2, option)
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(4 + idx, 2, option)
        # Display "git status --short" below the advanced menu
        status_out, _ = run_command("git status --short")
        status_lines = status_out.splitlines()
        start_row = 4 + len(adv_options) + 2
        stdscr.hline(start_row, 0, '-', curses.COLS)
        stdscr.addstr(start_row, 2, "File Status (git status --short):")
        available_rows = curses.LINES - (start_row + 2)
        for i, line in enumerate(status_lines[:available_rows]):
            stdscr.addstr(start_row + 1 + i, 2, line)
        stdscr.refresh()
        key = stdscr.getch()
        if key == 27:  # ESC in advanced menu returns to main menu
            break
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(adv_options) - 1:
            current_row += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            selected = adv_options[current_row]
            if selected == "Add Files":
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
            elif selected == "Show Diff":
                show_diff(stdscr)
            elif selected == "Back to Main Menu":
                break
            current_row = 0  # Reset after an operation

# --- Signal Handling ---
def signal_handler(sig, frame):
    curses.endwin()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)

# --- Main ---
def main(stdscr):
    curses.set_escdelay(25)
    curses.start_color()
    curses.use_default_colors()
    # Color pair 1: Header (white on blue)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    # Color pair 2: Selected menu option (black on white)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # Color pair 3: Error messages (red)
    curses.init_pair(3, curses.COLOR_RED, -1)
    # Color pair 4: Success/notification messages (green)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
