# [English](https://github.com/hxz393/ConfigCenterComparer/blob/main/doc/README_EN.md) | [中文](https://github.com/hxz393/ConfigCenterComparer/blob/main/README.md)

# 程序介绍

`ConfigCenterComparer` 是一款配置中心对比工具。它主要用于比较不同配置中心的配置数据，确保环境间配置的一致性和准确性。

主要特点：

- **支持多种配置中心**：兼容主流的 `Apollo` 和 `Nacos` 配置中心。实现跨集群数据获取。
- **数据格式化和比较**：提供图形界面，方便数据格式化和比较。
- **数据库集成**：集成 MySQL 数据库查询模块，支持 SSH 隧道连接。
- **日志记录和错误处理**：配备先进的日志系统和错误处理机制。
- **实用功能**：包含搜索、复制、导出等多种功能，并设有忽略列表。

主窗口截图：

![main screen](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/main_screen.jpg)

## 使用要求

下面使用场景介绍，除非明确说明不支持，否则需要自行测试结果。

### 操作系统

- **开发环境**：`Windows 10 专业工作站版`，版本 `22H2`。
- **兼容性**：支持 `Win 7 x64` 及更高版本操作系统。不支持`Win XP`。支持服务器 `Windows Server 2008` 以上版本。
- **跨平台特性**：由于 QT 跨平台特征，其他操作系统理论上可手动编译成可执行文件。编译指南详见下文。

### 配置中心

Nacos 支持 `yaml` 格式的配置。不支持其他格式。

已测试的配置中心及版本：

- **Apollo**：`2.0.x`、`2.1.x`
- **Nacos**：`v2.1.x `

其他版本未经测试。数据库结构差异可能导致查询失败。欢迎反馈相关问题。

### 数据库

- **测试版本**：MySQL `5.7`。理论上 `8.x` 也可支持。
- **大小写敏感**：数据库配置应关闭大小写敏感。Apollo 数据库查询 SQL 采用驼峰命名，无视大小写敏感配置。Nacos 数据库配置的兼容性待验证，欢迎反馈。



## 获取程序

在 Windows 平台，已打包两种版本。Win7 下可用版本，在文件名中标注了`-Win7(x64)`，请按需下载。其他操作系统用户，可尝试通过源码构建可执行程序，或在 Python IDE 中运行。

### 下载地址

软件下载方式：

