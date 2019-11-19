import requests
from pyquery import PyQuery as qp
from urllib.parse import urlencode

#此代码用于使用代理池获取搜狗微信的信息，当前版本还没实现把信息写入mongodb上
#使用此代码需要先开启代理池
cookies = """CXID=F53AAB2F5A898B85542F347222C4D576; SUID=F643EF783965860A5CDF6A0C000AC6E2; SUV=00573C6DDF493DF55CF38C209E5B6446; ABTEST=3|1562604342|v1; IPLOC=CN4401; weixinIndexVisited=1; ad=dkllllllll2tTLoGlllllV1XVRDlllllWndRdkllll9llllljCxlw@@@@@@@@@@@; sct=4; JSESSIONID=aaaqjW8zVSduuaVj9clRw; ppinf=5|1563034576|1564244176|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTYlOTklQkElRTglQjElQUF8Y3J0OjEwOjE1NjMwMzQ1NzZ8cmVmbmljazoxODolRTYlOTklQkElRTglQjElQUF8dXNlcmlkOjQ0Om85dDJsdU5xZ01NMGZIUkJsWVBHZkVHem56a3NAd2VpeGluLnNvaHUuY29tfA; pprdig=IixwMvsJkLRA4jJjzh_MeeSn7BQDZBCapdHjxHbkd9mvsybeSWfet3G7lFjA3hiGXTABxkZy5NuCfyEXqXNiBVjRg5UzRPel6DK1MbKeqViZzT6vfkZ59F-FHyOco7H-wRvEjn2MUHLc879JtQp3L2sEKE45U3wfEt7vsKkEBNs; sgid=26-36434075-AV0qA9DficQW9fslHldfRfro; ppmdig=15630402420000005d2e3758cbfc7919073832b653d5ca8f; PHPSESSID=bcbred32i76dci9utc6fj4k471; SNUID=DC61CC5B2327AFB1F340C3F32300B80B; seccodeRight=success; successCount=1|Sat, 13 Jul 2019 18:06:37 GMT"""
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie': cookies
}

proxies={}
#获取网页信息的方法，当被禁ip后，在选用代理池中别的ip进行爬取
def get_html(url,limit=8):
    global proxies
    print("使用的proxies是",proxies)
    try:
        count = 0
        r = requests.get(url,headers=header,allow_redirects=False,proxies=proxies)
        r.encoding = r.apparent_encoding
        if r.status_code == 200:
            return r.text
        elif r.status_code == 302:
            print("状态是302")
            if count <= limit:
                print("到判断次数了")
                proxy = get_proxy()
                proxies = {'http':'http://'+proxy}
                return get_html(url)
        else:
            print("返回的异常状态码是:",r.status_code)
    except:
        print("获取网页失败")


#获取搜狗微信索引页的方法
def get_index(KEYWORDS,PAGE):
    print("页数是:",PAGE)
    data = {
            'query': KEYWORDS,
            'type': 2,
            'page': PAGE
    }
    param = urlencode(data)
    url = "https://weixin.sogou.com/weixin?"+param
    print("url",url)
    html = get_html(url)
    return html

#获取代理池
def get_proxy():
    proxy = requests.get('http://127.0.0.1:5555/random').text
    print("获取的proxy:",proxy)
    return proxy
#解析索引页
def parse_index(html):
    doc = qp(html)
    items = doc('.news-box .news-list .txt-box h3 a').items()
    print("items")
    for item in items:
        yield item.attr('data-share')


def get_detail():
    pass

def parse_detail():
    pass

def save_to_mongo():
    pass

def main():
    start = 1
    stop = 100

    for i in range(start,stop):
        html = get_index('工作',i)
        results = parse_index(html)
        for result in results:
            print(result)



if __name__ == '__main__':

    main()
