# 英语跟读本 · 打包成 APK 的完整步骤

这个文件夹就是一个完整的安卓工程。你不需要在电脑上装任何开发工具，
把它传到 GitHub 上，GitHub 会免费帮你编译出 APK。

---

## 第 0 步：先看看做出来是什么样（1 分钟，可选但强烈建议）

双击打开 **`预览版-用浏览器打开.html`**。

这就是 App 的全部内容和交互，和装到手机上完全一样（只有朗读的声音来源不同）。
先玩一遍，觉得哪里要改，直接告诉我，改完再打包，省得来回折腾。

> 手机上想现在就用：把这个 html 传到手机，用 Chrome 打开，
> 菜单里选「添加到主屏幕」，就有图标了，也能离线用。

---

## 第 1 步：注册 GitHub（3 分钟）

打开 https://github.com ，点右上角 **Sign up**，用邮箱注册一个账号。全程免费。

---

## 第 2 步：新建一个仓库（1 分钟）

1. 登录后点右上角 **➕ → New repository**
2. **Repository name** 随便填，比如 `english-reader`
3. 选 **Private**（私有，只有你自己能看）或 Public 都行
4. **不要**勾选 "Add a README file"
5. 点 **Create repository**

---

## 第 3 步：上传文件（5 分钟）

在新建好的仓库页面，点 **uploading an existing file**（或 Add file → Upload files）。

把这个文件夹里的东西**全部**拖进去：

```
.github/          ← 最关键，别漏了
app/
build/
build.gradle
gradle.properties
settings.gradle
.gitignore
```

拖完后在下面的输入框写一句话（比如 `first`），点 **Commit changes**。

### ⚠️ 最容易出错的地方

`.github` 这个文件夹是以点开头的，有些系统会把它当成隐藏文件夹，拖不上去。

**上传完请检查**：仓库页面顶部有没有 **Actions** 这个标签，点进去有没有一个叫
「构建 APK」的任务在跑。如果没有，说明 `.github` 没传上去，按下面补救：

1. 仓库页面 → **Add file → Create new file**
2. 文件名那一栏，一个字一个字地输入：`.github/workflows/build-apk.yml`
   （输入斜杠时 GitHub 会自动帮你建文件夹，这是正常的）
3. 用记事本打开本地的 `.github/workflows/build-apk.yml`，全选复制，粘进去
4. 点 **Commit new file**

---

## 第 4 步：等它编译（3～6 分钟）

点仓库顶部的 **Actions** 标签，你会看到一个正在转的黄色圆点。
点进去可以看到实时日志。变成绿色的 ✓ 就成功了。

---

## 第 5 步：下载 APK

编译成功后有两个地方能拿到 APK，**推荐第一种**：

**方式一（手机上直接下载）**
用手机浏览器打开：`https://github.com/你的用户名/仓库名/releases/latest`
页面下方 Assets 里点 **EnglishReader.apk** 就开始下载了。

**方式二（电脑上下载）**
Actions → 点那次成功的运行 → 页面最下面 **Artifacts** → 点 `EnglishReader-APK`
下载下来是个 zip，解压出来就是 APK，再传到手机。

---

## 第 6 步：在小米 15 上安装

1. 点开下载好的 APK
2. 系统会提示「为了您的安全，禁止安装未知来源应用」→ 点 **设置**
3. 打开 **允许来自此来源的应用**
4. 返回，点 **安装**
5. 小米可能还会弹一个「应用未经安全检测」的确认框，点 **继续安装**

装好后桌面会出现一个红棕色的 **æ** 图标，叫「英语跟读本」。

---

## 关于朗读声音

App 用的是**手机系统自带的语音引擎**，不联网。如果点「听」没声音：

**设置 → 更多设置 → 语言和输入法 → 文字转语音（TTS）输出**

看看有没有装英文语音包。小米自带的引擎可能不支持英语，
可以在应用商店装一个 **Google 文字转语音**，装完在上面这个页面选它作为首选引擎。

> 就算完全没有声音也不影响使用 —— 谐音行和音标本来就是为了让你**自己念**出来的。

---

## 以后想改内容

所有内容都在 `build/` 文件夹里，是纯文本：

| 文件 | 内容 |
|---|---|
| `build/content_articles.py` | 10 篇文章的英文原文和中文翻译 |
| `build/content_phonemes.py` | 46 个音标的口型讲解、例词、易混对比 |
| `build/content_phonics.py` | 7 关拼读规则、小测题、单词题库 |
| `build/engine.py` | 谐音和音标的生成规则（改这里能调整谐音风格） |

改完之后需要重新生成 `app/src/main/assets/data.js`。
你自己跑需要 Python 环境（`pip install cmudict`，然后 `python gen.py`）——
或者直接把改好的文件发我，我帮你重新生成。

生成好新的 data.js 后，传回 GitHub 覆盖旧文件，Actions 会自动重新打一个新 APK。

---

## 出问题了怎么办

Actions 里如果出现红色的 ✗，点进去把**红色那一步的日志**截图或复制给我，我来改。
最常见的是 Gradle 或 SDK 版本对不上，改一行配置就好。
