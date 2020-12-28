from datetime import datetime


def show_cashfloww(month):
    """収支を表示する

    :param month: 収支を表示する年月
    """
    pass

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

    with open("data.tsv", "a") as f:
        f.write(row)

def show_cmd():
    print("# 使い方")
    print("1: 支出を記録する")
    print("2: 収入を記録する")
    print("3: 収支を確認する")
    print("q: アプリを終了する")
    print("")

def main():
    show_cmd()
    while True:
        cmd = input("コマンドを入力して下さい > ")
        if cmd == "1":
            show_input_form(True)
        elif cmd == "2":
            show_input_form(False)
        elif cmd == "3":
            print("収支")
        elif cmd == "q":
            print("アプリを終了します")
            break
        elif cmd == "h":
            print("アプリを終了します")
        else:
            print("不明なコマンドです")

if __name__ == "__main__":
    main()
