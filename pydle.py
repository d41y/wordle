import argparse
import pickle
import random
import sys

from collections import Counter
from colorama import Fore, Style

# introduce game
ASCII_INTRO = """
##################################################################################
#
#   ░▒▓███████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓███████▓▒░  ░▒▓█▓▒░        ░▒▓████████▓▒░ 
#   ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░        ░▒▓█▓▒░        
#   ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░        ░▒▓█▓▒░        
#   ░▒▓███████▓▒░   ░▒▓██████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░        ░▒▓██████▓▒░   
#   ░▒▓█▓▒░           ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░        ░▒▓█▓▒░        
#   ░▒▓█▓▒░           ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░        ░▒▓█▓▒░        
#   ░▒▓█▓▒░           ░▒▓█▓▒░     ░▒▓███████▓▒░  ░▒▓████████▓▒░ ░▒▓████████▓▒░ 
#
#
#   Errate das geheime 5-Buchstaben-Wort in maxiMal 6 Versuchen!
#   
#   Jeder Tipp muss ein gültiges deutsches Wort mit genau 5 Buchstaben sein.
#   Nach jedem Versuch bekommst du Hinweise durch Farben:
#   
#       🟩  Grün   - Buchstabe ist korrekt und an der richtigen Stelle.
#       🟨  Gelb   - Buchstabe ist im Wort, aber an der falschen Stelle.
#       ⬜  Grau   - Buchstabe kommt im Wort nicht vor.
#   
#   Überlege gut, tippe klug - und finde das Wort, bevor dir die Versuche ausgehen!
#   
#   Viel Spaß beim Knobeln - los geht's mit PYDLE!
#
###################################################################################
"""

