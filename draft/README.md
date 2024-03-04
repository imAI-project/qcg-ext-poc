# QChatGPT 3.x 新扩展方式草案

## 背景

### 历史问题

在过去的实践中，QChatGPT 直接从 `plugins` 目录下加载所有`.py`文件，这些文件中可以自由自定义类和函数，并通过 QChatGPT 提供的 API 注册插件类。但在实践中，我们发现此种加载方式存在以下问题：

#### 设计上的

- 插件类命名和插件包（目录）命名不符，造成混乱。
- 一个插件内实际上可以注册多个插件类，未强制限定。
- 插件需要的依赖由 QChatGPT 动态安装，这对网络环境较差的用户以及使用 Docker 的情况很不友好。
- 通过源代码发布的插件代码，管理松散，不利于分发。

#### 加载逻辑上的

- 遍历插件目录下所有py模块，无统一的入口

### 未来需求

- QChatGPT 可能会以可执行文件的形式发布，这时动态安装依赖将不再可行。
- 插件的发布和管理需要更加规范和统一的方式。

## 设计

### 插件的存储

在新的扩展方案中，插件仍然是存储在`plugins`目录下，`下载的插件`以zip包形式存放，正在开发的插件直接以源码形式存放。

树状图：

```
- main.py
- plugins/
    - __init__.py
    - PluginA/
        - __init__.py
        - plugin_a.py
    - PluginB/
        - __init__.py
        - plugin_b.py
    - PluginC.zip
    - PluginD.zip
```

插件zip包内部结构：

```
# PluginC.zip

- PluginC.zip
    - plugins/
        - PluginC/
            - __init__.py
            - plugin_c.py
    - PyMySQL/
        - __init__.py
        - ...
```

### 导入路径

QChatGPT 将各个插件的zip包添加到 `sys.path`。此时，无论是开发中的插件还是下载的插件，都可以通过`import plugins.PluginC`的方式导入自身的模块。
同时，先添加各个插件包，再添加`plugins`目录，可以保证开发中的插件优先于下载的插件。

### 依赖管理

插件的额外依赖（非QChatGPT的依赖）直接被打包到插件的zip包中，同时，基于上述的导入路径，插件可以直接导入自己的依赖。

### 插件管理 CLI

计划提供一个插件管理的命令行工具，用于打包、测试、上传（在GitHub Actions中自动打包）和下载插件。

### 插件 API

插件的注册、调用等 API 将额外设计。