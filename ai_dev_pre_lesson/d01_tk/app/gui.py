import json
import math
import shutil
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SOURCE_DATA_DIR = BASE_DIR.parent / "d01" / "data"
TZ = timezone(timedelta(hours=8))
APP_FONT_FAMILY = None
ROOT_ROLE_CODES = {"root", "019f4515-aebe-7710-b714-001d7a975f5e"}


def is_root(user):
    return user.get("role_code") in ROOT_ROLE_CODES


def configure_chinese_font(root):
    """Choose an installed CJK font and apply it to Tk's named fonts."""
    global APP_FONT_FAMILY
    candidates = (
        "Microsoft YaHei UI", "Microsoft YaHei", "SimHei",
        "PingFang SC", "Hiragino Sans GB", "Heiti SC",
        "Noto Sans CJK SC", "Noto Sans SC", "Source Han Sans SC",
        "WenQuanYi Micro Hei", "WenQuanYi Zen Hei", "Droid Sans Fallback",
    )
    installed = set(tkfont.families(root))
    APP_FONT_FAMILY = next((name for name in candidates if name in installed), None)

    if APP_FONT_FAMILY:
        for name in (
            "TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont",
            "TkCaptionFont", "TkSmallCaptionFont", "TkIconFont", "TkTooltipFont",
        ):
            try:
                tkfont.nametofont(name).configure(family=APP_FONT_FAMILY)
            except tk.TclError:
                pass
    return APP_FONT_FAMILY


def app_font(size, weight="normal"):
    family = APP_FONT_FAMILY or tkfont.nametofont("TkDefaultFont").actual("family")
    return family, size, weight



def now():
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