BUILTIN = ['Abtei', 'Achse', 'Aktie', 'Allee', 'Ampel', 'Angel', 'Angst', 'Anmut', 'Arche', 'Arena', 'Armee', 'Armut', 'Asche', 'Bange', 'Banja', 'Basis', 'Beere', 'Bibel', 'Biene', 'Binde', 'Binge', 'Birke', 'Birne', 'Bitte', 'Blase', 'Blume', 'Bluse', 'Bohle', 'Bohne', 'Bombe', 'Borke', 'Braut', 'Brise', 'Buche', 'Bucht', 'Causa', 'Chase', 'Combo', 'Datei', 'Dauer', 'Decke', 'Delle', 'Demut', 'Disco', 'Donau', 'Donna', 'Dosis', 'Droge', 'Ebene', 'Ecker', 'Eifel', 'Elite', 'Erbin', 'Erbse', 'Ernte', 'Esche', 'Etage', 'Ethik', 'Fabel', 'Fahne', 'Fahrt', 'Falle', 'Falte', 'Farbe', 'Farce', 'Faser', 'Fauna', 'Feder', 'Fehde', 'Feier', 'Feige', 'Feine', 'Ferne', 'Ferse', 'Feste', 'Fette', 'Fidel', 'Figur', 'Firma', 'Folge', 'Force', 'Frage', 'Frist', 'Front', 'Gabel', 'Garde', 'Gasse', 'Geige', 'Geste', 'Gilde', 'Gnade', 'Grube', 'Gruft', 'Gunst', 'Gurke', 'Halbe', 'Halde', 'Halle', 'Halse', 'Hanke', 'Hanse', 'Harfe', 'Haube', 'Havel', 'Helfe', 'Helle', 'Henne', 'Herde', 'Hetze', 'Hilfe', 'Hitze', 'Hymne', 'Ikone', 'Insel', 'Jacht', 'Jacke', 'Jause', 'Junta', 'Kalle', 'Kanne', 'Kante', 'Kappe', 'Karte', 'Kassa', 'Kasse', 'Kaste', 'Katze', 'Kehle', 'Kehre', 'Kelle', 'Kerbe', 'Kerwe', 'Kerze', 'Kette', 'Keule', 'Kippe', 'Kiste', 'Klage', 'Kohle', 'Kolbe', 'Komik', 'Kopie', 'Krida', 'Kripo', 'Krise', 'Krone', 'Kugel', 'Kunst', 'Kurve', 'Lanze', 'Larve', 'Latte', 'Lauda', 'Laune', 'Laute', 'Leber', 'Leere', 'Lehne', 'Liebe', 'Lilie', 'Linde', 'Linie', 'Linke', 'Linse', 'Liste', 'Lobby', 'Lodge', 'Logik', 'Loipe', 'Lunge', 'Lyrik', 'Mache', 'Macht', 'Mafia', 'Magie', 'Mamma', 'Mappe', 'Marge', 'Marke', 'Maske', 'Masse', 'Mathe', 'Mauer', 'Meile', 'Menge', 'Mensa', 'Metro', 'Meute', 'Miene', 'Milch', 'Milde', 'Miliz', 'Mimik', 'Missa', 'Mitte', 'Moral', 'Motte', 'Mulde', 'Mumie', 'Musik', 'Mutti', 'Nacht', 'Nadel', 'Narbe', 'Natur', 'Neige', 'Nelke', 'Niere', 'Nonne', 'Notiz', 'Nudel', 'Obhut', 'Olive', 'Optik', 'Order', 'Orgel', 'Orgie', 'Pacht', 'Palme', 'Panik', 'Pappe', 'Party', 'Pasta', 'Patte', 'Pauke', 'Petit', 'Pfote', 'Phase', 'Pille', 'Piste', 'Pizza', 'Plage', 'Plane', 'Polin', 'Polka', 'Ponte', 'Posse', 'Prise', 'Probe', 'Prosa', 'Pumpe', 'Puppe', 'Puste', 'Quere', 'Quote', 'Rache', 'Rampe', 'Ranch', 'Rasse', 'Ratio', 'Ratte', 'Raupe', 'Regel', 'Regie', 'Reife', 'Reihe', 'Reine', 'Reise', 'Rente', 'Revue', 'Rhone', 'Ricke', 'Riege', 'Rinde', 'Rinne', 'Rippe', 'Ritze', 'Robbe', 'Rolle', 'Route', 'Ruine', 'Runde', 'Runge', 'Sache', 'Sahne', 'Saite', 'Salbe', 'Salve', 'Sauna', 'Scham', 'Schau', 'Scheu', 'Sechs', 'Seele', 'Sehne', 'Seide', 'Seife', 'Seite', 'Sekte', 'Senke', 'Senna', 'Sense', 'Serie', 'Serra', 'Sicht', 'Silbe', 'Sitte', 'Skala', 'Sohle', 'Sonde', 'Sonne', 'Sorge', 'Sorte', 'Stadt', 'Statt', 'Stele', 'Stirn', 'Story', 'Stube', 'Stufe', 'Stute', 'Suche', 'Sucht', 'Suite', 'Summa', 'Summe', 'Szene', 'Tafel', 'Tanne', 'Tante', 'Tasse', 'Taste', 'Taufe', 'Terra', 'Theke', 'These', 'Tiefe', 'Tinte', 'Tolle', 'Tonne', 'Torte', 'Trage', 'Treue', 'Tulpe', 'Union', 'Untat', 'Verve', 'Villa', 'Vista', 'Waadt', 'Waage', 'Wache', 'Waffe', 'Waise', 'Walze', 'Wange', 'Wanne', 'Wanze', 'Warte', 'Weile', 'Weite', 'Welle', 'Werft', 'Weser', 'Wespe', 'Weste', 'Wette', 'Wiege', 'Wiese', 'Wiesn', 'Winde', 'Witwe', 'Woche', 'Wolga', 'Wolke', 'Wolle', 'Wonne', 'Wucht', 'Wunde', 'Wurst', 'Zange', 'Zeche', 'Zecke', 'Zeile', 'Zelle', 'Ziege', 'Zucht', 'Zunft', 'Zunge', 'Zutat', 'Abbau', 'Abend', 'Abruf', 'Abzug', 'Acker', 'Adler', 'After', 'Agent', 'Ahorn', 'Alarm', 'Alien', 'Allah', 'Altar', 'Anbau', 'Anger', 'Anruf', 'Anzug', 'Apfel', 'April', 'Arsch', 'Audit', 'Autor', 'Bader', 'Balte', 'Baron', 'Basar', 'Baske', 'Basso', 'Bauch', 'Bayer', 'Beach', 'Belag', 'Beleg', 'Beruf', 'Besen', 'Beton', 'Bezug', 'Biker', 'Blick', 'Blitz', 'Block', 'Blues', 'Bluff', 'Bobby', 'Boden', 'Bogen', 'Bolid', 'Bonus', 'Boxer', 'Brief', 'Brill', 'Brink', 'Brite', 'Brunn', 'Buchs', 'Busen', 'Chaot', 'Chart', 'Chief', 'Chili', 'Claim', 'Clown', 'Comic', 'Couch', 'Court', 'Crash', 'Creek', 'Curry', 'Dachs', 'Dampf', 'Dandy', 'Deich', 'Dekan', 'Dekor', 'Demos', 'Dinar', 'Dings', 'Dolch', 'Draht', 'Drang', 'Dreck', 'Drink', 'Drost', 'Dunst', 'Durst', 'Eagle', 'Eifer', 'Eimer', 'Einer', 'Eklat', 'Eleve', 'Elfer', 'Engel', 'Essay', 'Esser', 'Essig', 'Etter', 'Event', 'Exote', 'Faber', 'Faden', 'Falke', 'Feind', 'Finke', 'First', 'Fisch', 'Fjord', 'Flair', 'Flash', 'Fleck', 'Flirt', 'Fluch', 'Fluss', 'Flyer', 'Fokus', 'Fonds', 'Forst', 'Frack', 'Franc', 'Freak', 'Frost', 'Frust', 'Fuchs', 'Funke', 'Gatte', 'Gault', 'Geber', 'Geier', 'Glanz', 'Grant', 'Greif', 'Greis', 'Griff', 'Grill', 'Grips', 'Groll', 'Grund', 'Guide', 'Gusto', 'Haber', 'Hagel', 'Haken', 'Hauch', 'Hauer', 'Heber', 'Hecht', 'Heros', 'Hirte', 'Hoden', 'Honig', 'Huber', 'Idiot', 'Imker', 'Inder', 'Index', 'Indio', 'Input', 'Islam', 'Jemen', 'Jerez', 'Joint', 'Joker', 'Jubel', 'Jumbo', 'Junge', 'Juror', 'Kader', 'Kajak', 'Kakao', 'Kalif', 'Kamin', 'Kampf', 'Kanal', 'Kegel', 'Kelch', 'Kiosk', 'Klang', 'Klotz', 'Knabe', 'Knall', 'Knick', 'Kniff', 'Knopf', 'Knopp', 'Knorr', 'Kober', 'Kodex', 'Komet', 'Koran', 'Kosak', 'Krach', 'Kranz', 'Krebs', 'Kreis', 'Kreml', 'Krieg', 'Krimi', 'Krupp', 'Kubus', 'Kurde', 'Lachs', 'Laden', 'Laser', 'Leser', 'Level', 'Limes', 'Liter', 'Lloyd', 'Logos', 'Lotse', 'Lotus', 'Lover', 'Luchs', 'Lunch', 'Luxus', 'Macho', 'Magen', 'Makel', 'Maler', 'Markt', 'Match', 'Maure', 'Meier', 'Meter', 'Mimus', 'Modem', 'Moder', 'Modus', 'Monat', 'Motor', 'Mount', 'Multi', 'Nabel', 'Nagel', 'Nager', 'Nebel', 'Neffe', 'Neger', 'Notar', 'Ochse', 'Olymp', 'Orbit', 'Orden', 'Orkan', 'Oscar', 'Osten', 'Ozean', 'Panda', 'Papst', 'Pater', 'Pegel', 'Penis', 'Penny', 'Pfahl', 'Pfeil', 'Pfiff', 'Pflug', 'Pirat', 'Platz', 'Pokal', 'Poker', 'Porno', 'Preis', 'Prinz', 'Prior', 'Profi', 'Psalm', 'Pudel', 'Pulli', 'Punkt', 'Qualm', 'Quast', 'Quell', 'Rabbi', 'Radar', 'Rambo', 'Range', 'Rasen', 'Realo', 'Recke', 'Rhein', 'Ritus', 'Roman', 'Romeo', 'Rowdy', 'Rubel', 'Rubin', 'Rufer', 'Rumpf', 'Rusch', 'Russe', 'Sakko', 'Saldo', 'Salon', 'Salto', 'Samba', 'Samen', 'Satan', 'Saudi', 'Schah', 'Schal', 'Schub', 'Schuh', 'Scout', 'Segen', 'Seher', 'Senat', 'Serbe', 'Serge', 'Sinai', 'Sinto', 'Sound', 'Spalt', 'Spatz', 'Speck', 'Speer', 'Spike', 'Spion', 'Spitz', 'Sporn', 'Sport', 'Spott', 'Spray', 'Sprit', 'Spurt', 'Staat', 'Stahl', 'Stall', 'Stamm', 'Stand', 'Start', 'Staub', 'Steig', 'Stein', 'Stich', 'Stiel', 'Stier', 'Stoff', 'Stolz', 'Stopp', 'Strip', 'Strom', 'Stuck', 'Stuhl', 'Stunt', 'Sturz', 'Sumpf', 'Syrer', 'Tabak', 'Tadel', 'Taler', 'Tango', 'Tarif', 'Tauer', 'Teddy', 'Teich', 'Teint', 'Thron', 'Tiger', 'Tisch', 'Titel', 'Tobel', 'Torso', 'Touch', 'Track', 'Train', 'Trakt', 'Trank', 'Trapp', 'Traum', 'Trend', 'Trick', 'Trieb', 'Tritt', 'Troll', 'Trost', 'Trotz', 'Truck', 'Trunk', 'Trupp', 'Trust', 'Tumor', 'Turbo', 'Ultra', 'Umbau', 'Umweg', 'Umzug', 'Unfug', 'Ungar', 'Unmut', 'Unrat', 'Unter', 'Vater', 'Vichy', 'Virus', 'Vogel', 'Vokal', 'Wagen', 'Wedel', 'Welpe', 'Wille', 'Wodka', 'Wotan', 'Zenit', 'Zeuge', 'Zubau', 'Zuber', 'Zuruf', 'Zuzug', 'Zwang', 'Zweck', 'Zwerg', 'Zwist', 'Aarau', 'Aarau', 'Abgas', 'Acryl', 'Adieu', 'Album', 'Alibi', 'Alpha', 'Amman', 'Areal', 'Aroma', 'Asien', 'Athen', 'Atoll', 'Baden', 'Basel', 'Birma', 'Blatt', 'Blech', 'Bozen', 'Braun', 'Brett', 'Burma', 'Capri', 'Carol', 'Cello', 'Chaos', 'Chile', 'China', 'Chlor', 'Chrom', 'Cover', 'Credo', 'Dakar', 'Datum', 'Delhi', 'Depot', 'Dogma', 'Drama', 'Dubai', 'Duell', 'Duett', 'Eigen', 'Einst', 'Eisen', 'Elend', 'Email', 'Enzym', 'Ethos', 'Etwas', 'Fatum', 'Fazit', 'Feuer', 'Flach', 'Forte', 'Forum', 'Foyer', 'Futur', 'Gamma', 'Gebet', 'Gebot', 'Gehen', 'Genom', 'Genre', 'Getto', 'Ghana', 'Gleis', 'Glied', 'Gramm', 'Haben', 'Haifa', 'Haiti', 'Hallo', 'Handy', 'Hanoi', 'Haupt', 'Hertz', 'Hobby', 'Hotel', 'Hurra', 'Ibiza', 'Ideal', 'Idiom', 'Idyll', 'Image', 'Indiz', 'Ischl', 'Japan', 'Jetzt', 'Kabul', 'Kairo', 'Kamel', 'Katar', 'Kenia', 'Kleid', 'Klein', 'Klima', 'Komma', 'Konto', 'Korea', 'Korps', 'Kraul', 'Kreta', 'Kreuz', 'Label', 'Labor', 'Lager', 'Leben', 'Leder', 'Lehen', 'Licht', 'Lille', 'Limit', 'Linux', 'Lokal', 'Lotto', 'Luxor', 'Malta', 'Mandl', 'Manko', 'Meran', 'Miami', 'Minsk', 'Minus', 'Mixed', 'Moped', 'Motiv', 'Motto', 'Nepal', 'Nizza', 'Novum', 'Odeon', 'Omega', 'Opfer', 'Opium', 'Organ', 'Osaka', 'Padua', 'Paket', 'Panel', 'Paper', 'Parma', 'Pedal', 'Pfand', 'Pferd', 'Pfund', 'Pixel', 'Platt', 'Porto', 'Pound', 'Primo', 'Radio', 'Recht', 'Reich', 'Remis', 'Rondo', 'Rouge', 'Rudel', 'Ruder', 'Rugby', 'Sauer', 'Schaf', 'Segel', 'Seoul', 'Serum', 'Shirt', 'Sofia', 'Spiel', 'Steak', 'Stroh', 'Sujet', 'Sushi', 'Tamil', 'Tempo', 'Texas', 'Thema', 'Thing', 'Tirol', 'Tokio', 'Trier', 'Troja', 'Tunis', 'Turin', 'Tutti', 'Vaduz', 'Video', 'Viech', 'Visum', 'Votum', 'Wachs', 'Wales', 'Wesen', 'Worms', 'Wrack', 'Zabel', 'Zebra', 'Zitat', 'Zivil', 'Zutun']

