# Youtube video statistics with charts

Enter a Youtube channel link and get a chart with a number of videos uploaded per month.
Data acquired via Youtube API.

API endpoint
```
POST https://ytstats5.herokuapp.com/results
```
params
```
required: id=[channelID]
```
example
```
https://ytstats5.herokuapp.com/results?id=UCCezIgC97PvUuR4_gbFUs5g
```

Check it out at https://ytstats5.netlify.com/

[Frontend source code](https://github.com/korpog/yt-stats-vue)

![alt text](https://i.imgur.com/Cskkr5l.jpg)
