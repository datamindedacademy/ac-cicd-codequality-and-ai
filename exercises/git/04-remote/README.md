# Exercise 4: Clone from Azure Repos and push a branch

Words to use: remote, `origin`, clone, push, upstream branch, remote-tracking branch (`origin/main`), fetch, pull.

## Goal

Get a copy of your group's training repository from Azure Repos. Make a branch with a file in your own folder, and push it.

## Why this matters

A script that exists only on your laptop is gone when the laptop is. The remote is the backup, and the only way a colleague gets your work without an email attachment. You use it every day you work in a shared repository.

## Background

So far your repository lived only on your laptop. Real projects have a shared copy on a server. This shared copy is called a **remote**. In this training it lives in **Azure Repos**, the Git part of Azure DevOps. Azure Repos hosts the repository and adds sign-in, pull requests and pipelines. Your group has one repository there. The Git commands are the same as on your laptop.

Azure DevOps is organised in three levels: an **organisation**, which holds **projects**, which hold **repositories**. You see all three in the URL of a repository.

Terms used in this exercise:

| Term | Meaning |
|---|---|
| **remote** | A copy of the repository on a server. Its default name is `origin`. |
| **clone** | Download a full copy of a remote repository, with its whole history. |
| **push** | Send your commits to the remote. |
| **pull** | Get new commits from the remote and bring them into your branch. |
| **upstream** | The remote branch that your local branch is linked to. |

Everyone in your group works in the same repository. To avoid getting in each other's way, each person only adds files in their own folder: `participants/<your-name>/`. Use your first name in lowercase, without spaces or special characters, for example `anna`.

You sign in to Azure DevOps through **Git Credential Manager**, which comes with Git for Windows. The first time you clone or push, a window opens and asks you to sign in. Use the account the trainer invited, usually your work account. After that, it remembers you.

## Before you start

Your trainer gives you the repository URL. It looks like this:

```
https://dev.azure.com/<organisation>/<project>/_git/<training-repo>
```

You can also copy it yourself: open the project in the browser, go to **Repos > Files**, pick your group's repository at the top, and click **Clone**. The URL there may start with `https://<organisation>@dev.azure.com/...`. That form works too.

## Tasks

Stuck on a task? Look at the slides, the cheat sheet in `exercises/git/README.md`, or `git help <command>`.

### Task 1: Clone and look around

Clone the training repository into a folder next to your other exercises, not inside the course repository. A sign-in window opens the first time. Sign in with the account the trainer invited.

```powershell
New-Item -ItemType Directory -Force "$HOME\git-exercises"
cd "$HOME\git-exercises"
git clone https://dev.azure.com/<organisation>/<project>/_git/<training-repo>
cd <training-repo>
code .
```

`code .` opens the clone in its own VS Code window, as in exercises 1 to 3. Edit the files there and type your Git commands in its terminal (``Ctrl+` ``). You can close the window of the earlier exercise.

```
Cloning into '<training-repo>'...
remote: Azure Repos
remote: Found 8 objects to send. (12 ms)
Receiving objects: 100% (8/8), done.
```

The lines and numbers will differ. Then answer three questions from inside the clone, using Git and not the web page: what is the remote called and where does it point, which branches exist on the remote, and who made the last commit.

`git branch -a` shows something like this for a fresh clone. Other people's pushed branches appear here after a `git fetch`.

```
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

### Task 2: Push a branch

Everyone in your group works in the same repository, each in their own folder `participants/<your-name>/`. Use your first name in lowercase, for example `anna`.

Never work on `main`. Make a branch named `feature/<your-name>-intro`. On it, add the file `participants/<your-name>/about.md` with a few lines about yourself, and commit it as the only change. Push the branch to the remote so that your local branch is linked to it, and later `git push` and `git pull` need no extra arguments. Then find your branch and your commit in the browser, under **Repos > Branches** and **Repos > Commits**.

Exercise 5 starts from this branch, so finish this task.

Expected output of the push ends with:

```
 * [new branch]      feature/anna-intro -> feature/anna-intro
branch 'feature/anna-intro' set up to track 'origin/feature/anna-intro'.
```

`git status` says `Your branch is up to date with 'origin/feature/anna-intro'`, and `git branch -a` lists `remotes/origin/feature/anna-intro`.

Azure Repos may offer to create a pull request for your new branch, for example in a banner on the **Repos > Files** page. Ignore it: this morning you merge on the command line, and pull requests come this afternoon.

### Task 3: The remote moved while you were committing

This one is much harder.

A colleague pushes a commit to your branch on the remote while you have a new local commit that is not pushed yet. Do this with a neighbour (they clone the repository, switch to your branch, add a commit and push), or alone with a second clone of the repository in another folder, which plays the colleague.

1. Make a local commit on your branch, but do not push it yet.
2. Let the colleague push their commit to the same branch first.
3. Before you run `git push`, write down what you expect it to say. Then run it and compare.
4. Get both commits on the remote branch.
5. Explain in your own words how `git fetch` differs from `git pull`, using what you saw in `git log --oneline --graph --all` before and after the fetch.

Rules:

- No `git push --force`, and no `--force-with-lease`.
- Do not delete or recreate the branch.

The push is refused, and Git tells you why:

```
 ! [rejected]        feature/anna-intro -> feature/anna-intro (fetch first)
error: failed to push some refs to '...'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```

After the fetch, `git status -sb` says `[ahead 1, behind 1]`, and the graph has two lines that split from your first commit.

## Open question

After `git fetch` your laptop holds commits that are in none of your own branches. Where are they? You can work a whole week without network: name two things you can do offline with Git, and one you cannot.
