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
KOLLANE = (255, 255, 0)
PEALKIRI = "Hängmän"

pygame.mixer.music.load("DokiMusic.mp3")
pygame.mixer.music.set_volume(0.5)

taustapilt_menüü = pygame.image.load("hangman_menüü.png")
taustapilt_menüü = pygame.transform.scale(taustapilt_menüü, (LAIUS, KÕRGUS))
taustapilt_mäng = pygame.image.load("Doki.png")
taustapilt_mäng = pygame.transform.scale(taustapilt_mäng, (LAIUS,KÕRGUS))

menüü_reziim = True

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

#Loon Pygame'i akna
aken = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption(PEALKIRI)

pygame.mixer.music.play(-1)

vigu = 0
alusta_mäng = False
hovered_choice = None  #Valin menüüvalikule hiirega liikumise jälgimise

#Menüü tekstid ja nende asukohad ekraani peal
tekstid = [
    {"tekst": "Tere tulemast Hanggangi!", "x": 50, "y": 50},
    {"tekst": "Valige üks võimalus:", "x": 50, "y": 140},
    {"tekst": "Alusta Hängmäni mängu", "x": 50, "y": 200},
    {"tekst": "Hängman blitz (2min)", "x": 50, "y": 250},
    {"tekst": "Välju", "x": 50, "y": 300},
]
menüü_font = pygame.font.Font(None, 36)
teksti_värv = KOLLANE

#Funktsioon menüüvaliku hoveri jälgimiseks
def kas_valik_hover(x, y, valik_laius, valik_kõrgus):
    global hovered_choice
    hiire_x, hiire_y = pygame.mouse.get_pos()
    print("Hiir: x =", hiire_x, "y =", hiire_y)

    if x < hiire_x < x + valik_laius and y < hiire_y < y + valik_kõrgus:
        return True
    return False

#Funktsioon uue suvalise sõna saamiseks
def saa_suvaline_sõna():
    veebiaadress = "https://www.cl.ut.ee/ressursid/sagedused/tabel1.txt"
    urlfail = urlopen(veebiaadress)
    urlbaidid = urlfail.read()
    tekst = urlbaidid.decode()
    urlfail.close()

    sõnad = re.findall(r'^\w+', tekst, re.MULTILINE)

    sobivad_sõnad = [sõna.upper() for sõna in sõnad if len(sõna) > 2]
    
    if sõnad:
        suvaline_indeks = random.randint(0, len(sõnad) - 1)
        suvaline_sõna = sobivad_sõnad[suvaline_indeks]
        return suvaline_sõna
    else:
        print("Ei leitud sobivaid sõnu")
        return ""

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
                    suvaline_sõna = saa_suvaline_sõna().upper()
                    mängusõna = list(suvaline_sõna)  #Konverteerib sõna suurteks tähtedeks
                    varjatud_sõna = ["_" if tähemärk.isalpha() else tähemärk for tähemärk in mängusõna]
                    print("Varjatud sõna:", varjatud_sõna)
                    menüü_jookseb = False
                    valiku_näitaja = 0
                elif valiktekst == "Hängman blitz":
                    alusta_mäng = True
                    suvaline_sõna = saa_suvaline_sõna().upper()
                    mängusõna = list(suvaline_sõna)  #Konverteerib sõna suurteks tähtedeks
                    varjatud_sõna = ["_" if tähemärk.isalpha() else tähemärk for tähemärk in mängusõna]
                    print("Varjatud sõna:", varjatud_sõna)
                    menüü_jookseb = False
                    valiku_näitaja = 1
                elif valiktekst == "Välju":
                    menüü_jookseb = False
                    pygame.quit()

    #Kui mäng pole veel alustatud, siis kuva menüüd
    if not alusta_mäng:
        aken.blit(taustapilt_menüü, (0, 0))
        for tekst_info in tekstid:
            tekst = menüü_font.render(tekst_info["tekst"], True, teksti_värv)
            aken.blit(tekst, (tekst_info["x"], tekst_info["y"]))

        #Valitud menüüvaliku hoveri näitamine
        if hovered_choice:
            hover_x, hover_y = 200, 440
            tekst = menüü_font.render("Valitud: " + hovered_choice, True, VALGE)
            aken.blit(tekst, (hover_x, hover_y))

    # Kui mängu käima paned, siis kuvab alguspilti
    if alusta_mäng:
        aken.fill((20,20,20))
        aken.blit(hangman_pildid[vigu], (65, 50))

    pygame.display.update()

#Täiendatud varjatud sõna loomine, kõik tähed nähtavad
varjatud_sõna = list("_" * len(suvaline_sõna))

#Kõik tähed nähtavad
kõik_tähed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖÕ")

