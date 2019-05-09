### card 界面设计及实现

-------------------------- Apirl 16th -------------------------- 

##### 实现了卡片初步的UI

问题：暂时没有解决图片加文字的高度与swiper组件保持一致，

为了方便，计划使用 scroll-view 来存放内容，因为要防止文字特别多的情况，

同时固定住 card 的大小

-------------------------- Apirl 18th -------------------------- 

##### 进一步细化UI，实现scroll-view

- 计算 card 高度

```js
 onLoad: function (options) {
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
```

