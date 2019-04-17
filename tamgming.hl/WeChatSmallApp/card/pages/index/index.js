//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    pic: [{
      url: "../pictures/001.jpg",
      text: "罗杰·班尼斯特：四分钟内跑完一英里的第一人,1954年5月6日上午，罗杰•班尼斯特爵士（Sir Roger Bannister）完成了一件不可能的事情。\n当时英国《每日电讯报》撰文称四分钟内跑完一英里（约1600米）是“体育运动最伟大的目标”，“就像珠穆朗玛峰一样是难以到达、看似无法做到的事情”。",
      card_color: "rgba(252,157,154,0.18)"
    },
    {
      url: "../pictures/002.jpg",
      text: "阿什利塔·福曼：全球拥有最多吉尼斯世界纪录称号的挑战者\n在吉尼斯世界纪录档案中，有很多人都是多项纪录的保持者。但谁都比不上阿什利塔·福曼（Ashrita Furman）创下的世界纪录称号多。阿什利塔·福曼来自纽约布鲁克林，他是当今世界上拥有最多吉尼斯世界纪录称号的挑战者。",
      card_color: "rgba(131,175,155, 0.18)"
    },
    {
      url: "../pictures/003.jpg",
      text: "佩吉·惠特森：太空行走次数最多的女性\n从苏联宇航员尤里·加加林到美国宇航员尼尔•阿姆斯特朗和巴兹·奥尔德林，全世界最著名的太空旅行者往往都是男性。\n但是美国女宇航员佩吉·惠特森（Peggy Whitson）所取得的伟大成就，对于平衡这种男女失衡的局面大有帮助。",
      card_color: "rgba(249,205,173, 0.18)",
    },
    {
      url: "../pictures/004.jpg",
      text: "尼尔·阿姆斯特朗和巴兹·奥尔德林：登上月球的第一人\n“这是我个人的一小步，却是人类迈出的一大步。”\n没有人能否认尼尔•阿姆斯特朗（Neil Armstrong）1969年7月20日晚上登陆月球时所说的第一句话具有的象征性意义。",
      card_color: "rgba(200,200,169, 0.18)",
    }
    ],
    swiper_h: "",
    touch: {
      x: 0,
      y: 0
    },
    lastX: 0,          //滑动开始x轴位置
    lastY: 0,          //滑动开始y轴位置
    text: "没有滑动",
  },
  
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var query = wx.createSelectorQuery();
    query.select('.card').boundingClientRect()
    let vm = this;
    query.exec((res) => {
      var Height = (res[0].height + 20) + "px";
      vm.setData({
        swiper_h: Height
      })
      // console.log(listHeight);
      // 这样并不能动态获取每个swiper-item的高度
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

    if (this.data.text == "向右滑动") {
      this.animation.scale(0.6).rotate(20).step({ duration: 300, })
        .rotate(0).scale(1).step({ duration: 300, })
      this.setData({ animation: this.animation.export() })
    }
    else if (this.data.text == "向左滑动") {
      this.animation.scale(0.6).rotate(-20).step({ duration: 300, })
        .rotate(0).scale(1).step({ duration: 300, })
      this.setData({ animation: this.animation.export() })
    }
    this.setData({
      text: "没有滑动",
    });
  },
  skew: function () {
    this.animation.rotate(Math.random() * 720 - 360).step()
      .scale(Math.random() * 2).step()
      .rotate(0).scale(1).step()
    this.setData({ animation: this.animation.export() })
  }
})
