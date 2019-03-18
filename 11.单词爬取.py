import urllib.request
import re
import random
import math
import threading
def wordCrawler(url):
    #获取爬取网页信息
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    req = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(req)
    HTML = response.read().decode('utf-8')
    return HTML
def getInfo(HTML):
    #设置正则，匹配所需内容
    pattern = r'<p><span id="src(.*?)<a class="sp dictvoice voice-js log-js"'
    re_info = re.compile(pattern,re.S)
    infoList = re_info.findall(HTML)
    return infoList

def getWord(infoList):
    #返回单词列表
    pat = r'<span>(.*?)</span>'
    re_word = re.compile(pat,re.S)
    wordlist = []
    listterm = []
    for i in range(len(infoList)):
        strTerm = infoList[i].replace(r')">',r'<span>')
        listterm = re_word.findall(strTerm)
        wordlist.append(listterm)
    return wordlist
def getSentence(wordList):
    #单词拼接成句
    strl3 = ''
    listAll=[]
    for i in range(len(wordList)):
        list1 = wordList[i]
        strl = " ".join(list1)
        list2 = strl.split(' ')
        num = list2.count('')
        for t in range(num):
            list2.remove('')
        strl2 = ' '.join(list2)
        strl2 += '\n'
        listAll.append(strl2)
    return listAll

def writeToFile(listAll,path,n):
    path = 'sentence'+str(n)+'.txt'
    with open(path,'w') as f2:
        for i in range(len(listAll)):
            info = listAll[i] #获取存储字符串
            pat = r'<b>(.*?)</b>'
            re_word = re.compile(pat, re.S)
            word = re_word.findall(info) #单词
            url = 'http://dict.youdao.com/w/' + word[0].replace(' ', '') + '/#keyfrom=dict2.top'
            astart = '<a href="'+url+'"><b>'
            aend = '</b></a>'
            info2 = info.replace('<b>',astart)
            info2 = info2.replace('</b>',aend)
            info2 += '</br></br>'
            f2.write(info2)



def run(n):

    listAll = []
    path = 'sentence.txt'

    with open('2501-5000.txt', 'r') as f:
        data = f.readline(n)
        data = f.readline()
        num = n
        listOne = []
        while data:
            num += 1
            print(num)
            url = 'http://dict.youdao.com/w/' + data.replace('\n', '') + '/#keyfrom=dict2.top'
            HTML = wordCrawler(url)
            infoList = getInfo(HTML)
            wordList = getWord(infoList)
            listOne = getSentence(wordList)  # 存储句子
            listAll += listOne
            data = f.readline()
            if int(math.fmod(num, 200)) == 0 or num==2500:
                random.shuffle(listAll)
                writeToFile(listAll, path, n)

                '''
                lock = threading.Lock()
                lock.acquire()
                try:
                    writeToFile(listAll, path,n)
                finally:
                    lock.release()
                    break
                '''
                listAll = []
                break

if __name__ == '__main__':


    t1 = threading.Thread(target=run,args=(200,))
    t1.start()
    t2 = threading.Thread(target=run, args=(4000,))
    t2.start()
    t3 = threading.Thread(target=run, args=(600,))
    t3.start()
    t4 = threading.Thread(target=run, args=(800,))
    t4.start()
    t5 = threading.Thread(target=run, args=(1000,))
    t5.start()
    run(0)
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print("OK")