- **方式一**：前往 [release](https://github.com/hxz393/ConfigCenterComparer/releases) 页面下载 `ConfigCenterComparer.exe`。
- **方式二**：通过 [百度网盘](https://pan.baidu.com/s/1RK7uBqaqgqJHLJbadXI48g?pwd=6666) 下载 `ConfigCenterComparer.7z` 压缩包，解压后运行。
- **方式三**：直连 [下载](https://www.x2b.net/download/ConfigCenterComparer.7z)

下载的压缩包，需要解压缩后再运行，否则程序配置将无处保存。

### 自行打包

手动编译需要事先安装好 `Python 3.7` 以上版本、`PyQT 5.10` 以上版本和 `pyinstaller 5.6` 软件包。其他第三方依赖库有：`PyMySQL`、`PyYAML`、`paramiko`、`requests`、`sshtunnel`，没有版本规定。

编译步骤如下：

1. 在安装有 `Git` 的主机上克隆项目。命令如下：

   ```sh
   git clone https://github.com/hxz393/ConfigCenterComparer.git
   ```

   或者在 [项目主页](https://github.com/hxz393/ConfigCenterComparer) 点击绿色`<> Code` 按钮选择 `Download ZIP` 选项，[下载](https://github.com/hxz393/ConfigCenterComparer/archive/refs/heads/main.zip) 源码压缩包。下载完毕后用压缩软件或命令工具解压缩。

2. 使用命令切换到项目路径下面。

   例如在 Windows 系统下面，打开 `CMD` 命令提示符，输入：

   ```sh
   cd B:\git\ConfigCenterComparer
   B:
   ```

   在 Linux 系统下面，使用 `cd` 命令切换到项目路径下面：

   ```sh
   cd /root/ConfigCenterComparer
   ```

   如果使用 `PyCharm` 作为 IDE，可以直接在自带的终端栏目输入下面打包命令。

3. 使用 `pyinstaller` 命令编译打包成可执行文件：

   ```sh
   pyinstaller -F -w -i media/main.ico --add-data 'media/;media' ConfigCenterComparer.py
   ```

   如果使用 `Anaconda` 作为虚拟环境，打包时要加上 `-p` 参数，指定虚拟环境所在目录。例如：
   
   ```sh
   pyinstaller -F -w -i media/main.ico --add-data media/;media -p C:\ProgramData\Anaconda3\envs\ccc ConfigCenterComparer.py
   ```
   
   成功编译后，可执行文件会生成到 `dist` 目录下面。



## 开发相关

下面是和开发有关的信息。

### 程序原理

本程序主要运行流程如下：

1. 通过查询 Apollo 数据库的 `app`、`namespace` 和 `item` 表，获取到 `AppId`（或 `Name`）、`NamespaceName`、`Key`、`Value` 和 `DataChange_LastTime` 字段的数据。
   如果是 Nacos 数据库，则查询 `config_info` 表中字段 `data_id`、`group_id`、`content` 和 `gmt_modified` 字段的数据。然后对 `content` 字段的 `yaml` 格式内容，解析分割成多条配置。
2. 对每条配置信息，组合名字、分组和键名作为唯一索引，将各个环境的配置值和配置修改时间合并插入结果字典中。
3. 对比各配置环境的值，得到一致性信息，更新到结果字典中。
4. 通过对比过滤列表，得到是否过滤的信息，更新到结果字典中。
5. 将所有结果插入到主窗口表格中。
6. 应用过滤器对表行或单元进行着色。执行其他显示优化动作。

如果程序运行中发生错误，只要不影响运行的，不会弹窗提示，但会在右下角状态栏标签中提示「发生错误」。可以查看日志是否有程序 Bug 或其他问题。

### 模块说明

项目结构说明如下：

- `ConfigCenterComparer.py`：主程序。
- `config/`：配置文件夹，包含语言字典和全局变量。
- `lib/`：实用功能库，存放通用函数，包括文件处理、数据库查询等。
- `media/`：媒体文件夹，存放图标等。
- `module/`：包含项目相关函数的模块，如查询配置路径、执行查询和格式化结果。
- `ui/`：和 UI 定义操作有关的模块。

### 语言翻译

由于程序文本量较少，因此使用一个语言字典来储存所有显示文字。文件路径是：`config\lang_dict_all.py`，可在此文件中添加其他语言翻译。

### 开源许可

遵循 [GPL-3.0 license](https://github.com/hxz393/ConfigCenterComparer/blob/main/LICENSE)。违反开源社区准则，将追究法律责任。



# 程序使用

在使用 `ConfigCenterComparer` 前，请仔细阅读本章节。

## 设置

首次使用时，需先进入设置页面进行配置。

### 程序设置

在工具栏或「选项」菜单中，选择「程序设置」进入设置界面。如下图所示：

![main settings](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/main_settings.jpg)

配置文件位于 `config\config_main.json`。请勿手动修改以避免错误。若配置文件损坏，可删除重新生成。

各配置项说明如下：

- **选择语言**

  默认为「English」。选择可切换程序显示语言。

- **选择配置中心类型**

  可选「Apollo」或「Nacos」。根据选择读取不同的连接配置文件。

- **选择 Apollo 服务名字段**

  当选择配置中心类型为「Apollo」时生效，设置数据库中哪个字段作为服务名显示字段。下拉框选项「AppId」和「Name」，分别对应 Apollo「应用信息」中的「AppId」和「应用名称」。

- **表格颜色开关**

  如果配置条目数量有上万条，可以关闭表格颜色展示，能大幅提高运行速度。

- **替换服务名**

  - 在输入框中填入「原名」和「新名」，可对服务名进行完全替换。通常用于不同环境内服务名对齐。例如开发环境的 AppId 为「1025」，其他环境的 AppId 名为「api-web」，将 1025 替换为 api-web 后，才好在程序中对 api-web 的配置进行对比。

  - 可以设置多组服务名替换，各服务名之间用空格分开。「原名」和「新名」内的字段数量必须一致，内容一一对应，否则会截断多出的字段。替换操作每个服务名只进行一次。

  - 服务名完全匹配的情况下，才会进行替换。上面的例子中，1025 并不会匹配到 AppId 为「10258」或「api-1025」的服务名。需要替换必须输入全名。

  - 替换服务名在裁剪服务名之后进行，请注意下先后顺序。

- **裁剪服务名**

  - 删除服务名中的前缀或后缀。和替换服务名类似，用于服务名对齐。前缀从服务名开头匹配，后缀从从服务名末尾匹配，匹配到了则从服务名中删除匹配的文字。例如设置后缀裁剪为「.yaml」，则所有形如「api-web.yaml」的服务名，会被替换成「api-web」。
  - 可以设置多组裁剪字段，各裁剪字段之间用空格分开。每个服务名只进行一次前缀和后缀裁剪，匹配到了则不进行后续判断。例如设置前缀裁剪为「pc-」，后缀裁剪为「.yaml -web」，则服务名「pc-api-web.yaml」最多被裁剪为「api-web」。
  - 服务名裁剪和替换操作都严格区别大小写。

### 连接设置

配置好主设置后，还需要配置数据库。从工具栏或 「选项」菜单中，点击「连接配置」按钮或选项进入数据库配置窗口。如图所示：

![connect settings](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/connect_settings.jpg)

Apollo 和 Nacos 的连接配置分别保存在 `config\config_apollo.json` 和 `config\config_nacos.json`。同样，不建议手动修改。

最多支持四套环境配置比对，通过选项卡点击切换。Apollo 和 Nacos 连接需要的配置一样，各配置项说明如下：

- **启用**

  勾选「MySQL 连接配置」中的「启用」选项后，当前环境才加入配置对比。如果需要通过 SSH 隧道连接数据库，勾选「SSH 隧道配置」中的「启用」选项，并填入相关参数。

- **地址**

  输入 MySQL 或 SSH 主机的 IP 地址或域名。例如：「192.168.1.1」或「yourdomain.com」。

- **端口**

  输入 MySQL 或 SSH 连接的端口号。例如：「3306」或「22」。

- **用户名**

  输入有连接权限的用户名。例如：「apollo」或「root」。

- **密码**

  输入连接用户名的密码。

- **库名**

  配置库所在的库名，例如 Apollo 默认使用的库名「ApolloConfigDB」，Nacos 默认使用的库名「nacos」。



## 开始

点击「测试连接」或「开始运行」按钮后，按钮变为灰色状态。运行完毕会显示弹窗或数据，完成时间主要由网络速度决定，请耐心等待。

### 测试

配置好数据库连接后，可以先进行连通性测试。从工具栏或 「开始」菜单中，点击「测试连接」按钮或选项进行测试：

- 如果连接顺畅，大约 10 秒后会弹窗显示 MySQL 和 SSH 连接测试结果。
- 如果有网络或配置问题，导致连接失败，可能需要一段时间才会弹窗显示测试结果。可以在「查看日志」中分析连接失败具体原因。

### 运行

所有配置完毕后，从工具栏或 「开始」菜单中，点击「开始运行」按钮或选项，开始从数据库中获取数据：

- 如果一切顺利，主窗口表单中，将会显示所有从数据库中拉取到的数据。
- 如果有个别环境连接失败，将不会在最终结果中展示对应环境配置。可以在「查看日志」中分析连接失败具体原因。
- 如果要获取更新配置，可重新点击「开始运行」来更新表格。程序不会将结果缓存到本地文件中。

### 查重

从数据库获取到数据后，从工具栏或 「开始」菜单中，点击「配置查重」按钮或选项，可以对运行结果进行进一步查重。这个查重功能，对比的是同一环境下重复配置。例如：

在公共配置中配置过数据库连接池大小，那么在其他应用私有配置中，同样配置数据库连接池大小，且值与公共环境一致，可以认为应用私有配置中存在重复配置。

查重功能可以查找出此类配置。查重结果窗口如下图所示：

![connect settings](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/comparison_results.jpg)

窗口分为两块：

- 主要区域为查重结果表格，通过选项卡对不同环境进行区分。出了主窗口中见过的字段，最左侧还有一列数字行号，由分组号码和组内号码组成。
- 上面有两个输入框，具体作用为：
  - 公共配置输入框，用于标记公共配置所在行。输入公共配置名例如 `global` ，点击「设置」后，global 所在的整行会以红色字体显示。
  - 搜索输入框，从配置键或值中搜索内容。没有匹配的行将会被隐藏。搜索字段不区分大小写。



## 结果展示

主界面从上到下分别为菜单栏、工具栏、过滤栏、主表格和状态栏，下面主要说明主表格。

### 表头

表头分为以下项目：

- **服务**：服务名，Apollo 中为「AppId」或 「应用名称」。Nacos 中只有一个字段，为「Data Id」。
- **分组**：Apollo 中的「Namespace」，一般私有命名空间叫「application」。Nacos 中的字段为 「Group」。
- **配置键**：Apollo 中的 「Key」。Nacos 中为从「配置内容」提取的字段，格式和 Apollo 中的一样。
- **值**：默认按不同环境分为四列，表头为环境名称。Apollo 中的 「Value」。Nacos 中为从「配置内容」提取的字段。
- **修改时间**：默认隐藏。按不同环境分为四列，为对应环境配置最后修改时间。
- **一致性**：分为四种状态。
  - 完全一致：表示所有环境配置值完全相等。要求对比环境至少有两个。
  - 部分一致：生产环境和预览环境的值相等，但与其他环境的值不等。
  - 未知状态：仅单个环境配置有值。其他环境可能没有配置，也可能值获取失败。
  - 不一致：所有不符合以上状态的情况，都归为不一致。
- **忽略**：值为「是」或者「否」。为用户手动设置。

表头支持拖动排列，点击表头能排序。表头右键菜单可以选择隐藏或显示某列数据。

### 颜色

获取到配置数据后，主窗口表单会以不同颜色显示每条配置状态。其含义代表如下：

- 灰色：在忽略列表中，忽略值为「是」。
- 绿色：一致性值为「完全一致」。
- 蓝色：一致性值为「部分一致」。
- 红色：没有配置或没有获取到配置值的单元。
- 白色：默认状态。



## 过滤操作

过滤栏分为三部分：过滤服务、快速过滤和全局搜索。三种方法可组合使用，以便快速查找和对比配置。

### 过滤服务

在下拉框中选择服务名，表格中则只显示选中的服务配置。默认为显示所有配置。

### 快速过滤

针对「一致性」和「忽略」列的值进行过滤。在下拉框中选择过滤条件，选中的条件如果匹配某行的值，匹配行会从表格中隐藏。

如果勾选「反选」框，则表格中只会展示匹配的行。

### 全局搜索

在输入框中输入搜索内容，点击搜索按钮，对所有表格数据进行字符串搜索。匹配值的单元以高亮显示，没有匹配值的行会隐藏。

### 重置条件

点击搜索按钮旁边的重置按钮，会将所有过滤条件重置，清除搜索输入框内容，显示完整的表格内容。



## 编辑操作

程序不会对原始配置做任何修改，忽略列表存放在本地 `config\config_skip.txt` 文件中。

### 复制内容

用鼠标点击或拖动单元格，在右键弹出菜单或工具栏中选择「复制内容」，选中的数据会复制保存到系统剪切板中。

### 导出列表

将当前表格显示的数据，导出到文件中。从「编辑」菜单栏或表格右键菜单中，选择「导出列表」，在文件保存窗口选择导出格式。支持 `JSON` 或 `CSV` 格式，点击保存后即可导出。

### 忽略操作

用户可自定义要忽略的配置行。用鼠标点击或拖动单元格，在右键弹出菜单或工具栏中选择「加入忽略」，配置行会被标记为已忽略。之后可应用快速过滤来隐藏已忽略的配置行。

解除忽略操作同理，选择「取消忽略」，配置行将从过滤列表中移除。



## 帮助操作

包括查看日志、检查程序新版本和查看程序信息功能。

### 查看日志

从「帮助」菜单或快速工具栏选择「查看日志」，打开日志查看窗口：

![view logs](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/view_logs.jpg)

左上角下拉框可以选择要显示的日志等级。例如选择「WARNING」，则只会显示 WARNING 等级以上的日志，INFO 等级的日志信息会被过滤掉。

左下角「提交反馈」按钮，点击会跳转到 GitHub 项目 Issues 页面，方便提交错误信息。

左下角「清空」按钮，点击会清空日志文件内容。日志文件存放在 `logs` 目录内，超过 1MB 大小会回滚，最多保留十个文件。

右下角「刷新」按钮，点击可以切换日志持续显示模式，方便监控日志。

### 检查更新

从「帮助」菜单选择「检查更新」，将会在线检查程序是否有更新版本。以弹窗告知检查结果。

### 关于软件

从「帮助」菜单选择「关于软件」，弹出程序说明和构建信息。

### 调试程序

开发调试代码使用，对用户没有实际作用。



# 常见问题

软件运行遇见错误时，先查看日志，如果是连接问题，请检查配置后再重试。然后参考下面常见问题解决方案。最后查看所有 [Issue](https://github.com/hxz393/ConfigCenterComparer/issues) 中是否有同样问题。如需进一步帮助，可以提交新 [Issue](https://github.com/hxz393/ConfigCenterComparer/issues) ，并附上相关日志。



# 更新日志

为避免更新日志过长，只保留最近更新日志。

## 版本 1.1.0（2023.11.28）

新增内容：

1. 新增配置查重功能；
2. 日志查看窗口新增刷新按钮。

优化内容：

1. 修改语言管理类，切换语言立即生效，不再需要重启；
2. 修改配置管理类，减少对配置文件读取次数；
3. 修改日志查看窗口显示模式，可独立主窗口运行；
4. 修改代码以向下支持到 Python 3.7，并提供 Win 7 下可用版本。

## 版本 1.0.2（2023.11.21）

新增内容：

1. 新增表格颜色开关，应对数据量过大导致性能下降。

修复内容：

1. 修改颜色应用逻辑，提升运行速度；
2. 优化主线程代码，提高 UI 稳定性。



## 版本 1.0.1（2023.11.19）

修复内容：

1. 开始运行前，清空过滤栏条件，避免再次运行时界面卡死；
2. 优化日志显示文字。



## 版本 1.0.0（2023.11.19）

发布初版。
