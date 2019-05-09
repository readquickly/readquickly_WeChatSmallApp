const app = getApp()

Page({
  data: {
    underline:""
  },
  onLoad: function () {
  },
  copy_link: function () {
    let vm = this
    vm.setData({
      underline: "underline"
    })
    // 0.1s show the underline
    setTimeout(function () {
      //要延时执行的代码
      wx.setClipboardData({
        data: "This my copyed content",
        success(res) {
          vm.setData({
            underline: ""
          })
        }
      })
    }, 100)    
  }
  
})
