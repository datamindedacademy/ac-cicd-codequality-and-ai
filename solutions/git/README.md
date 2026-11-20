# Git exercises: solutions

Expected command sequences and answers, per exercise and per task. Hashes are written as `<hash>`. Yours will differ unless noted.

Commands are for Windows PowerShell 5.1. Replace `anna` with your own name.

## Exercise 1: Your first commit

### Tasks 1 and 2

```powershell
# task 1
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git init -b main
git add conversions.py
git commit -m "Add bar to psi conversion"
git add measurements.csv
git commit -m "Add first measurements"
git log --oneline

# task 2: edit both files and save them
git status
git add conversions.py
git diff --staged
git commit -m "Add Celsius to Kelvin conversion"
git add measurements.csv
git diff --staged
git commit -m "Add fourth measurement run"
git log --oneline
git status
```

Before the first `git add` in task 2, `git status` lists both files as modified under "Changes not staged for commit".

### Task 3

```powershell
git add -p conversions.py
# hunks come in file order: n for the docstring hunk, y for the new function
git diff --staged
git commit -m "Add kelvin_to_celcius"
git add conversions.py
git commit -m "Reword the module docstring"
git log --oneline
# the typo is in the commit before the last: take both commits apart, keep the edits
git reset --soft HEAD~2
git reset
git add -p conversions.py
# n for the docstring hunk, y for the new function
git commit -m "Add kelvin_to_celsius"
git add conversions.py
git commit -m "Reword the module docstring"
git log --oneline
git status
```

`git add -p` goes through the changes hunk by hunk and stages only the ones you accept, so one file can go into two commits. The two edits must be far enough apart to be separate hunks (`s` splits a hunk further).

`git reset --soft HEAD~2` moves the branch back two commits and keeps all their changes staged. `git reset` then unstages them, so the file is changed in the working tree and nothing is lost. The edits are still in the file, so the two commits can be made again with the right message. `git log --oneline` then shows six commits and `git status` is clean. Other routes that work: `git reset --soft HEAD~1`, `git stash`, `git commit --amend -m "..."` on the earlier commit, `git stash pop`, then commit again. If a commit seems lost, `git reflog` still lists it.

### Open question

About 50 MB, once (less if the content compresses). Git stores the content of a file under the hash of that content, and the file name is not part of it. The names live in the snapshot, which points twice at the same stored content. The two commits do not get the same hash. The hash of a commit covers the snapshot, the parent, the author, the committer, the dates and the message. Your names and the times differ, so the hashes differ, although both commits point at the same snapshot.

## Exercise 2: Explore the history

### Tasks 1 and 2

```powershell
# task 1
git log --oneline
git show --stat <hash-of-Add-measurements-and-analyse_run-script>

# task 2
git log -S273.15 --format="%h %an %ad %s" --date=short
# edit conversions.py: KELVIN_OFFSET = 0, save
git status
git restore conversions.py
git status
```

`git log -S<text>` lists the commits that added or removed that text. `git restore <file>` throws away the uncommitted edit for good. There is no undo for it.

### Task 3

```powershell
git log --oneline
git revert <hash-of-Fix-Kelvin-offset>
# Git stops: CONFLICT in conversions.py
git status
# in conversions.py keep BAR_TO_PSI = 14.5038 and KELVIN_OFFSET = 273.0, delete the marker lines
git add conversions.py
git revert --continue
git log --oneline
uv run python analyse_run.py
```

`git revert` makes a new commit that does the opposite of the chosen commit, so the original stays in the log, followed by `Revert "Fix Kelvin offset"`. Here it conflicts: the revert wants `KELVIN_OFFSET = 273.0` and `BAR_TO_PSI = 14.5`, but the later commit "Use more precise bar to psi factor" changed the line next to it, and Git does not guess when changes touch neighbouring lines. The conflict shows both versions between `<<<<<<< HEAD` and `>>>>>>>`. The result to keep is the later `BAR_TO_PSI = 14.5038` plus the reverted `KELVIN_OFFSET = 273.0`. `git revert --continue` opens an editor for the message (save and close, or use `git revert --continue --no-edit`). `git revert --abort` goes back to before the revert. `analyse_run.py` then prints 108.78 psi and 358.33 K. (Checked with the setup script history.)

