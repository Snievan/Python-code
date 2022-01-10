
## time series axis for ticks
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig, ax = plt.subplots(figsize=(20,6))
ax.plot(x,y,label = 'A1车直流负载电流',linestyle='-',color = 'black')
# ax2 = ax.twinx()
ax.plot(x,z,label = 'A2车直流负载电流',linestyle='--',color = 'black')
hours = mdates.HourLocator(interval = 1)
h_fmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(h_fmt)
ax.tick_params(axis='x', labelsize=18 )
ax.tick_params(axis='y', labelsize=18 )
plt.xlabel('时间/小时:分钟   ',fontsize=18,loc='center')
plt.ylabel('电流 I/A   ',fontsize=18,loc='center')
plt.title('2020年7月11日:' +'NJNL_T4车直流负载电流随时间变化曲线（按3min分割）',fontsize=20)
plt.legend(fontsize=15)
```