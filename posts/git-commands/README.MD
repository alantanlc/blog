# Git Commands

Commonly used Git commands.

## Overview

1. Commands
1. Combinations  

## Commands

View local branches:

```shell
$ git branch
```

View all local and remote branches:

```shell
$ git branch --all
```

Create and checkout to a new branch that doesn’t yet exist on local:

```shell
$ git checkout -b feature/22.7_fix
```

Check out to an existing local branch:

```shell
$ git checkout feature/22.7
```

Checkout and track a remote branch on local. Here, `origin` is the name of your remote repository:

```shell
$ git checkout --track origin/feature/22.8
```

View local changes:

```shell
$ git status
```

Stage all local changes:

```shell
$ git add .
```

Stage changes containing `java` in the file path:

```shell
$ git add *java*
```

Unstage all changes. This does not delete the local changes from disk, it only removes them from the staging area:

```shell
$ git reset .
```

Unstage changes containing `java` in the file path:

```shell
$ git reset *java*
```

Delete all local changes. Note that this cannot be undone:

```shell
$ git restore .
```

Delete changes containing `java` in the file path. Note that this cannot be undone:

```shell
$ git restore *java*
```

Commit staged changes:

```shell
$ git commit -m "JIRA-1 add README"
```

Push a new local branch to remote:

```shell
$ git push --set-upstream origin feature/22.7_fix
```

Push changes to an existing remote branch:

```shell
$ git push
```

Pull changes of local checkout branch from remote:

```shell
$ git pull
```

Pull changes from a remote branch to local checkout branch. This essentially __merges__ from the remote branch to the local checkout branch:

```shell
$ git pull origin feature/22.8
```

Delete a local branch. `-D` force deletes the branch even if it hasn't been pushed or merged yet:

```shell
$ git branch -D feature/22.7
```

Delete a remote branch:

```shell
$ git push --delete origin feature/22.7
```

Stash local changes:

```shell
$ git stash -- *
```

View stack of stashes:

```shell
$ git stash list
```

View changes for a stash 0 in stack:

```shell
$ git stash show 0
```

Pop stash from top of stack:

```shell
$ git stash pop
```

Pop stash #1 from stack:

```shell
$ git stash pop 1
```

Delete stash #0 from stack. Note that this cannot be undone:

```shell
$ git stash drop 0
```

Clear entire stack of stashes. Note that this cannot be undone:

```shell
$ git stash clear
```
