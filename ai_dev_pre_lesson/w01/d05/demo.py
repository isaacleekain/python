import json

q13
func_b()
没有
没有
"caught"

q14
0

q15
"invalid score"

q16
"A"

q17
"A"
"C"
"D"
"E"

q18
KeyError
不会
不会
不会

q19
try最好放到函数外
文件读取错误应该抓 FileNotFoundError
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
try:
    data = load_data(path)
except FileNotFoundError:
    print("FileNotFoundError")
except json.JSONDecodeError:
    print("JSONDecodeError")
    
q20
A -> main 没文件可以直接停止处理
B -> main 数据损坏可以直接停止处理
C -> process_students 坏数据跳过，需要在循环中的except中continue
D -> process_students 坏数据跳过，需要在循环中的except中continue
E -> process_students 坏数据跳过，需要在循环中的except中continue

q21
第一种，因为score先判断类型能否转换为int，有问题先跳出，可以执行下一步
如果是第二种，score=int(score)没有捕获错误，会直接报错停止处理
