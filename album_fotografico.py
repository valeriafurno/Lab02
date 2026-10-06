"""CARICA LE FOTO DAL FILE, CREANDO UN NUOVO ANNO OGNI VOLTA CHE COMPARE PER LA PRIMA VOLTA"""
def carica_da_file(file_path):
    try:
        with open(file_path,'r', encoding='utf-8') as f:
            album={} #il mio album fotografico sarà un dizionario:
            # con chiave anno e valore associato una lista di foto di quell'anno
            f.readline()
            for line in f:
                campi=line.rstrip('\n').split(',')
                #ogni foto è rappresentata da un dizionario
                foto={
                    "codice":campi[0],
                    "titolo": campi[1],
                    "autore":campi[2],
                    "mese":int(campi[3]),
                    }
                anno =int( campi[4])

                #controllo se ogni anno non è ancora presente come chiave nel mio dizionario album

                if anno not in album: #se è la prima volta che incontro quell'anno
                    # creo la chiave anno e una nuova lista contenente la foto
                    album[anno]=[foto]
                else:
                    album[anno].append(foto) #aggiungo la foto se l'anno esiste già
        return album
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    foto = {
        "codice": codice,
        "titolo":titolo,
        "autore": autore,
        "mese": mese,
        # "anno":campi[4],
        }

    if mese<1 or mese>12: #controllo se il numero inserito in input è valido
        print(f'Formato data non valido')
        return None

    #una foto ha un codice univoco, quindi non può esisterne un'altra con lo stesso
     #faccio un controllo e se esiste restituisco None
    for anno_i in album.keys():
        for foto_i in album[anno_i]:
            if codice== foto_i["codice"]:
                return None
    try:
        #provare ad aggiungere in modalità append('a') una foto al file
        with open(file_path,'a') as f:

            #se l'anno della nuova foto non è già presente, creo una nuova chiave con lista delle foto
            if anno not in album.keys():
                album[anno]=[foto]
            else:           #se l'anno esiste aggiungo direttamente la foto
                album[anno].append(foto)
            f.write(f'{codice},{titolo},{autore},{mese},{anno}\n')
        return foto
    except FileNotFoundError:
        return None

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""

    #controllo che ci sia una foto con il codice inserito e in caso positivo, restituisco i dati di quella foto
    for anno_i in album.keys():
        for foto_i in album[anno_i]:
            if codice== foto_i["codice"]:
                return f'{foto_i["codice"]}, {foto_i["titolo"]}, {foto_i["autore"]}, {foto_i["mese"]}, {anno_i}'
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    titoli_foto=[] #lista vuota in cui inserisco i titoli
    anno=int(anno)

    #controllo se anno richiesto non è una chiave e restituisce None
    if anno not in album:
        return None

    album_dellanno = album[anno]

    for foto in album_dellanno: #per ogni foto che appartiene a quell'anno, prendo il titolo e lo
        # aggiungo alla lista di titoli per quell'anno
        fototitolo = foto["titolo"]
        titoli_foto.append(fototitolo)

    if len(titoli_foto): #controllo che lista non sia vuota e ordino i titoli in ordine alfabetico
        titoli_foto.sort()
        return titoli_foto
    else:
        return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                #print(album)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