### Open question

`git reflog` lists where HEAD has been, including commits that no branch points to. Find the hash there, then `git switch -c rescue <hash>` gives the commit a branch again. Git removes unreferenced commits only after a period, 30 or 90 days by default, so there is time to find them. This does not help for edits that were never committed.

## Exercise 3: Branches and merging

### Tasks 1 and 2

```powershell
uv run python exercises/git/setup_exercise.py 3
cd "<path printed by the script>"

# task 1
git switch -c feature/pressure-kpa
# edit conversions.py: add bar_to_kpa at the end
git add conversions.py
git commit -m "Add bar to kPa conversion"
git switch main
git merge feature/pressure-kpa
git branch -d feature/pressure-kpa

# task 2
git merge experiment/psi-precision
# open conversions.py in VS Code, click "Accept Incoming Change"
# check that no <<<<<<<, ======= or >>>>>>> remains, save
git add conversions.py
git commit -m "Merge experiment/psi-precision"
git log --oneline --graph --all --decorate
```

### Task 3

```powershell
Add-Content README.md "TODO: check the units"
git switch feature/temperature-report
git rebase main
# error: cannot rebase: You have unstaged changes.
git stash
git rebase main
# CONFLICT in conversions.py on "Add Celsius to Fahrenheit conversion"
# edit conversions.py: keep both functions (bar_to_kpa first, then celsius_to_fahrenheit), no markers
git add conversions.py
git rebase --continue
# the editor opens for the commit message: save and close it
# Successfully rebased and updated refs/heads/feature/temperature-report.
git switch main
git merge feature/temperature-report
git branch -d feature/temperature-report
git stash pop
git log --oneline --graph --all --decorate
git status --short
uv run python analyse_run.py
```

Notes:

- Git refuses to rebase with uncommitted changes. `git stash` parks the README line, `git stash pop` brings it back. `git rebase --autostash main` does both in one go.
- The conflict comes in the second commit, because `main` and the branch both appended to the end of `conversions.py`. The rebase stops there. After `git add` and `git rebase --continue` the third commit is replayed without trouble. `git rebase --abort` returns to before the rebase.
- Expected: the graph in the README, ` M README.md` from `git status --short`, and four lines from `analyse_run.py`: mean pressure, mean temperature, min temperature and mean temperature in Fahrenheit. Checked with the setup script.
- Why the hashes changed: a commit's hash covers its content, its parent and its metadata. After the rebase each commit has a different parent (the first sits on the new tip of `main`, the others on the commit before them), so Git made new commits with the same changes and new hashes. The old ones are no longer on the branch. That is also why rebasing commits that are already pushed and used by others is a bad idea: they still have the old ones.

### Open question

Each commit stores the hash of its parent, or of both parents for a merge commit. `git log --graph` draws the lines from those links, not from branch names. A branch is a small text file under `.git/refs/heads/` that contains one commit hash (or a line in `.git/packed-refs`). Creating a branch writes that file, which is why it costs nothing.

## Exercise 4: Clone from Azure Repos and push a branch

### Tasks 1 and 2

```powershell
New-Item -ItemType Directory -Force "$HOME\git-exercises"
cd "$HOME\git-exercises"
git clone https://dev.azure.com/<organisation>/<project>/_git/<training-repo>
cd <training-repo>
git remote -v
git branch -a
git log -1
git switch -c feature/anna-intro
New-Item -ItemType Directory -Force participants/anna
Set-Content participants/anna/about.md "# Anna`n`nI work at Atlas Copco. I use Python to analyse compressor test data."
git add participants/anna/about.md
git commit -m "Add intro for Anna"
git push -u origin feature/anna-intro
git status
git branch -a
```

