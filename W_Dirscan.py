import requests
import queue
import threading
import optparse
import time

q = queue.Queue()

class WDirScan(object):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    }

    def __init__(self, url, output):
        self.url = url
        self.output = output


    def scanning(self):

        while not q.empty():

            dir = q.get()
            urls = self.url + dir
            urls = urls.replace("\n", "")
            response = requests.get(urls, headers = WDirScan.headers)
            response.encoding = "utf-8"
            res_code = response.status_code
            if res_code == 200:

                if not "页面不存在" in response.text:
                    print("[+]%s%s%d" % (urls, "-" * 50, res_code))
                    # print("%s%s%s" % (urls, "-" * 50, res_code))
                    output = open(self.output, "a+")
                    output.write(urls + "\n")
                    output.close()
            else:
                print("[-]%s%s%d" % (urls, "-" * 50, res_code))


def main():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="urls", help="以http或https开头的url")
    parser.add_option("-d", "--dict", dest="dict_name", default="dict.txt", help="不指定字典则使用默认字典")
    parser.add_option("-t", "--thread", dest="thread", default=10, help="不指定线程数则默认使用10线程")
    parser.add_option("-o", "--output", dest="output", default="1.txt", help="导出文件名,如xx.txt,不指定则默认使用1.txt作为文件名")
    (options, args) = parser.parse_args()
    url = options.urls
    dict_name = options.dict_name
    thread = options.thread
    output = options.output
    # print(url, dict_name, thread, output)
    w_dirscan = WDirScan(url, output)
    print("[*]扫描程序开始，目标Url：%s" % url)
    for dir in open(dict_name, "r"):
        q.put(dir)
    for i in range(int(thread)):
        t = threading.Thread(target=w_dirscan.scanning)
        t.start()
        t.join()
    print("扫描结果已保存于：%s" % output)
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("总耗时：%0.2f" % (end - start))