class Store:
    FILES = ("user", "role", "account", "account_type", "category", "direction", "transaction")

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        for name in self.FILES:
            target = DATA_DIR / f"{name}.json"
            source = SOURCE_DATA_DIR / f"{name}.json"
            if not target.exists():
                if source.exists():
                    shutil.copyfile(source, target)
                else:
                    target.write_text("[]", encoding="utf-8")

    def load(self, name):
        with (DATA_DIR / f"{name}.json").open(encoding="utf-8") as file:
            return json.load(file)

    def save(self, name, records):
        with (DATA_DIR / f"{name}.json").open("w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=4)

    def login(self, username, password):
        return next((u for u in self.load("user") if not u.get("is_deleted")
                     and u.get("name") == username and u.get("password") == password), None)

    def choices(self, name, user=None):
        rows = [r for r in self.load(name) if not r.get("is_deleted")]
        if user and name in {"account", "category"} and not is_root(user):
            rows = [r for r in rows if r.get("user_id") in {user["id"], None}
                    or r.get("is_default")]
        return rows

    def transactions(self, user):
        rows = self.choices("transaction")
        if is_root(user):
            return rows
        return [r for r in rows if r.get("created_by") == user["id"]]

    def transaction(self, transaction_id):
        return next((r for r in self.choices("transaction") if r.get("id") == transaction_id), None)

    def update_transaction(self, transaction_id, values, user):
        rows = self.load("transaction")
        for row in rows:
            if row.get("id") == transaction_id and not row.get("is_deleted"):
                row.update(values)
                row["updated_at"] = now()
                row["updated_by"] = user["id"]
                self.save("transaction", rows)
                return True
        return False

    def add(self, name, values, user):
        rows = self.load(name)
        stamp = now()
        values.update({"id": str(uuid.uuid4()), "created_at": stamp, "updated_at": stamp,
                       "created_by": user["id"], "updated_by": user["id"],
                       "is_deleted": False, "is_default": False})
        if name in {"account", "account_type", "category"}:
            values["user_id"] = user["id"]
        rows.append(values)
        self.save(name, rows)

    def adjust_account_balance(self, account_id, new_balance, category_id, user):
        accounts = self.load("account")
        account = next((row for row in accounts
                        if row.get("id") == account_id and not row.get("is_deleted")), None)
        if not account:
            raise ValueError("账户不存在或已被删除。")

        old_balance = float(account.get("balance", 0))
        difference = new_balance - old_balance
        if difference == 0:
            raise ValueError("新余额与当前余额相同。")
        direction_code = "income" if difference > 0 else "expense"

        categories = self.choices("category", user)
        category = next((row for row in categories if row.get("id") == category_id), None)
        if not category:
            raise ValueError("请选择有效的调整分类。")
        if category.get("direction_code") != direction_code:
            direction_name = "收入" if direction_code == "income" else "支出"
            raise ValueError(f"余额变化属于{direction_name}，请选择对应的分类。")

        stamp = now()
        account["balance"] = new_balance
        account["updated_at"] = stamp
        account["updated_by"] = user["id"]

        owner_id = user["id"]
        if is_root(user):
            user_ids = {row["id"] for row in self.choices("user")}
            if account.get("user_id") in user_ids:
                owner_id = account["user_id"]
        transactions = self.load("transaction")
        transactions.append({
            "id": str(uuid.uuid4()),
            "date": datetime.now(TZ).strftime("%Y-%m-%d"),
            "time": datetime.now(TZ).strftime("%H:%M:%S"),
            "amount": f"{abs(difference):.2f}",
            "account_id": account_id,
            "direction_code": direction_code,
            "category_id": category_id,
            "note": f"账户余额调整：{old_balance:.2f} -> {new_balance:.2f}",
            "created_at": stamp,
            "updated_at": stamp,
            "created_by": owner_id,
            "updated_by": user["id"],
            "is_deleted": False,
            "is_default": False,
        })
        self.save("account", accounts)
        self.save("transaction", transactions)

    def delete_transaction(self, transaction_id):
        rows = self.load("transaction")
        for row in rows:
            if row["id"] == transaction_id:
                row["is_deleted"] = True
                row["updated_at"] = now()
        self.save("transaction", rows)


class LoginFrame(ttk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master, padding=40)
        self.on_login = on_login
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text="个人记账系统", font=app_font(22, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(20, 30))
        ttk.Label(self, text="用户名").grid(row=1, column=0, padx=8, pady=8, sticky="e")
        ttk.Label(self, text="密码").grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.username = ttk.Entry(self, width=30)
        self.password = ttk.Entry(self, width=30, show="*")
        self.username.grid(row=1, column=1, pady=8)
        self.password.grid(row=2, column=1, pady=8)
        ttk.Button(self, text="登录", command=self.submit).grid(row=3, column=0, columnspan=2, pady=20)
        self.password.bind("<Return>", lambda _event: self.submit())
        self.username.focus_set()

    def submit(self):
        self.on_login(self.username.get().strip(), self.password.get())


class FormDialog(tk.Toplevel):
    def __init__(self, master, title, fields, submit):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.entries = {}
        body = ttk.Frame(self, padding=18)
        body.pack(fill="both", expand=True)
        for row, (key, label, kind, options, default) in enumerate(fields):
            ttk.Label(body, text=label).grid(row=row, column=0, padx=6, pady=7, sticky="e")
            if kind == "combo":
                widget = ttk.Combobox(body, state="readonly", width=28)
                widget["values"] = list(options)
                if default in options:
                    widget.current(list(options).index(default))
                elif options:
                    widget.current(0)
            else:
                widget = ttk.Entry(body, width=31, show="*" if kind == "password" else "")
                if default:
                    widget.insert(0, default)
            widget.grid(row=row, column=1, padx=6, pady=7)
            self.entries[key] = widget

        def save():
            values = {key: widget.get().strip() for key, widget in self.entries.items()}
            if submit(values):
                self.destroy()

        ttk.Button(body, text="保存", command=save).grid(row=len(fields), column=0, pady=14)
        ttk.Button(body, text="取消", command=self.destroy).grid(row=len(fields), column=1, pady=14)


class AccountManagerDialog(tk.Toplevel):
    def __init__(self, master, store, user, account_names, accounts,
                 category_names, categories, on_change):
        super().__init__(master)
        self.store = store
        self.user = user
        self.accounts = accounts
        self.on_change = on_change
        self.title("账户管理")
        self.geometry("820x560")
        self.minsize(720, 480)
        self.transient(master)

        selector = ttk.Frame(self, padding=(14, 14, 14, 8))
        selector.pack(fill="x")
        ttk.Label(selector, text="账户：").pack(side="left")
        self.account_combo = ttk.Combobox(selector, state="readonly", width=24,
                                          values=account_names)
        self.account_combo.pack(side="left")
        self.account_combo.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        if account_names:
            self.account_combo.current(0)

        info = ttk.LabelFrame(self, text="账户信息", padding=12)
        info.pack(fill="x", padx=14, pady=6)
        self.info_text = tk.StringVar()
        ttk.Label(info, textvariable=self.info_text).grid(row=0, column=0, columnspan=5,
                                                          sticky="w", pady=(0, 10))
        ttk.Label(info, text="新余额：").grid(row=1, column=0, sticky="e")
        self.balance_entry = ttk.Entry(info, width=16)
        self.balance_entry.grid(row=1, column=1, padx=(0, 14))
        ttk.Label(info, text="调整分类：").grid(row=1, column=2, sticky="e")

        self.category_values = categories
        self.category_combo = ttk.Combobox(
            info, state="readonly", width=18, values=category_names)
        self.category_combo.grid(row=1, column=3, padx=(0, 14))
        if self.category_values:
            self.category_combo.current(0)
        ttk.Button(info, text="调整余额并记账", command=self.adjust_balance).grid(row=1, column=4)

        table_frame = ttk.LabelFrame(self, text="账户交易", padding=8)
        table_frame.pack(fill="both", expand=True, padx=14, pady=(6, 14))
        columns = ("date", "time", "direction", "category", "amount", "note")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        labels = ("日期", "时间", "类型", "分类", "金额", "备注")
        widths = (105, 85, 80, 110, 100, 250)
        for column, label, width in zip(columns, labels, widths):
            self.tree.heading(column, text=label)
            self.tree.column(column, width=width, anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if account_names:
            self.refresh()
        else:
            self.info_text.set("暂无可管理的账户。")
            self.balance_entry.configure(state="disabled")

    def current_account_id(self):
        return self.accounts.get(self.account_combo.get())

    def refresh(self):
        account_id = self.current_account_id()
        account = next((row for row in self.store.choices("account", self.user)
                        if row.get("id") == account_id), None)
        if not account:
            return

        account_types = {row["id"]: row["name"]
                         for row in self.store.choices("account_type")}
        users = {row["id"]: row["name"] for row in self.store.choices("user")}
        self.info_text.set(
            f"名称：{account.get('name', '')}    "
            f"类型：{account_types.get(account.get('account_type_id'), '未知')}    "
            f"所有者：{users.get(account.get('user_id'), '默认')}    "
            f"当前余额：{float(account.get('balance', 0)):.2f}"
        )
        self.balance_entry.delete(0, "end")
        self.balance_entry.insert(0, f"{float(account.get('balance', 0)):.2f}")

        directions = {row["code"]: row["name"]
                      for row in self.store.choices("direction")}
        categories = {row["id"]: row["name"]
                      for row in self.store.choices("category")}
        rows = [row for row in self.store.transactions(self.user)
                if row.get("account_id") == account_id]
        rows.sort(key=lambda row: (row.get("date", ""), row.get("time", "")),
                  reverse=True)
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=(
                row.get("date", ""), row.get("time", ""),
                directions.get(row.get("direction_code"), "未知"),
                categories.get(row.get("category_id"), "未知"),
                row.get("amount", ""), row.get("note", ""),
            ))

    def adjust_balance(self):
        account_id = self.current_account_id()
        category_id = self.category_values.get(self.category_combo.get())
        try:
            new_balance = float(self.balance_entry.get().strip())
            if not math.isfinite(new_balance):
                raise ValueError("余额必须是有效的有限数字。")
            self.store.adjust_account_balance(
                account_id, new_balance, category_id, self.user)
        except (TypeError, ValueError) as error:
            messagebox.showerror("无法调整余额", str(error), parent=self)
            return
        self.refresh()
        self.on_change()
        messagebox.showinfo("调整成功", "账户余额已更新，并已生成对应交易。",
                            parent=self)


class MainFrame(ttk.Frame):
    def __init__(self, master, store, user, logout):
        super().__init__(master, padding=10)
        self.store, self.user, self.logout = store, user, logout
        self.name_to_id = {}
        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text=f"欢迎，{user['name']}", font=app_font(13, "bold")).pack(side="left")
        ttk.Button(top, text="退出登录", command=logout).pack(side="right")
        self.book = ttk.Notebook(self)
        self.book.pack(fill="both", expand=True)
        self.transaction_tab = ttk.Frame(self.book, padding=8)
        self.manage_tab = ttk.Frame(self.book, padding=8)
        self.stats_tab = ttk.Frame(self.book, padding=8)
        self.book.add(self.transaction_tab, text="交易明细")
        self.book.add(self.manage_tab, text="基础资料")
        self.book.add(self.stats_tab, text="统计")
        self.build_transactions()
        self.build_manage()
        self.build_stats()
        self.refresh()

    def build_transactions(self):
        bar = ttk.Frame(self.transaction_tab)
        bar.pack(fill="x", pady=(0, 8))

        filters = ttk.Frame(bar)
        filters.pack(fill="x")
        ttk.Label(filters, text="日期：").pack(side="left")
        self.keyword = ttk.Entry(filters, width=13)
        self.keyword.pack(side="left")
        self.keyword.bind("<KeyRelease>", lambda _event: self.refresh())

        self.filter_values = {}
        for key, label, data_name in (
            ("account", "账户：", "account"),
            ("direction", "收支类型：", "direction"),
            ("category", "分类：", "category"),
        ):
            names, mapping = self.option_data(data_name)
            self.filter_values[key] = mapping
            ttk.Label(filters, text=label).pack(side="left", padx=(10, 0))
            combo = ttk.Combobox(filters, state="readonly", width=11,
                                 values=("全部",) + names)
            combo.current(0)
            combo.pack(side="left")
            combo.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
            setattr(self, f"{key}_filter", combo)

        ttk.Button(filters, text="清空筛选", command=self.clear_filters).pack(side="left", padx=10)

        actions = ttk.Frame(bar)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="新增交易", command=self.add_transaction).pack(side="left")
        ttk.Button(actions, text="修改选中", command=self.edit_transaction).pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="删除选中", command=self.delete_transaction).pack(side="left", padx=8)
        ttk.Button(actions, text="刷新", command=self.refresh).pack(side="left")
        ttk.Label(actions, text="排序：").pack(side="left", padx=(15, 0))
        self.sort_key = ttk.Combobox(actions, state="readonly", width=12,
                                     values=("日期时间", "金额（高到低）", "创建时间"))
        self.sort_key.current(0)
        self.sort_key.pack(side="left")
        self.sort_key.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        columns = ("user", "date", "time", "direction", "category", "account", "amount", "note")
        self.tree = ttk.Treeview(self.transaction_tab, columns=columns, show="headings")
        labels = ("用户", "日期", "时间", "类型", "分类", "账户", "金额", "备注")
        widths = (90, 105, 85, 75, 100, 110, 100, 190)
        for column, label, width in zip(columns, labels, widths):
            self.tree.heading(column, text=label)
            self.tree.column(column, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", lambda _event: self.edit_transaction())

    def build_manage(self):
        ttk.Label(self.manage_tab, text="新增基础资料", font=app_font(14, "bold")).pack(pady=20)
        buttons = ttk.Frame(self.manage_tab)
        buttons.pack()
        for text, command in (("新增分类", self.add_category), ("新增账户", self.add_account),
                              ("账户管理", self.manage_accounts),
                              ("新增账户类型", self.add_account_type), ("新增用户", self.add_user)):
            ttk.Button(buttons, text=text, command=command, width=18).pack(side="left", padx=8)
        ttk.Label(self.manage_tab, text="提示：新增用户仅限管理员；所有数据保存在 d02/data。",
                  foreground="#666").pack(pady=25)

    def build_stats(self):
        self.stats_text = tk.StringVar()
        ttk.Label(self.stats_tab, textvariable=self.stats_text, font=app_font(15),
                  justify="left").pack(anchor="nw", padx=30, pady=30)

    def maps(self):
        return ({r["code"]: r["name"] for r in self.store.choices("direction")},
                {r["id"]: r["name"] for r in self.store.choices("category")},
                {r["id"]: r["name"] for r in self.store.choices("account")})

    def refresh(self):
        rows = self.store.transactions(self.user)
        keyword = self.keyword.get().strip()
        if keyword:
            rows = [r for r in rows if keyword in r.get("date", "")]
        for key, field in (("account", "account_id"), ("direction", "direction_code"),
                           ("category", "category_id")):
            selected = getattr(self, f"{key}_filter").get()
            if selected != "全部":
                selected_id = self.filter_values[key].get(selected)
                rows = [r for r in rows if r.get(field) == selected_id]
        sort = self.sort_key.get()
        if sort == "金额（高到低）":
            rows.sort(key=lambda r: float(r.get("amount", 0)), reverse=True)
        elif sort == "创建时间":
            rows.sort(key=lambda r: r.get("created_at", ""), reverse=True)
        else:
            rows.sort(key=lambda r: (r.get("date", ""), r.get("time", "")), reverse=True)
        directions, categories, accounts = self.maps()
        users = {r["id"]: r["name"] for r in self.store.choices("user")}
        self.tree.delete(*self.tree.get_children())
        for item in rows:
            self.tree.insert("", "end", iid=item["id"], values=(
                users.get(item.get("created_by"), "未知"),
                item.get("date"), item.get("time"),
                directions.get(item.get("direction_code"), "未知"),
                categories.get(item.get("category_id"), "未知"),
                accounts.get(item.get("account_id"), "未知"),
                item.get("amount"), item.get("note", "")))
        all_rows = self.store.transactions(self.user)
        amounts = [float(r.get("amount", 0)) for r in all_rows]
        income = sum(float(r.get("amount", 0)) for r in all_rows if r.get("direction_code") == "income")
        expense = sum(float(r.get("amount", 0)) for r in all_rows if r.get("direction_code") == "expense")
        self.stats_text.set(f"交易笔数：{len(all_rows)}\n\n总收入：{income:.2f}\n\n总支出：{expense:.2f}\n\n结余：{income-expense:.2f}\n\n"
                            f"最大金额：{max(amounts, default=0):.2f}\n\n平均金额：{sum(amounts)/len(amounts) if amounts else 0:.2f}")

    def clear_filters(self):
        self.keyword.delete(0, "end")
        for key in ("account", "direction", "category"):
            getattr(self, f"{key}_filter").current(0)
        self.refresh()

    def option_data(self, name):
        rows = self.store.choices(name, self.user)
        name_counts = {}
        for row in rows:
            name_counts[row["name"]] = name_counts.get(row["name"], 0) + 1
        users = {r["id"]: r["name"] for r in self.store.choices("user")}
        mapping = {}
        for row in rows:
            label = row["name"]
            if name_counts[label] > 1:
                owner = users.get(row.get("user_id"), "默认")
                label = f"{label}（{owner}）"
            mapping[label] = row.get("id", row.get("code"))
        return tuple(mapping), mapping

    def add_transaction(self):
        account_names, accounts = self.option_data("account")
        direction_names, directions = self.option_data("direction")
        category_names, categories = self.option_data("category")
        if not account_names or not category_names:
            messagebox.showwarning("缺少资料", "请先创建账户和分类。")
            return
        current = datetime.now(TZ)
        fields = (("date", "日期", "entry", (), current.strftime("%Y-%m-%d")),
                  ("time", "时间", "entry", (), current.strftime("%H:%M:%S")),
                  ("amount", "金额", "entry", (), ""), ("account", "账户", "combo", account_names, ""),
                  ("direction", "交易类型", "combo", direction_names, ""),
                  ("category", "分类", "combo", category_names, ""), ("note", "备注", "entry", (), ""))

        def submit(v):
            try:
                datetime.strptime(v["date"], "%Y-%m-%d")
                datetime.strptime(v["time"], "%H:%M:%S")
                if float(v["amount"]) < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("输入错误", "请检查日期、时间和非负金额。")
                return False
            self.store.add("transaction", {"date": v["date"], "time": v["time"], "amount": v["amount"],
                "account_id": accounts[v["account"]], "direction_code": directions[v["direction"]],
                "category_id": categories[v["category"]], "note": v["note"]}, self.user)
            self.refresh()
            return True
        FormDialog(self, "新增交易", fields, submit)

    def edit_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一条交易。")
            return
        transaction = self.store.transaction(selected[0])
        if not transaction:
            messagebox.showerror("错误", "该交易记录不存在或已被删除。")
            self.refresh()
            return
        if not is_root(self.user) and transaction.get("created_by") != self.user["id"]:
            messagebox.showerror("权限不足", "只能修改自己的交易记录。")
            return

        account_names, accounts = self.option_data("account")
        direction_names, directions = self.option_data("direction")
        category_names, categories = self.option_data("category")

        def selected_label(mapping, value):
            return next((label for label, item_id in mapping.items() if item_id == value), "")

        fields = (
            ("date", "日期", "entry", (), transaction.get("date", "")),
            ("time", "时间", "entry", (), transaction.get("time", "")),
            ("amount", "金额", "entry", (), str(transaction.get("amount", ""))),
            ("account", "账户", "combo", account_names,
             selected_label(accounts, transaction.get("account_id"))),
            ("direction", "交易类型", "combo", direction_names,
             selected_label(directions, transaction.get("direction_code"))),
            ("category", "分类", "combo", category_names,
             selected_label(categories, transaction.get("category_id"))),
            ("note", "备注", "entry", (), transaction.get("note", "")),
        )

        def submit(values):
            try:
                datetime.strptime(values["date"], "%Y-%m-%d")
                datetime.strptime(values["time"], "%H:%M:%S")
                if float(values["amount"]) < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("输入错误", "请检查日期、时间和非负金额。")
                return False
            updated = {
                "date": values["date"],
                "time": values["time"],
                "amount": values["amount"],
                "account_id": accounts[values["account"]],
                "direction_code": directions[values["direction"]],
                "category_id": categories[values["category"]],
                "note": values["note"],
            }
            if not self.store.update_transaction(transaction["id"], updated, self.user):
                messagebox.showerror("保存失败", "该交易记录不存在或已被删除。")
                return False
            self.refresh()
            return True

        FormDialog(self, "修改交易", fields, submit)

    def simple_add(self, data_name, title, extra_fields=()):
        fields = (("name", "名称", "entry", (), ""),) + extra_fields
        def submit(v):
            if not v["name"]:
                messagebox.showerror("输入错误", "名称不能为空。")
                return False
            if any(r.get("name") == v["name"] for r in self.store.choices(data_name)):
                messagebox.showerror("输入错误", "该名称已存在。")
                return False
            self.store.add(data_name, v, self.user)
            messagebox.showinfo("成功", f"{title}已保存。")
            return True
        FormDialog(self, title, fields, submit)

    def add_category(self):
        names, mapping = self.option_data("direction")
        fields = (("direction", "收支类型", "combo", names, ""),)
        def submit(v):
            if not v["name"]:
                messagebox.showerror("输入错误", "名称不能为空。")
                return False
            self.store.add("category", {"name": v["name"], "direction_code": mapping[v["direction"]]}, self.user)
            return True
        FormDialog(self, "新增分类", (("name", "名称", "entry", (), ""),) + fields, submit)

    def manage_accounts(self):
        account_names, accounts = self.option_data("account")
        category_names, categories = self.option_data("category")
        AccountManagerDialog(
            self, self.store, self.user, account_names, accounts,
            category_names, categories, self.refresh)

    def add_account(self):
        names, mapping = self.option_data("account_type")
        def submit(v):
            if not v["name"]:
                messagebox.showerror("输入错误", "名称不能为空。")
                return False
            self.store.add("account", {"name": v["name"], "account_type_id": mapping[v["type"]], "balance": 0}, self.user)
            return True
        FormDialog(self, "新增账户", (("name", "名称", "entry", (), ""),
            ("type", "账户类型", "combo", names, "")), submit)

    def add_account_type(self):
        self.simple_add("account_type", "新增账户类型")

    def add_user(self):
        if self.user.get("role_code") != "admin" and not is_root(self.user):
            messagebox.showerror("权限不足", "只有管理员可以新增用户。")
            return
        role_names, roles = self.option_data("role")
        def submit(v):
            if len(v["name"]) < 4 or len(v["password"]) < 8:
                messagebox.showerror("输入错误", "用户名至少 4 位，密码至少 8 位。")
                return False
            if any(u["name"] == v["name"] for u in self.store.choices("user")):
                messagebox.showerror("输入错误", "用户名已存在。")
                return False
            self.store.add("user", {"name": v["name"], "password": v["password"],
                           "role_code": roles[v["role"]]}, self.user)
            return True
        FormDialog(self, "新增用户", (("name", "用户名", "entry", (), ""),
            ("password", "密码", "password", (), ""), ("role", "角色", "combo", role_names, "")), submit)

    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一条交易。")
        elif messagebox.askyesno("确认删除", "确定删除选中的交易吗？"):
            self.store.delete_transaction(selected[0])
            self.refresh()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        chinese_font = configure_chinese_font(self)
        self.title("个人记账系统 - Tkinter")
        self.geometry("980x650")
        self.minsize(820, 520)
        self.store = Store()
        self.frame = None
        self.show_login()
        if not chinese_font:
            self.after_idle(lambda: messagebox.showwarning(
                "缺少中文字体",
                "系统中没有检测到可用的中文字体，文字可能显示为方块。\n\n"
                "Windows 请安装或启用“微软雅黑”；Linux 请安装 fonts-noto-cjk 后重启程序。",
            ))

    def swap(self, frame):
        if self.frame:
            self.frame.destroy()
        self.frame = frame
        self.frame.pack(fill="both", expand=True)

    def show_login(self):
        self.swap(LoginFrame(self, self.try_login))

    def try_login(self, username, password):
        user = self.store.login(username, password)
        if not user:
            messagebox.showerror("登录失败", "用户名或密码错误。")
            return
        self.swap(MainFrame(self, self.store, user, self.show_login))


def main():
    Application().mainloop()


if __name__ == "__main__":
    main()