def parse_args():
    parser = argparse.ArgumentParser(description="Pydle: Ein Wordle-Spiel in Python")
    parser.add_argument('--pickle', help='Lies eine Pickle Wordlist-Datei zum Spielen ein')
    parser.add_argument('--wordlist', help='Lies eine gewöhnliche Wordlist-Datei zum Spielen ein')
    parser.add_argument('--builtin', action='store_true', help='Lies die eingebaute Wordlist zum Spielen ein')
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)
    
    return args

def pkl_file(pklfile):
    """
    reading pickle file - pickle file has to be in list format
    """
    with open(pklfile, 'rb') as f:
        content = pickle.load(f)
    return content

def wordlist_file(wordlist):
    """
    reading standard wordlist file and putting into list
    """
    with open(wordlist, 'r') as f:
        content = [line.strip() for line in f if line.strip()]
    return content

def print_intro():
    """
    introduces the game to the player
    """
    print(Fore.LIGHTBLUE_EX, ASCII_INTRO)
    print(Style.RESET_ALL)

def guess_interaction(selected_word):
    """
    handles logic in interacting with user
    """
    guess_count = 1
    match = False

    while not match and guess_count < 7:
        guess = input(f'({guess_count}) \u2192 ').upper()

        while len(guess) != 5:
            guess = input(f'Das Wort muss 5 Buchstaben lang sein.\n({guess_count}) \u2192 ').upper()

        if guess == selected_word:
            print('Du hast gewonnen!')
            match = True
            return True

        result = evaluate_guess(guess, selected_word)

        guess_count += 1

        print_colored(result)
        print()

    print(f'Du hast verloren! Das gesuchte Wort war:', end='')
    print(Fore.RED, f'{selected_word}')
    print(Style.RESET_ALL)
    return False

