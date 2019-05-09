var Crawler = require("crawler");	// 导入 crawler 
var MongoClient = require('mongodb').MongoClient;	// 导入 mongodb
var url = "mongodb://localhost:27017/";		// MongoDB数据运行的URL

var c = new Crawler({
    jQuery: false,
    callback: function (error, res, done) {
        if (error) {
            console.log(error);
        } else {
            var items_array = [];
            var str = res.body;
            var obj = JSON.parse(str);
            obj = obj.data.items;
            var items_len = obj.length;
            MongoClient.connect(url, {useNewUrlParser: true}, function (err, db) {
                if (err) throw err;
                var dbo = db.db("article_items");	// 如果没有article_items数据库，会自动创建

                for (var i = 0; i < items_len; i++) {
                    items_array[i] = {};	// new 一个对象
                    items_array[i].title = obj[i].title;	// 创建 title 属性，并赋值
                    items_array[i].description = obj[i].description;
                    items_array[i].news_url = obj[i].news_url;
                    items_array[i].published_at = obj[i].published_at;
                    dbo.collection("items").insertOne(items_array[i], function (err, res) {	// 将items_array[i]写入 items 集合中,会自动创建
                        if (err) throw err;
                    });
                }
                db.close();
            });
        }
    }
});

c.queue('https://36kr.com/pp/api/newsflash?per_page=20');