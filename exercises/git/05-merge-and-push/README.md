# Exercise 5: Merge into main and share it

Words to use: merge, `main`, pull, push, rejected push, fetch first, delete a remote branch, prune, merge conflict.

## Goal

Bring your branch `feature/<your-name>-intro` from exercise 4 into `main` with the command line, push `main` so everyone gets it, and clean up the branch, on your laptop and on the remote.

## Why this matters

A branch that never reaches `main` helps nobody. Bringing it in, sharing it and cleaning up after you is the end of every change. With ten people pushing to the same `main`, you also learn what happens when someone else was faster, and how to recover without losing anyone's work.

## Background

In exercise 3 you merged a branch into `main` on your laptop. Now `main` also lives on the remote, and everyone in your group shares it. The steps:

1. Bring your local `main` up to date with the remote, so you merge into the latest version.
2. Merge your branch into `main`.
3. Push `main`.

Ten people do this at the same time. Your push is refused when someone else pushed to `main` after your last pull: the remote has commits that you do not have, and Git does not throw them away. You get them first, then push again. This is the same refusal as in task 3 of exercise 4, now on `main`.

After the merge your branch is finished. Delete it on your laptop and on the remote. Your laptop still lists the remote branches that other people deleted, until you tell Git to forget them.

A merge or pull that makes a merge commit opens an editor for the message. Save and close it (in VS Code: close the tab), or give the message on the command line.

In this training the shared `main` accepts direct pushes from everyone. Real teams protect `main` and use pull requests: they come this afternoon.

## Before you start

You need your branch `feature/<your-name>-intro` from exercise 4, pushed to the remote, and a clean `git status`. Work in your clone of the training repository.

Run this once, so that `git pull` merges when your `main` and the remote's `main` both have new commits:

```powershell
git config --global pull.rebase false
```

## Tasks

Stuck on a task? Look at the slides, the cheat sheet in `exercises/git/README.md`, or `git help <command>`.

### Task 1: Merge your branch into main and push

Bring your local `main` up to date with the remote. Merge `feature/<your-name>-intro` into it. Push `main`.

If your push is refused, read the message, get the new commits from the remote and push again. Repeat until the push is accepted. Do not use any force option.

A refused push looks like this:

```
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '...'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```

Result: the push ends with `main -> main`, and `git status` says `Your branch is up to date with 'origin/main'`. Your folder `participants/<your-name>/` is on `main` in the browser under **Repos > Files**, next to the folders of the others who already pushed. `git log --oneline --graph -10` shows your commit and probably one or more merge commits.

### Task 2: Clean up

Your branch is in `main` now. Delete it on your laptop and on the remote. Then make your laptop forget the remote branches that other people deleted.

Result: `git branch -a` no longer lists `feature/<your-name>-intro`, not as a local branch and not under `remotes/origin/`. Once everyone in your group is done, it shows only:

```
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

Under **Repos > Branches** in the browser, your branch is gone too.

### Task 3: Two people, one line

This one is much harder.

Do this with a neighbour, or alone with a second clone of the repository in another folder, which plays the neighbour.

1. Both of you start from an up-to-date `main`. Each makes a new branch and changes the same line of the shared `README.md` in a different way, and commits.
2. Each merges their branch into `main` and pushes. The first push is accepted.
3. Before the second person gets the new commits, they write down what they expect. Then they do it, resolve the conflict on their laptop and push `main`.
4. Look at `git log --oneline --graph -10`. Point at the commit where the conflict was resolved and say what its two parents are.
5. Delete both branches, local and remote.

Rules:

- No `git push --force` and no `--force-with-lease`.
- Do not edit the file or resolve the conflict in the browser.
- Do not delete or reset `main`.
- Keep the change to `README.md` harmless. The trainer may change it back.

The second person's pull stops with `CONFLICT (content): Merge conflict in README.md`, and `git status` shows `both modified: README.md`. After the resolution, the push is accepted, and `README.md` on the remote has the line the second person chose.

## Open question

Anyone in your group can now push anything to `main`: a typo, a script that crashes, a password, a deleted folder. What could go wrong in a real team? What would you want the server to check before a change reaches `main`, and who should look at it?
