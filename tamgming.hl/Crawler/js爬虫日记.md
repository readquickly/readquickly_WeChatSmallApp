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

-------------------------- 2019， April 6th --------------------------

- 在Windows下安装MongoDB，并使用cmd进入到bin目录下
- 执行mongod.exe --dbpath "一个空白文件的目录"
- 打开另一个cmd，同样进入bin目录下，执行mongo.exe，在此终端可以执行MongoDB的各种命令 

- npm install mongodb

mongodb的一些入门操作

- `var MongoClient = require("mongodb").MongoClient;`     *导包*
- `var url = "mongodb://localhost:27017/"`  *存MongoDB运行的URL，端口默认27017*
- `MongoClient.connect(url, {useNewUrlParser: true}, function (err, db) { });`   *配参*
- *函数体中可以对数据库进行操作，操作完执行* `db.close();` *断开与数据的连接*

