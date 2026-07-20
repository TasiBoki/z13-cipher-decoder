import itertools
import sys
import multiprocessing
import os
import math
from collections import Counter

# --- KONFIGURÁCIÓ ---
Z13_CIPHER = "AEN+8KM8M+NAM"
UNIQUE_SYMBOLS_STR = "AEN+8KM"
TARGET_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ZODIAC_WORDS = ["KILL", "NAME", "DEATH", "POST", "TIME", "DONE"]

# Gyanúsítottak
SUSPECT_KEYS = {
    "GARYFRANCISPO": [ord(c) - ord('A') for c in "GARYFRANCISPO"],
    "LAWRENCEKANES": [ord(c) - ord('A') for c in "LAWRENCEKANES"],
    "ARTHURALLENSS": [ord(c) - ord('A') for c in "ARTHURALLENSS"],
    "RICHARDGAIKOW": [ord(c) - ord('A') for c in "RICHARDGAIKOW"],
}

def init_worker():
    global WORDS_SET
    
    # Dinamikus elérési út: az aktuális Python fájl mappáját keresi meg
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "words.txt")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            WORDS_SET = {word.strip().upper() for word in f if 3 <= len(word.strip()) <= 6}
    except:
        WORDS_SET = {"DONE", "KANE", "SEND", "KILL", "TIME", "BOLT", "LITE", "TEMP"}

def worker_task(args):
    permutation, trans_mode = args
    table = str.maketrans(UNIQUE_SYMBOLS_STR, "".join(permutation))
    raw_decrypted = Z13_CIPHER.translate(table)
    
    best_score = 0
    best_text = raw_decrypted
    best_key = "NONE"

    for name, key_shifts in SUSPECT_KEYS.items():
        shifted_chars = []
        for i, char in enumerate(raw_decrypted):
            shift = key_shifts[i % len(key_shifts)]
            shifted_val = (ord(char) - ord('A') + shift) % 26
            shifted_chars.append(chr(shifted_val + ord('A')))
        
        decrypted = "".join(shifted_chars)
        
        score = 0
        for word in ZODIAC_WORDS:
            if word in decrypted: score += len(word) * 20
        
        for i in range(len(decrypted) - 3):
            if decrypted[i:i+4] in WORDS_SET: score += 50
        
        if score > best_score:
            best_score = score
            best_text = decrypted
            best_key = name

    return (best_text, best_score, trans_mode, "".join(permutation), best_key)

def run_crack():
    # 1. Fájlok tisztítása
    if os.path.exists("results.txt"): os.remove("results.txt")
    
    print("[+] Turbózott motor indítása...")
    
    total_tasks = math.perm(len(TARGET_LETTERS), len(UNIQUE_SYMBOLS_STR))
    processed = 0
    seen_patterns = Counter()
    all_results = []
    
    tasks = ((p, 1) for p in itertools.permutations(TARGET_LETTERS, len(UNIQUE_SYMBOLS_STR)))
    
    # Pool indítása
    with multiprocessing.Pool(initializer=init_worker) as pool:
        for result in pool.imap_unordered(worker_task, tasks, chunksize=1000):
            processed += 1
            
            if result and result[1] >= 200:
                # Zajszűrés minta alapján
                pattern_key = result[0][1:5] + result[0][-4:]
                seen_patterns[pattern_key] += 1
                
                # Írás, ha KANE, vagy ritka minta
                if seen_patterns[pattern_key] < 50 or result[4] == "KANE":
                    all_results.append(result)
                    
                    # 2. Garanciális fájlba írás
                    with open("results.txt", "a", encoding="utf-8") as res_file:
                        res_file.write(f"TEXT: {result[0]} | SCORE: {result[1]} | KEY: {result[4]} | PERM: {result[3]}\n")
                        res_file.flush() # Azonnali kiírás a lemezre
                    
                    # Konzol kijelzés
                    if result[4] == "KANE":
                        print(f"\n[!!!] KANE TALÁLAT: {result[0]} | Pont: {result[1]}")
                    elif result[1] >= 230:
                        print(f"\n[!] TALÁLAT: {result[0]} | Pont: {result[1]} | Kulcs: {result[4]}")

            # Progresszió
            if processed % 5000 == 0:
                percent = (processed / total_tasks) * 100
                sys.stdout.write(f"\r[+] Feldolgozva: {percent:.2f}% | Találatok: {len(all_results)}")
                sys.stdout.flush()

    # Legjobb 20 mentése
    print("\n[+] Elemzés befejezve. Mentés a best_v2.txt-be...")
    best_results = sorted(all_results, key=lambda x: x[1], reverse=True)[:20]
    with open("best_v2.txt", "w", encoding="utf-8") as f:
        for res in best_results:
            f.write(f"TEXT: {res[0]} | SCORE: {res[1]} | KEY: {res[4]} | PERM: {res[3]}\n")

if __name__ == "__main__":
    run_crack()