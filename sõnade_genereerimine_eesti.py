from urllib.request import urlopen
import random 
import re

veebiaadress = "https://www.cl.ut.ee/ressursid/sagedused/tabel1.txt"

urlfail = urlopen(veebiaadress)
urlbaidid = urlfail.read()
tekst = urlbaidid.decode()
urlfail.close()

sõnad = re.findall(r'^\w+', tekst, re.MULTILINE)


if sõnad:

    suvaline_indeks = random.randint(0, len(sõnad) - 1)
    suvaline_sõna = sõnad[suvaline_indeks]
    print(suvaline_sõna)