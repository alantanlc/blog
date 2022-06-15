# Git Commands

Git commands that I commonly use.

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

Checkout and track a remote branch on local. Here, `origin` is the name of your remote ll

```shell
$ git checkout -b feature/22.8
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

Unstage all changes. This does not delete the local changes, only removes them from staging area:

```shell
$ git reset .
```

Unstage changes containing `java` in the file path:

```shell
$ git reset *java*
```

Delete all local changes:

```bash
$ git restore .
```

Delete changes containing `java` in the file path:

```shell
$ git restore *java*
```

Commit staged changes:

```shell
$ git commit -m "JIRA-1 add README"
```

Push a new local branch to remote:

```bash
$ git push --set-upstream origin feature/22.7_fix
```

Push changes to an existing remote branch:

```bash
$ git push
```

Delete a local branch. `-D` force deletes the branch even if it hasn't been pushed or merged yet:

```shell
$ git branch -D feature/22.7
```

Delete a remote branch:

```shell
$ git push --delete origin feature/22.7
```


