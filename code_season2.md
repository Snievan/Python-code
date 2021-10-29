- [Class related](#class-related)
  - [get subclass module's filename](#get-subclass-modules-filename)
- [pandas](#pandas)
  - [change column-data-types](#change-column-data-types)
- [Itertools](#itertools)
  - [Grouper](#grouper)
  - [pivot](#pivot)
  - [stack](#stack)
- [sys](#sys)
- [Time relate](#time-relate)
  - [pd: ymd to unix](#pd-ymd-to-unix)
  - [pd: unix to ymd](#pd-unix-to-ymd)
  - [pd.time grouper](#pdtime-grouper)
- [csv](#csv)
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


# Class related

## get subclass module's filename

```py
import importlib

class BaseClass:
    def __init__(self):
        m = importlib.import_module(self.__module__)
        print m.__file__
```

# pandas
## change column-data-types

# Itertools
## Grouper
```py
from itertools import zip_longest
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
```

## pivot 
- pivot
- adad

## stack
```python
def split_by_last_sep(name: str, sep: str = '-'):
    """Seperate the sentence with last seperator"""
    name_list = name.split(sep)
    prefix = sep.join(name_list[:-1])
    suffix = name_list[-1]
    if prefix == '' or suffix == '':
        raise ValueError(
            f"There is no seperator '{sep}' in the string has wrong format")
    return prefix, suffix


def stack_dataframe(df: pd.DataFrame, stack_columns: List[str], suffix_name: str, sep: str = '-') -> pd.DataFrame:
    """Stack the datafram. Trans columns to rows.
    For example:    
    the og data has cols ['val-1','val-2'] these cols can be trans to follow format:    
        coach   val 
        1       *   
        2       *   
    """
    df = df.copy()
    column_name_tuple = [split_by_last_sep(col, sep) for col in stack_columns]
    index_columns = [col for col in df if col not in stack_columns]
    df.set_index(index_columns, inplace=True)
    df = df[stack_columns]

    # set multi column namses
    multicol = pd.MultiIndex.from_tuples(column_name_tuple)
    df.columns = multicol

    # stack
    df_stack = df.stack()

    # change added
    index_names = list(df_stack.index.names)
    index_names[-1] = suffix_name
    df_stack.index.set_names(index_names, inplace=True)

    df_stack.reset_index(inplace=True)

    return df_stack
```
# sys
- sys.getsizeof()

# Time relate
## pd: ymd to unix
```python
pd.Timestamp('2021-04-01 00:02:35.234').timestamp()
```

## pd: unix to ymd
```python
df5['ymd'] = pd.to_datetime(df5['time'].values, unit = 'ms', utc= True).tz_convert("Asia/Shanghai")
```


## pd.time grouper
```python
df.groupby(pd.Grouper(key="Publish date", freq="1W")).mean()
```

# csv 
```python
def write_log(log_data: list, file_path: str = './ae_model.csv'):
    'Write log data to local csv file'
    with open(file_path, 'a',newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(log_data)
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