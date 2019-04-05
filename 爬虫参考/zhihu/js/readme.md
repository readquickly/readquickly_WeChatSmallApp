### 利用js进行爬虫

-------------------------- 2019， April 5th --------------------------

- 安装Node.js，并配置Webstorm
- npm install crawler
- 在NetWork中找到XHR，一个一个地找对应渲染HTML数据相关的js（通过preview），请求地址填相应的

Request URL

```js
var Crawler = require("crawler");

var c = new Crawler({
    callback : function (error, res, done) {
        if(error) {
            console.log(error);
        }
        else {
            var str = res.body;	// 获得 json 字符串
            var obj = JSON.parse(str);	// 将 json 字符串转为 json 对象
            var len = obj.data.length;	// json 对象 data 对应一个数组
            for(var i = 0; i < len; i++) {
                console.log(obj.data[i]);	// 将每篇文章的简略信息打印出来
            }
        }
    }
});

c.queue('https://zhuanlan.zhihu.com/api/columns/natureresearch/articles?limit=100&offset=100')
```

参数设为100，爬取Nature自然科研的一百篇文章的简略信息

如果需要存入Nature.json文件中，可添加

```js
var fs = require("fs");
var data_str = JSON.stringify(obj.data);
fs.writeFile('Nature.json', data_str, function(err) {
    if(err) {
        console.log(err);
    }
});
```

在Nature10.js只爬取十篇文章为例