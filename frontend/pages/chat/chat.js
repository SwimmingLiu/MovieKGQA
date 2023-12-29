// pages/contact/contact.js
const app = getApp();
var inputVal = '';
var msgList = [];
var showReminder = true;
var imageUrl = '/img/voice.png' 

// 假设 asr.js 存放在 utils 目录下
const asr = require('../../utils/asr.min.js');
/** asr.js **/
// 获取应用实例
// 和使用插件调用方式有所区别：
let speechRecognizerManager;
// 引入asr.js实例时：
speechRecognizerManager = asr.getRecorderSpeechRecognizer; // isLog 非必填参数，类型为boolean，当值 为true时可打印日志调试。 

// 若不需要录音，只调用识别功能的话，按如下方式调用，识别结果回调和使用 录音 + 识别回调一致：
let speechRecognizer = new asr.SpeechRecognizer(); // isLog 非必填参数，类型为boolean
let resultText = '';  
var windowWidth = wx.getSystemInfoSync().windowWidth;
var windowHeight = wx.getSystemInfoSync().windowHeight;
var keyHeight = 0;

var kgqa_url = "https://fish-sincere-yearly.ngrok-free.app/q/";
//var key='4df93a740973db51a50ff9dea1304f80.XwsWdfe2xyxYnvRy'; //存放API秘钥1
var key='6e30fbcc202f5013028d92d7098fef3b.i22ixkhUroSuO6Yv'; //我的API秘钥
var model="chatglm_lite";   //选择模型 轻量级
// var _url= 'http://47.96.133.86:5000/'; //我的服务器接口
// var _url= 'http://47.115.23.82:5000/'; //服务器接口
var _url= 'https://ai.stdiet.top';
//var _url='https://open.bigmodel.cn/api/paas/v3/model-api/chatglm_lite/sse_invoke';


/**
 * 初始化数据
 */
function initData(that) {
  inputVal = '';
 
  msgList = [
    // {
    //   speaker: 'server',
    //   contentType: 'text',
    //   content: '您好，我是您的电影知识问答助手。您可以随意问我与电影相关的问题，例如“成龙是谁？”'
    // },
    // {
    //   speaker: 'customer',
    //   contentType: 'text',
    //   content: '好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的好的'
    // }
  ]
  showReminder = true;
  that.setData({
    msgList,
    inputVal,
    showReminder,
    imageUrl,
    socket: null,
    speechRecognizerManager: null,
    isCanSendData: false,
    result: '',
    res:'',
    recording: false,
    disabled: false,
    isRecognizeStop: false,
    recognizeResult: ''
  })
 
}

/**
 * 计算msg总高度
 */
// function calScrollHeight(that, keyHeight) {
//   var query = wx.createSelectorQuery();
//   query.select('.scrollMsg').boundingClientRect(function(rect) {
//   }).exec();
// }

