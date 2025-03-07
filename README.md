以下是该单词本程序的简介和使用说明文档：

# 智能单词本 v2.0 使用手册

## 程序简介
**智能单词本**是一款专为语言学习者设计的桌面应用程序，主要功能包括：
- 📖 本地词库管理（增删查改）
- 🌐 联网词典查询
- 🔁 智能复习模式
- 🔄 自动按字母顺序排列单词
- 📥 数据持久化存储（JSON格式）
- 🎯 双语互译测试

**核心优势**：
1. 本地+云端双词库支持
2. 自动维护单词排序
3. 智能随机出题算法
4. 简洁直观的用户界面
5. 跨平台运行能力

## 系统要求
- Python 3.6+
- 需要网络连接（仅限联网查询功能）
- 推荐屏幕分辨率：1280x720以上

## 使用说明

### 主界面布局
```
[单词输入框] [释义输入框]
[添加] [删除] [本地查询] [联网查询]
[显示全部] [开始复习] [帮助文档]
```

### 基础操作指南

#### 1️⃣ 添加单词
1. 在"单词"栏输入英文单词（不区分大小写）
2. 在"释义"栏输入中文解释
3. 点击"添加单词"按钮
✅ 成功提示：状态栏显示"成功添加: 单词"
⚠️ 错误提示：空输入/重复单词时弹出警告

#### 2️⃣ 删除单词
1. 在"单词"栏输入要删除的单词
2. 点击"删除单词"按钮
✅ 成功提示：状态栏显示"已删除: 单词"
⚠️ 提示：删除不存在的单词时会提示"单词不存在"

#### 3️⃣ 查询功能
- **本地查询**：
  1. 输入单词后点击"本地查询"
  2. 弹出窗口显示本地存储的释义

- **联网查询**：
  1. 输入单词后点击"联网查询"
  2. 显示进度条等待网络响应
  3. 弹出窗口显示完整词典释义

#### 4️⃣ 显示全部单词
点击"显示全部"按钮：
- 弹出可滚动窗口
- 按字母顺序显示所有单词及释义
- 格式：`• abandon         抛弃，放弃`

### 高级功能

#### 🔁 智能复习模式
1. 点击"开始复习"
2. 随机出现两种题型：
   - 英译中："请输入'apple'的释义"
   - 中译英："请输入对应'苹果'的单词"
3. 输入答案后立即显示正误
4. 按任意顺序完成所有单词测试

⏸ 中途退出：点击"取消"按钮终止复习

#### ⚙️ 数据管理
- 自动保存：每次修改后自动保存到`wordbook.json`
- 手动备份：可复制/重命名`wordbook.json`文件
- 数据恢复：用有效JSON文件替换当前文件

### 快捷键参考
| 操作       | Windows/Linux | macOS     |
|------------|---------------|-----------|
| 确认输入   | Enter         | Return    |
| 关闭弹窗   | Esc           | Command+. |
| 快速清空   | Ctrl+Backspace| ⌘+Delete  |

## 注意事项
1. 联网查询依赖第三方API，响应速度可能受网络影响
2. 单词存储自动转为小写，但查询时大小写不敏感
3. 建议定期备份`wordbook.json`文件
4. 复习模式中取消后需要重新开始才能继续

## 技术支持
点击"帮助文档"按钮访问在线文档，包含：
- [最新版本下载](https://github.com/Janson20/----/releases)
- 常见问题解答
- 错误代码查询
- [用户论坛入口](http://janson20-forum.great-site.net/viewforum.php?f=15)

---

该说明文档可通过程序内的"帮助文档"按钮直接访问在线版本，建议用户在使用前阅读完整文档以获得最佳体验。