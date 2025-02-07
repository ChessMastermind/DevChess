#!/usr/bin/env python3
import curses
import os
import subprocess
import sys

# Minimum dimensions for the terminal window.
MIN_HEIGHT = 24
MIN_WIDTH = 80

def run_command(command):
    """
    Runs a shell command and returns a tuple (output, return_code).
    Combines both stdout and stderr.
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
    height, width = stdscr.getmaxyx()
    if height < MIN_HEIGHT or width < MIN_WIDTH:
        stdscr.clear()
        stdscr.addstr(
            0, 0,
            f"Window too small! Minimum size: {MIN_WIDTH}x{MIN_HEIGHT}. Current size: {width}x{height}",
            curses.color_pair(3)
        )
        stdscr.addstr(2, 0, "Please resize the window and try again. Press any key to exit.")
        stdscr.getch()
        sys.exit(1)

def get_repo_name():
    """
    Returns a repository name string based on whether a Git repository exists
    and whether it has a remote called origin.
    """
    if not os.path.isdir('.git'):
        return "Not a Git Repository"
    out, code = run_command("git remote get-url origin")
    if code == 0 and out.strip():
        # Expect remote URL forms like:
        #   git@github.com:user/repo.git
        #   https://github.com/user/repo.git
        repo_name = out.strip().split('/')[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]
        return repo_name
    else:
        return "Local Git Repository"

def draw_header(stdscr):
    """
    Draws a header on the top row with the repository name centered.
    Also draws a horizontal line below.
    """
    height, width = stdscr.getmaxyx()
    repo_name = get_repo_name()
    header_str = f" Repository: {repo_name} "
    start_x = max((width - len(header_str)) // 2, 0)
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(0, 0, " " * width)
    stdscr.addstr(0, start_x, header_str)
    stdscr.attroff(curses.color_pair(1))
    stdscr.hline(1, 0, curses.ACS_HLINE, width)

def ensure_git_repo(stdscr):
    """
    Checks if the current directory is a Git repository. If not, prompts the user
    to initialize one. Returns True if a repository exists (or is just created),
    or False if the user cancels.
    """
    if not os.path.isdir('.git'):
        stdscr.clear()
        draw_header(stdscr)
        stdscr.addstr(3, 0, "This directory is not a Git repository.", curses.color_pair(3))
        stdscr.addstr(4, 0, "Would you like to initialize one? (y/n): ")
        stdscr.refresh()
        ch = stdscr.getch()
        if chr(ch).lower() == 'y':
            out, code = run_command("git init")
            if code == 0:
                stdscr.addstr(6, 0, "Git repository initialized successfully.", curses.color_pair(4))
            else:
                stdscr.addstr(6, 0, "Error initializing repository.", curses.color_pair(3))
            stdscr.addstr(8, 0, "Press any key to continue...")
            stdscr.getch()
        else:
            stdscr.addstr(6, 0, "Operation cancelled. Press any key to return.", curses.color_pair(3))
            stdscr.getch()
            return False
    return True

def connect_remote(stdscr):
    """
    If no remote is connected, offers the user the option to create a new GitHub repository
    or import an existing remote URL.
    """
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(3, 0, "No remote repository connected.", curses.color_pair(3))
    stdscr.addstr(4, 0,
                  "Press 'C' to create a new GitHub repo, 'I' to import an existing remote URL, or any other key to cancel: ")
    stdscr.refresh()
    ch = stdscr.getch()
    if chr(ch).lower() == 'c':
        create_github_repo(stdscr)
    elif chr(ch).lower() == 'i':
        stdscr.addstr(6, 0, "Enter remote URL: ")
        curses.echo()
        remote_url = stdscr.getstr(6, 18).decode('utf-8').strip()
        curses.noecho()
        if remote_url:
            out, code = run_command(f"git remote add origin {remote_url}")
            if code == 0:
                stdscr.addstr(8, 0, "Remote added successfully.", curses.color_pair(4))
            else:
                stdscr.addstr(8, 0, "Failed to add remote.", curses.color_pair(3))
        else:
            stdscr.addstr(8, 0, "No URL provided. Operation cancelled.", curses.color_pair(3))
        stdscr.addstr(10, 0, "Press any key to continue...")
        stdscr.getch()
    else:
        stdscr.addstr(6, 0, "Operation cancelled. Press any key.")
        stdscr.getch()

def create_github_repo(stdscr):
    """
    Creates (or connects) a GitHub repository using gh. This function:
      1. Checks for (and if necessary, initializes) a local Git repository.
      2. Stages all files and attempts an initial commit.
      3. Prompts for a repository name.
      4. Uses gh to create the GitHub repo (with the current directory as source),
         sets remote origin, and pushes the commit.
    """
    stdscr.clear()
    draw_header(stdscr)
    if not ensure_git_repo(stdscr):
        return

    stdscr.addstr(3, 0, "Staging all files...", curses.A_BOLD)
    stdscr.refresh()
    out, _ = run_command("git add -A")
    stdscr.addstr(4, 0, out)
    stdscr.refresh()

    stdscr.addstr(5, 0, "Creating initial commit...", curses.A_BOLD)
    stdscr.refresh()
    out_commit, code_commit = run_command("git commit -m 'Initial commit'")
    if code_commit != 0:
        if "nothing to commit" in out_commit.lower():
            stdscr.addstr(6, 0, "Nothing to commit. (Maybe an initial commit already exists.)", curses.color_pair(3))
        else:
            stdscr.addstr(6, 0, "Error during commit:", curses.color_pair(3))
            stdscr.addstr(7, 0, out_commit, curses.color_pair(3))
    else:
        stdscr.addstr(6, 0, "Initial commit created.", curses.color_pair(4))
    stdscr.addstr(8, 0, "Enter new repository name: ")
    stdscr.refresh()
    curses.echo()
    repo_name = stdscr.getstr(8, 27).decode('utf-8').strip()
    curses.noecho()
    if not repo_name:
        stdscr.addstr(10, 0, "Repository name cannot be empty. Press any key to return.", curses.color_pair(3))
        stdscr.getch()
        return

    gh_cmd = f"gh repo create {repo_name} --public --source=. --remote=origin --push --confirm"
    stdscr.addstr(10, 0, f"Creating GitHub repository '{repo_name}'...", curses.A_BOLD)
    stdscr.refresh()
    out_gh, code_gh = run_command(gh_cmd)
    if code_gh == 0:
        stdscr.addstr(12, 0, "GitHub repository created and pushed successfully.", curses.color_pair(4))
    else:
        stdscr.addstr(12, 0, "Error creating GitHub repository:", curses.color_pair(3))
        stdscr.addstr(13, 0, out_gh, curses.color_pair(3))
    stdscr.addstr(15, 0, "Press any key to continue...")
    stdscr.getch()

def add_files(stdscr):
    """
    Prompts the user for a file pattern to add (or adds all if left blank),
    then runs git add.
    """
    stdscr.clear()
    draw_header(stdscr)
    prompt = "Enter file pattern to add (leave blank to add all files): "
    stdscr.addstr(3, 0, prompt)
    stdscr.refresh()
    curses.echo()
    pattern = stdscr.getstr(3, len(prompt)).decode('utf-8').strip()
    curses.noecho()
    cmd = "git add -A" if pattern == "" else f"git add {pattern}"
    out, code = run_command(cmd)
    if code == 0:
        stdscr.addstr(5, 0, "Files added successfully.", curses.color_pair(4))
    else:
        stdscr.addstr(5, 0, "Error adding files:", curses.color_pair(3))
        stdscr.addstr(6, 0, out, curses.color_pair(3))
    stdscr.addstr(8, 0, "Press any key to continue...")
    stdscr.getch()

def commit_changes(stdscr):
    """
    Prompts the user for a commit message, stages all files,
    and creates a commit.
    """
    stdscr.clear()
    draw_header(stdscr)
    prompt = "Enter commit message: "
    stdscr.addstr(3, 0, prompt)
    stdscr.refresh()
    curses.echo()
    commit_msg = stdscr.getstr(3, len(prompt)).decode('utf-8').strip()
    curses.noecho()
    if not commit_msg:
        stdscr.addstr(5, 0, "Commit message cannot be empty. Press any key to return.", curses.color_pair(3))
        stdscr.getch()
        return

    stdscr.addstr(5, 0, "Staging all files...", curses.A_BOLD)
    stdscr.refresh()
    out_add, _ = run_command("git add -A")
    stdscr.addstr(6, 0, out_add)
    stdscr.refresh()

    stdscr.addstr(7, 0, "Committing changes...", curses.A_BOLD)
    stdscr.refresh()
    out_commit, code_commit = run_command(f'git commit -m "{commit_msg}"')
    if code_commit == 0:
        stdscr.addstr(8, 0, "Changes committed successfully.", curses.color_pair(4))
    else:
        if "nothing to commit" in out_commit.lower():
            stdscr.addstr(8, 0, "Nothing to commit.", curses.color_pair(3))
        else:
            stdscr.addstr(8, 0, "Error during commit:", curses.color_pair(3))
            stdscr.addstr(9, 0, out_commit, curses.color_pair(3))
    stdscr.addstr(11, 0, "Press any key to continue...")
    stdscr.getch()

def push_repo(stdscr):
    """
    Pushes local commits to the remote repository.
    """
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(3, 0, "Pushing changes to remote...", curses.A_BOLD)
    stdscr.refresh()
    out, code = run_command("git push")
    if code == 0:
        stdscr.addstr(5, 0, "Push successful.", curses.color_pair(4))
    else:
        stdscr.addstr(5, 0, "Error during push:", curses.color_pair(3))
        stdscr.addstr(6, 0, out, curses.color_pair(3))
    stdscr.addstr(8, 0, "Press any key to continue...")
    stdscr.getch()

def pull_repo(stdscr):
    """
    Pulls changes from the remote repository.
    """
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(3, 0, "Pulling changes from remote...", curses.A_BOLD)
    stdscr.refresh()
    out, code = run_command("git pull")
    if code == 0:
        stdscr.addstr(5, 0, "Pull successful.", curses.color_pair(4))
    else:
        stdscr.addstr(5, 0, "Error during pull:", curses.color_pair(3))
        stdscr.addstr(6, 0, out, curses.color_pair(3))
    stdscr.addstr(8, 0, "Press any key to continue...")
    stdscr.getch()

def git_status(stdscr):
    """
    Displays the current Git status.
    """
    stdscr.clear()
    draw_header(stdscr)
    out, _ = run_command("git status")
    # Print the status line by line starting at row 3.
    row = 3
    for line in out.splitlines():
        stdscr.addstr(row, 0, line)
        row += 1
    stdscr.addstr(row + 1, 0, "Press any key to continue...")
    stdscr.getch()

def create_issue(stdscr):
    """
    Prompts the user for an issue title and optional body,
    and creates a GitHub issue using gh.
    """
    stdscr.clear()
    draw_header(stdscr)
    prompt_title = "Enter issue title: "
    stdscr.addstr(3, 0, prompt_title)
    stdscr.refresh()
    curses.echo()
    title = stdscr.getstr(3, len(prompt_title)).decode('utf-8').strip()
    curses.noecho()
    if not title:
        stdscr.addstr(5, 0, "Issue title cannot be empty. Press any key to return.", curses.color_pair(3))
        stdscr.getch()
        return
    prompt_body = "Enter issue body (optional): "
    stdscr.addstr(5, 0, prompt_body)
    stdscr.refresh()
    curses.echo()
    body = stdscr.getstr(5, len(prompt_body)).decode('utf-8').strip()
    curses.noecho()
    cmd = f'gh issue create --title "{title}"'
    if body:
        cmd += f' --body "{body}"'
    stdscr.addstr(7, 0, "Creating issue...", curses.A_BOLD)
    stdscr.refresh()
    out, code = run_command(cmd)
    if code == 0:
        stdscr.addstr(9, 0, "Issue created successfully.", curses.color_pair(4))
    else:
        stdscr.addstr(9, 0, "Error creating issue:", curses.color_pair(3))
        stdscr.addstr(10, 0, out, curses.color_pair(3))
    stdscr.addstr(12, 0, "Press any key to continue...")
    stdscr.getch()

def view_log(stdscr):
    """
    Displays the last 10 commits from the Git log.
    """
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(3, 0, "Recent commit log (last 10 commits):", curses.A_BOLD)
    out, _ = run_command("git log --oneline -n 10")
    row = 5
    for line in out.splitlines():
        stdscr.addstr(row, 0, line)
        row += 1
    stdscr.addstr(row + 1, 0, "Press any key to continue...")
    stdscr.getch()

def main_menu(stdscr):
    """
    Displays the main menu and dispatches the selected option.
    All menu text is left aligned (starting at column 2), while the header is centered.
    """
    curses.curs_set(0)
    current_row = 0
    menu = [
        "Initialize/Connect Repository",
        "Create GitHub Repository (with all files)",
        "Add Files",
        "Commit Changes",
        "Push to Remote",
        "Pull from Remote",
        "Git Status",
        "Create Issue",
        "View Log",
        "Exit"
    ]
    while True:
        stdscr.clear()
        check_min_window(stdscr)
        draw_header(stdscr)
        # Display menu items starting from row 3.
        for idx, item in enumerate(menu):
            if idx == current_row:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(3 + idx, 2, item)
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(3 + idx, 2, item)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if menu[current_row] == "Initialize/Connect Repository":
                if ensure_git_repo(stdscr):
                    # If repository exists, check remote connection.
                    out, code = run_command("git remote get-url origin")
                    if code != 0:
                        connect_remote(stdscr)
            elif menu[current_row] == "Create GitHub Repository (with all files)":
                create_github_repo(stdscr)
            elif menu[current_row] == "Add Files":
                add_files(stdscr)
            elif menu[current_row] == "Commit Changes":
                commit_changes(stdscr)
            elif menu[current_row] == "Push to Remote":
                push_repo(stdscr)
            elif menu[current_row] == "Pull from Remote":
                pull_repo(stdscr)
            elif menu[current_row] == "Git Status":
                git_status(stdscr)
            elif menu[current_row] == "Create Issue":
                create_issue(stdscr)
            elif menu[current_row] == "View Log":
                view_log(stdscr)
            elif menu[current_row] == "Exit":
                break

def main(stdscr):
    # Initialize colors.
    curses.start_color()
    curses.use_default_colors()
    # Pair 1: Header (white on blue)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    # Pair 2: Selected menu option (black on white)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # Pair 3: Error messages (red on default)
    curses.init_pair(3, curses.COLOR_RED, -1)
    # Pair 4: Success messages (green on default)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
