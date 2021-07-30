- [pandas](#pandas)
  - [pivot](#pivot)
  - [stack](#stack)
- [sys](#sys)
- [Time convert](#time-convert)
  - [pd.time to unix](#pdtime-to-unix)
  - [pd.time grouper](#pdtime-grouper)


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