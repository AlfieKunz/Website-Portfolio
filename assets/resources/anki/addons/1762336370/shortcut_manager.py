from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, saveGeom, restoreGeom
from anki.utils import json
import os
import copy
from . import custom_shortcuts
from . import cs_functions as functions

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "default_config.json")
# 用户自定义配置文件路径，默认为None，表示使用插件默认路径
USER_CONFIG_PATH = None

# 定义不由插件处理而是保留Anki原始功能的快捷键列表
DISABLED_SHORTCUTS = [
    "editor insert latex", 
    "editor insert latex equation", 
    "editor insert latex math environment", 
    "editor insert mathjax inline", 
    "editor insert mathjax block", 
    "editor insert mathjax chemistry"
]

# 翻译字典
TRANSLATIONS = {
    "zh_CN": {
        "window_title": "快捷键设置",
        "search": "搜索:",
        "main_tab": "主界面",
        "editor_tab": "编辑器",
        "reviewer_tab": "复习界面",
        "browser_tab": "浏览器",
        "toolbar_tab": "工具栏",
        "function_col": "功能",
        "shortcut_col": "快捷键",
        "disable_all": "禁用所有快捷键",
        "disable_current_tab": "禁用当前页所有快捷键",
        "restore_default": "恢复默认设置",
        "restore_current_tab": "恢复当前页所有快捷键",
        "reset_shortcut": "恢复默认",
        "apply": "应用",
        "cancel": "取消",
        "ok": "确定",
        "nop_hint": "<nop> 表示禁用",
        "default_file_missing": "找不到默认配置文件",
        "changes_saved": "快捷键设置已保存，请重启Anki以应用更改",
        "disabled_shortcut": "此快捷键由Anki原生功能直接处理，不受本插件影响",
        "config_path": "配置文件路径:",
        "browse_btn": "浏览",
        "reset_path_btn": "重置路径",
        "path_selected": "已选择配置文件路径：",
        "save_config_success": "配置已保存到指定路径",
        "save_config_error": "保存配置文件失败",
        "config_path_note": "设置自定义配置路径可以在不同设备间同步快捷键设置",
        "readable_names": {
            # 主界面
            "main debug": "调试",
            "main deckbrowser": "牌组浏览器",
            "main study": "学习",
            "main add": "添加",
            "main browse": "浏览",
            "main stats": "统计",
            "main sync": "同步",
            
            # 编辑器
            "editor card layout": "卡片布局",
            "editor bold": "粗体",
            "editor italic": "斜体",
            "editor underline": "下划线",
            "editor superscript": "上标",
            "editor subscript": "下标",
            "editor remove format": "移除格式",
            "editor foreground": "文字颜色",
            "editor change col": "背景颜色",
            "editor change deck": "更改牌组",
            "editor cloze": "填空题",
            "editor cloze alt": "填空题（不增加编号）",
            "editor cloze forced increment": "填空题（强制增加编号）",
            "editor cloze no increment": "填空题（不增加编号）",
            "editor add media": "添加媒体",
            "editor record sound": "录制声音",
            "editor insert latex": "插入LaTeX",
            "editor insert latex equation": "插入LaTeX方程",
            "editor insert latex math environment": "插入LaTeX数学环境",
            "editor insert mathjax inline": "插入MathJax行内公式",
            "editor insert mathjax block": "插入MathJax块级公式",
            "editor insert mathjax chemistry": "插入MathJax化学公式",
            "editor html edit": "HTML编辑",
            "editor focus tags": "焦点到标签",
            "editor confirm add card": "确认添加卡片",
            "editor add card close window": "添加卡片并关闭窗口",
            "editor change note type": "更改笔记类型",
            "editor toggle sticky current": "切换当前字段固定",
            "editor toggle sticky all": "切换全部字段固定",
            "editor block indent": "增加缩进",
            "editor block outdent": "减少缩进",
            "editor list insert ordered": "插入有序列表",
            "editor list insert unordered": "插入无序列表",
            
            # 复习界面
            "reviewer edit current": "编辑当前卡片",
            "reviewer flip card 1": "翻转卡片 1",
            "reviewer flip card 2": "翻转卡片 2",
            "reviewer flip card 3": "翻转卡片 3",
            "reviewer replay audio 1": "重播音频 1",
            "reviewer replay audio 2": "重播音频 2",
            "reviewer set flag 1": "设置红色标记",
            "reviewer set flag 2": "设置橙色标记",
            "reviewer set flag 3": "设置绿色标记",
            "reviewer set flag 4": "设置蓝色标记",
            "reviewer set flag 5": "设置粉色标记",
            "reviewer set flag 6": "设置青色标记",
            "reviewer set flag 7": "设置紫色标记",
            "reviewer set flag 0": "清除标记",
            "reviewer mark card": "标记卡片",
            "reviewer bury note": "搁置笔记",
            "reviewer bury card": "搁置卡片",
            "reviewer suspend note": "暂停笔记",
            "reviewer suspend card": "暂停卡片",
            "reviewer delete note": "删除笔记",
            "reviewer play recorded voice": "播放录音",
            "reviewer record voice": "录制声音",
            "reviewer set due date": "设置到期日期",
            "reviewer options menu": "选项菜单",
            "reviewer choice 1": "选择 1（重来）",
            "reviewer choice 2": "选择 2（困难）",
            "reviewer choice 3": "选择 3（良好）",
            "reviewer choice 4": "选择 4（简单）",
            "reviewer pause audio": "暂停音频",
            "reviewer seek backward": "快退",
            "reviewer seek forward": "快进",
            "reviewer card info": "卡片信息",
            "reviewer previous card info": "上一张卡片信息",
            "reviewer more options": "更多选项",
            
            # 浏览器
            "window_browser preview": "预览",
            "window_browser reschedule": "重新安排",
            "window_browser select all": "全选",
            "window_browser undo": "撤销",
            "window_browser invert selection": "反选",
            "window_browser find": "查找",
            "window_browser goto note": "转到笔记",
            "window_browser goto next note": "下一个笔记",
            "window_browser goto previous note": "上一个笔记",
            "window_browser guide": "帮助",
            "window_browser change note type": "更改笔记类型",
            "window_browser find and replace": "查找和替换",
            "window_browser filter": "筛选",
            "window_browser goto card list": "转到卡片列表",
            "window_browser reposition": "重新排序",
            "window_browser first card": "第一张卡片",
            "window_browser last card": "最后一张卡片",
            "window_browser close": "关闭",
            "window_browser info": "信息",
            "window_browser add tag": "添加标签",
            "window_browser remove tag": "移除标签",
            "window_browser suspend": "暂停",
            "window_browser delete": "删除",
            "window_browser add note": "添加笔记",
            "window_browser change deck": "更改牌组",
            "window_browser flag_red": "红色标记",
            "window_browser flag_orange": "橙色标记",
            "window_browser flag_green": "绿色标记",
            "window_browser flag_blue": "蓝色标记",
            "window_browser goto sidebar": "转到侧边栏",
            "window_browser toggle mark": "切换标记",
            "window_browser clear unused tags": "清除未使用标签",
            "window_browser find duplicates": "查找重复项",
            "window_browser select notes": "选择笔记",
            "window_browser manage note types": "管理笔记类型",
            "window_browser save current filter": "保存当前筛选",
            "window_browser remove current filter": "移除当前筛选",
            "window_browser sidebar search": "侧边栏搜索",
            "window_browser sidebar select": "侧边栏选择",
            "window_browser forget card": "忘记卡片",
            
            # 工具栏
            "m_toolbox quit": "退出",
            "m_toolbox preferences": "首选项",
            "m_toolbox undo": "撤销",
            "m_toolbox see documentation": "查看文档",
            "m_toolbox switch profile": "切换配置文件",
            "m_toolbox export": "导出",
            "m_toolbox import": "导入",
            "m_toolbox study": "学习",
            "m_toolbox create filtered deck": "创建筛选牌组",
            "m_toolbox addons": "附加组件"
        },
        "language": "语言/Language:",
        "zh_CN": "中文",
        "en_US": "英文"
    },
    "en_US": {
        "window_title": "Keyboard Shortcuts",
        "search": "Search:",
        "main_tab": "Main",
        "editor_tab": "Editor",
        "reviewer_tab": "Reviewer",
        "browser_tab": "Browser",
        "toolbar_tab": "Toolbar",
        "function_col": "Function",
        "shortcut_col": "Shortcut",
        "disable_all": "Disable All Shortcuts",
        "disable_current_tab": "Disable Current Tab Shortcuts",
        "restore_default": "Restore Defaults",
        "restore_current_tab": "Restore Current Tab Shortcuts",
        "reset_shortcut": "Reset",
        "apply": "Apply",
        "cancel": "Cancel",
        "ok": "OK",
        "nop_hint": "<nop> means disabled",
        "default_file_missing": "Default configuration file not found",
        "changes_saved": "Shortcut settings saved. Please restart Anki to apply changes",
        "disabled_shortcut": "This shortcut is handled by Anki's native functionality and not affected by this add-on",
        "config_path": "Config File Path:",
        "browse_btn": "Browse",
        "reset_path_btn": "Reset Path",
        "path_selected": "Config path selected: ",
        "save_config_success": "Configuration saved to the specified path",
        "save_config_error": "Failed to save configuration file",
        "config_path_note": "Setting custom config path allows syncing shortcuts between devices",
        "readable_names": {
            # Main interface
            "main debug": "Debug",
            "main deckbrowser": "Deck Browser",
            "main study": "Study",
            "main add": "Add",
            "main browse": "Browse",
            "main stats": "Statistics",
            "main sync": "Sync",
            
            # Editor
            "editor card layout": "Card Layout",
            "editor bold": "Bold",
            "editor italic": "Italic",
            "editor underline": "Underline",
            "editor superscript": "Superscript",
            "editor subscript": "Subscript",
            "editor remove format": "Remove Format",
            "editor foreground": "Text Color",
            "editor change col": "Background Color",
            "editor change deck": "Change Deck",
            "editor cloze": "Cloze",
            "editor cloze alt": "Cloze Alt",
            "editor cloze forced increment": "Cloze Forced Increment",
            "editor cloze no increment": "Cloze No Increment",
            "editor add media": "Add Media",
            "editor record sound": "Record Sound",
            "editor insert latex": "Insert LaTeX",
            "editor insert latex equation": "Insert LaTeX Equation",
            "editor insert latex math environment": "Insert LaTeX Math Environment",
            "editor insert mathjax inline": "Insert MathJax Inline",
            "editor insert mathjax block": "Insert MathJax Block",
            "editor insert mathjax chemistry": "Insert MathJax Chemistry",
            "editor html edit": "HTML Edit",
            "editor focus tags": "Focus Tags",
            "editor confirm add card": "Confirm Add Card",
            "editor add card close window": "Add Card Close Window",
            "editor change note type": "Change Note Type",
            "editor toggle sticky current": "Toggle Sticky Current",
            "editor toggle sticky all": "Toggle Sticky All",
            "editor block indent": "Block Indent",
            "editor block outdent": "Block Outdent",
            "editor list insert ordered": "Insert Ordered List",
            "editor list insert unordered": "Insert Unordered List",
            
            # Reviewer
            "reviewer edit current": "Edit Current",
            "reviewer flip card 1": "Flip Card 1",
            "reviewer flip card 2": "Flip Card 2",
            "reviewer flip card 3": "Flip Card 3",
            "reviewer replay audio 1": "Replay Audio 1",
            "reviewer replay audio 2": "Replay Audio 2",
            "reviewer set flag 1": "Set Red Flag",
            "reviewer set flag 2": "Set Orange Flag",
            "reviewer set flag 3": "Set Green Flag",
            "reviewer set flag 4": "Set Blue Flag",
            "reviewer set flag 5": "Set Pink Flag",
            "reviewer set flag 6": "Set Turquoise Flag",
            "reviewer set flag 7": "Set Purple Flag",
            "reviewer set flag 0": "Clear Flag",
            "reviewer mark card": "Mark Card",
            "reviewer bury note": "Bury Note",
            "reviewer bury card": "Bury Card",
            "reviewer suspend note": "Suspend Note",
            "reviewer suspend card": "Suspend Card",
            "reviewer delete note": "Delete Note",
            "reviewer play recorded voice": "Play Recorded Voice",
            "reviewer record voice": "Record Voice",
            "reviewer set due date": "Set Due Date",
            "reviewer options menu": "Options Menu",
            "reviewer choice 1": "Choice 1 (Again)",
            "reviewer choice 2": "Choice 2 (Hard)",
            "reviewer choice 3": "Choice 3 (Good)",
            "reviewer choice 4": "Choice 4 (Easy)",
            "reviewer pause audio": "Pause Audio",
            "reviewer seek backward": "Seek Backward",
            "reviewer seek forward": "Seek Forward",
            "reviewer card info": "Card Info",
            "reviewer previous card info": "Previous Card Info",
            "reviewer more options": "More Options",
            
            # Browser
            "window_browser preview": "Preview",
            "window_browser reschedule": "Reschedule",
            "window_browser select all": "Select All",
            "window_browser undo": "Undo",
            "window_browser invert selection": "Invert Selection",
            "window_browser find": "Find",
            "window_browser goto note": "Go to Note",
            "window_browser goto next note": "Go to Next Note",
            "window_browser goto previous note": "Go to Previous Note",
            "window_browser guide": "Guide",
            "window_browser change note type": "Change Note Type",
            "window_browser find and replace": "Find and Replace",
            "window_browser filter": "Filter",
            "window_browser goto card list": "Go to Card List",
            "window_browser reposition": "Reposition",
            "window_browser first card": "First Card",
            "window_browser last card": "Last Card",
            "window_browser close": "Close",
            "window_browser info": "Info",
            "window_browser add tag": "Add Tag",
            "window_browser remove tag": "Remove Tag",
            "window_browser suspend": "Suspend",
            "window_browser delete": "Delete",
            "window_browser add note": "Add Note",
            "window_browser change deck": "Change Deck",
            "window_browser flag_red": "Red Flag",
            "window_browser flag_orange": "Orange Flag",
            "window_browser flag_green": "Green Flag",
            "window_browser flag_blue": "Blue Flag",
            "window_browser goto sidebar": "Go to Sidebar",
            "window_browser toggle mark": "Toggle Mark",
            "window_browser clear unused tags": "Clear Unused Tags",
            "window_browser find duplicates": "Find Duplicates",
            "window_browser select notes": "Select Notes",
            "window_browser manage note types": "Manage Note Types",
            "window_browser save current filter": "Save Current Filter",
            "window_browser remove current filter": "Remove Current Filter",
            "window_browser sidebar search": "Sidebar Search",
            "window_browser sidebar select": "Sidebar Select",
            "window_browser forget card": "Forget Card",
            
            # Toolbar
            "m_toolbox quit": "Quit",
            "m_toolbox preferences": "Preferences",
            "m_toolbox undo": "Undo",
            "m_toolbox see documentation": "See Documentation",
            "m_toolbox switch profile": "Switch Profile",
            "m_toolbox export": "Export",
            "m_toolbox import": "Import",
            "m_toolbox study": "Study",
            "m_toolbox create filtered deck": "Create Filtered Deck",
            "m_toolbox addons": "Add-ons"
        },
        "language": "Language/语言:",
        "zh_CN": "Chinese",
        "en_US": "English"
    }
}