def evaluate_guess(guess, selected_word):
    """
    checks the guess and portions it for colorizing
    """
    result = [None] * len(guess)
    selected_word_count = Counter(selected_word) # creates counter for each letter in selected_word

    for index, letter in enumerate(guess):
        if letter == selected_word[index]:
            result[index] = ('match', letter)
            selected_word_count[letter] -= 1 # subtracts 1 if found so colorizing yellow stays inside logic

    for index, letter in enumerate(guess):
        if result[index] is not None:
            continue
        elif letter in selected_word_count and selected_word_count[letter] > 0:
            result[index] = ('partial', letter)
            selected_word_count[letter] -= 1 # subtracts 1 if found so colorizing yellow stays inside logic
        else:
            result[index] = ('not', letter)
    return result

def print_colored(result):
    """
    colorizes the guesses
    """
    for i in range(len(result)):
        status, letter = result[i]
        if status == 'match':
            print(Fore.GREEN + f'{letter}', end='')
        elif status == 'partial':
            print(Fore.YELLOW + f'{letter}', end='')
        else:
            print(Fore.LIGHTWHITE_EX + f'{letter}', end='')
    print(Style.RESET_ALL)    

if __name__=='__main__':

    args = parse_args()

    if args.pickle:
        content = pkl_file(args.pickle)
    elif args.wordlist:
        content = wordlist_file(args.wordlist)
    elif args.builtin:
        content = BUILTIN

    try:
        print_intro()
        guess_interaction(random.choice(content).upper())
        print('Bis zum nächsten Mal!')
    except KeyboardInterrupt:
        print()
        print('You pressed CTRL+C. Bis zum nächsten Mal!')
        sys.exit()
    except Exception:
        print('Something happened, I need to end the game. Bis zum nächsten Mal!')
        sys.exit()