`origin` is the default name Git gives to the remote you cloned from. `git branch -a` also lists the remote-tracking branches (`remotes/origin/...`), which are your laptop's record of what the remote had at the last fetch. `-u` sets the upstream, so later `git push` and `git pull` need no arguments.

### Task 3

The second clone `..\other` plays the colleague (a neighbour does the same from their laptop).

```powershell
# in your clone: a local commit, not pushed
Set-Content participants/anna/mine.md "my change"
git add participants/anna/mine.md
git commit -m "My commit"

# make the other clone, switch to the branch, commit, push
git clone https://dev.azure.com/<organisation>/<project>/_git/<training-repo> ..\other
cd ..\other
git switch feature/anna-intro
Set-Content participants/anna/theirs.md "colleague change"
git add participants/anna/theirs.md
git commit -m "Colleague commit"
git push

# back in your clone: the push is rejected
cd ..\<training-repo>
git push
git fetch
git status -sb
git log --oneline --graph --all
git pull --no-rebase
git push
```

Expected: `git push` ends with `! [rejected] ... (fetch first)`. After `git fetch`, `git status -sb` shows `[ahead 1, behind 1]` and the graph shows `My commit` and `Colleague commit` as two lines from the same parent. `git pull --no-rebase` makes a merge commit (`Merge branch 'feature/anna-intro' of ...`) and the following `git push` is accepted. Also fine: `git fetch` then `git merge origin/feature/anna-intro`, or `git pull --rebase` (this rewrites only the unpushed local commit, so no force is needed).

`--no-rebase` is there because a plain `git pull` on diverged branches stops with `fatal: Need to specify how to reconcile divergent branches` unless `pull.rebase` is configured.

`git fetch` downloads the new commits and moves `origin/feature/anna-intro`. It does not touch your branch or your files. `git pull` is `git fetch` followed by a merge (or rebase) of the fetched commits into your current branch.

### Open question

They sit under the remote-tracking branches such as `origin/main` and `origin/<other branches>`. `git branch -a` lists them. Offline you can commit, branch, merge, read the history and diff. You cannot push, pull or fetch, because those need the remote.

## Exercise 5: Merge into main and share it

### Tasks 1 and 2

```powershell
git config --global pull.rebase false     # once, see "Before you start"
git status                                # clean, on feature/anna-intro
git switch main
git pull
git merge feature/anna-intro              # fast-forward, or a merge commit (editor: save and close)
git push
# if refused with "(fetch first)": someone pushed to main after your pull
git pull                                  # merge commit "Merge branch 'main' of ..."
git push                                  # repeat pull and push until accepted
git log --oneline --graph -10

# task 2
git branch -d feature/anna-intro
git push origin --delete feature/anna-intro
git fetch --prune
git branch -a
```

The first person whose branch starts from the tip of `main` gets a fast-forward. Everyone after them merges into a `main` that has moved, so Git makes a merge commit. `git merge --no-edit feature/anna-intro` skips the editor.

The push is refused when the remote `main` has a commit that your local `main` does not have: the remote cannot simply move forward to your commit without losing that one. `git pull` fetches it and merges it into your `main`, and then your `main` contains everything, so the push is a plain move forward and is accepted. Without `pull.rebase false`, a `git pull` on diverged branches can stop with `fatal: Need to specify how to reconcile divergent branches`; `git pull --no-rebase` does the same in one go. `git pull --rebase` also works here: it replays your unpushed commits on top of the remote `main`. Force pushing would throw away the other person's commit and is never the answer on a shared `main`.

`git branch -d` works because the branch is now part of `main`. `git push origin --delete feature/anna-intro` removes the branch on the remote, and the output ends with `- [deleted]         feature/anna-intro`. `git fetch --prune` removes the `remotes/origin/...` entries of branches that other people deleted.

### Task 3

Both start from an up-to-date `main`. The other clone `..\other` plays the neighbour.

