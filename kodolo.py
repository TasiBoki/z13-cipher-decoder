import itertools
import os
import sys
import math
from collections import Counter

# ==========================================
# 1. ALAPADATOK ÉS KONFIGURÁCIÓ
# ==========================================
Z13_CIPHER = "AEN+8KM8M+NAM"

# Egyedi szimbólumok kigyűjtése -> ['A', 'E', 'N', '+', '8', 'K', 'M'] (7 egyedi karakter)
UNIQUE_SYMBOLS = list(set(Z13_CIPHER))
# Sztring formátum a beépített gyors fordításhoz (.translate()-hez)
UNIQUE_SYMBOLS_STR = "".join(UNIQUE_SYMBOLS)

# Kiemelt Zodiac kulcsszavak
ZODIAC_WORDS = ["KILL", "NAME", "DEATH", "POST"]

# Ismert gyanúsítottak tisztított nevei
SUSPECTS = {
    "ARTHUR LEIGH ALLEN": "ARTHURLEIGHALLEN",
    "GARY FRANCIS POST": "GARYFRANCISPOST",
    "LAWRENCE KANE": "LAWRENCEKANE",
    "RICHARD GAIKOWSKI": "RICHARDGAIKOWSKI",
    "ROSS SULLIVAN": "ROSSSULLIVAN"
}

# Előre kiszámítjuk a gyanúsítottak betűgyakoriságát az anagramma-szűrőhöz (Gyorsítás!)
SUSPECT_COUNTERS = {name: Counter(clean) for name, clean in SUSPECTS.items()}

