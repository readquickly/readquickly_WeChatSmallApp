'use strict'

// 用观察者模式来完成把 getLocation 完成后再 getWeather 的过程，参考https://www.cnblogs.com/darrenji/p/3927096.html

var weather_data = {};
var IconPath = "./img/icon/";
var collapseSettle = {
        blockParent: '#mineWeather_div',
        beforeD: null,
        afterD: null,
        blockSize: { width: "150", height: "150" },
};

// Get Location Infomation
$(document).on('weather.ask', function (e, loc) {
        if (loc == 'auto_ip') {
                if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(function (position) {
                                // 获取成功，处理后发布给 Get city Data, 为满足 高德api 经度在前，纬度在后 的要求
                                var loc = position.coords.longitude.toString() + ',' + position.coords.latitude.toString();
                                $(document).trigger('weather.location.done', loc);
                                // console.log('Location', loc);
                        }, function (err) {
                                // 获取失败，不处理，发布给 Get Weather Data
                                alert('获取地理位置失败，显示IP所在位置的天气。');
                                $(document).trigger('weather.city.done', loc);
                        });
                } else {
                        // navigator.geolocation 不可用，不处理，发布给 Get Weather Data
                        alert('获取地理位置失败，显示IP所在位置的天气。');
                        $(document).trigger('weather.city.done', loc);
                }
        } else {
               // 用户指定了city，不处理，发布给 Get Weather Data
               $(document).trigger('weather.city.done', loc); 
        }
})

// Get city Data
$(document).on('weather.location.done', function (e, loc) {
        // 高德地图
        var KEY = '0803d861050139a6e380bdca73ef68a9';
        var host = 'https://restapi.amap.com/v3/geocode/regeo?';
        var url = host + 'location=' + loc + '&key=' + KEY;
        $.getJSON(url, function (data) {
                var city = data.regeocode.addressComponent.city;
                $(document).trigger('weather.city.done', city)
        })
})

// Get Weather Data
$(document).on('weather.city.done', function (e, loc) {
        // 和风天气
        var KEY = 'HE1812241515581296';
        var HOSTS = {
                wtr: 'https://free-api.heweather.net/s6/weather?',
                air: 'https://free-api.heweather.net/s6/air/now?'
        };
        for (var hostKey in HOSTS) {
                var url = HOSTS[hostKey] + 'location=' + loc + '&key=' + KEY;
                // console.log(url);
                (function (item) {
                        $.getJSON(url, function (data) {
                                var res = {};
                                res[item] = data.HeWeather6[0];
                                $(document).trigger('weather.data.got', res);
                                // console.log('Raw', res);
                        });
                })(hostKey);

        }
})

// Merge Weather Data
$(document).on('weather.data.got', function (e, data) {
        // console.log('merging', data);
        weather_data[Object.keys(data)[0]] = Object.values(data)[0];
        // console.log('merged data', weather_data);
        if (Object.keys(weather_data).length == 2) {      // Have got both weather and air
                $(document).trigger('weather.data.merged');
        }
})

