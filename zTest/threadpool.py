import time
from concurrent.futures import ThreadPoolExecutor  # 导入线程池模块

thread_pool = ThreadPoolExecutor(5)  # 设置线程池大小


def main(num):
    return f"这是第 {num}"


def start():
    for num in range(10000):
        thread_object = thread_pool.submit(main, num)  # 参数为要执行的函数和所传参数
        thread_object.add_done_callback(parse)  # 把线程结果传递给parse函数


def parse(obj):
    print(obj.result())  # 通过result方法获取值


if __name__ == '__main__':
    now = time.time()
    start()
    print(f"总共耗时: {time.time() - now}")