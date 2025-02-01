# 蔚蓝档案日服iOS汉化补丁
# Blue Archive Chinese Simplified Localization Patch
## **须知**

本项目是“按原样”提供的，不附带任何形式的明示或默示担保，
包括但不限于对适销性、特定用途的适用性以及非侵权的担保。
在任何情况下，无论是因合同、侵权行为或其他行为引起的，
本项目的作者或版权所有者对任何索赔、损害或其他责任均不承担责任，
无论这些是因本项目或本项目的使用或其他交易而产生的。

此项目只包含脚本，没有包含汉化资源及涉及版权/知识产权的资源

## 如何自行获取汉化资源
作者将在脚本内留一个文件服务器链接。但是，不要指望作者维护这个链接

[资源库](https://github.com/asfu222/BACNLocalizationResources)
[资源链接](https://asfu222.github.io/BACNLocalizationResources/)

**如果作者链接失效**：

你可以自己创建一个本地文件服务器链接。

只需把汉化资源拖进`项目地址/assets/BA版本/正确文件相对地址`

~~列如：`./assets/r76_odfuvebzfonktr6yf71a_3/TableBundles/ExcelDB.db`~~

现已改，请用这个格式：`./assets/latest/TableBundles/ExcelDB.db`

然后运行 `file_server.cmd` 或 `file_server.sh`即可

当然，你也可以用其它方式搭建文件服务器。都一样

此方式核心逻辑是 `python -m http.server -d {文件根目录}`

你可以从包含以下所需资源的汉化软件或包获取汉化资源：
 - `TableBundles/ExcelDB.db`
 - `TableBundles/TableCatalog.bytes`

**注意**：

- 游戏会打乱某些文件名。你需要自行判断并把名字改回去
- 如果你有备用安卓设备/模拟器，可以用OurPlay的汉化资源
- （推荐渠道）[99手游加速器](https://www.99jiasu.net/)：汉化后，到`/Android/data/com.YostarJP.BlueArchive/files/` 找寻
- [OurPlay](https://m.ourplay.net/): 自行找寻模拟器环境。快速找寻需使用`root`，不推荐
- 从国服获取（需使用特定软件替换文本且从新打包）较为复杂，且没有全部
- 用特点软件拆开并机翻/手动翻译，并从新打包。

### 如汉化资源没有`TableBundles/TableCatalog.bytes`请注意
因为日服的crc校验机制，无法直接用这个汉化资源。需生成一个crc值，文件大小对应的`TableCatalog.bytes`

首先，电脑上下载一个有效的`TableBundles/TableCatalog.bytes`。可以从其它汉化资源库`TableCatalog.bytes`或安卓获得：`Android/data/com.YostarJP.BlueArchive/files/TableBundles/TableCatalog.bytes`

也可以从官方下载，不过需要BA版本号，列如：[`https://prod-clientpatch.bluearchiveyostar.com/r76_odfuvebzfonktr6yf71a_3/TableBundles/TableCatalog.bytes`](https://prod-clientpatch.bluearchiveyostar.com/r76_odfuvebzfonktr6yf71a_3/TableBundles/TableCatalog.bytes)

接下来我们需要根据汉化资源的`TableBundles/ExcelDB.db`生成相应的`TableCatalog.bytes`

把`ExcelDB.db`拖进含有`patch_table_catalog.py`的文件夹。然后运行用`python`运行`patch_table_catalog.py`

脚本吐出来`TableCatalog.bytes`的就是你所需要的。

## 教程
### 在运行前，需进行以下步骤
 ### - 电脑需要安装[mitmproxy](https://mitmproxy.org/)
 ### - （WireGuard协议）手机上，应用商店下个WireGuard APP
 ### - （其它协议）请自行寻找方法。下面有一些建议
 ### - 手机上，把蔚蓝档案日服删了重下（不知道清除数据行不行，但是保险起见请重下）
 ### - 做完后，回到电脑上继续跟教程

`cd`到这个项目文件夹，然后在Windows上运行`start.cmd`或Linux上运行`start.sh`

会弹出个`mitmproxy`设置网页窗口
- 脚本默认使用`WireGuard`协议代理请求。也可以在`Capture`设置内打开其它协议->使用`HTTP`，`SOCKS5`，或其它的协议代理
- iOS内，`HTTP`在`WiFi设置`可以设置HTTP代理：默认`http://电脑IP:8080`
- 如果你有QuantumultX，Loon，Surge等可以用`SOCKS5`代理：默认`socks5://电脑IP:1080`

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
### 请注意！关于下载速度，什么时候汉化好的问题
下载完所需文件很快。在能看到主界面时就汉化好了（主界面左下角点开看是汉字）
此时可以切断`mitmproxy`的VPN了，后面的7G什么的文件不是汉化资源
如果想用加速器，现在可以用了

## 常见错误
  ### - Client TLS handshake failed. The client may not trust the proxy's certificate for ... -> 没给`mitmproxy` `Root`证书权限
  ### - `mitm.it`啥都没有/没有证书下载界面 -> 请确认你用的是`http`，而非`https`
  ### - 不知道BA版本号怎么办？-> 可以打开游戏用这脚本内`mitmproxy`内`flow list`查找含有官网网址的链接：列如`GET https://prod-clientpatch.bluearchiveyostar.com/r76_odfuvebzfonktr6yf71a_3/TableBundles/ExcelDB.db`。类似请求有很多，把r开头的那个复制就行了。也可以去改脚本，只检查最后文件名，然后文件名一样的就下载某资源。
  ### - 不知道还有什么其它常见问题，这个教程应该很详细了
