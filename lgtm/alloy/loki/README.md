different kinds of queries in loki

There are:
pattern
regexp

```code
    count_over_time(
        {color="pink"} | regexp "(?P<video_url>.videos)"
        )

    count_over_time(
        {color="pink"} | regexp "(?P<video_url>[\\w|/]+)"
        [5m])


        count_over_time(
        {color="pink"} | regexp "(?P<video_url>(?<=\\/)(.*?)(?=\\/|$))"
        [5m])

        count_over_time(
        {color="pink"} | regexp "(?P<video_url>\\/[\\w|$]+)"
        [5m])
```
