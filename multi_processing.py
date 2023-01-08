from multiprocessing import Process, cpu_count

import urllib3
from bs4 import BeautifulSoup, SoupStrainer

print("Number of cpu : ", cpu_count())


head = {
    "User-Agent": "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
    "X-Requested-With": "XMLHttpRequest"
}
url = "https://yorumbudur.com"


with open('/Users/ma/Desktop/pythons/tez_inaremie/blm5105/urunlinkleri.txt') as f:
    urunlinkleri = list(f)
print("urunlinkleri length: ", str(len(urunlinkleri)))


def splitList(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


listOfUrunLinkleri = list(splitList(urunlinkleri, 50))
print("listOfUrunLinkleri length: ", str(len(listOfUrunLinkleri)))


def yorumLinkleriniAl(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url, headers=head)
    parse_only = SoupStrainer('a')
    html = BeautifulSoup(r.data, 'html.parser', parse_only=parse_only)
    baglar = set()
    for s in html.contents:
        bag = s.get('href')
        if bag is None:
            continue
        if (len(bag) > 4 and bag.startswith('/yorumlar/')):
            baglar.add(bag)
    return baglar


def urunListesiYorumLinkleriniAl(urunListesi, processNo):
    yorumLinkleri = set()
    sira = 0
    for urunLinki in urunListesi:
        urunLinki = urunLinki.strip(' \t\n\r')
        sira += 1
        print("processNo: ", processNo, "sira: ",
              sira, "urunLinki: ", urunLinki)
        basl = yorumLinkleriniAl(url + urunLinki)
        for bb in basl:
            yorumLinkleri.add(bb)

    with open('/Users/ma/Desktop/pythons/tez_inaremie/blm5105/process_' + str(processNo) + '_yorumlinkleri.txt', 'a') as the_file:
        for tl in yorumLinkleri:
            the_file.write(tl + '\n')


if __name__ == '__main__':
    processes = []
    for i in range(len(listOfUrunLinkleri)):
        p = Process(target=urunListesiYorumLinkleriniAl,
                    args=(listOfUrunLinkleri[i], i))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print("Done")
