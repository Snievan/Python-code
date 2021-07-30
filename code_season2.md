- [pandas](#pandas)
  - [pivot](#pivot)
  - [stack](#stack)
- [sys](#sys)
- [Time convert](#time-convert)
  - [pd.time to unix](#pdtime-to-unix)
  - [pd.time grouper](#pdtime-grouper)
- [git](#git)
  - [PUSHING CHANGES](#pushing-changes)
  - [CREATE A BRANCH FOR DESIRED FEATRUE](#create-a-branch-for-desired-featrue)
  - [AFTER COMMIT PUSH BRANCH TO REMOTE](#after-commit-push-branch-to-remote)
  - [MERGE A BRANCH](#merge-a-branch)
  - [DELETETING A BRANCH](#deleteting-a-branch)
  - [AMEND COMMIT MESSAG](#amend-commit-messag)
  - [MOVE COMMIT](#move-commit)
  - [UNDO MASTER COMMIT](#undo-master-commit)
  - [REVERT COMMIT](#revert-commit)


# pandas

## pivot 
- pivot
- adad

## stack

# sys
- sys.getsizeof()

# Time convert
## pd.time to unix
```python
pd.Timestamp('2021-04-01 00:02:35.234').timestamp()
```


## pd.time grouper
```python
df.groupby(pd.Grouper(key="Publish date", freq="1W")).mean()
```

# git

```shell
git remote -v
git branch -a 

```

##  PUSHING CHANGES
```
$ git diff
$ git status
$ git add -A
$ git commit -m 'changed somethin'

# git pull origin master
$ git push origin master
```

##  CREATE A BRANCH FOR DESIRED FEATRUE

```
$ git branch calc-divide
$ git checkout calc-divide
```

## AFTER COMMIT PUSH BRANCH TO REMOTE
```
$ git push -u origin calc-divide
$ git branch -a
```
## MERGE A BRANCH
```
$ git checkout master

$ git pull origin master

$ git branch --merged

$ git merge calc-divide

$ git push origin master
```

## DELETETING A BRANCH
```
$ git branch --merged

$ git branch -d calc-divide

$ git branch -a 

$ git push origin --delete calc-divide
```

## AMEND COMMIT MESSAG
```
$ git commit --amend -m 'Complete Subtract'
```

## MOVE COMMIT
```
$ git log  
$ git checkout subtract-feature

# git cherry-pick 1bxasdad 
 

```

## UNDO MASTER COMMIT
```
$ git checkout master
$ git log
$ git reset --soft/mix/hard 111xxxx
 
```

## REVERT COMMIT
```
$ git log
$ git revert hashxxx
$ git log
```