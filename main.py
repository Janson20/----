import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import json
import random
import webbrowser
import requests
import threading
from tkinter.ttk import Progressbar
import hashlib
import bisect  # 新增导入bisect模块
class Word:
    def __init__(self, word, meaning):
        self.word = word.strip().lower()  # 统一存储为小写
        self.meaning = meaning.strip()

class WordBook:
    def __init__(self, filename):
        self.filename = filename
        self.words = self.load_words()

    def load_words(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                words = [Word(item['word'], item['meaning']) for item in json.load(file)]
                words.sort(key=lambda x: x.word)  # 加载后按单词排序
                return words
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_words(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([{'word': w.word, 'meaning': w.meaning} for w in self.words], 
                     file, ensure_ascii=False, indent=2)

    def add_word(self, word, meaning):
        if not word or not meaning:
            raise ValueError("单词和释义不能为空")
        if any(w.word == word.lower() for w in self.words):
            raise ValueError("单词已存在")
        new_word = Word(word, meaning)
        # 使用bisect找到插入位置以保持有序
        words_keys = [w.word for w in self.words]
        insert_pos = bisect.bisect_left(words_keys, new_word.word)
        self.words.insert(insert_pos, new_word)
        self.save_words()

    def remove_word(self, word):
        target = word.lower()
        original_count = len(self.words)
        self.words = [w for w in self.words if w.word != target]
        if len(self.words) < original_count:
            self.save_words()
            return True
        return False

    def search_local(self, word):
        target = word.lower()
        return next((w for w in self.words if w.word == target), None)

    @staticmethod
    def search_online(word):
        try:
            response = requests.get(
                f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
                timeout=10
            )
            if response.ok:
                return "\n".join(
                    f"{i+1}. {defn['definition']}" 
                    for entry in response.json()
                    for meaning in entry.get('meanings', [])
                    for i, defn in enumerate(meaning.get('definitions', []))
                )
            else:
                return "未找到释义"
        except requests.exceptions.RequestException as e:
            return "查询失败，请检查网络连接或稍后再试"


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("智能单词本 v2.0")
        self.wordbook = WordBook('wordbook.json')
        
        # 界面布局优化
        self.setup_ui()
        self.review_running = False  # 复习模式状态控制
        
    def setup_ui(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Label(input_frame, text="单词:").grid(row=0, column=0, sticky='e')
        self.word_entry = tk.Entry(input_frame, width=25)
        self.word_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="释义:").grid(row=1, column=0, sticky='e')
        self.meaning_entry = tk.Entry(input_frame, width=25)
        self.meaning_entry.grid(row=1, column=1, padx=5)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        actions = [
            ("添加单词", self.add_word),
            ("删除单词", self.remove_word),
            ("本地查询", self.search_local),
            ("联网查询", self.search_online),
            ("显示全部", self.show_all),
            ("开始复习", self.start_review),
            ("帮助文档", self.show_help)
        ]
        
        for i, (text, cmd) in enumerate(actions):
            tk.Button(btn_frame, text=text, width=10, command=cmd)\
                .grid(row=i//2, column=i%2, padx=5, pady=3)
                
        self.status_bar = tk.Label(self.root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # 核心功能方法改进
    def add_word(self):
        word = self.word_entry.get()
        meaning = self.meaning_entry.get()
        try:
            self.wordbook.add_word(word, meaning)
            self.update_status(f"成功添加: {word}")
            self.clear_entries()
        except ValueError as e:
            messagebox.showwarning("输入错误", str(e))

    def remove_word(self):
        word = self.word_entry.get().strip()
        if word:
            if self.wordbook.remove_word(word):
                self.update_status(f"已删除: {word}")
            else:
                messagebox.showinfo("提示", "单词不存在")
        else:
            messagebox.showwarning("错误", "请输入要删除的单词")

    def search_local(self):
        word = self.word_entry.get().strip()
        if word:
            found = self.wordbook.search_local(word)
            if found:
                self.show_result(f"{word} 的释义", found.meaning)
            else:
                messagebox.showinfo("提示", "本地词库未收录该单词")

    def search_online(self):
        def fetch_definition():
            self.toggle_loading(True)
            try:
                word = self.word_entry.get().strip()
                if not word:
                    return
                definition = WordBook.search_online(word)
                self.root.after(0, lambda: self.show_result(f"{word} 的联网释义", definition))
            finally:
                self.toggle_loading(False)
                
        threading.Thread(target=fetch_definition, daemon=True).start()

    def show_all(self):
        top = tk.Toplevel(self.root)
        top.title("全部单词")
        
        text_area = scrolledtext.ScrolledText(top, wrap=tk.WORD, width=50, height=20)
        text_area.pack(padx=10, pady=10)
        
        content = "\n".join(f"• {w.word:15}{w.meaning}" for w in self.wordbook.words)
        text_area.insert(tk.END, content or "词库为空")
        text_area.configure(state=tk.DISABLED)

    def start_review(self):
        if not self.wordbook.words:
            messagebox.showinfo("提示", "词库为空，请先添加单词")
            return
            
        self.review_running = True
        self.review_words = random.sample(self.wordbook.words, len(self.wordbook.words))
        self.next_question()

    def next_question(self):
        if not self.review_running or not self.review_words:
            self.review_running = False
            return
            
        word = self.review_words.pop(0)
        mode = random.choice(['英译中', '中译英'])
        
        prompt = (f"请输入'{word.word}'的释义：" if mode == '英译中' else 
                 f"请输入对应'{word.meaning}'的单词：")
                 
        answer = simpledialog.askstring("复习模式", prompt)
        
        if answer is None:  # 用户点击取消
            self.review_running = False
            return
            
        correct = (answer.strip().lower() == word.meaning.lower() if mode == '英译中' else
                  answer.strip().lower() == word.word.lower())
                  
        msg = "正确！" if correct else f"错误，正确答案是：{word.meaning if mode == '英译中' else word.word}"
        messagebox.showinfo("结果", msg)
        
        self.root.after(100, self.next_question)  # 延迟下个问题

    # 辅助方法
    def toggle_loading(self, show):
        if show:
            self.loading = Progressbar(self.status_bar, mode='indeterminate')
            self.loading.pack(side=tk.RIGHT)
            self.loading.start(10)
        else:
            if hasattr(self, 'loading'):
                self.loading.stop()
                self.loading.destroy()

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="就绪"))

    def clear_entries(self):
        self.word_entry.delete(0, tk.END)
        self.meaning_entry.delete(0, tk.END)

    def show_result(self, title, content):
        top = tk.Toplevel(self.root)
        top.title(title)
        
        text = scrolledtext.ScrolledText(top, wrap=tk.WORD, width=50, height=15)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, content)
        text.configure(state=tk.DISABLED)

    def show_help(self):
        webbrowser.open("https://github.com/Janson20/----/wiki/%E7%AE%80%E4%BB%8B")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
