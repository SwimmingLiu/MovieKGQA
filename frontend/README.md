# 小程序前端代码注意事项

## 使用流程

1. 下载 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

2. 导入frontend项目
3. 修改 pages\chat\chat.js

```js
  const params = {
      // 腾讯云调用语音API的密钥
      secretkey: '',
      secretid:  '',
      appid: 0,
  	  ...
  }
```

4. 打包预览