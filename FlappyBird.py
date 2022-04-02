import pgzrun
import random

WIDTH = 600
HEIGHT = 400

wysokoscPaska = 50
polozeniePaska = Rect((0,0), (WIDTH, wysokoscPaska))
kolor = 'green'

ikona_usmiech = Actor('grinning_cat', center=polozeniePaska.center)
ikona_usmiech_2 = Actor('grinning_cat_with_smiling_eyes', center=polozeniePaska.center)
ikona_smutek = Actor('pouting_cat', center=polozeniePaska.center)
ikona_usmiech_aktywny = Actor('smiling_cat_with_heart_eyes', center=polozeniePaska.center)
ikona_calus = Actor('kissing_cat', center=polozeniePaska.center)

def on_mouse_move(pos):
    global pozycjaKursora
    pozycjaKursora = pos

def generowaniePrzeszkody():
    global przeszkodaGora, przeszkodaDol, przeszkoda_X, wysokoscPrzeszkody, przeszkody, iloscPrzeszkod
    przeszkoda_X = 550
    y = random.randint(20, 180)
    wysokoscPrzeszkody = y
    przeszkodaGora = Rect((przeszkoda_X, wysokoscPaska), (50, wysokoscPrzeszkody))
    przeszkodaDol = Rect((przeszkoda_X, wysokoscPrzeszkody + 200), (50, HEIGHT - wysokoscPrzeszkody))
    przeszkody.insert(0, (przeszkodaGora, przeszkodaDol))

def draw():
    global bird_Y, nacisniecia, nacisnieciaKlawiszy
    screen.fill('black')
    for p in przeszkody:
        screen.draw.filled_rect(p[0], kolor)
        screen.draw.filled_rect(p[1], kolor)

    size = images.bird_small.get_size()
    screen.blit(images.bird_small, Rect((100, bird_Y), size))

    screen.draw.text('{:03d}'.format(czas), midright=(polozeniePaska.right, polozeniePaska.centery),
        fontsize=wysokoscPaska, color='red', fontname = 'crashed_scoreboard')
    screen.draw.text('{:03d}'.format(iloscPokonanych), midleft=(polozeniePaska.left, polozeniePaska.centery),
        fontsize=wysokoscPaska, color='red', fontname = 'crashed_scoreboard')

    if ikona_calus.collidepoint(pozycjaKursora):
        ikona_calus.draw()
    elif koniecGry:
        if wygrana:
            ikona_usmiech_aktywny.draw()
        else:
            ikona_smutek.draw()
    else:
        if nacisnieciaKlawiszy == 1:
            ikona_usmiech_2.draw()
        else:
            ikona_usmiech.draw()

def update():
    return

def on_key_down(key):
    global nacisniecia, nacisnieciaKlawiszy
    if key == keys.SPACE:
        nacisniecia = 1
    elif key == keys.ESCAPE:
        exit()
    nacisnieciaKlawiszy = 1

def on_key_up():
    global nacisniecia, nacisnieciaKlawiszy
    nacisnieciaKlawiszy = 0

def on_mouse_down(pos):
    if ikona_calus.collidepoint(pos):
        stop(False)
        start()
    elif ikona_smutek.collidepoint(pos):
        stop(False)
        start()
    elif ikona_usmiech.collidepoint(pos):
        stop(False)
        start()
    elif ikona_usmiech_2.collidepoint(pos):
        stop(False)
        start()
    elif ikona_usmiech_aktywny.collidepoint(pos):
        stop(pos)
        start()

def aktualizujCzas():
    global przeszkoda_X, przeszkodaGora, przeszkodaDol, licznik, przeszkody, bird_Y, nacisniecia, czas, licznikCzasu, iloscPokonanych

    licznikCzasu += 1
    if licznikCzasu == 100:
        czas += 1
        licznikCzasu = 0

    licznik += 1
    if licznik == 150:
        generowaniePrzeszkody()
        licznik = 0
    for p in przeszkody:
        p[0][0] -= 1
        p[1][0] -= 1
        print(p[0][0])
    bird_Y += 1
    if nacisniecia == 1:
        bird_Y -= 50
        nacisniecia = 0
    size = images.bird_small.get_size()
    if bird_Y <= wysokoscPaska:
        stop(False)
    if bird_Y + size[1] >= HEIGHT:
        stop(False)
    
    for p in przeszkody:
        if p[0].collidepoint(100 + size[0], bird_Y):
            stop(False)
        elif p[1].collidepoint(100 + size[0], bird_Y + size[1]):
            stop(False)
        if p[0][0] + 50 == 100 + size[0]:
            iloscPokonanych += 1
    if iloscPokonanych == 25:
        stop(True)


def stop(_wygrana):
    global wygrana, koniecGry
    clock.unschedule(aktualizujCzas)
    koniecGry = True
    wygrana = _wygrana

def start():
    global przeszkody, nacisniecia, licznik, bird_Y, czas, licznikCzasu, iloscPokonanych, koniecGry, pozycjaKursora, nacisnieciaKlawiszy
    clock.schedule_interval(aktualizujCzas, 0.01)
    koniecGry = False
    przeszkody = []
    nacisniecia = 0
    nacisnieciaKlawiszy = 0
    czas = 0
    licznikCzasu = 0
    licznik = 0
    bird_Y = 200
    iloscPokonanych = 0
    pozycjaKursora = (-1, -1)
    generowaniePrzeszkody()

start()

pgzrun.go()