// Echo Collapse
$(document).on('weather.data.merged', function () {
        // 加载数据
        var data = weather_data.wtr;
        var blockParent = collapseSettle.blockParent,
                beforeD = collapseSettle.beforeD,
                afterD = collapseSettle.afterD,
                blockSize = collapseSettle.blockSize;
        // 重整数据
        var weatherCollapse = {
                loc: "",
                cond: "",       // 天气状况（阴，晴，...)
                tmp: "",        // 实况温度
                icon_src: IconPath         // 先在这里指定 path ，后面加上 filename 就行
        };
        if (!data || data.status !== 'ok') {
                weatherCollapse.loc = "天气";
                weatherCollapse.cond = "😨天气加载失败";
                weatherCollapse.tmp = "";
                weatherCollapse.icon_src += "999.png";
        } else {
                weatherCollapse.loc = data.basic.location || "天气";
                weatherCollapse.cond = data.now.cond_txt || "😨天气加载失败";
                weatherCollapse.tmp = (data.now.tmp + "˚C") || "";
                weatherCollapse.icon_src += (data.now.cond_code + ".png") || "999.png";
        }
        // 用一个 Canvas 安放 weather block
        var weatherCanvas = document.createElement("canvas");
        weatherCanvas.id = "mineWeatherCollapse_canvas";
        weatherCanvas.width = blockSize.width;
        weatherCanvas.height = blockSize.height;

        var ctx = weatherCanvas.getContext('2d');
        ctx.globalCompositeOperation = "xor";
        // 天气图
        var img = new Image();
        img.src = weatherCollapse.icon_src;
        var imgSize = (parseInt(blockSize.width) + parseInt(blockSize.height)) / 2 * 0.8;

        img.onload = function () {
                ctx.drawImage(img, 0, 0, imgSize, imgSize);
        }
        // 城市
        ctx.font = (imgSize / (6 + weatherCollapse.loc.length / 2)).toString() + "px Arial";
        ctx.fillStyle = "#ffbb0a";
        ctx.fillText(weatherCollapse.loc, imgSize * 0.8 - Math.pow(weatherCollapse.loc.length, 2), imgSize / 5)
        // 天气状态
        ctx.font = (imgSize / (3 + weatherCollapse.cond.length)).toString() + "px Arial";
        ctx.strokeText(weatherCollapse.cond, 0, imgSize / 0.9);
        // 当前温度
        ctx.fillStyle = "#0accff";
        ctx.font = (imgSize / (3 + weatherCollapse.tmp.length)).toString() + "px Arial ";
        ctx.fillText(weatherCollapse.tmp, imgSize * 0.6, imgSize * 1.1)

        // 输出
        var pt = $(blockParent);
        if (pt) {
                if (beforeD && !afterD) {
                        var bt = $(beforeD);
                        bt.before(weatherCanvas);
                } else if (!beforeD && afterD) {
                        var at = $(afterD);
                        at.after(weatherCanvas);
                } else {
                        pt.append(weatherCanvas);
                }
        }

        // 控制详情开关
        $('#mineWeatherCollapse_canvas').click(function () {
                weatherExpand(collapseSettle.blockParent, null, '#mineWeatherCollapse_canvas');
                $('#mineWeatherExpand').ready(function () {
                        $('#close_weather').click(function () {
                                $('#mineWeatherExpand').hide('slow');
                                location.href = "#mineWeatherCollapse_canvas";
                        });
                        $('#more_weather').click(function () {
                                var moreWeather = 'http://api.p.weatherdt.com/h5.html?id=FuToYa86aN';
                                window.open(moreWeather, '_blank');
                        });
                });
                location.href = "#mineWeatherCollapse_canvas";
        });
})

