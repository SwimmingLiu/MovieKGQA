//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: 'Hello World',
    avatarUrl:'',
    nickName:''
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  loginCenterIndex: function(){
    
    wx.navigateTo({
      url: '../chat/chat'
    })
  },
  
  onLoad: function () {
    //console.log('onLoad')
    var that = this
    //调用应用实例的方法获取全局数据
    app.getUserInfo(function(userInfo){
      //更新数据
      that.setData({
        userInfo:userInfo
      })
    });
    wx.showShareMenu({
      withShareTicket:true,
      menus:['shareAppMessage','shareTimeline']
      })
  },
    /**
   * 退回上一页
   */
  toBackClick: function() {
    wx.navigateBack({})
  },
  onShow: function () {
    let that = this;
    wx.getUserInfo({
      success: function (res) {
        that.setData({
          avatarUrl: res.userInfo.avatarUrl,
          nickName: res.userInfo.nickName
        });
      },
      fail: function (res) {
        // 用户拒绝授权或其他失败情况处理
      }
    });
  }

})
