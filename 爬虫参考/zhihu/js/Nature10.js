var Crawler = require("crawler");
var fs = require("fs");

var c = new Crawler({
    jQuery: false,
    callback : function (error, res, done) {
        if(error) {
            console.log(error);
        }
        else {
            var str = res.body;	// 获得 json 字符串
            var obj = JSON.parse(str);	// 将 json 字符串转为 json 对象
            var data_str = JSON.stringify(obj.data);
            fs.writeFile('Nature10.json', data_str, function(err) {
                if(err) {
                    console.log(err);
                }
            });
        }
    }
});

c.queue('https://zhuanlan.zhihu.com/api/columns/natureresearch/articles?limit=10&offset=10');