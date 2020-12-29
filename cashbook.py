"""
シンプルなおこづかい帳アプリ
"""
from pathlib import Path
from datetime import datetime, timedelta


DATA_FILE = Path("data.tsv")


def read_data_file(year, month):
    """データファイルから年月で指定したデータ読み込む"""
    rows = []

    if not DATA_FILE.exists():
        return rows

    with DATA_FILE.open() as f:
        for row in f:
            # 末尾の改行を除去
            row = row.strip()
            cols = row.split("\t")
            cf_year, cf_month, cf_day = int(cols[0]), int(cols[1]), int(cols[2])
            if cf_year != year or cf_month != month:
                continue
            rows.append(
                {
                    "cf_date": datetime(cf_year, cf_month, cf_day),
                    "note": cols[3],
                    "amount": int(cols[4]),
                }
            )
    return rows


def get_last_date(year, month):
    """指定した年月の月末日を取得する"""
    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) - timedelta(days=1)
    return last_date


def show_cashflow(year, month):
    """収支明細を表示する"""
    first_date = datetime(year, month, 1)
    last_date = get_last_date(year, month)

    print(f"### {first_date:%Y/%m/%d} - {last_date:%Y/%m/%d} の収支明細 ###")
    print()

    # 収入の合計
    income = 0
    # 支出の合計
    payment = 0
    # 指定した年月のデータ
    rows = read_data_file(year, month)
    for row in rows:
        print(f"{row['cf_date']:%m/%d(%a)}\t{row['note']}\t{row['amount']}")
        if row["amount"] >= 0:
            income += row["amount"]
        else:
            payment += row["amount"]

    print()
    print("(収入) - (支出) = (収支)")
    print(f"{income} - {-payment} = {income + payment}")
    print()


def show_current_cashflow():
    """現在の月の収支明細を表示する"""
    today = datetime.today()
    show_cashflow(today.year, today.month)


def input_cashflow(is_payment):
    """収支を入力する"""
    if is_payment:
        print("支出を記録します")
    else:
        print("収入を記録します")

    # 日付を入力
    cf_date = input("日付 > ")
    try:
        cf_date = datetime.strptime(cf_date, "%Y/%m/%d")
    except ValueError:
        print("入力された日付が不正です")
        print("")
        return

    # 内容を入力
    note = input("内容 > ")

    # 金額を入力
    amount = input("金額 > ")
    try:
        amount = int(amount)
    except ValueError:
        print("入力された金額が不正です")
        print("")
        return

    # 支出の場合は金額をマイナスにする
    if is_payment:
        amount = amount * -1

    # 収支を記録
    add_cashflow(cf_date, note, amount)
    # 現在の月の収支明細を表示する
    show_current_cashflow()


def input_show_month():
    """指定した年月の収支明細を表示する"""
    print("収支明細を表示する年月を入力して下さい(例: 2021/1)")
    year_month = input("年月 > ")
    try:
        year_month = datetime.strptime(year_month, "%Y/%m")
    except ValueError:
        print("入力された年月が不正です")
        print("")
        return
    show_cashflow(year_month.year, year_month.month)


def add_cashflow(cf_date, note, amount):
    """収支を記録する"""
    row = (
        "\t".join(
            [
                str(cf_date.year),
                str(cf_date.month),
                str(cf_date.day),
                note,
                str(amount),
            ]
        )
        + "\n"
    )

    with DATA_FILE.open("a") as f:
        f.write(row)


def show_cmd():
    """使い方を表示する"""
    print("# 使い方")
    print("1: 支出を記録する")
    print("2: 収入を記録する")
    print("3: 収支を確認する")
    print("q: アプリを終了する")
    print("")


def main():
    show_current_cashflow()
    while True:
        show_cmd()
        cmd = input("コマンドを入力して下さい > ")
        if cmd == "1":
            input_cashflow(True)
        elif cmd == "2":
            input_cashflow(False)
        elif cmd == "3":
            input_show_month()
        elif cmd == "q":
            print("アプリを終了します")
            break
        else:
            print("不明なコマンドです")


if __name__ == "__main__":
    main()