function weatherExpand(blockParent, beforeD = null, afterD = null) {  // 父元素的jQuery选择器, 显示的位置。
        // 相关函数
        function getDailyForecast(daily) {
                return {
                        icon_d: IconPath + daily.cond_code_d + ".png",
                        icon_n: IconPath + daily.cond_code_n + ".png",
                        cond_d: daily.cond_txt_d,
                        cond_n: daily.cond_txt_n,
                        tmp_max: daily.tmp_max,
                        tmp_min: daily.tmp_min,
                        Rrain: daily.pop        // 降水概率
                }
        }

        // 获取数据
        var weatherData = weather_data.wtr;
        var airData = weather_data.air;
        // console.log(weatherData);
        // console.log(airData);
        // 数据整理
        var barWeatherBlock = {
                location: "",
                now: {},
                forecast: [],
                lifestyle: [],
                update: ""
        };

        if (!weatherData || !airData || weatherData.status !== 'ok' || airData.status !== 'ok') {
                // location
                barWeatherBlock.location = "重新加载";
                // now
                barWeatherBlock.now.cond = "😨";
                barWeatherBlock.now.tmp = "";
                barWeatherBlock.now.fl = "";    // 体感温度
                barWeatherBlock.now.icon_src = IconPath + "999.png";
                barWeatherBlock.now.aqi = "";
                barWeatherBlock.now.airQlty = "";
                barWeatherBlock.now.vis = "";
                barWeatherBlock.now.wind_dir = "";
                barWeatherBlock.now.wind_spd = "";
                barWeatherBlock.now.hum = "";   // 相对湿度
                barWeatherBlock.now.Rrain = "";
                // forecast
                barWeatherBlock.forecast = [null, null, null];
                // lifestyle
                barWeatherBlock.lifestyle.push("Fault to get the weather data from services ");
                // update
                barWeatherBlock.update = "";
        } else {
                // location
                barWeatherBlock.location = weatherData.basic.location || "重新加载";
                // now
                barWeatherBlock.now.cond = weatherData.now.cond_txt || "😨";
                barWeatherBlock.now.tmp = (weatherData.now.tmp + "˚C") || "";
                barWeatherBlock.now.fl = (weatherData.now.fl + "˚C") || "";
                barWeatherBlock.now.icon_src = (IconPath + weatherData.now.cond_code + ".png") || (IconPath + "999.png");
                barWeatherBlock.now.aqi = airData.air_now_city.aqi || "";
                barWeatherBlock.now.airQlty = airData.air_now_city.qlty || "";
                barWeatherBlock.now.vis = (weatherData.now.vis + "km") || "";
                barWeatherBlock.now.wind_dir = weatherData.now.dir || "";
                barWeatherBlock.now.wind_spd = (weatherData.now.wind_spd + "km/h") || "";
                barWeatherBlock.now.hum = weatherData.now.hum || "";
                barWeatherBlock.now.Rrain = weatherData.now.pcpn || "";
                // forecast
                barWeatherBlock.forecast.push(weatherData.daily_forecast.map(getDailyForecast));
                // lifestyle
                barWeatherBlock.lifestyle.push(weatherData.lifestyle.map(x => x.txt));
                // update
                barWeatherBlock.update = weatherData.update.loc || "Newest";

        }

        // 构建 DOM
        // Parent
        var bar = $('<div id="mineWeatherExpand"></div>');
        bar.css('background-color', '#eaefef');
        bar.css('color', '#000000');
        var bar_cont_encap = $('<div class="container">');
        var bar_cont = $('<div class="row" id="weatherCont"></div>');
        // Head & Location
        var div_head = $('<div class="container"></div>');
        var div_head_cont = $('<div class="header"></div>');
        div_head_cont.append('<button type="button" id="close_weather" class="close"><span>&times;</span></button>');
        div_head_cont.append('<h1>mine Weather</h1>');
        div_head_cont.append('<p style="text-align: right"><a href="./unfound">' + barWeatherBlock.location + '</a></p>');        // 暂时不可更改城市
        div_head_cont.append('<p style="text-align: right"><small>数据刷新时间: ' + barWeatherBlock.update + '<small></p>');
        div_head.append(div_head_cont);
        // now
        var div_now = $('<div class="col-xs-5 col-sm-3 col-md-3" id="weatherNow" style="Arial, Helvetica, sans-serif; text-align: jusifity;"></div>');
        div_now.append('<h2 style="font-family: STKaiti, KaiTi, sans-serif;"><strong>当前</strong></h2><br>')
        div_now.append('<img src="' + barWeatherBlock.now.icon_src + '" alt="' + barWeatherBlock.now.cond + '">');
        div_now.append('<strong>' + barWeatherBlock.now.cond + '</strong>');
        div_now.append('<p>当前气温: &nbsp;' + barWeatherBlock.now.tmp + '</p>');
        div_now.append('<p>体感温度: &nbsp' + barWeatherBlock.now.fl + '</p>');
        div_now.append('<p>空气质量: &nbsp;' + barWeatherBlock.now.airQlty + '</p>');
        div_now.append('<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A&nbsp;Q&nbsp;I: &nbsp;' + barWeatherBlock.now.aqi + '</p>');
        div_now.append('<p>&nbsp;&nbsp;&nbsp;能见度: &nbsp;' + barWeatherBlock.now.vis + '</p>');
        div_now.append('<p>相对湿度: &nbsp;' + barWeatherBlock.now.hum + '</p>');
        div_now.append('<p>&nbsp;&nbsp;&nbsp;降水量: &nbsp;' + barWeatherBlock.now.Rrain + '</p>');
        div_now.append('<p>&nbsp;&nbsp;&nbsp;风情况: &nbsp;' + barWeatherBlock.now.wind_dir + barWeatherBlock.now.wind_spd + '</p>');
        // forecast
        var div_forecast = $('<div class="col-xs-6 col-sm-4 col-md-4" id="weatherForecast" style="font-family: STFangsong, FangSong, Arial, Helvetica, sans-serif"></div>');
        var forecast_cont = ['', '', ''];
        var pic_size = "30px";
        // console.log(barWeatherBlock.forecast);
        for (var i = 0; i < 3; i++) {
                // console.log(i, barWeatherBlock.forecast);
                forecast_cont[i] = '<img src="' +
                        barWeatherBlock.forecast[0][i].icon_d +
                        '" alt="' +
                        barWeatherBlock.forecast[0][i].cond_txt_d +
                        '" width="' + pic_size + '" height="' + pic_size + '"> --> <img src="' +
                        barWeatherBlock.forecast[0][i].icon_n +
                        '" alt="' +
                        barWeatherBlock.forecast[0][i].cond_txt_n +
                        '" width="' + pic_size + '" height="' + pic_size + '"> : &nbsp;' +
                        barWeatherBlock.forecast[0][i].tmp_min +
                        '~' +
                        barWeatherBlock.forecast[0][i].tmp_max +
                        '&nbsp;----&nbsp;降水概率: ' +
                        barWeatherBlock.forecast[0][i].Rrain
        }
        div_forecast.append('<h2 style="font-family: STKaiti, KaiTi, sans-serif"><strong>预报</strong></h2><br>');
        div_forecast.append('<p>今天: ' + forecast_cont[0] + '</p><hr>');
        div_forecast.append('<p>明天: ' + forecast_cont[1] + '</p><hr>');
        div_forecast.append('<p>后天: ' + forecast_cont[2] + '</p>');
        // lifestyle
        var div_lifestyle = $('<div class="col-xs-6 col-sm-4 col-md-4"" id="weatherLifestyle" style="font-family: STKaiti, KaiTi, sans-serif"></div>');
        div_lifestyle.append('<h2 style="font-family: STKaiti, KaiTi, sans-serif"><strong>生活</strong></h2><br>');
        for (var i of barWeatherBlock.lifestyle[0]) {
                div_lifestyle.append('<p>' + i + '</p>');
        }
        // 整合
        bar_cont.append(div_now);
        bar_cont.append(div_forecast);
        bar_cont.append(div_lifestyle);

        bar_cont_encap.append(bar_cont);

        bar.append('<br><br><hr>');
        bar.append(div_head);
        bar.append(bar_cont_encap);
        bar.append('<hr>');
        bar.append('<button type="button" id="more_weather" style="text-align: center">Learn more</button>');
        bar.append('<p style="text-align: center"><small>Data & Icon from: <a href="https://www.heweather.com" target="_blank">Heweather</a></small></p>');
        bar.append('<hr>');

        // 输出
        var pt = $(blockParent);
        if (pt) {
                if (beforeD && !afterD) {
                        var bt = $(beforeD);
                        bt.before(bar);
                } else if (!beforeD && afterD) {
                        var at = $(afterD);
                        at.after(bar);
                } else {
                        pt.append(bar);
                }
        }
}