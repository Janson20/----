import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random
import webbrowser

class Word:
    def __init__(self, word, meaning):
        self.word = word
        self.meaning = meaning

class WordBook:
    def __init__(self, filename):
        self.filename = filename
        self.words = self.load_words()

    def load_words(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                words_data = json.load(file)
                return [Word(word['word'], word['meaning']) for word in words_data]
        except FileNotFoundError:
            return []

    def save_words(self):
        words_data = [{'word': word.word, 'meaning': word.meaning} for word in self.words]
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(words_data, file, ensure_ascii=False, indent=4)

    def add_word(self, word, meaning):
        new_word = Word(word, meaning)
        self.words.append(new_word)
        self.save_words()

    def remove_word(self, word):
        for w in self.words:
            if w.word == word:
                self.words.remove(w)
                self.save_words()
                return

    def search_word(self, word):
        for w in self.words:
            if w.word == word:
                return w
        return None

    def show_all_words(self):
        return [(word.word, word.meaning) for word in self.words]

    def review_words(self):
        if not self.words:
            return []
        review_list = []
        for _ in range(len(self.words)):
            review_word = random.choice(self.words)
            review_mode = random.choice(['英译中', '中译英'])
            review_list.append((review_word, review_mode))
        return review_list

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("记单词程序")
        self.wordBook = WordBook('word_book.json')

        tk.Label(root, text="单词：").grid(row=0, column=0)
        self.word_entry = tk.Entry(root)
        self.word_entry.grid(row=0, column=1)

        tk.Label(root, text="意思：").grid(row=1, column=0)
        self.meaning_entry = tk.Entry(root)
        self.meaning_entry.grid(row=1, column=1)

        tk.Button(root, text="添加单词", command=self.add_word).grid(row=2, column=0, columnspan=2)
        tk.Button(root, text="删除单词", command=self.remove_word).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="查找单词", command=self.search_word).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="显示所有单词", command=self.show_all_words).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="复习单词", command=self.review_words).grid(row=6, column=0, columnspan=2)
        tk.Button(root, text="帮助", command=self.open_help).grid(row=7, column=0, columnspan=2)  # 添加帮助按钮

    def add_word(self):
        word = self.word_entry.get().strip()
        meaning = self.meaning_entry.get().strip()
        if word and meaning:
            self.wordBook.add_word(word, meaning)
            messagebox.showinfo("提示", f"单词 '{word}' 已添加到单词本并保存到本地文件。")
            self.word_entry.delete(0, tk.END)
            self.meaning_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("错误", "单词和意思不能为空！")

    def remove_word(self):
        word = self.word_entry.get().strip()
        if word:
            self.wordBook.remove_word(word)
            messagebox.showinfo("提示", f"单词 '{word}' 已从单词本中移除并更新本地文件。")
        else:
            messagebox.showwarning("错误", "请输入要删除的单词！")

    def search_word(self):
        word = self.word_entry.get().strip()
        if word:
            found_word = self.wordBook.search_word(word)
            if found_word:
                messagebox.showinfo("提示", f"单词 '{word}' 的意思是：'{found_word.meaning}'")
            else:
                messagebox.showinfo("提示", f"单词 '{word}' 不在单词本中。")
        else:
            messagebox.showwarning("错误", "请输入要查找的单词！")

    def show_all_words(self):
        words = self.wordBook.show_all_words()
        if words:
            message = "\n".join([f"{word} - {meaning}" for word, meaning in words])
            messagebox.showinfo("单词本中的单词", message)
        else:
            messagebox.showinfo("提示", "单词本为空。")

    def review_words(self):
        review_list = self.wordBook.review_words()
        if not review_list:
            messagebox.showinfo("提示", "单词本为空，无法复习。")
            return
        messagebox.showinfo("提示", "开始复习单词...")
        for review_word, review_mode in review_list:
            if review_mode == '英译中':
                user_answer = simpledialog.askstring("复习单词", f"请回忆单词 '{review_word.word}' 的意思：")
                if user_answer.strip().lower() == review_word.meaning.strip().lower():
                    messagebox.showinfo("提示", "回答正确！")
                elif user_answer == None:
                    self.root.destroy()
                else:
                    messagebox.showinfo("提示", f"回答错误，正确意思是：'{review_word.meaning}'")
            else:
                user_answer = simpledialog.askstring("复习单词", f"请回忆意思为 '{review_word.meaning}' 的单词：")
                if user_answer.strip().lower() == review_word.word.strip().lower():
                    messagebox.showinfo("提示", "回答正确！")
                elif user_answer == None:
                    self.root.destroy()
                else:
                    messagebox.showinfo("提示", f"回答错误，正确单词是：'{review_word.word}'")
    def open_help(self):
        help_url = "https://github.com/Janson20/----/wiki"  # 替换为实际的帮助网站 URL
        webbrowser.open(help_url)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()