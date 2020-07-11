# 北捷 各站 車廂擁擠度 圖形化

北捷 各站 車廂擁擠度 圖形化

聽說前陣子北捷推出了 [車廂擁擠度即時告知功能](https://udn.com/news/story/7323/4545992),用那個API畫畫看圖OAO  

```
python3 crawl.py #抓取資料,抓取
python3 draw.py 222.json #畫圖
```



- 2020-07-16 (六) 非上班時刻 頂埔->南港展覽館
    ![](https://github.com/chenliTW/MRT-analysis/raw/master/pic/one.png)
    - BL05 出海山後亞東突然變多人
    - BL06 府中沒人要走去第一跟第最後一節車廂
    - BL11 西門站首次出現下降趨勢(板橋有微小微小下降)
    - BL15 過忠孝復興就沒有增加的趨勢
    - BL18 市政府下將的超陡
    - 沒神摸人要搭第一跟第六節車廂

    ![](https://github.com/chenliTW/MRT-analysis/raw/master/pic/multi.png)