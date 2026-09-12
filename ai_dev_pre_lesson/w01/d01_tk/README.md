# d01_tk Tkinter 可视化记账程序

这是 `d01` 命令行程序的 Tkinter 图形界面版本。首次运行时会把 `d01/data` 复制到
`d01_tk/data`，以后只修改 `d01_tk` 的数据，不影响原程序。

## 运行

在项目根目录执行：

```bash
python ai_dev_pre_lesson/d01_tk/app/main.py
```

也可以进入 `d01_tk` 后执行：

```bash
python app/main.py
```

默认数据中的管理员账号是 `admin` / `admin`。如使用复制过来的现有数据，也可以使用
你已经在 `d01` 创建的用户登录。

> Tkinter 需要桌面显示环境。在 Dev Container/WSL 中运行时，应配置 WSLg 或 X Server；
> 最简单的方式通常是在带有 Tkinter 的 Windows Python 环境中启动本文件。


如果中文显示为方块，说明运行程序的系统缺少中文字体。Windows 可在“可选功能”中安装
中文字体；Ubuntu/Debian/WSL 可执行：

```bash
sudo apt update && sudo apt install fonts-noto-cjk
```

安装后关闭并重新启动程序。程序会自动选用微软雅黑、苹方、Noto Sans CJK 或文泉驿等
已安装的中文字体。

## 账户管理

登录后进入“基础资料”，点击“账户管理”：

- 选择账户可查看账户类型、所有者、当前余额及该账户的交易记录。
- 输入新余额并选择与余额变化方向一致的分类，然后点击“调整余额并记账”。
- 余额增加会生成收入交易，余额减少会生成支出交易。
- root 可以管理并查看所有用户的账户和交易。

## 主要结构

- `app/gui.py`：窗口、表单、列表和 JSON 数据访问。
- `app/main.py`：程序入口。
- `data/`：首次启动自动生成，作为 d01_tk 的独立数据目录。
