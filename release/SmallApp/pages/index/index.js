//index.js
//获取应用实例
const app = getApp()
var QQMapWX = require('../../utils/qqmap-wx-jssdk.js');
var qqmapsdk;

Page({
  data: {
    card_colors: ["rgba(252,157,154,0.18)", "rgba(131,175,155, 0.18)", "rgba(249,205,173, 0.18)", "rgba(200,200,169, 0.18)"],
    res_data: [],      // 存储请求得到的数据
    pic: [],
    city: '北京',         // 存储当前城市，默认北京
    currentIndex: 0,  // 表示当前滑块的index
    index: 0,         // 表示当前内容在所有res_data中的index, 即当前用户看到的卡片的index
    underline: "",    // 当前复制链接是否有下划线
    swiper_h: "",
    pic_h: "",
    text_h: "",
    touch: {
      x: 0,
      y: 0
    },
    lastX: 0,          //滑动开始x轴位置
    lastY: 0,          //滑动开始y轴位置
    text: "没有滑动",
    copy_href: "https://www.baidu.com/s?wd=",
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 配置key
    qqmapsdk = new QQMapWX({
      key: 'XXXXXXXXXXXXXXXX'
    });

    this.getUserLocation(); // 获取位置并请求数据
    // 由于设置了swiper的margin-top为10px
    let Height0 = (wx.getSystemInfoSync().windowHeight - 10) + "px";
    // 多减去26px，一是阴影10px，二是实现margin-bottom为16px的效果
    // 注意图片不会以原比例缩放，固定高度占45%，目前还没出现特别难看的效果
    let Height1 = (wx.getSystemInfoSync().windowHeight - 36) * 0.45 + "px";
    let Height2 = (wx.getSystemInfoSync().windowHeight - 36) * 0.55 + "px";
    this.setData({
      swiper_h: Height0,
      pic_h: Height1,
      text_h: Height2
    })

  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    this.animation = wx.createAnimation()
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  getUserLocation: function () {
    let vm = this;
    wx.getSetting({
      success: (res) => {
        // console.log(JSON.stringify(res))
        //res.authSetting['scope.userLocation']==undefined 表示初始化进入该界面
        //res.authSetting['scope.userLocation']==false 表示非初始化进入该页面且未授权
        //res.authSetting['scope.userLocation']==true 表示地理位置授权
        if (res.authSetting['scope.userLocation'] != undefined && res.authSetting['scope.userLocation'] != true) {
          wx.showModal({
            title: '请求授权当前位置',
            content: '需要获取当前位置，请确认授权',
            success: function (res) {
              if (res.cancel) {
                wx.showToast({
                  title: '拒绝授权',
                  icon: 'none',
                  duration: 1000
                })
              } else if (res.confirm) {
                wx.openSetting({
                  success: function (dataAu) {
                    if (dataAu.authSetting['scope.userLocation'] == true) {
                      wx.showToast({
                        title: '授权成功',
                        icon: 'success',
                        duration: 1000
                      })
                      //再次授权，调用wx.getLocation的API
                      vm.getLocation();
                    } else {
                      wx.showToast({
                        title: '授权失败',
                        icon: 'none',
                        duration: 1000
                      })
                    }
                  }
                })
              }
            }
          })
        } else if (res.authSetting['scope.userLocation'] == undefined) {
          //调用wx.getLocation的API
          vm.getLocation();
        }
        else {
          //调用wx.getLocation的API
          vm.getLocation();
        }
      }
    })
  },
  //微信获得经纬度
  getLocation: function () {
    let vm = this;
    wx.getLocation({
      type: 'wgs84',
      success: function (res) {
        // console.log(JSON.stringify(res))
        var latitude = res.latitude
        var longitude = res.longitude
        vm.getLocal(latitude, longitude)
      },
      fail: function (res) {
        // console.log('fail' + JSON.stringify(res))
        wx.showToast({
          title: '获取地理位置失败',
          icon: 'none',
          duration: 1000
        })
      }
    })
  },
  // 获取当前地理位置
  getLocal: function (latitude, longitude) {
    let vm = this;
    qqmapsdk.reverseGeocoder({
      location: {
        latitude: latitude,
        longitude: longitude
      },
      success: function (res) {
        // console.log(JSON.stringify(res));
        // console.log(res.result.address)
        let city = res.result.ad_info.city
        // 设置当前城市
        vm.setData({
          city: city,
        })
        // 获取地址成功请求数据
        let pic = []
        wx.request({
          url: 'http://XXXXXXXXXXX/readquickly/api/getnews',    // 填写ip或者域名
          data: {
            city: city
          },
          header: {
            'content-type': 'application/json' // 默认值
          },
          success(res) {
            console.log(res.data);   // 打印数据
            // 将请求到的数据赋给res_data
            vm.setData({
              res_data: res.data
            })
            // 初次渲染第一张卡片
            pic[0] = vm.data.res_data[vm.data.index];
            pic[0].card_color = vm.data.card_colors[0];   // 注意：请求网络API，success中函数是一个独立的线程
            pic[0].pic = "../pictures/none.png"
            pic[1] = { 'title': '文章标题', 'source': '文章来源', 'href': '原文地址', 'time': '发布时间', 'text': '文章内容', 'pic': '../pictures/none.png' };
            pic[1].card_color = vm.data.card_colors[1];
            pic[2] = pic[1];
            pic[3] = pic[1];
            let copy_href = "https://www.baidu.com/s?wd=" + pic[0].title

            // 将初始pic的值赋给data中的pic
            vm.setData({
              pic: pic,
              copy_href: copy_href
            })
          },
          fail() {
            console.log("请求失败");
          }
        })
      },
      fail: function (res) {
        wx.showToast({
          title: '获取地理位置失败',
          icon: 'none',
          duration: 1000
        })
        // 获取地址失败，默认传北京
        let pic = []
        wx.request({
          url: 'http://XXXXXXXXXX/readquickly/api/getnews',    // 填写ip或者域名
          data: {
            city: '北京'
          },
          header: {
            'content-type': 'application/json' // 默认值
          },
          success(res) {
            console.log(res.data);   // 打印数据
            // 将请求到的数据赋给res_data
            vm.setData({
              res_data: res.data
            })
            // 初次渲染第一张卡片
            pic[0] = vm.data.res_data[vm.data.index];
            pic[0].card_color = vm.data.card_colors[0];   // 注意：请求网络API，success中函数是一个独立的线程
            pic[0].pic = "../pictures/none.png"
            pic[1] = { 'title': '文章标题', 'source': '文章来源', 'href': '原文地址', 'time': '发布时间', 'text': '文章内容', 'pic': '../pictures/none.png' };
            pic[1].card_color = vm.data.card_colors[1];
            pic[2] = pic[1];
            pic[3] = pic[1];
            let copy_href = "https://www.baidu.com/s?wd=" + pic[0].title

            // 将初始pic的值赋给data中的pic
            vm.setData({
              pic: pic,
              copy_href: copy_href
            })
          },
          fail() {
            console.log("请求失败");
          }
        })
      }
    })
  },

  //滑动移动事件
  handletouchmove: function (event) {
    var currentX = event.touches[0].pageX
    var currentY = event.touches[0].pageY
    var tx = currentX - this.data.lastX
    var ty = currentY - this.data.lastY
    var text = ""
    //左右方向滑动
    if (Math.abs(tx) > Math.abs(ty)) {
      if (tx < 0)
        text = "向左滑动"
      else if (tx > 0)
        text = "向右滑动"
    }
    //上下方向滑动
    else {
      if (ty < 0)
        text = "向上滑动"
      else if (ty > 0)
        text = "向下滑动"
    }

    //将当前坐标进行保存以进行下一次计算
    this.data.lastX = currentX
    this.data.lastY = currentY
    this.setData({
      text: text,
    });
  },

  //滑动开始事件
  handletouchtart: function (event) {
    this.data.lastX = event.touches[0].pageX
    this.data.lastY = event.touches[0].pageY
  },
  //滑动结束事件
  handletouchend: function (event) {

    // 获取当前index、currentIndex
    let index = this.data.index;
    let currentIndex = this.data.currentIndex;
    // 获取当前所有数据的长度
    let len = this.data.res_data.length;

    if (this.data.text == "向右滑动") {
      // 右滑，改变index，--
      if (index > 0)
        index--;
      else
        index = len - 1;
      // 右滑，改变currentIndex， --
      if (currentIndex > 0)
        currentIndex--;
      else
        currentIndex = 3;

      let temp = this.data.res_data[index];
      temp.card_color = this.data.card_colors[currentIndex];

      // 因为currentIndex是变量所以修改data中pic某一index下的数据需要做一下处理
      let temp_str = 'pic[' + currentIndex + ']';
      let copy_href = temp.href;

      // 如果图片为空，则给出none.png
      if (!temp.pic)
        temp.pic = "../pictures/none.png"
      // 如果链接为空，则百度搜索title  
      if (!copy_href)
        copy_href = "https://www.baidu.com/s?wd=" + temp.title;

      this.animation.scale(0.6).rotate(20).step({ duration: 300, })
        .rotate(0).scale(1).step({ duration: 300, })
      this.setData({
        copy_href: copy_href,
        text: "没有滑动",
        index: index,
        currentIndex: currentIndex,
        [temp_str]: temp,
        animation: this.animation.export(),
      })
    }
    else if (this.data.text == "向左滑动") {
      // 左滑，改变index，++
      if (index < len - 1)
        index++;
      else
        index = 0;
      // 左滑，改变currentIndex， ++
      if (currentIndex < 3)
        currentIndex++;
      else
        currentIndex = 0;

      let temp = this.data.res_data[index];
      temp.card_color = this.data.card_colors[currentIndex];

      // 因为currentIndex是变量所以修改data中pic某一index下的数据需要做一下处理
      let temp_str = 'pic[' + currentIndex + ']';
      // let copy_href = this.data.res_data[index].href;
      let copy_href = temp.href

      // 如果图片为空，则给出none.png
      if (!temp.pic)
        temp.pic = "../pictures/none.png"
      // 如果链接为空，则百度搜索title 
      if (!copy_href)
        copy_href = "https://www.baidu.com/s?wd=" + temp.title;

      this.animation.scale(0.6).rotate(-20).step({ duration: 300, })
        .rotate(0).scale(1).step({ duration: 300, })
      this.setData({
        copy_href: copy_href,
        text: "没有滑动",
        index: index,
        currentIndex: currentIndex,
        [temp_str]: temp,
        animation: this.animation.export(),
      })
    }

  },
  skew: function () {
    this.animation.rotate(Math.random() * 720 - 360).step()
      .scale(Math.random() * 2).step()
      .rotate(0).scale(1).step()
    this.setData({ animation: this.animation.export() })
  },

  // 复制链接函数
  copy_link: function () {

    let href = this.data.copy_href;
    this.setData({
      underline: "underline"
    })
    // 下滑线出现持续0.1s
    let vm = this
    setTimeout(function () {
      //要延时执行的代码
      wx.setClipboardData({
        data: href,
        success(res) {
          vm.setData({
            underline: ""
          })
        }
      })
    }, 100)
  },

})