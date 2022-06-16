# Git Commands

Commonly used Git commands.

## Overview

1. Commands 
1. Combinations
1. Merge Conflicts 

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

Abort a merge in case of a merge conflict:

```shell
$ git merge --abort
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

View changes for stash `0` in stack:

```shell
$ git stash show 0
```

Pop stash from top of stack:

```shell
$ git stash pop
```

Pop stash `1` from stack:

```shell
$ git stash pop 1
```

Delete stash `0` from stack. Note that this cannot be undone:

```shell
$ git stash drop 0
```

Clear entire stack of stashes. Note that this cannot be undone:

```shell
$ git stash clear
```

## Combinations

When you have local changes but need to switch to another branch:

```shell
$ git add .
$ git stash -- *
$ git checkout feature/22.7_fix
```

When you are done and want to switch back to your previous local changes:

```shell
$ git checkout feature/22.7
$ git stash pop
```

When you no longer need the local changes:

```shell
$ git reset .
$ git restore .
```

Sometimes `git restore` may not be able to fully remove your local changes (e.g. newly created files). In that case, try this instead:

```shell
$ git add .
$ git stash -- *
$ git stash drop 0
```

When you need to remotely merge a branch:

```shell
$ git checkout feature/22.8
$ git pull origin feature/22.7
$ git push
```

## Merge Conflict

Sometimes a conflict may occur when merging branches:

```shell
$ git checkout feature/22.8
$ git pull origin feature/22.7

conflict
```

__Steps to resolve__

Get list of conflicted files:

```shell
$ git status

```

Resolve each conflicted file:

```shell
$ 
```

Commit the de-conflicted changes and continue with the merge:

```shell
$ git add .
$ git commit
Close notepad
$ git push
```

