# 用来参考的 mineWeather

在这个目录下有两个主要的实现源代码(`*.js`)，二者的主要区别是: 
* `weather.js` 是一开始实现的版本
* `weather_0.2.0.js` 中加入了高德地图确定定位（需要https才能用）并使用了链条上式的设计。

## 可用的 API 使用方式

### 移动端

```
<!-- mineWeather -->
http://api.p.weatherdt.com/h5.html?id=FuToYa86aN
```

### Web插件

```
<!-- mineWeather -->
<div id="weather-view-he"></div>
<script>
WIDGET = {ID: 'yhevzGf1Yc'};
</script>
<script type="text/javascript" src="http://api.p.weatherdt.com/float/static/js/r.js?v=1111"></script>
```

API--空气质量
https://free-api.heweather.net/s6/air/now?location=beijing&key=HE1812241515581296

API--生活指数
https://free-api.heweather.net/s6/weather/lifestyle?location=kunming&key=HE1812241515581296

API--日月出落
https://free-api.heweather.net/s6/solar/sunrise-sunset?location=kunming&key=HE1812241515581296

常规天气数据集合
https://free-api.heweather.net/s6/weather?location=kunming&key=HE1812241515581296

实况数据
https://free-api.heweather.net/s6/weather/now?location=kunming&key=HE1812241515581296