#Siin näita kaotus ekraani kus kuvab viimast pilti
mängija_kaotas_tekst = "Mängija kaotas! Õige sõna oli: " + suvaline_sõna
mängija_kaotas_render = menüü_font.render(mängija_kaotas_tekst, True, VALGE)
mängija_kaotas_varjund = menüü_font.render(mängija_kaotas_tekst, True, MUST)

teksti_rect = mängija_kaotas_render.get_rect(topleft=(65, 300))
varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)
mängu_kestus = 120
algus_aeg = pygame.time.get_ticks()

#Põhimängu tsükkel
mängu_jookseb = True
while mängu_jookseb:
    for sündmus in pygame.event.get():
        if sündmus.type == pygame.QUIT:
            mängu_jookseb = False
            pygame.quit()
            sys.exit()

        #Koodi lisamine, et haldada mängu loogikat
        if alusta_mäng and valiku_näitaja == 0:
            taustapilt = taustapilt_mäng
            menüü_reziim = False

            arvatud_tähed = set()
            if sündmus.type == pygame.KEYDOWN:
                if sündmus.unicode.isalpha():  #Kontrollib, kas sisestatud sümbol on täht
                    arvatud_täht = sündmus.unicode.upper()
                    if arvatud_täht in kõik_tähed:
                        kõik_tähed.remove(arvatud_täht)  ##Eemalda täht valikust
                        if arvatud_täht in suvaline_sõna:
                            #Õige tähe arvamine, vaheta varjatud sõna vastavalt
                            for i, täht in enumerate(suvaline_sõna):
                                if täht == arvatud_täht:
                                    varjatud_sõna[i] = arvatud_täht
                            print("Õige täht:", arvatud_täht)
                        else:
                            vigu += 1
                            print("Vale täht:", arvatud_täht)
                            if vigu == 7:
                                #Mängija kaotas
                                aken.fill((20, 20, 20))
                                aken.blit(hangman_pildid[vigu], (65, 50))
                                aken.blit(mängija_kaotas_varjund, varjundi_rect.topleft)
                                aken.blit(mängija_kaotas_render, teksti_rect.topleft)
                                pygame.display.update()
                                pygame.time.delay(5000)  #Ootab 5000 ms (5 sekundit)
                                pygame.quit()
                                sys.exit()

            if not menüü_reziim:
                aken.blit(taustapilt, (0, 0))

                aken.blit(hangman_pildid[vigu], (65, 50))

                #Kuvab varjatud sõna
                varjatud_tekst = " ".join(varjatud_sõna)
                varjatud_tekst_render = menüü_font.render(varjatud_tekst, True, VALGE)
                varjatud_tekst_varjund = menüü_font.render(varjatud_tekst, True, MUST)

                teksti_rect = varjatud_tekst_render.get_rect(topleft=(65, 420))
                varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)

                aken.blit(varjatud_tekst_varjund, varjundi_rect.topleft)
                aken.blit(varjatud_tekst_render, teksti_rect.topleft)

                #Kuvab arvatud tähed
                arvatud_tähed_render = menüü_font.render("Arvatud tähed: " + ", ".join(set(arvatud_tähed)), True, VALGE)
                arvatud_tähed_varjund = menüü_font.render("Arvatud tähed: " + ", ".join(set(arvatud_tähed)), True, MUST)

                teksti_rect = arvatud_tähed_render.get_rect(topleft=(65, 460))
                varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)

                aken.blit(arvatud_tähed_varjund, varjundi_rect.topleft)
                aken.blit(arvatud_tähed_render, teksti_rect.topleft)

                #Kuvab tähti, mida peab arvama
                valikus_olevad_tähed = ", ".join(kõik_tähed)
                peab_arvama_render = menüü_font.render("Valikus olevad tähed: " + valikus_olevad_tähed, True, VALGE)
                peab_arvama_varjund = menüü_font.render("Valikus olevad tähed: " + valikus_olevad_tähed, True, MUST)

                if peab_arvama_render.get_width() > LAIUS:
                    #Vähendab teksti suurust, et see mahuks ekraanile
                    uus_font = pygame.font.Font(None, 22)
                    peab_arvama_render = uus_font.render("Valikus olevad tähed: " + valikus_olevad_tähed, True, VALGE)
                    peab_arvama_varjund = uus_font.render("Valikus olevad tähed: " + valikus_olevad_tähed, True, MUST)

                teksti_rect = peab_arvama_render.get_rect(topleft=(65, 500))
                varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)

                aken.blit(peab_arvama_varjund, varjundi_rect.topleft)
                aken.blit(peab_arvama_render, teksti_rect.topleft)

                #Kuvab sõna pikkuse
                sõna_pikkus_render = menüü_font.render("Sõna pikkus: " + str(len(suvaline_sõna)), True, VALGE)
                sõna_pikkus_varjund = menüü_font.render("Sõna pikkus: " + str(len(suvaline_sõna)), True, MUST)

                teksti_rect = sõna_pikkus_render.get_rect(topleft=(65, 540))
                varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)

                aken.blit(sõna_pikkus_varjund, varjundi_rect.topleft)
                aken.blit(sõna_pikkus_render, teksti_rect.topleft)

        elif alusta_mäng and valiku_näitaja == 1:
            taustapilt = taustapilt_mäng
            menüü_reziim = False

            jooksnud_aeg = (pygame.time.get_ticks() - algus_aeg) // 1000

            if jooksnud_aeg >= mängu_kestus:
                print("Aeg sai otsa!")
                pygame.quit()
                sys.exit()

            arvatud_tähed = set()
            if sündmus.type == pygame.KEYDOWN:
                if sündmus.unicode.isalpha():  #Kontrollib, kas sisestatud sümbol on täht
                    arvatud_täht = sündmus.unicode.upper()
                    if arvatud_täht in kõik_tähed:
                        kõik_tähed.remove(arvatud_täht)  ##Eemalda täht valikust
                        if arvatud_täht in suvaline_sõna:
                            #Õige tähe arvamine, vaheta varjatud sõna vastavalt
                            for i, täht in enumerate(suvaline_sõna):
                                if täht == arvatud_täht:
                                    varjatud_sõna[i] = arvatud_täht
                            print("Õige täht:", arvatud_täht)
                        else:
                            vigu += 1
                            print("Vale täht:", arvatud_täht)
                            if vigu == 7:
                                #Mängija kaotas
                                aken.fill((20, 20, 20))
                                aken.blit(hangman_pildid[vigu], (65, 50))
                                aken.blit(mängija_kaotas_varjund, varjundi_rect.topleft)
                                aken.blit(mängija_kaotas_render, teksti_rect.topleft)
                                pygame.display.update()
                                pygame.time.delay(5000)  #Ootab 5000 ms (5 sekundit)
                                pygame.quit()
                                sys.exit()

            if not menüü_reziim:
                aken.blit(taustapilt, (0, 0))

                aken.blit(hangman_pildid[vigu], (65, 50))

                #Kuvab varjatud sõna
                varjatud_tekst = " ".join(varjatud_sõna)
                varjatud_tekst_render = menüü_font.render(varjatud_tekst, True, VALGE)
                varjatud_tekst_varjund = menüü_font.render(varjatud_tekst, True, MUST)

                teksti_rect = varjatud_tekst_render.get_rect(topleft=(65, 420))
                varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)

                aken.blit(varjatud_tekst_varjund, varjundi_rect.topleft)
                aken.blit(varjatud_tekst_render, teksti_rect.topleft)

                #Kuvab arvatud tähed
                arvatud_tähed_render = menüü_font.render("Arvatud tähed: " + ", ".join(set(arvatud_tähed)), True, VALGE)
                arvatud_tähed_varjund = menüü_font.render("Arvatud tähed: " + ", ".join(set(arvatud_tähed)), True, MUST)

                teksti_rect = arvatud_tähed_render.get_rect(topleft=(65, 460))
                varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)

                aken.blit(arvatud_tähed_varjund, varjundi_rect.topleft)
                aken.blit(arvatud_tähed_render, teksti_rect.topleft)

                #Kuvab tähti, mida peab arvama
                valikus_olevad_tähed = ", ".join(kõik_tähed)
                peab_arvama_render = menüü_font.render("Valikus olevad tähed: " + valikus_olevad_tähed, True, VALGE)
                peab_arvama_varjund = menüü_font.render("Valikus olevad tähed: " + valikus_olevad_tähed, True, MUST)

                if peab_arvama_render.get_width() > LAIUS:
                    #Vähendab teksti suurust, et see mahuks ekraanile
                    uus_font = pygame.font.Font(None, 22)
                    peab_arvama_render = uus_font.render("Valikus olevad tähed: " + valikus_olevad_tähed, True, VALGE)
                    peab_arvama_varjund = uus_font.render("Valikus olevad tähed: " + valikus_olevad_tähed, True, MUST)

                teksti_rect = peab_arvama_render.get_rect(topleft=(65, 500))
                varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)

                aken.blit(peab_arvama_varjund, varjundi_rect.topleft)
                aken.blit(peab_arvama_render, teksti_rect.topleft)

                #Kuvab sõna pikkuse
                sõna_pikkus_render = menüü_font.render("Sõna pikkus: " + str(len(suvaline_sõna)), True, VALGE)
                sõna_pikkus_varjund = menüü_font.render("Sõna pikkus: " + str(len(suvaline_sõna)), True, MUST)

                teksti_rect = sõna_pikkus_render.get_rect(topleft=(65, 540))
                varjundi_rect = pygame.Rect(teksti_rect.left - 2, teksti_rect.top - 2, teksti_rect.width + 4, teksti_rect.height + 4)

                aken.blit(sõna_pikkus_varjund, varjundi_rect.topleft)
                aken.blit(sõna_pikkus_render, teksti_rect.topleft)

    pygame.display.update()