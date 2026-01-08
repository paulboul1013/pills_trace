import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os

class MedicineTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("每日用藥紀錄追蹤")
        self.root.geometry("500x750")
        self.root.configure(bg='#E6F3FF')
        
        self.records_file = "pills_records.txt"
        self.daily_count = {"早餐": 0, "午餐": 0, "晚餐": 0}
        
        # 載入今日記錄
        self.load_today_count()
        
        # 建立主畫面
        self.create_main_frame()
        
    def create_main_frame(self):
        """創建主畫面"""
        # 清除現有內容
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 標題框
        title_frame = tk.Frame(self.root, bg='#4F46E5', height=100)
        title_frame.pack(fill='x', padx=0, pady=0)
        
        title_label = tk.Label(title_frame, text="每日用藥紀錄", 
                              font=('Microsoft JhengHei', 24, 'bold'),
                              bg='#4F46E5', fg='white')
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(title_frame, text="", 
                                 font=('Microsoft JhengHei', 11),
                                 bg='#4F46E5', fg='#C7D2FE')
        subtitle_label.pack()
        
        # 主內容區
        content_frame = tk.Frame(self.root, bg='#E6F3FF')
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # 上半部分：進度顯示
        top_frame = tk.Frame(content_frame, bg='#E6F3FF')
        top_frame.pack(fill='x', pady=(0, 10))
        
        # 今日進度
        total_count = sum(self.daily_count.values())
        progress_label = tk.Label(top_frame, text=f"{total_count}/3", 
                                 font=('Arial', 40, 'bold'),
                                 bg='#E6F3FF', fg='#4F46E5')
        progress_label.pack()
        
        progress_text = tk.Label(top_frame, text="今日已服用次數", 
                                font=('Microsoft JhengHei', 11),
                                bg='#E6F3FF', fg='#6B7280')
        progress_text.pack(pady=(0, 10))
        
        # 三餐按鈕區域
        meals_frame = tk.Frame(content_frame, bg='#E6F3FF')
        meals_frame.pack(fill='x', pady=(0, 10))
        
        meals = ["早餐", "午餐", "晚餐"]
        for meal in meals:
            self.create_meal_button(meals_frame, meal)
        
        # 按鈕區域框架（佔用更多空間）
        button_frame = tk.Frame(content_frame, bg='#E6F3FF')
        button_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # 查看記錄按鈕
        view_btn = tk.Button(button_frame, text=" 查看所有記錄",
                            font=('Microsoft JhengHei', 18, 'bold'),
                            bg='#4F46E5', fg='white',
                            activebackground='#4338CA',
                            activeforeground='white',
                            relief='flat', bd=0,
                            padx=30, pady=20,
                            cursor='hand2',
                            command=self.show_records)
        view_btn.pack(pady=10, fill='x')
    
    def create_meal_button(self, parent, meal):
        """創建餐次按鈕"""
        is_recorded = self.daily_count[meal] >= 1
        
        # 根據是否已記錄改變框架樣式
        if is_recorded:
            frame = tk.Frame(parent, bg='#F0FDF4', relief='solid', bd=1, highlightthickness=2,
                            highlightbackground='#86EFAC')
        else:
            frame = tk.Frame(parent, bg='white', relief='solid', bd=1, highlightthickness=2,
                            highlightbackground='#C7D2FE')
        frame.pack(fill='x', pady=5)
        
        # 根據是否已記錄改變按鈕樣式
        if is_recorded:
            btn_text = f"✓ {meal}"
            btn_bg = '#D1FAE5'
            btn_fg = '#065F46'
            btn_active_bg = '#A7F3D0'
        else:
            btn_text = f" {meal}"
            btn_bg = 'white'
            btn_fg = '#1F2937'
            btn_active_bg = '#EEF2FF'
        
        btn = tk.Button(frame, text=btn_text,
                       font=('Microsoft JhengHei', 16, 'bold'),
                       bg=btn_bg, fg=btn_fg,
                       activebackground=btn_active_bg,
                       activeforeground=btn_fg,
                       relief='flat', bd=0,
                       anchor='w', padx=20, pady=15,
                       cursor='hand2',
                       command=lambda: self.add_record(meal))
        btn.pack(side='left', fill='both', expand=True)
        
        # 根據是否已記錄改變計數標籤顏色
        if is_recorded:
            count_color = '#10B981'
            label_bg = '#F0FDF4'
        else:
            count_color = '#4F46E5'
            label_bg = 'white'
        
        count_label = tk.Label(frame, text=f"{self.daily_count[meal]}/1",
                              font=('Arial', 20, 'bold'),
                              bg=label_bg, fg=count_color)
        count_label.pack(side='right', padx=20)
    
    def add_record(self, meal):
        """新增用藥記錄"""
        # 檢查該餐次今天是否已經記錄過
        if self.daily_count[meal] >= 1:
            messagebox.showwarning("提醒", f"{meal} 今天已經記錄過了！\n每餐每天只能記錄一次。")
            return
        
        now = datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%I:%M")
        am_pm = "上午" if now.hour < 12 else "下午"
        
        record = f"{date_str}, {time_str}, {am_pm}, {meal}\n"
        
        # 寫入檔案
        with open(self.records_file, 'a', encoding='utf-8') as f:
            f.write(record)
        
        # 更新計數
        self.daily_count[meal] += 1
        
        # 重新載入畫面
        self.create_main_frame()
        
        messagebox.showinfo("成功", f"已記錄 {meal} 服藥！")
    
    def load_today_count(self):
        """載入今日服藥次數"""
        if not os.path.exists(self.records_file):
            return
        
        today = datetime.now().strftime("%Y/%m/%d")
        self.daily_count = {"早餐": 0, "午餐": 0, "晚餐": 0}
        
        with open(self.records_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and today in line:
                    parts = line.strip().split(', ')
                    if len(parts) >= 4:
                        meal = parts[3]
                        if meal in self.daily_count:
                            self.daily_count[meal] += 1
    
    def show_records(self):
        """顯示所有記錄"""
        # 清除現有內容
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 標題框
        title_frame = tk.Frame(self.root, bg='#4F46E5', height=80)
        title_frame.pack(fill='x')
        
        # 返回按鈕和標題在同一行
        header_frame = tk.Frame(title_frame, bg='#4F46E5')
        header_frame.pack(fill='x', padx=10, pady=15)
        
        back_btn = tk.Button(header_frame, text=" 返回",
                           font=('Microsoft JhengHei', 11, 'bold'),
                           bg='#6366F1', fg='white',
                           activebackground='#4338CA',
                           relief='flat', bd=0,
                           padx=15, pady=8,
                           cursor='hand2',
                           command=self.create_main_frame)
        back_btn.pack(side='left')
        
        title_label = tk.Label(header_frame, text="用藥記錄", 
                              font=('Microsoft JhengHei', 20, 'bold'),
                              bg='#4F46E5', fg='white')
        title_label.pack(side='left', padx=20)
        
        # 記錄列表框架
        list_frame = tk.Frame(self.root, bg='#E6F3FF')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 創建滾動區域
        canvas = tk.Canvas(list_frame, bg='#E6F3FF', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#E6F3FF')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 讀取記錄
        records = []
        if os.path.exists(self.records_file):
            with open(self.records_file, 'r', encoding='utf-8') as f:
                records = [line.strip() for line in f if line.strip()]
        
        if not records:
            no_record_label = tk.Label(scrollable_frame, text="尚無用藥記錄",
                                      font=('Microsoft JhengHei', 14),
                                      bg='#E6F3FF', fg='#9CA3AF')
            no_record_label.pack(pady=50)
        else:
            # 顯示記錄數量
            count_label = tk.Label(scrollable_frame, text=f"共 {len(records)} 筆記錄",
                                  font=('Microsoft JhengHei', 11),
                                  bg='#E6F3FF', fg='#6B7280')
            count_label.pack(anchor='w', padx=10, pady=(5, 10))
            
            # 倒序顯示（最新在前）
            for i, record in enumerate(reversed(records)):
                self.create_record_item(scrollable_frame, record, len(records) - i - 1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_record_item(self, parent, record, index):
        """創建記錄項目"""
        parts = record.split(', ')
        if len(parts) < 4:
            return
        
        date_str, time_str, am_pm, meal = parts[0], parts[1], parts[2], parts[3]
        
        item_frame = tk.Frame(parent, bg='white', relief='solid', bd=1,
                             highlightthickness=1, highlightbackground='#C7D2FE')
        item_frame.pack(fill='x', padx=10, pady=5)
        
        # 內容區
        content_frame = tk.Frame(item_frame, bg='white')
        content_frame.pack(fill='x', padx=15, pady=12)
        
        # 左側信息
        info_frame = tk.Frame(content_frame, bg='white')
        info_frame.pack(side='left', fill='both', expand=True)
        
        meal_label = tk.Label(info_frame, text=meal,
                             font=('Microsoft JhengHei', 12, 'bold'),
                             bg='#4F46E5', fg='white',
                             padx=12, pady=4)
        meal_label.pack(side='left')
        
        date_label = tk.Label(info_frame, text=f"  {date_str}",
                             font=('Microsoft JhengHei', 11),
                             bg='white', fg='#1F2937')
        date_label.pack(side='left')
        
        time_label = tk.Label(info_frame, text=f"{time_str} {am_pm}",
                             font=('Microsoft JhengHei', 10),
                             bg='white', fg='#6B7280')
        time_label.pack(anchor='w', padx=(42, 0))
        
        # 右側按鈕
        btn_frame = tk.Frame(content_frame, bg='white')
        btn_frame.pack(side='right')
        
        edit_btn = tk.Button(btn_frame, text="修改",
                           font=('Arial', 12),
                           bg='#DBEAFE', fg='#1E40AF',
                           activebackground='#BFDBFE',
                           relief='flat', bd=0,
                           width=3, height=1,
                           cursor='hand2',
                           command=lambda: self.edit_record(index))
        edit_btn.pack(side='left', padx=2)
        
        delete_btn = tk.Button(btn_frame, text="刪除",
                             font=('Arial', 12),
                             bg='#FEE2E2', fg='#991B1B',
                             activebackground='#FECACA',
                             relief='flat', bd=0,
                             width=3, height=1,
                             cursor='hand2',
                             command=lambda: self.delete_record(index))
        delete_btn.pack(side='left', padx=2)
    
    def edit_record(self, index):
        """編輯記錄"""
        # 讀取所有記錄
        with open(self.records_file, 'r', encoding='utf-8') as f:
            records = f.readlines()
        
        if index >= len(records):
            return
        
        # 創建編輯視窗
        edit_window = tk.Toplevel(self.root)
        edit_window.title("編輯記錄")
        edit_window.geometry("350x250")
        edit_window.configure(bg='#E6F3FF')
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        tk.Label(edit_window, text="修改時間", 
                font=('Microsoft JhengHei', 14, 'bold'),
                bg='#E6F3FF').pack(pady=20)
        
        # 日期輸入
        date_frame = tk.Frame(edit_window, bg='#E6F3FF')
        date_frame.pack(pady=5)
        tk.Label(date_frame, text="日期 (YYYY/MM/DD):", 
                font=('Microsoft JhengHei', 11),
                bg='#E6F3FF').pack(side='left', padx=5)
        date_entry = tk.Entry(date_frame, font=('Arial', 11), width=15)
        date_entry.pack(side='left')
        
        # 時間輸入
        time_frame = tk.Frame(edit_window, bg='#E6F3FF')
        time_frame.pack(pady=5)
        tk.Label(time_frame, text="時間 (HH:MM):", 
                font=('Microsoft JhengHei', 11),
                bg='#E6F3FF').pack(side='left', padx=5)
        time_entry = tk.Entry(time_frame, font=('Arial', 11), width=10)
        time_entry.pack(side='left', padx=5)
        
        # AM/PM 選擇
        ampm_var = tk.StringVar(value="上午")
        ampm_frame = tk.Frame(time_frame, bg='#E6F3FF')
        ampm_frame.pack(side='left')
        tk.Radiobutton(ampm_frame, text="上午", variable=ampm_var, value="上午",
                      font=('Microsoft JhengHei', 10),
                      bg='#E6F3FF').pack(side='left')
        tk.Radiobutton(ampm_frame, text="下午", variable=ampm_var, value="下午",
                      font=('Microsoft JhengHei', 10),
                      bg='#E6F3FF').pack(side='left')
        
        # 填入現有資料
        old_parts = records[index].strip().split(', ')
        if len(old_parts) >= 4:
            date_entry.insert(0, old_parts[0])
            time_entry.insert(0, old_parts[1])
            ampm_var.set(old_parts[2])
        
        def save_changes():
            new_date = date_entry.get()
            new_time = time_entry.get()
            new_ampm = ampm_var.get()
            
            if not new_date or not new_time:
                messagebox.showerror("錯誤", "請填寫完整資料")
                return
            
            records[index] = f"{new_date}, {new_time}, {new_ampm}, {old_parts[3]}\n"
            
            with open(self.records_file, 'w', encoding='utf-8') as f:
                f.writelines(records)
            
            edit_window.destroy()
            self.load_today_count()
            self.show_records()
            messagebox.showinfo("成功", "記錄已更新！")
        
        # 按鈕
        btn_frame = tk.Frame(edit_window, bg='#E6F3FF')
        btn_frame.pack(pady=20)
        
        save_btn = tk.Button(btn_frame, text="儲存", 
                           font=('Microsoft JhengHei', 12, 'bold'),
                           bg='#10B981', fg='white',
                           activebackground='#059669',
                           relief='flat', bd=0,
                           padx=25, pady=8,
                           cursor='hand2',
                           command=save_changes)
        save_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="取消", 
                             font=('Microsoft JhengHei', 12),
                             bg='#9CA3AF', fg='white',
                             activebackground='#6B7280',
                             relief='flat', bd=0,
                             padx=25, pady=8,
                             cursor='hand2',
                             command=edit_window.destroy)
        cancel_btn.pack(side='left', padx=5)
    
    def delete_record(self, index):
        """刪除記錄"""
        if messagebox.askyesno("確認刪除", "確定要刪除此記錄嗎？"):
            with open(self.records_file, 'r', encoding='utf-8') as f:
                records = f.readlines()
            
            if index < len(records):
                del records[index]
                
                with open(self.records_file, 'w', encoding='utf-8') as f:
                    f.writelines(records)
                
                self.load_today_count()
                self.show_records()

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicineTracker(root)
    root.mainloop()