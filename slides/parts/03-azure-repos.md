---
layout: section
---

# Azure <span class="dm-accent">Repos</span>

---
layout: default
label: 3 · Azure Repos
---

# Git is the <span class="dm-accent">engine</span>, Azure DevOps is <span class="dm-accent">one car</span> built around it

<div class="race">
<div class="engine"><div class="i-mdi-engine-outline ico" /><b>Git</b><span>the engine: commits, branches, merges, history</span><em>free, runs on your laptop, works without internet</em></div>
<div class="cars">
<div class="car now"><div class="i-mdi-car-sports ico" /><b>Azure DevOps</b><span>Repos, pull requests, Pipelines, Boards</span><em>used at Atlas Copco</em></div>
<div class="car"><div class="i-mdi-car-sports ico" /><b>GitHub</b><span>pull requests, Actions, Issues</span></div>
<div class="car"><div class="i-mdi-car-sports ico" /><b>GitLab</b><span>merge requests, CI/CD, Issues</span></div>
</div>
</div>

<p class="note">Same engine, so the same <code>git</code> commands everywhere. Only the dashboard differs: the web pages, the buttons, the names.</p>

<style>
.race { display: grid; grid-template-columns: 1fr 1.6fr; gap: 22px; align-items: stretch; margin-top: 14px; }
.engine, .car { display: flex; flex-direction: column; gap: 4px; padding: 14px 16px; border-radius: 10px; background: var(--dm-surface); color: var(--dm-premium); font-size: 14px; }
.engine { justify-content: center; border-left: 6px solid var(--dm-premium); }
.engine b { font-size: 24px; }
.cars { display: flex; flex-direction: column; gap: 8px; }
.car b { font-size: 17px; }
.car.now { background: var(--dm-connecting); color: #fff; }
.ico { font-size: 30px; color: var(--dm-connecting); }
.car.now .ico { color: #fff; }
.engine em, .car em { font-style: normal; font-weight: 600; font-size: 13px; opacity: 0.85; }
</style>

<!--
People mix up Git and GitHub, or Git and Azure DevOps, all the time. Use the race car. Git is the engine: it does the real work of versioning, it runs on your laptop, and everything this morning so far used only the engine, without any website. GitHub, Azure DevOps and GitLab are different cars built around that same engine. Each adds a body and a dashboard: a place to store the shared copy, a web page to browse it, pull requests, and extras such as pipelines and boards. This morning we only use the shared copy; pull requests and pipelines come this afternoon. Because the engine is the same, git clone, push and pull work identically on all three; only the dashboard differs, so a tutorial that shows GitHub screens still teaches you the right Git commands. Atlas Copco drives the Azure DevOps car. This afternoon the analogy comes back: the pipeline is the scrutineering every car passes before it may race, and the branch policies are the race rules.
-->

---
layout: default
label: 3 · Azure Repos
---

# <span class="dm-accent">Clone</span> copies the repository and its history

```powershell
git clone https://dev.azure.com/<organisation>/<project>/_git/<training-repo>
cd <training-repo>
git remote -v
```

```text
origin  https://dev.azure.com/<organisation>/<project>/_git/<training-repo> (fetch)
origin  https://dev.azure.com/<organisation>/<project>/_git/<training-repo> (push)
```

- The URL: **Repos > Files**, pick the repository, then **Clone**
- The first time, a window asks you to sign in (Git Credential Manager)
- `clone` creates the remote `origin`

<style>
.slidev-code { font-size: 14px !important; line-height: 1.5 !important; }
</style>

<!--
Show this live in the browser: the project, Repos, Files, the repository dropdown at the top, and the Clone button. The URL has three parts after dev.azure.com: the organisation, the project and, after _git, the repository. The Clone button sometimes puts the organisation name with an at sign in front of dev.azure.com; both forms work. Clone copies the whole repository, history included, into a new folder and sets up the remote for you. The sign-in window is Git Credential Manager, which ships with Git for Windows and remembers the token afterwards. Sign in with the account that was invited to the organisation. Origin is only the default nickname for the URL. Do not clone into a OneDrive or network folder; use a local path.
-->

---
layout: default
label: 3 · Azure Repos
---

# <span class="dm-accent">Push</span> uploads commits, <span class="dm-accent">pull</span> downloads them

```powershell
git push -u origin feature/bar-to-psi   # first push of a new branch
git push                                 # later pushes
git pull                                 # fetch and merge new commits
git fetch                                # only download, change nothing
```

- `-u` sets the upstream: it links your local branch to the remote one, needed only once
- `origin/main` is a **remote-tracking branch**: your laptop's last known copy of `main` on the server, updated by `fetch` and `pull`
- `pull` is `fetch` plus merge: commit or restore your edits first

<p class="ask" v-click><b>Question</b>Your laptop is stolen on the train. Which work is gone?</p>

<style>
.slidev-code { font-size: 16px !important; line-height: 1.5 !important; }
</style>

<!--
The first push of a new branch creates it on the server. Show it in the browser under Repos, Branches, and the commit under Repos, Commits. Azure Repos may also offer to create a pull request for the new branch; ignore it for now, pull requests come this afternoon. Pull is what you type daily. Fetch is the careful variant when you want to see what is coming before it touches your files. The upstream is the remote branch your local branch follows, so later push and pull need no arguments. Origin slash main is a remote-tracking branch: your laptop's memory of main on the server, which only changes when you fetch or pull. If a pull produces a conflict, it is the same conflict you saw earlier. Question on the slide: every commit you did not push, and every change you did not commit. What is on the server is safe. Push at the end of every working session.
-->

---
layout: statement
title: Exercise - remote
---

# Exercise time: <span class="dm-accent">the remote</span>

<p class="mt-6 text-lg opacity-80"><code>exercises/git/04-remote</code></p>
<p class="mt-2 text-sm opacity-70">Clone from Azure Repos, branch, commit, push</p>

<!--
Participants clone their group's training repository from Azure Repos, create a branch, commit a small file in their own folder and push it. This is the first time they sign in, so expect authentication questions: wrong account, wrong tenant, TF401019. The trainer guide has the fixes. Have the URLs on screen.
-->

---
layout: default
label: 3 · Azure Repos
---

# Bring your branch into <span class="dm-accent">main</span> and share it

```powershell
git switch main
git pull                                       # latest main from the remote
git merge feature/anna-intro                   # your branch into main
git push                                       # share main
git branch -d feature/anna-intro               # clean up your laptop
git push origin --delete feature/anna-intro    # and the remote
```

```text
 ! [rejected]        main -> main (fetch first)
```

- Refused? Someone else pushed to `main` first: `git pull`, then `git push` again
- Never force push to a shared `main`

<style>
.slidev-code { font-size: 14px !important; line-height: 1.45 !important; }
</style>

<!--
This is the same merge as in exercise 3, now with a shared main. First get the latest main, because you want to merge into what everyone else already pushed. Then merge your branch, then push main. Show it live with your own branch. Then show the refusal: push a commit to main from a second clone first, and push from the first clone. Git refuses because the remote has a commit you do not have, and pushing would throw it away. The fix is always the same: git pull, which merges their commit into your main, then git push. With ten people pushing at once this can take two or three rounds; that is normal. A force push would wipe out the other person's work, so never on main. After the merge the branch is done: delete it locally with branch -d and on the remote with push origin --delete. Fetch with prune makes your laptop forget the branches other people deleted. In this training main accepts direct pushes from everyone. In a real team the server protects main, and changes go in through a pull request with a review and checks. That is this afternoon.
-->

---
layout: statement
title: Exercise - merge and push
---

# Exercise time: <span class="dm-accent">merge and push</span>

<p class="mt-6 text-lg opacity-80"><code>exercises/git/05-merge-and-push</code></p>
<p class="mt-2 text-sm opacity-70">Pull main, merge your branch, push, delete the branch</p>

<!--
Participants bring their branch from the previous exercise into main on the command line, push main, and delete the branch locally and on the remote. Ten people push to the same main, so most pushes get refused at least once: let it happen, it is the lesson. Pair people up for the last task, a conflict on the same line of the shared README.
-->

---
layout: statement
title: Demo - Git in VS Code
---

# Demo: <span class="dm-accent">Git in VS Code</span>

<p class="mt-6 text-lg opacity-80">Optional practice: <code>exercises/git/06-git-in-vscode</code></p>

<p class="mt-4 text-sm opacity-80">In the <b>Source Control view</b>: + stages, Commit commits, <b>Publish Branch</b> is the first push, <b>Sync Changes</b> pulls and then pushes.</p>

<p class="words"><b>Words you can now use</b> clone · origin · push · pull · fetch · upstream · origin/main · rejected push · push --delete · fetch --prune</p>

<style>
.words { font-size: 15px; opacity: 0.9; margin-top: 40px; }
.words b { margin-right: 8px; }
</style>

<!--
Trainer demo of the same cycle in the Source Control view (control shift G): changed files, click for the diff, plus to stage, message and Commit, merging into main from the menu, Sync Changes for pull and push, and the branch name at the bottom left. If there is time, show a .gitignore taking effect: an output folder disappears from the list once it is ignored. Ignoring only helps for files that are not committed yet, so never commit passwords, tokens or large raw data. Participants can do exercise 06 afterwards in their own time.
-->
