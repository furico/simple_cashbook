from pathlib import Path
from datetime import datetime, timedelta


DATA_FILE = Path("data.tsv")


def show_cashflow(year, month):
    """収支を表示する

    :param month: 収支を表示する年月
    """
    if not DATA_FILE.exists():
        return

    rows = []
    income = 0
    payment = 0
    with open(DATA_FILE) as f:
        for row in f:
            row = row.strip()
            cols = row.split("\t")
            cf_year, cf_month, cf_day = int(cols[0]), int(cols[1]), int(cols[2])
            if cf_year == year and cf_month == month:
                rows.append({
                    "cf_date": datetime(cf_year, cf_month, cf_day),
                    "note": cols[3],
                    "amount": int(cols[4]),
                })

    month_first = datetime(year, month, 1)
    if month == 12:
        month_last = datetime(year, month, 31)
    else:
        month_last = datetime(year, month + 1, 1) - timedelta(days=1)

    print(f"### {month_first:%Y/%m/%d} - {month_last:%Y/%m/%d} の収支明細 ###")
    print()

    for row in rows:
        print(f"{row['cf_date']:%m/%d(%b)}\t{row['note']}\t{row['amount']}")
        if row["amount"] >= 0:
            income += row["amount"]
        else:
            payment += row["amount"]

    print()
    print("(収入) - (支出) = (収支)")
    print(f"{income} - {-payment} = {income + payment}")
    print()


def show_input_form(is_payment):
    """収支の入力フォームを表示する

    :param is_payment: 支出フラグ
    """
    if is_payment:
        print("支出を記録します")
    else:
        print("収入を記録します")

    # 日付を入力
    cf_date = input("日付 > ")
    try:
        cf_date = datetime.strptime(cf_date, "%Y/%m/%d")
    except ValueError as e:
        print("入力された日付が不正です")
        print("")
        return

    # 内容を入力
    note = input("内容 > ")

    # 金額を入力
    amount = input("金額 > ")
    try:
        amount = int(amount)
    except ValueError as e:
        print("入力された金額が不正です")
        print("")
        return

    # 支出の場合は金額をマイナスにする
    if is_payment:
        amount = amount * -1

    add_cashflow(cf_date, note, amount)

def input_month():
    """年月を入力する"""
    print("収支明細を表示する年月を入力して下さい(例: 2021/1)")
    year_month  = input("年月 > ")
    year_month = datetime.strptime(year_month, "%Y/%m")
    return year_month.year, year_month.month


def add_cashflow(cf_date, note, amount):
    """収支を記録する

    :param cf_date: 収支のあった日付
    :param cf_date: 収支の内容
    :param amount: 収支の金額
    """
    row = "\t".join([
        str(cf_date.year),
        str(cf_date.month),
        str(cf_date.day),
        note,
        str(amount),
    ]) + "\n"

    with open(DATA_FILE, "a") as f:
        f.write(row)

def show_cmd():
    print("# 使い方")
    print("1: 支出を記録する")
    print("2: 収入を記録する")
    print("3: 収支を確認する")
    print("q: アプリを終了する")
    print("")


def main():
    today = datetime.today()
    while True:
        show_cashflow(today.year, today.month)
        show_cmd()
        cmd = input("コマンドを入力して下さい > ")
        if cmd == "1":
            show_input_form(True)
        elif cmd == "2":
            show_input_form(False)
        elif cmd == "3":
            year, month = input_month()
            show_cashflow(year, month)
        elif cmd == "q":
            print("アプリを終了します")
            break
        else:
            print("不明なコマンドです")

if __name__ == "__main__":
    main()
