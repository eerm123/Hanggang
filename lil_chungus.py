import pygame
import sys
from urllib.request import urlopen
import random 
import re
import time

#Algseadistus
pygame.init()
LAIUS, KÕRGUS = 800, 600
MUST = (0, 0, 0)
VALGE = (255, 255, 255)
PEALKIRI = "Hängmän"

#Lisatud Hängmäni pildid
hangman_pildid = [
    pygame.image.load("hängmän1.png"),
    pygame.image.load("hängmän2.png"),
    pygame.image.load("hängmän3.png"),
    pygame.image.load("hängmän4.png"),
    pygame.image.load("hängmän5.png"),
    pygame.image.load("hängmän6.png"),
    pygame.image.load("hängmän7.png"),
    pygame.image.load("hängmän8.png"),
]

#Loon Pygamei akna
aken = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption(PEALKIRI)

vigu = 7
alusta_mäng = False
hovered_choice = None  #Valin menüüvalikule hiirega liikumise jälgimise

#Menüü tekstid ja nende asukohad ekraani peal
tekstid = [
    {"tekst": "Yo yo wälcome tu the gaem!", "x": 50, "y": 50},
    {"tekst": "Valige üks võimalus:", "x": 50, "y": 90},
    {"tekst": "Alusta Hängmäni mängu", "x": 50, "y": 170},
    {"tekst": "Hängman tupsu all", "x": 50, "y": 220},
    {"tekst": "Välju", "x": 50, "y": 250},
]
menüü_font = pygame.font.Font(None, 36)
teksti_värv = VALGE

#Funktsioon menüüvaliku hoveri jälgimiseks
def kas_valik_hover(x, y, valik_laius, valik_kõrgus):
    global hovered_choice
    hiire_x, hiire_y = pygame.mouse.get_pos()
    print("Hiir: x =", hiire_x, "y =", hiire_y)

    if x < hiire_x < x + valik_laius and y < hiire_y < y + valik_kõrgus:
        return True
    return False

#Suvalise sõna genereerimine äraarvamiseks
def suvaline_sõna():
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

#Main menüü tsükkel
menüü_jookseb = True
while menüü_jookseb:
    for sündmus in pygame.event.get():
        if sündmus.type == pygame.QUIT:
            menüü_jookseb = False
            pygame.quit()
            sys.exit()
    
    for i, tekst_info in enumerate(tekstid[2:]):
        x, y, valiktekst = tekst_info["x"], tekst_info["y"], tekst_info["tekst"]
        valik_laius, valik_kõrgus = 200, 40
        if kas_valik_hover(x, y, valik_laius, valik_kõrgus):
            hovered_choice = valiktekst
            if i == 0:
                tekstid[2]["tekst"] = "Alusta Hängmäni mängu"
            else:
                tekstid[2]["tekst"] = "Alusta Hängmäni mängu"
        else:
            if hovered_choice == valiktekst:
                hovered_choice = None
                tekstid[2]["tekst"] = "Alusta Hängmäni mängu"

        if sündmus.type == pygame.MOUSEBUTTONDOWN and sündmus.button == 1:
            if kas_valik_hover(x, y, valik_laius, valik_kõrgus):
                valiktekst = tekst_info["tekst"]
                if valiktekst == "Alusta Hängmäni mängu":
                    alusta_mäng = True
                    menüü_jookseb = False
                    valiku_näitaja = 0
                elif valiktekst == "Hängman tupsu all":
                    alusta_mäng = True
                    menüü_jookseb = False
                    valiku_näitaja = 1
                elif valiktekst == "Välju":
                    menüü_jookseb = False
                    pygame.quit()


    #Kui mäng pole veel alustatud, siis kuva menüüd
    if not alusta_mäng:
        aken.fill(MUST)

        for tekst_info in tekstid:
            tekst = menüü_font.render(tekst_info["tekst"], True, teksti_värv)
            aken.blit(tekst, (tekst_info["x"], tekst_info["y"]))

        #Valitud menüüvaliku hoveri näitamine
        if hovered_choice:
            hover_x, hover_y = 200, 440
            tekst = menüü_font.render("Valitud: " + hovered_choice, True, VALGE)
            aken.blit(tekst, (hover_x, hover_y))



    #Kui mängu käima paned, siis kuvab algus pilti
    if alusta_mäng:
        aken.fill(VALGE)
        aken.blit(hangman_pildid[vigu], (65, 50))
        
    pygame.display.update()

    #Kui mängu käima paned ja valisid hängman tupsu all, läheb mängul taimer käima
    if alusta_mäng and valiku_näitaja == 1:
        aken.fill(VALGE)
        aken.blit(hangman_pildid[vigu], (65, 50))

        countdown_duration = 10

        for i in range(countdown_duration, 0, -1):
            print(i)
            time.sleep(1)

        print("Aeg sai otsa!")
        mängu_jookseb = False
        pygame.quit()
        sys.exit()
    pygame.display.update()




#Põhimängu tsükkel
mängu_jookseb = True
while mängu_jookseb:
    for sündmus in pygame.event.get():
        if sündmus.type == pygame.QUIT:
            mängu_jookseb = False
            pygame.quit()
            sys.exit()

    #Koodi lisamine, et haldada mängu loogikat
    "..... enter something cool"


    pygame.display.update()