```powershell
# person 1 (and person 2 in the same way, with a different text on the same line)
git switch main
git pull
git switch -c feature/anna-readme
# change the first line of README.md, save
git add README.md
git commit -m "Change the README title"
git switch main
git merge feature/anna-readme
git push                                  # person 1: accepted

# person 2, after person 1 pushed
git switch main
git merge feature/ben-readme              # fine locally: person 1's commit is not here yet
git push                                  # refused: (fetch first)
git pull
# CONFLICT (content): Merge conflict in README.md
git status                                # both modified: README.md
# open README.md, keep the line you want, remove <<<<<<<, ======= and >>>>>>>, save
git add README.md
git commit -m "Merge origin/main, keep one README title"
git push                                  # accepted
git log --oneline --graph -10

# both: clean up
git branch -d feature/anna-readme
git push origin --delete feature/anna-readme
git fetch --prune
```

What to expect before the pull: the push is refused because person 1 pushed first, and the pull will stop with a conflict on that line, because both `main` versions changed it since their common parent. Git does not choose between two edits of the same line.

The commit that resolves the conflict is the merge commit made by `git commit` after `git add`. Its first parent is person 2's local `main` (with their merge of `feature/ben-readme`), and its second parent is `origin/main` with person 1's change. The push is accepted because the remote `main` is now an ancestor of the local `main`. No force is needed, and nobody's commit is lost: both versions of the line stay in the history, and the file has the version chosen during the resolution. `git merge --abort` returns to before the pull if the resolution goes wrong.

### Open question

Anything that reaches `main` is what everyone pulls next: a script that crashes, a broken import, a password, a deleted folder or a change nobody understood. With direct pushes, the only check is the discipline of each person, and the first sign of a problem is a colleague whose script stops working. Teams protect `main` on the server: direct pushes are refused, changes come in through a pull request, at least one other person reviews and approves it, and a pipeline runs the linter and the tests before the merge is allowed. In Azure Repos that is a branch policy with reviewers and build validation. That is the afternoon.

## Exercise 6: Git in VS Code

Trainer demo in class. Participants repeat it alone afterwards. Everything here is optional.

Equivalent commands for the VS Code clicks:

| VS Code | Command line |
|---|---|
| Bottom-left branch name, **Create new branch...** | `git switch -c feature/anna-vscode` |
| **+** next to a file | `git add <file>` |
| **Commit** | `git commit -m "..."` |
| **Publish Branch** | `git push -u origin feature/anna-vscode` |
| **...** > **Pull** | `git pull` |
| **...** > **Branch** > **Merge...** | `git merge feature/anna-vscode` (on `main`) |
| **Sync Changes** | `git pull`, then `git push` |
| `Git: Delete Branch...` | `git branch -d feature/anna-vscode` |

The `.gitignore` part:

```powershell
git switch main
git switch -c feature/anna-ignore
New-Item -ItemType Directory -Force participants/anna/output
Set-Content participants/anna/output/summary.csv "run,mean_bar"
Set-Content participants/anna/output/plot.png "not a real picture"
Set-Content participants/anna/.gitignore "output/`n*.png`n.venv/`n__pycache__/"
git status
git add participants/anna/.gitignore
git commit -m "Add .gitignore for Anna's folder"
git status
```

Before the `.gitignore` exists, `git status` lists `participants/anna/output/`. Afterwards it lists only `participants/anna/.gitignore` as new. After the commit: "nothing to commit, working tree clean".

Check yourself:

1. The **+** (Stage Changes) button.
2. `U` is untracked (new file, not yet in Git). `M` is modified (a tracked file with changes).
3. `git push -u origin <branch>`: it creates the branch on the remote and links the local branch to it.
4. No. A file that is already tracked stays tracked and stays in the history. You would need `git rm --cached <file>` to stop tracking it (not covered in this training).

### Open question

The repository is about 200 MB larger (less if the data compresses well), because the file is still in the history. `.gitignore` only affects files that Git does not track yet, so it does nothing for a file that is already committed. Removing it needs a history rewrite, for example with `git filter-repo`, and a forced push. Everyone then has to clone again. It is cheaper to ignore data files from the start.

## The "With Copilot" task of exercise 6

Generated commit messages describe the diff. Add the reason when it is not obvious.