# ==========================================
# 2. OPTIMALIZÁLT SZÓTÁR BEOLVASÁS
# ==========================================
def load_dictionary(file_path):
    print(f"[-] Szótár betöltése: {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # OPTIMALIZÁLÁS: Csak a 3 és 8 karakter közötti szavakat tartjuk meg, ahogy javasoltad!
            words = {line.strip().upper() for line in f if 2 < len(line.strip()) < 9}
        print(f"[+] Sikeresen betöltve {len(words)} releváns angol szó.")
        return words
    except FileNotFoundError:
        print(f"[!] Hiba: A fájl nem található a megadott útvonalon!")
        print(f"[-] Alapértelmezett mini-szótár használata.")
        return {"MY", "NAME", "IS", "KILL", "THE", "AND", "FOR", "THAT", "EDWARD", "ARTHUR"}

# ÁLLÍTSD BE A SAJÁT FÁJLOD ELÉRÉSI UTÁT!
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DICTIONARY_PATH = os.path.join(SCRIPT_DIR, "words.txt")

# ==========================================
# 3. SEGÉDFÜGGVÉNYEK (PONTOZÁS ÉS TRANSZPOZÍCIÓ)
# ==========================================
def score_anagram(text, text_counter):
    """Megnézi, mennyire egyeznek a betűk a gyanúsítottak neveivel."""
    anagram_score = 0
    best_suspect_match = "Nincs"
    
    for name, suspect_count in SUSPECT_COUNTERS.items():
        matches = sum(min(text_counter[char], suspect_count[char]) for char in text_counter if char in suspect_count)
        
        if matches >= 8:  # Ha legalább 8 betű stimmel
            current_score = matches * 4
            if current_score > anagram_score:
                anagram_score = current_score
                best_suspect_match = name
                
    return anagram_score, best_suspect_match

def score_text(text):
    """Pontozza a szöveget a szótár és a Zodiac szavak alapján."""
    score = 0
    for word in ENGLISH_DICTIONARY:
        if word in text:
            score += len(word) * 2
            
    for word in ZODIAC_WORDS:
        if word in text:
            score += len(word) * 3
            
    return score

def apply_transposition(cipher_text, mode=1):
    """Karakter-átrendezési variációk."""
    if mode == 1:
        return cipher_text
    elif mode == 2:
        return cipher_text[::-1]
    elif mode == 3:
        return cipher_text[::2] + cipher_text[1::2]
    return cipher_text

# ==========================================
# 4. FŐ KÓDFEJTŐ MOTOR (PROGRES BAR-RAL)
# ==========================================
def crack_z13(top_n=15):
    print("\n==================================================")
    print("      Z13 KÓDFEJTŐ MOTOR ELINDÍTVA (VIZUÁLIS)     ")
    print("==================================================")
    print(f"[-] Eredeti rejtjel: {Z13_CIPHER}")
    print(f"[-] Tesztelt ábécé betűkészlete (bővített):")
    
    # Kicsit bővítettem a betűkészletet, hogy az összes gyanúsított neve beleférjen
    target_letters = "AENIKMORTYSHWBDLGCFXU" 
    print(f"    {target_letters}")
    
    results = []
    
    # Összes permutáció kiszámítása a folyamatjelzőhöz
    total_combinations = math.perm(len(target_letters), len(UNIQUE_SYMBOLS))
    total_steps = total_combinations * 3  # 3 transzpozíciós mód miatt
    
    checked_count = 0
    current_best_score = 0
    current_best_text = "Nincs még találat"
    update_interval = 100000  # Hány lépésenként frissítse a képernyőt (így nem lassítja a kiírás a futást)

    for trans_mode in [1, 2, 3]:
        current_cipher = apply_transposition(Z13_CIPHER, mode=trans_mode)
        
        for permutation in itertools.permutations(target_letters, len(UNIQUE_SYMBOLS)):
            checked_count += 1
            
            # --- Vizuális visszacsatolás ---
            if checked_count % update_interval == 0 or checked_count == total_steps:
                progress = (checked_count / total_steps) * 100
                bar_length = 20
                filled_length = int(bar_length * progress // 100)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                
                sys.stdout.write(
                    f"\r[{bar}] {progress:.1f}% | Mód: {trans_mode} | "
                    f"Legjobb: {current_best_text} ({current_best_score} p.)"
                )
                sys.stdout.flush()
            # -------------------------------

            # OPTIMALIZÁLÁS: C-szintű karakter-helyettesítés map helyett translate-tel!
            translation_table = str.maketrans(UNIQUE_SYMBOLS_STR, "".join(permutation))
            decrypted_text = current_cipher.translate(translation_table)
            
            # Pontozások lekérése
            word_score = score_text(decrypted_text)
            
            text_counter = Counter(decrypted_text)
            anagram_score, suspect_match = score_anagram(decrypted_text, text_counter)
            
            total_score = word_score + anagram_score
            
            if total_score > current_best_score:
                current_best_score = total_score
                current_best_text = decrypted_text
            
            # Csak a komolyabb találatokat mentjük el a listába
            if total_score > 15:
                results.append({
                    'text': decrypted_text,
                    'score': total_score,
                    'trans_mode': trans_mode,
                    'suspect': suspect_match
                })
                
    print("\n\n[+] Keresés sikeresen befejeződött!")
    
    # Eredmények szűrése és rendezése
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    seen = set()
    unique_results = []
    
    for r in results:
        if r['text'] not in seen:
            seen.add(r['text'])
            unique_results.append(r)
            if len(unique_results) == top_n:
                break
                
    # Eredménytábla kirajzolása
    print(f"\n== TOP {len(unique_results)} LEHETSÉGES MEGOLDÁS ANAGRAMMA SZŰRÉSSEL ==")
    print(f"{'Sorszám':<8}{'Dekódolt szöveg':<16}{'Pont':<8}{'Mód':<5}{'Gyanúsított egyezés':<20}")
    print("-" * 65)
    for i, res in enumerate(unique_results, 1):
        print(f"{i:<8}{res['text']:<16}{res['score']:<8}{res['trans_mode']:<5}{res['suspect']:<20}")

# ==========================================
# PROGRAM INDÍTÁSA
# ==========================================
if __name__ == "__main__":
    crack_z13(top_n=15)