Page({

  /**
   * 页面的初始数据
   */
  data: {
    scrollHeight: '100vh',
    inputBottom: 0,
    zhanweiHeight:'100px',
    scrollTop: 10000,
    reminderList: [
        {
            reminderText:'Stephen Chow是谁?'
        },
        {
            reminderText:'张国荣演了多少电影？'
        },
        {
            reminderText:'霸王别姬上映时间?'
        },
        {
            reminderText:'梁朝伟的作品有哪些?'
        },
        {
            reminderText:'周星驰演了哪些风格的电影？'
        },
        {
            reminderText:'肖申克的救赎讲了什么？'
        },
        {
            reminderText:'黄渤的家乡?'
        },
        {
            reminderText:'周润发演过哪些喜剧类电影？'
        },
        {
            reminderText:'阿甘正传的风格是什么？'
        }
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    initData(this);
    this.setData({
      //cusHeadIcon: app.globalData.userInfo.avatarUrl,
    });
    wx.showShareMenu({
      withShareTicket:true,
      menus:['shareAppMessage','shareTimeline']
      })
    
    this.speechRecognizerManager = speechRecognizerManager();

    // 开始识别
    this.speechRecognizerManager.OnRecognitionStart = (res) => {
      console.log('开始识别', res);
      this.isCanSendData = true;
      this.setData({
        recording: true,
        disabled: true,
        result: '',
      });
    };
 
    // 一句话开始
    this.speechRecognizerManager.OnSentenceBegin = (res) => {
      console.log('一句话开始', res);
    };
    // 识别变化时
    this.speechRecognizerManager.OnRecognitionResultChange = (res) => {
      console.log('识别变化时', res);
      this.setData({
        result: `${resultText || ''}${res.result.voice_text_str}`
      });
    };
    // 一句话结束
    this.speechRecognizerManager.OnSentenceEnd = (res) => {
      console.log('一句话结束', res);
      resultText += res.result.voice_text_str;
      this.setData({
        result: resultText
      });
    };
    // 识别结束
    this.speechRecognizerManager.OnRecognitionComplete = (res) => {
      console.log('识别结束', res);
      this.isRecognizeStop = true;
      this.setData({
        recording: false,
        disabled: false
      });
    };
    // 识别错误
    this.speechRecognizerManager.OnError = (res) => {
      console.log(res);
      this.isCanSendData = false;
      this.setData({
        recording: false,
        disabled: false
      });
    };
  },
  startLy:  async function(e){
    const self = this;
    wx.getSetting({
      success(res) {
        if (!res.authSetting['scope.record']) {
          wx.authorize({
            scope: 'scope.record',
            success() {
              // 用户已经同意小程序使用录音功能，后续调用 record 接口不会弹窗询问
              self.startAsr();
            }, fail() {
              wx.showToast({ title: '未获取录音权限', icon: 'none' });
              // console.log("fail auth")
            }
          });
        } else {
          self.startAsr();
          // console.log("record has been authed")
        }
      }, 
      fail(res) {
        // console.log("fail",res)
      }
    });
  },
  startAsr: function() {
    // wx.showToast({
    //   title: '建立连接中',
    //   icon: 'none'
    // });
    resultText = '';
    const params = {
      // 用户参数
      secretkey: '',
      secretid:  '',
      appid: 0,
      // 录音参数
      // duration: 100000,
      // frameSize: 1.28,  //单位:k

      // 实时识别接口参数
      engine_model_type : '16k_zh',
      // 以下为非必填参数，可跟据业务自行修改
      // hotword_id : '08003a00000000000000000000000000',
      needvad: 1,
      filter_dirty: 1,
      filter_modal: 1,
      filter_punc: 1,
      // convert_num_mode : 1,
      word_info: 2,
      vad_silence_time: 200
    };

    this.speechRecognizerManager.start(params);
    wx.vibrateShort();
  },
  endLy: function(e){
    this.setData({
      recording: false,
      disabled: false
    });
    this.speechRecognizerManager.stop();
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {
    this.setData({
        scrollTop: 10000
  })
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },
  /**
   * 获取聚焦
   */
  focus: function(e) {
    
    keyHeight = e.detail.height;
    this.setData({
        zhanweiHeight:keyHeight + 100 + 'px',
        scrollHeight: (windowHeight - keyHeight - 100) + 'px'
    });
    this.setData({
      toView: 'msg-' + (msgList.length - 1),
      inputBottom: keyHeight + 'px',
      showReminder : false
    })
    //计算msg高度
    // calScrollHeight(this, keyHeight);
    this.pageScrollToBottom();
  },

//失去聚焦(软键盘消失)
    blur: function(e) {
    this.setData({
     zhanweiHeight: '100px',
      scrollHeight: '100vh',
      inputBottom: 0,
      showReminder : true
    });
    this.pageScrollToBottom();
  },
  onTextareaInput:function(e){
    this.setData({
        inputVal:e.detail.value,
        toView: 'msg-' + (msgList.length - 1)
      })
  },

//页面自动滚动到底部
pageScrollToBottom: function() {
    this.setData({
        scrollTop: windowHeight + 10000
  })
      // wx.createSelectorQuery().select('#scrollpage').boundingClientRect(function(rect){
    //     wx.pageScrollTo({
    //         scrollTop: rect.bottom, // 设置一个足够大的值，以确保能够滚动到页面底部
    //         duration: 100 // 滚动持续时间
    //     });
    // }).exec();   
},
/*
    监听提示语
*/
    handleClick: function (e) {
    const text = e.currentTarget.dataset.text; // 获取view中存储的文本内容
    const inputText = text; // 将文本内容赋值给input的值
    // 使用选择器获取textarea组件，并设置其内容
    // 更新 textarea 的值
    this.setData({
        inputVal: inputText
      });
},
 gptRequest:function(inputvalue){
    let that = this;
    inputVal = '';
     wx.request({
            url: _url, 
            data:{
                APIModel:model,
                APIkey:key,
                info: inputvalue
            },
            
            //封装返回数据格式
            header: {
                'Content-Type': 'application/json'
            },
            //请求成功的回调
            success: function(res) {
             // console.log(res.data);
              
              let data = res.data;
            //   console.log(res.data);
              msgList.push({
                speaker:  'server',
                contentType: 'text',
                content: res.data + "(made by chatgpt)"
              })
              //调用set方法，告诉系统数据已经改变   启动循环，循环聊天信息
              that.setData({
                msgList,
                inputVal,
              })
              that.pageScrollToBottom();
              wx.setNavigationBarTitle({
                title: "电影知识系统小助手"
            })
            },
            fail: function (res) {
                msgList.push({
                    speaker:  'server',
                    contentType: 'text',
                    content: "发送请求失败，请检查你的网络。" + res.errMsg,
                  })
                  //调用set方法，告诉系统数据已经改变   启动循环，循环聊天信息
                  that.setData({
                    msgList,
                    inputVal
                  })
                  that.pageScrollToBottom();
                  wx.setNavigationBarTitle({
                    title: "电影知识系统小助手"
                })
              }

          })

 },
  /**
   * 发送点击监听
   */
  sendClick: function(e) {
    if (this.data.inputVal != ''){
        let inputvalue = this.data.inputVal;
        wx.setNavigationBarTitle({
            title: "对方正在输入中"
        })
        msgList.push({
            speaker: 'customer',
            contentType: 'text',
            content: this.data.inputVal
          })
        let that = this;
        inputVal = '';
        wx.request({
            url: kgqa_url + this.data.inputVal,
            method: 'POST', // 请求方法为 POST
            // data:{
            //     data : 
            // },
            //封装返回数据格式
            // header: {
            //     'Content-Type': 'application/json'
            // },
            //请求成功的回调
            success: function(res) {
             // console.log(res.data);
              
              let data = res.data;
              if (res.statusCode == 200 && typeof(res.data.answer) == "string"){
                  if (res.data.answer.includes("没有找到答案。") || res.data.answer.includes("抱歉，我无法理解这个问题")){
                        that.gptRequest(inputvalue);
                        return -1;
                  }else{
                    msgList.push({
                        speaker:  'server',
                        contentType: 'text',
                        content: res.data.answer,
                      })
                  }

                //调用set方法，告诉系统数据已经改变   启动循环，循环聊天信息
              }else if (res.statusCode == 200 && typeof(res.data.answer) == "object"){
                msgList.push({
                    speaker:  'server',
                    contentType: 'text',
                    content: res.data.answer.introduction,
                    image: res.data.answer.image
                })
              }
              else{
                    that.gptRequest(inputvalue);
                    return -1;
                }
                that.setData({
                    msgList,
                    inputVal,
                })
                that.pageScrollToBottom();
                wx.setNavigationBarTitle({
                    title: "电影知识系统小助手"
                })
            },
            fail: function (res) {
                msgList.push({
                    speaker:  'server',
                    contentType: 'text',
                    content: "发送请求失败，请检查你的网络。" + res.errMsg,
                  })
                  //调用set方法，告诉系统数据已经改变   启动循环，循环聊天信息
                  that.setData({
                    msgList,
                    inputVal
                  })
                  that.pageScrollToBottom();
                  wx.setNavigationBarTitle({
                    title: "电影知识系统小助手"
                })
              }
          });
        inputVal = '';
        this.setData({
            msgList,
            inputVal,                
        });
        that.pageScrollToBottom(); 
    }
  },

  /**
   * 退回上一页
   */
  toBackClick: function() {
    wx.navigateBack({})
  },
  voiceStart:function(e){
    let that = this;
    if (imageUrl == "/img/voice.png"){
        imageUrl = "/img/stop.svg"
        this.setData({
            imageUrl: imageUrl
        });
        this.startLy();
        this.setData({
            recording: true,
            scrollHeight: (windowHeight - 200) + 'px'
        }, () => {
            console.log("进入底部事件");
            this.pageScrollToBottom();
        });
    }
    else{
        imageUrl = "/img/voice.png"
        this.setData({
            imageUrl: imageUrl
        })
        this.endLy();
        inputVal = this.data.result;
        console.log(inputVal);
        this.setData({
            inputVal: inputVal
        });
        this.setData({
            scrollHeight: (windowHeight - 100) + 'px'
        });
    }

  },

})
