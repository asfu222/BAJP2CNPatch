# 蔚蓝档案日服iOS/汉化补丁
## **须知**

本项目是“按原样”提供的，不附带任何形式的明示或默示担保，
包括但不限于对适销性、特定用途的适用性以及非侵权的担保。
在任何情况下，无论是因合同、侵权行为或其他行为引起的，
本项目的作者或版权所有者对任何索赔、损害或其他责任均不承担责任，
无论这些是因本项目或本项目的使用或其他交易而产生的。

此项目只包含脚本，没有包含汉化资源及涉及版权/知识产权的资源

## 如何自行获取汉化资源
作者将在脚本内留一个文件服务器链接。但是，不要指望作者维护这个链接

**如果作者链接失效**：

你可以自己创建一个本地文件服务器链接。

只需把汉化资源拖进`项目地址/assets/BA版本/正确文件相对地址`

列如：`./assets/r76_odfuvebzfonktr6yf71a_3/TableBundles/ExcelDB.db`

然后运行 `file_server.cmd` 或 `file_server.sh`即可

当然，你也可以用其它方式搭建文件服务器。都一样

此方式核心逻辑是 `python -m http.server -d {文件根目录}`

你可以从包含以下所需资源的汉化软件或包获取汉化资源：
 - `TableBundles/ExcelDB.db`
 - `TableBundles/TableCatalog.bytes`

**注意**：

- 游戏会打乱某些文件名。你需要自行判断并把名字改回去
- 如果你有备用安卓设备/模拟器，可以用OurPlay的汉化资源
- （推荐渠道）[99手游加速器](https://www.99jiasu.net/)：汉化后，到`/Android/data/com.YostarJP.BlueArchive/` 找寻
- [OurPlay](https://m.ourplay.net/): 汉化后，到`/Android/data/com.excean.gspace/gameplugins/com.YostarJP.BlueArchive/` 找寻
## 教程
### 在运行前，需进行以下步骤
 ### - 电脑需要安装[mitmproxy](https://mitmproxy.org/)
 ### - 手机上，把蔚蓝档案日服删了重下（不知道清除数据行不行，但是保险起见请重下）
 ### - 做完后，回到电脑上继续跟教程

`cd`到这个项目文件夹，然后在Windows上运行`start.cmd`或Linux上运行`start.sh`

会弹出个`mitmproxy`设置网页窗口
- 脚本默认使用`WireGuard`协议代理请求。也可以在`Capture`设置内打开其它协议->使用`HTTP`，`SOCKS5`，或其它的协议代理
- iOS内，`HTTP`在`WiFi设置`可以设置HTTP代理：默认`http://电脑IP:8080`
- 如果你有QuantumultX，Loon，Surge等可以用`SOCKS5`代理：默认`http://电脑IP:1080`

### WireGuard协议
请在`Capture`找到`WireGuard`的二维码，在手机`WireGuard`APP上扫描并添加VPN

### 注意
由于本方法依赖VPN，国内加速器在汉化过程无法使用。汉化后可用
### 下载安装mitmproxy证书
链接到VPN后，请打开`http://mitm.it`并下载iOS的证书。然后打开设置并安装证书。
### 请注意
这个证书还需要`Root`权限。但是，在iOS上，`Root`证书很容易安装。

只需到`通用/关于/下滑至管理信任证书设置`点开并给`mitmproxy` `Root`证书权限即可。

### 确保你还是链接到了`mitmproxy`的VPN，然后打开蔚蓝档案日服
下载完所有文件后，就能看见汉化了

## 常见错误
  ### - Client TLS handshake failed. The client may not trust the proxy's certificate for ... -> 没给`mitmproxy` `Root`证书权限
  ### - `mitm.it`啥都没有/没有证书下载界面 -> 请确认你用的是`http`，而非`https`
  ### - 不知道还有什么其它常见问题，这个教程应该很详细了