class ShortcutManagerDialog(QDialog):
    def __init__(self, parent=None):
        super(ShortcutManagerDialog, self).__init__(parent)
        self.parent = parent
        
        # 初始化配置
        self.config = mw.addonManager.getConfig(__name__)
        
        # 设置默认语言
        self.current_lang = self.config.get("interface_language", "zh_CN")
        if self.current_lang not in TRANSLATIONS:
            self.current_lang = "zh_CN"  # 默认为中文
            
        # 设置对话框基本属性
        self.setWindowTitle(self.tr("window_title"))
        self.setMinimumSize(800, 600)
        
        # 从配置文件中恢复窗口大小
        restoreGeom(self, "shortcutManager")
        
        # 设置界面
        self.setup_ui()
        
        # 加载快捷键设置数据
        self.load_shortcuts()
        
        # 设置语言选择框的当前值
        index = self.language_combo.findData(self.current_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        
        # 根据当前语言更新界面文本
        self.update_ui_language()
            
        # 尝试连接主题变化的信号
        try:
            from aqt.theme import theme_manager
            theme_manager.night_mode_changed.connect(self.on_theme_changed)
        except (ImportError, AttributeError):
            pass
            
    def tr(self, key):
        """翻译辅助函数"""
        return TRANSLATIONS[self.current_lang].get(key, key)
        
    def update_ui_language(self):
        """根据当前语言更新UI文本"""
        self.setWindowTitle(self.tr("window_title"))
        
        # 更新顶部区域文本
        self.search_label.setText(self.tr("search"))
        self.language_label.setText(self.tr("language"))
        self.language_combo.setItemText(0, self.tr("zh_CN"))
        self.language_combo.setItemText(1, self.tr("en_US"))
        
        # 更新标签页名称
        self.tabs.setTabText(0, self.tr("main_tab"))
        self.tabs.setTabText(1, self.tr("editor_tab"))
        self.tabs.setTabText(2, self.tr("reviewer_tab"))
        self.tabs.setTabText(3, self.tr("browser_tab"))
        self.tabs.setTabText(4, self.tr("toolbar_tab"))
        
        # 更新表格列头
        self.refresh_table_names()
        
        # 更新配置文件路径区域文本
        self.path_label.setText(self.tr("config_path"))
        self.browse_btn.setText(self.tr("browse_btn"))
        self.reset_path_btn.setText(self.tr("reset_path_btn"))
        self.path_note_label.setText(self.tr("config_path_note"))
        
        # 更新按钮文本
        self.disable_all_btn.setText(self.tr("disable_all"))
        self.disable_current_tab_btn.setText(self.tr("disable_current_tab"))
        self.restore_default_btn.setText(self.tr("restore_default"))
        self.restore_current_tab_btn.setText(self.tr("restore_current_tab"))
        self.apply_btn.setText(self.tr("apply"))
        self.cancel_btn.setText(self.tr("cancel"))
        self.ok_btn.setText(self.tr("ok"))
        
        # 更新提示文本
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            for row in range(table.rowCount()):
                shortcut_container = table.cellWidget(row, 1)
                if shortcut_container:
                    # 查找布局中的QLineEdit和QPushButton
                    shortcut_editor = None
                    restore_button = None
                    
                    for i in range(shortcut_container.layout().count()):
                        widget = shortcut_container.layout().itemAt(i).widget()
                        if isinstance(widget, QLineEdit):
                            shortcut_editor = widget
                        elif isinstance(widget, QPushButton):
                            restore_button = widget
                    
                    if shortcut_editor:
                        shortcut_editor.setPlaceholderText(self.tr("nop_hint"))
                        
                    if restore_button:
                        restore_button.setText(self.tr("reset_shortcut"))
    
    def refresh_table_names(self):
        """更新标签页和表头名称"""
        # 更新标签页名称
        self.tabs.setTabText(0, self.tr("main_tab"))
        self.tabs.setTabText(1, self.tr("editor_tab"))
        self.tabs.setTabText(2, self.tr("reviewer_tab"))
        self.tabs.setTabText(3, self.tr("browser_tab"))
        self.tabs.setTabText(4, self.tr("toolbar_tab"))
        
        # 更新表格头
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            table.setHorizontalHeaderLabels([self.tr("function_col"), self.tr("shortcut_col")])
            
        # 更新各表格中功能的名称显示（根据语言）
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            for row in range(table.rowCount()):
                try:
                    # Qt 6
                    key = table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                except AttributeError:
                    # Qt 5
                    key = table.item(row, 0).data(Qt.UserRole)
                
                name_item = table.item(row, 0)
                name_item.setText(self.get_readable_name(key))
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # 顶部区域 - 搜索和语言选择
        top_layout = QHBoxLayout()
        
        # 搜索框
        search_layout = QHBoxLayout()
        self.search_label = QLabel("搜索:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_shortcuts)
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        
        # 语言选择
        language_layout = QHBoxLayout()
        self.language_label = QLabel("语言:")
        self.language_combo = QComboBox()
        self.language_combo.addItem("中文", "zh_CN")
        self.language_combo.addItem("English", "en_US")
        self.language_combo.currentIndexChanged.connect(self.change_language)
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo)
        
        top_layout.addLayout(search_layout)
        top_layout.addStretch()
        top_layout.addLayout(language_layout)
        
        main_layout.addLayout(top_layout)
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.editor_tab = QWidget()
        self.reviewer_tab = QWidget()
        self.browser_tab = QWidget()
        self.toolbar_tab = QWidget()
        
        self.tabs.addTab(self.main_tab, "主界面")
        self.tabs.addTab(self.editor_tab, "编辑器")
        self.tabs.addTab(self.reviewer_tab, "复习界面")
        self.tabs.addTab(self.browser_tab, "浏览器")
        self.tabs.addTab(self.toolbar_tab, "工具栏")
        
        # 创建快捷键表格
        self.main_table = self.create_table()
        self.editor_table = self.create_table()
        self.reviewer_table = self.create_table()
        self.browser_table = self.create_table()
        self.toolbar_table = self.create_table()
        
        # 设置标签页布局
        self.setup_tab(self.main_tab, self.main_table)
        self.setup_tab(self.editor_tab, self.editor_table)
        self.setup_tab(self.reviewer_tab, self.reviewer_table)
        self.setup_tab(self.browser_tab, self.browser_table)
        self.setup_tab(self.toolbar_tab, self.toolbar_table)
        
        main_layout.addWidget(self.tabs)
        
        # 配置文件路径设置区域
        config_path_layout = QVBoxLayout()
        
        # 添加提示文本
        path_note_label = QLabel(self.tr("config_path_note"))
        path_note_label.setWordWrap(True)
        config_path_layout.addWidget(path_note_label)
        self.path_note_label = path_note_label
        
        # 路径选择区域
        path_layout = QHBoxLayout()
        self.path_label = QLabel(self.tr("config_path"))
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        
        # 显示当前配置文件路径
        if USER_CONFIG_PATH:
            self.path_input.setText(USER_CONFIG_PATH)
        
        self.browse_btn = QPushButton(self.tr("browse_btn"))
        self.browse_btn.clicked.connect(self.select_config_path)
        
        self.reset_path_btn = QPushButton(self.tr("reset_path_btn"))
        self.reset_path_btn.clicked.connect(self.reset_config_path)
        
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        path_layout.addWidget(self.reset_path_btn)
        
        config_path_layout.addLayout(path_layout)
        main_layout.addLayout(config_path_layout)
        
        # 底部按钮 - 改为垂直布局，包含三行按钮
        button_layout = QVBoxLayout()
        
        # 第一行：当前标签页操作按钮
        first_row_layout = QHBoxLayout()
        self.disable_current_tab_btn = QPushButton("禁用当前页所有快捷键")
        self.disable_current_tab_btn.clicked.connect(self.disable_current_tab_shortcuts)
        
        self.restore_current_tab_btn = QPushButton("恢复当前页所有快捷键")
        self.restore_current_tab_btn.clicked.connect(self.restore_current_tab_shortcuts)
        
        first_row_layout.addWidget(self.disable_current_tab_btn)
        first_row_layout.addWidget(self.restore_current_tab_btn)
        
        # 第二行：全局操作按钮
        second_row_layout = QHBoxLayout()
        self.disable_all_btn = QPushButton("禁用所有快捷键")
        self.disable_all_btn.clicked.connect(self.disable_all_shortcuts)
        
        self.restore_default_btn = QPushButton("恢复默认设置")
        self.restore_default_btn.clicked.connect(self.restore_default)
        
        second_row_layout.addWidget(self.disable_all_btn)
        second_row_layout.addWidget(self.restore_default_btn)
        
        # 第三行：确认和取消按钮
        third_row_layout = QHBoxLayout()
        self.apply_btn = QPushButton("应用")
        self.apply_btn.clicked.connect(self.apply_changes)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.accept)
        
        third_row_layout.addStretch()
        third_row_layout.addWidget(self.apply_btn)
        third_row_layout.addWidget(self.cancel_btn)
        third_row_layout.addWidget(self.ok_btn)
        
        # 将三行布局添加到垂直布局中
        button_layout.addLayout(first_row_layout)
        button_layout.addLayout(second_row_layout)
        button_layout.addLayout(third_row_layout)
        
        main_layout.addLayout(button_layout)
    
    def change_language(self, index):
        """切换界面语言"""
        new_lang = self.language_combo.itemData(index)
        if new_lang != self.current_lang:
            self.current_lang = new_lang
            # 更新界面文本
            self.update_ui_language()
            
            # 更新配置
            self.config["interface_language"] = new_lang
            # 保存到全局配置
            mw.addonManager.writeConfig(__name__, self.config)
            
            # 更新菜单项文本
            custom_shortcuts.update_shortcut_manager_menu_text(new_lang)
    
    def setup_tab(self, tab, table):
        layout = QVBoxLayout(tab)
        # 设置边距使表格居中显示
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(table)
    
    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["功能", "快捷键"])
        
        # 设置表格策略为扩展，以适应对话框大小
        try:
            # Qt 6
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        except AttributeError:
            # Qt 5
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
        table.setSizePolicy(sizePolicy)
        
        # 修改列宽以适应表格大小
        try:
            # Qt 6
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        except AttributeError:
            # Qt 5
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        table.verticalHeader().setVisible(False)
        return table
    
    def load_shortcuts(self):
        # 清空表格
        self.clear_tables()
        
        # 加载主界面快捷键
        main_shortcuts = {k: v for k, v in self.config.items() if k.startswith("main ") and not isinstance(v, dict)}
        self.populate_table(self.main_table, main_shortcuts)
        
        # 加载编辑器快捷键
        editor_shortcuts = {k: v for k, v in self.config.items() if k.startswith("editor ") and not isinstance(v, dict)}
        self.populate_table(self.editor_table, editor_shortcuts)
        
        # 加载复习界面快捷键
        reviewer_shortcuts = {k: v for k, v in self.config.items() if k.startswith("reviewer ") and not isinstance(v, dict)}
        self.populate_table(self.reviewer_table, reviewer_shortcuts)
        
        # 加载浏览器快捷键
        browser_shortcuts = {k: v for k, v in self.config.items() if k.startswith("window_browser ") and not isinstance(v, dict)}
        self.populate_table(self.browser_table, browser_shortcuts)
        
        # 加载工具栏快捷键
        toolbar_shortcuts = {k: v for k, v in self.config.items() if k.startswith("m_toolbox ") and not isinstance(v, dict)}
        self.populate_table(self.toolbar_table, toolbar_shortcuts)
    
    def clear_tables(self):
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            table.setRowCount(0)
    
    def populate_table(self, table, shortcuts):
        for i, (key, value) in enumerate(sorted(shortcuts.items())):
            table.insertRow(i)
            
            # 功能名称
            name_item = QTableWidgetItem(self.get_readable_name(key))
            # 修复 Qt 6 兼容性问题
            try:
                # Qt 6
                name_item.setData(Qt.ItemDataRole.UserRole, key)  # 存储原始键名
            except AttributeError:
                # Qt 5
                name_item.setData(Qt.UserRole, key)  # 存储原始键名
            table.setItem(i, 0, name_item)
            
            # 创建一个水平布局容器
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(5, 0, 5, 0)
            layout.setSpacing(5)
            
            # 快捷键编辑
            shortcut_editor = QLineEdit(value)
            shortcut_editor.setPlaceholderText(self.tr("nop_hint"))
            # 设置快捷键编辑框的最小宽度为200像素
            shortcut_editor.setMinimumWidth(200)
            
            # 禁用特定快捷键的编辑功能
            if key in DISABLED_SHORTCUTS:
                shortcut_editor.setEnabled(False)
                # 检查是否处于暗色模式
                try:
                    from aqt.theme import theme_manager
                    if theme_manager.night_mode:
                        # 暗色主题样式
                        shortcut_editor.setStyleSheet("background-color: #222222; color: #888888;")
                    else:
                        # 亮色主题样式
                        shortcut_editor.setStyleSheet("background-color: #f0f0f0; color: #888888;")
                except (ImportError, AttributeError):
                    # 如果无法导入或获取主题信息，则使用默认样式
                    shortcut_editor.setStyleSheet("background-color: #f0f0f0; color: #888888;")
                    
                try:
                    # Qt 6
                    shortcut_editor.setToolTip(self.tr("disabled_shortcut"))
                except AttributeError:
                    # Qt 5
                    shortcut_editor.setToolTip(self.tr("disabled_shortcut"))
            
            # 添加快捷键编辑框到布局
            layout.addWidget(shortcut_editor, 1)  # 设置伸展因子为1
            
            # 创建恢复默认按钮
            restore_button = QPushButton()
            # 设置按钮文本
            restore_button.setText(self.tr("reset_shortcut"))
            # 设置按钮样式为紧凑型
            restore_button.setMaximumWidth(200)
            restore_button.setFixedHeight(20)
            
            # 检查是否为禁用的快捷键
            if key in DISABLED_SHORTCUTS:
                restore_button.setEnabled(False)
            
            # 按钮点击时恢复该快捷键的默认值
            restore_button.clicked.connect(lambda checked, k=key, editor=shortcut_editor: self.restore_single_shortcut(k, editor))
            
            # 添加按钮到布局
            layout.addWidget(restore_button)
            
            # 将容器设置为单元格的部件
            table.setCellWidget(i, 1, container)
    
    def get_readable_name(self, key):
        # 将配置键名转换为人类可读的名称
        try:
            readable_names = TRANSLATIONS[self.current_lang]["readable_names"]
            if key in readable_names:
                return readable_names[key]
        except (KeyError, TypeError):
            pass
        
        # 如果没有特定映射，就移除前缀并美化显示
        parts = key.split(" ")
        if len(parts) > 1:
            name = " ".join(parts[1:])
            return name.replace("_", " ").title()
        
        return key
    
    def filter_shortcuts(self):
        search_text = self.search_input.text().lower()
        
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            for row in range(table.rowCount()):
                name_item = table.item(row, 0)
                container = table.cellWidget(row, 1)
                
                # Find the QLineEdit within the container
                shortcut_editor = None
                for i in range(container.layout().count()):
                    widget = container.layout().itemAt(i).widget()
                    if isinstance(widget, QLineEdit):
                        shortcut_editor = widget
                        break
                
                shortcut_text = ""
                if shortcut_editor:
                    shortcut_text = shortcut_editor.text().lower()
                
                if search_text in name_item.text().lower() or search_text in shortcut_text:
                    table.setRowHidden(row, False)
                else:
                    table.setRowHidden(row, True)
    
    def get_shortcut_values(self):
        # 先复制完整的配置以保留所有原始属性
        result = copy.deepcopy(self.config)
        
        # 更新快捷键设置
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            for row in range(table.rowCount()):
                # 修复 Qt 6 兼容性问题
                try:
                    # Qt 6
                    key = table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                except AttributeError:
                    # Qt 5
                    key = table.item(row, 0).data(Qt.UserRole)
                
                # 从容器中获取QLineEdit控件
                container = table.cellWidget(row, 1)
                shortcut_editor = None
                
                # 查找布局中的QLineEdit
                for i in range(container.layout().count()):
                    widget = container.layout().itemAt(i).widget()
                    if isinstance(widget, QLineEdit):
                        shortcut_editor = widget
                        break
                
                if shortcut_editor:
                    value = shortcut_editor.text()
                    
                    # 确保禁用的快捷键保持<nop>值
                    if key in DISABLED_SHORTCUTS:
                        result[key] = "<nop>"
                    else:
                        result[key] = value
        
        # 确保语言设置被保留
        result["interface_language"] = self.current_lang
        
        return result
    
    def disable_all_shortcuts(self):
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            for row in range(table.rowCount()):
                # 获取键名来判断是否为禁用的快捷键
                try:
                    # Qt 6
                    key = table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                except AttributeError:
                    # Qt 5
                    key = table.item(row, 0).data(Qt.UserRole)
                    
                # 跳过已禁用的快捷键
                if key in DISABLED_SHORTCUTS:
                    continue
                    
                container = table.cellWidget(row, 1)
                # 查找布局中的QLineEdit
                shortcut_editor = None
                for i in range(container.layout().count()):
                    widget = container.layout().itemAt(i).widget()
                    if isinstance(widget, QLineEdit):
                        shortcut_editor = widget
                        break
                
                if shortcut_editor:
                    shortcut_editor.setText("<nop>")
    
    def disable_current_tab_shortcuts(self):
        """禁用当前标签页中的所有快捷键"""
        current_index = self.tabs.currentIndex()
        current_table = None
        
        # 根据当前标签页索引获取对应的表格
        if current_index == 0:  # 主界面
            current_table = self.main_table
        elif current_index == 1:  # 编辑器
            current_table = self.editor_table
        elif current_index == 2:  # 复习界面
            current_table = self.reviewer_table
        elif current_index == 3:  # 浏览器
            current_table = self.browser_table
        elif current_index == 4:  # 工具栏
            current_table = self.toolbar_table
            
        if current_table:
            # 将当前表格中的所有快捷键设置为<nop>
            for row in range(current_table.rowCount()):
                # 获取键名来判断是否为禁用的快捷键
                try:
                    # Qt 6
                    key = current_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                except AttributeError:
                    # Qt 5
                    key = current_table.item(row, 0).data(Qt.UserRole)
                
                # 跳过已禁用的快捷键
                if key in DISABLED_SHORTCUTS:
                    continue
                
                container = current_table.cellWidget(row, 1)
                # 查找布局中的QLineEdit
                shortcut_editor = None
                for i in range(container.layout().count()):
                    widget = container.layout().itemAt(i).widget()
                    if isinstance(widget, QLineEdit):
                        shortcut_editor = widget
                        break
                
                if shortcut_editor:
                    shortcut_editor.setText("<nop>")
    
    def restore_default(self):
        # 从默认配置文件加载
        if not os.path.exists(DEFAULT_CONFIG_PATH):
            showInfo(self.tr("default_file_missing"))
            return
        
        # 从默认配置文件加载
        with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
            default_config = json.load(f)
        
        # 保留用户自定义配置路径
        if USER_CONFIG_PATH and "config_file_path" not in default_config:
            default_config["config_file_path"] = USER_CONFIG_PATH
        
        # 恢复所有快捷键到默认值
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            for row in range(table.rowCount()):
                try:
                    # Qt 6
                    key = table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                except AttributeError:
                    # Qt 5
                    key = table.item(row, 0).data(Qt.UserRole)
                    
                # 跳过已禁用的快捷键
                if key in DISABLED_SHORTCUTS:
                    continue
                    
                if key in default_config:
                    container = table.cellWidget(row, 1)
                    # 查找布局中的QLineEdit
                    shortcut_editor = None
                    for i in range(container.layout().count()):
                        widget = container.layout().itemAt(i).widget()
                        if isinstance(widget, QLineEdit):
                            shortcut_editor = widget
                            break
                    
                    if shortcut_editor:
                        shortcut_editor.setText(default_config[key])
    
    def apply_changes(self):
        # 获取当前设置的快捷键
        new_config = self.get_shortcut_values()
        
        # 保存用户自定义路径到配置
        if USER_CONFIG_PATH:
            new_config["config_file_path"] = USER_CONFIG_PATH
            
            # 同时保存到用户自定义路径
            try:
                with open(USER_CONFIG_PATH, "w", encoding="utf-8") as f:
                    json.dump(new_config, f, ensure_ascii=False, indent=4)
            except Exception as e:
                showInfo(f"{self.tr('save_config_error')}: {str(e)}")
        
        # 保存到Anki配置
        mw.addonManager.writeConfig(__name__, new_config)
        
        # 重新加载插件
        showInfo(self.tr("changes_saved"))
    
    def accept(self):
        self.apply_changes()
        saveGeom(self, "shortcutManager")
        super(ShortcutManagerDialog, self).accept()
    
    def reject(self):
        saveGeom(self, "shortcutManager")
        super(ShortcutManagerDialog, self).reject()

    def restore_current_tab_shortcuts(self):
        """恢复当前标签页中的所有快捷键到默认设置"""
        if not os.path.exists(DEFAULT_CONFIG_PATH):
            showInfo(self.tr("default_file_missing"))
            return
            
        # 从默认配置文件加载
        with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
            default_config = json.load(f)
        
        current_index = self.tabs.currentIndex()
        current_table = None
        prefix = ""
        
        # 根据当前标签页索引获取对应的表格和前缀
        if current_index == 0:  # 主界面
            current_table = self.main_table
            prefix = "main "
        elif current_index == 1:  # 编辑器
            current_table = self.editor_table
            prefix = "editor "
        elif current_index == 2:  # 复习界面
            current_table = self.reviewer_table
            prefix = "reviewer "
        elif current_index == 3:  # 浏览器
            current_table = self.browser_table
            prefix = "window_browser "
        elif current_index == 4:  # 工具栏
            current_table = self.toolbar_table
            prefix = "m_toolbox "
            
        if current_table:
            # 恢复当前表格中的所有快捷键到默认设置
            for row in range(current_table.rowCount()):
                try:
                    # Qt 6
                    key = current_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                except AttributeError:
                    # Qt 5
                    key = current_table.item(row, 0).data(Qt.UserRole)
                    
                # 跳过已禁用的快捷键
                if key in DISABLED_SHORTCUTS:
                    continue
                    
                # 确认键存在于默认配置中
                if key in default_config:
                    container = current_table.cellWidget(row, 1)
                    # 查找布局中的QLineEdit
                    shortcut_editor = None
                    for i in range(container.layout().count()):
                        widget = container.layout().itemAt(i).widget()
                        if isinstance(widget, QLineEdit):
                            shortcut_editor = widget
                            break
                    
                    if shortcut_editor:
                        shortcut_editor.setText(default_config[key])

    def restore_single_shortcut(self, key, editor):
        """恢复单个快捷键到默认值"""
        if not os.path.exists(DEFAULT_CONFIG_PATH):
            showInfo(self.tr("default_file_missing"))
            return
            
        # 从默认配置文件加载
        with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
            default_config = json.load(f)
        
        # 检查键是否存在于默认配置中
        if key in default_config:
            editor.setText(default_config[key])
        else:
            # 如果键不在默认配置中（可能是新增的功能），设置为<nop>
            editor.setText("<nop>")

    def select_config_path(self):
        """选择配置文件保存路径"""
        global USER_CONFIG_PATH
        
        # 获取用户选择的文件路径
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("config_path"),
            os.path.expanduser("~"),
            "JSON Files (*.json)"
        )
        
        if file_path:
            # 更新全局变量
            USER_CONFIG_PATH = file_path
            # 更新界面显示
            self.path_input.setText(file_path)
            # 保存路径到配置
            self.config["config_file_path"] = file_path
            # 将当前配置保存到选定的路径
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=4)
                showInfo(self.tr("save_config_success"))
            except Exception as e:
                showInfo(f"{self.tr('save_config_error')}: {str(e)}")
                
    def reset_config_path(self):
        """重置配置文件路径为默认"""
        global USER_CONFIG_PATH
        USER_CONFIG_PATH = None
        self.path_input.clear()
        # 从配置中移除自定义路径
        if "config_file_path" in self.config:
            del self.config["config_file_path"]

    def on_theme_changed(self):
        """当主题变化时更新UI样式"""
        # 更新所有表格中的禁用快捷键文本框样式
        for table in [self.main_table, self.editor_table, self.reviewer_table, self.browser_table, self.toolbar_table]:
            for row in range(table.rowCount()):
                # 获取键名
                try:
                    # Qt 6
                    key = table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                except AttributeError:
                    # Qt 5
                    key = table.item(row, 0).data(Qt.UserRole)
                
                # 仅处理禁用的快捷键
                if key in DISABLED_SHORTCUTS:
                    container = table.cellWidget(row, 1)
                    # 查找文本框
                    for i in range(container.layout().count()):
                        widget = container.layout().itemAt(i).widget()
                        if isinstance(widget, QLineEdit):
                            # 根据当前主题设置样式
                            try:
                                from aqt.theme import theme_manager
                                if theme_manager.night_mode:
                                    # 暗色主题样式
                                    widget.setStyleSheet("background-color: #222222; color: #888888;")
                                else:
                                    # 亮色主题样式
                                    widget.setStyleSheet("background-color: #f0f0f0; color: #888888;")
                            except (ImportError, AttributeError):
                                # 默认样式
                                widget.setStyleSheet("background-color: #f0f0f0; color: #888888;")

def init_config_path():
    """初始化配置文件路径"""
    global USER_CONFIG_PATH
    
    # 从Anki配置中获取路径
    config = mw.addonManager.getConfig(__name__)
    if config and "config_file_path" in config:
        path = config["config_file_path"]
        if os.path.exists(os.path.dirname(path)):
            USER_CONFIG_PATH = path

def open_shortcut_manager():
    # 初始化配置路径
    init_config_path()
    
    dialog = ShortcutManagerDialog(mw)
    # 修复 Qt 6 兼容性问题
    try:
        # Qt 6
        dialog.exec()
    except AttributeError:
        # Qt 5
        dialog.exec_() 