import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os
import pandas as pd
root = tk.Tk()
root.title("Quản lý nhân viên")
root.geometry('400x400')
CSV_FILE = "employees.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Mã", "Tên", "Đơn vị", "Chức danh", "Ngày sinh", "Giới tính", "Số CMND", "Ngày cấp", "Nơi cấp"])
def save_employee():
    employee_data = {
        "Mã": entry_id.get(),
        "Tên": entry_name.get(),
        "Đơn vị": entry_department.get(),
        "Chức danh": entry_position.get(),
        "Ngày sinh": entry_birthdate.get(),
        "Giới tính": gender_var.get(),
        "Số CMND": entry_id_card.get(),
        "Ngày cấp": entry_issue_date.get(),
        "Nơi cấp": entry_issue_place.get()
    }
    if not all(employee_data.values()):
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
        return
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(employee_data.values())
    messagebox.showinfo("Thành công", "Đã lưu thông tin nhân viên")
    clear_fields()
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_department.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_birthdate.delete(0, tk.END)
    gender_var.set("Nam")
    entry_id_card.delete(0, tk.END)
    entry_issue_date.delete(0, tk.END)
    entry_issue_place.delete(0, tk.END)
def show_today_birthdays():
    today = datetime.now().strftime("%d/%m/%Y")
    birthdays = []
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Ngày sinh"] == today:
                birthdays.append(row)
    if birthdays:
        message = "\n".join([f"Mã: {e['Mã']}, Tên: {e['Tên']}" for e in birthdays])
        messagebox.showinfo("Sinh nhật hôm nay", message)
    else:
        messagebox.showinfo("Sinh nhật hôm nay", "Không có nhân viên nào sinh nhật hôm nay.")
def export_to_excel():
    try:
        df = pd.read_csv(CSV_FILE)
        df["Tuổi"] = df["Ngày sinh"].apply(lambda x: (datetime.now() - datetime.strptime(x, "%d/%m/%Y")).days // 365)
        df = df.sort_values(by="Tuổi", ascending=False)
        output_file = "employee_list.xlsx"
        df.to_excel(output_file, index=False, encoding="utf-8")
        messagebox.showinfo("Thành công", f"Danh sách nhân viên đã xuất ra file {output_file}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xuất file: {e}")
# Thông tin nhân viên
frame = ttk.LabelFrame(root, text="Thông tin nhân viên")
frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
#hop kiem
var1 = tk.BooleanVar()
checkbox1 = tk.Checkbutton(root, text="Là khách hàng", variable=var1, font=("Arial", 8))
checkbox1.place(x=130,y=6)
var2 = tk.BooleanVar()
checkbox2 = tk.Checkbutton(root, text="Là nhà cung cấp", variable=var2, font=("Arial", 8))
checkbox2.place(x=230,y=6)
# Các nhãn và ô nhập liệu
labels = ["Mã", "Tên", "Đơn vị", "Chức danh", "Ngày sinh", "Giới tính", "Số CMND", "Ngày cấp", "Nơi cấp"]
entry_id = ttk.Entry(frame)
entry_name = ttk.Entry(frame)
entry_department = ttk.Entry(frame)
entry_position = ttk.Entry(frame)
entry_birthdate = ttk.Entry(frame)
entry_id_card = ttk.Entry(frame)
entry_issue_date = ttk.Entry(frame)
entry_issue_place = ttk.Entry(frame)
gender_var = tk.StringVar(value="Nam")
gender_male = ttk.Radiobutton(frame, text="Nam", variable=gender_var, value="Nam")
gender_female = ttk.Radiobutton(frame, text="Nữ", variable=gender_var, value="Nữ")
widgets = [
    ("Mã", entry_id),
    ("Tên", entry_name),
    ("Đơn vị", entry_department),
    ("Chức danh", entry_position),
    ("Ngày sinh", entry_birthdate),
    ("Giới tính", (gender_male, gender_female)),
    ("Số CMND", entry_id_card),
    ("Ngày cấp", entry_issue_date),
    ("Nơi cấp", entry_issue_place)
]
for i, (label, widget) in enumerate(widgets):
    ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    if isinstance(widget, tuple):
        widget[0].grid(row=i, column=1, sticky="w")
        widget[1].grid(row=i, column=2, sticky="w")
    else:
        widget.grid(row=i, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
btn_frame = ttk.Frame(root)
btn_frame.grid(row=1, column=0, pady=10)
btn_save = ttk.Button(btn_frame, text="Lưu thông tin", command=save_employee)
btn_save.grid(row=0, column=0, padx=5)
btn_birthdays = ttk.Button(btn_frame, text="Sinh nhật hôm nay", command=show_today_birthdays)
btn_birthdays.grid(row=0, column=1, padx=5)
btn_export = ttk.Button(btn_frame, text="Xuất toàn bộ danh sách", command=export_to_excel)
btn_export.grid(row=0, column=2, padx=5)
root.mainloop()