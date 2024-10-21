Teoretická časť - návrh protokolu (6 bodov)
Požiadavky na návrh protokolu sú nasledovné:

nadviazanie spojenia medzi dvoma stranami a dohodnutie si parametrov spojenia (ako napr. TCP handshake),
umožniť poslať dáta po fragmentoch s veľkosťou zadanou zo vstupu od používateľa,
overenie integrity poslanej správy na strane príjemcu,
vedieť znova poslať stratenú alebo poškodenú správu,
zabezpečenie vzájomnej kontroly medzi uzlami, či je účastník na druhej strane spojenia stále aktívny,
umožniť úmyselne vytvoriť chybu v niektorej z prenášaných správ s cieľom simulovať poškodené dáta,
ostatné veci, ktoré považujete za dôležité.
Výstupom tejto časti je dokumentácia, v ktorej predstavíte návrh svojho protokolu a plán implementácie jednotlivých mechanizmov. Následne túto dokumentáciu prediskutujete so svojím cvičiacim počas kontrolného bodu, kde získate pripomienky na zapracovanie do praktickej časti. Dokumentácia musí obsahovať nasledujúce časti:

štruktúru hlavičiek vášho protokolu,
opis metódy na kontrolu integrity prenesenej správy (napr. ak si zvolíte CRC16, tak ho opíšete ako sa vypočíta, rovnako postupovať pri iných metódach),
opis metódy na zabezpečenie spoľahlivého prenosu dát (ARQ),
opis metódy na udržanie spojenia (Keep-Alive),
diagramy opisujúce predpokladané správanie vášho uzla/uzlov, použite UML diagramy ako napr. sekvenčný, aktivity a stavový (používajte vhodné nástroje, ako napr. miro alebo draw.io, nie skicár).
Pri hodnotení sa zohľadňuje prehľadnosť a zrozumiteľnosť odovzdanej dokumentácie ako aj kvalita navrhovaného riešenia. Dokumentácia musí obsahovať aj formálne časti ako úvodnú stranu, obsah, číslovanie strán atď. Konkrétnejšie informácie o jednotlivých požiadavkách na program nájdete v praktickej časti.

Praktická časť - implementácia p2p komunikátora (19 bodov vrátane doimplementácie)
V tejto časti implementujte P2P komunikátor podľa vášho návrhu, pričom zohľadnite pripomienky z kontrolného bodu. Vaše hodnotenie bude založené na splnení nasledujúcich úloh:

1. Vytvorenie a overenie základnej funkčnosti spojenia
Vytvoriť P2P spojenie medzi dvoma uzlami, dohodnutie si parametrov spojenia a overiť funkčnosť spojenia odoslaním textu v oboch smeroch komunikácie. Používateľské rozhranie na každom uzle musí umožňovať nastaviť nasledovné parametre:

port na ktorom uzol počúva,
IP adresu a port na cieľový uzol na ktorý sa bude posielať text/súbor.
Prezentovať úspešný prenos prostredníctvom Wireshark(WS) tak, aby ste vedeli identifikovať správy patriace vášmu protokolu v správnom poradí a vedeli ukázať jednotlivé polia vášho protokolu.

2. Prenos textu/súboru - fragmentácia
V počítačových sieťach fragmentácia označuje proces rozdelenia veľkých dátových blokov na menšie fragmenty pred ich odoslaním cez sieť. Tento proces je často nevyhnutný na zabezpečenie optimálneho prenosu dát, či už kvôli vyťaženosti siete alebo kvôli vlastnostiam daného prenosového média.

Vašou úlohou je implementovať proces fragmentácie s nasledujúcimi vlastnosťami. Používateľské rozhranie uzla musí umožniť dynamické nastavenie veľkosti fragmentu počas behu programu (medzi jednotlivými prenosmi). Pri prenose textu/súboru môžu nastať dva scenáre, ktoré je potrebné implementovať a úspešne demonštrovať pre získanie bodov:

prenos bez fragmentácie - veľkosť textu/súboru je menšia alebo rovná nastavenej maximálnej veľkosti fragmentu, vtedy sa text/súbor prenesie ako jeden celok bez zbytočného paddingu.
prenos s fragmentáciou - veľkosť textu/súboru je väčšia ako nastavená maximálna veľkosť fragmentu, odosielajúci uzol rozdelí súbor na menšie fragmenty, ktoré pošle samostatne.
Nastavenie veľkosti fragmentu musí byť obmedzené tak, aby používateľ nemohol zvoliť veľkosť, ktorá by spôsobila opätovnú fragmentáciu fragmentov na linkovej vrstve. Režijné správy, ktoré slúžia na riadenie komunikácie, sa prenášajú vždy bez fragmentácie. Na uzle je požadované, aby si používateľ mohol vybrať súbor na odoslanie z ktoréhokoľvek priečinka v súborovom systéme zariadenia.

V prípade prenosu s fragmentáciou je potrebné na jednotlivých uzloch vypísať nasledujúce informácie:

Odosielajúci uzol - zobrazí názov posielaného súboru (pri textovej správe sa tento údaj ignoruje), veľkosť textu/súboru, počet odoslaných fragmentov a veľkosť fragmentu. Ak má posledný fragment inú veľkosť než ostatné fragmenty, je potrebné tiež vypísať aj veľkosť posledného fragmentu.
Prijímajúci uzol - zobrazí správu o prijatí každého fragmentu s poradovým číslom a informáciou o tom, či bol fragment prenesený bez chýb. Po prijatí celého textu/súboru uzol zobrazí informáciu o úspešnom prijatí, čas trvania prenosu, veľkosť textu/súboru a absolútnu cestu, kam bol súbor uložený.
3. Prenos textu/súboru - poškodenie a strata dát
V sieťovej komunikácii občas dochádza k strate alebo poškodeniu dát počas prenosu. Z tohto dôvodu musí váš P2P komunikátor zaviesť mechanizmus na kontrolu chýb a zabezpečiť opätovné vyžiadanie stratených alebo poškodených fragmentov dát. Komunikátor musí podporovať pozitívne (ACK) aj negatívne (NACK) potvrdenia správ.

Vašou úlohou je vybrať a implementovať jednu metódu pre spoľahlivý prenos dát, tzv. Automatic Repeat Request (ARQ). Jednotlivé metódy sú hodnotené podľa ich zložitosti. Na výber máte tieto ARQ metódy:

Stop & wait (S&W)
Go Back-N (GBN)
Selective Repeat (SR)
Vylepšená Go Back-N/Selective Repeat (dynamický sliding window, optimalizácia počtu ACK správ, ... )
Základnou požiadavkou na splnenie tejto úlohy je úspešne preniesť text/súbor aj pri simulácii chýb prenosu, pričom musí byť korektne implementovaná detekcia chýb a ARQ metóda. Podrobnejšie informácie o jednotlivých metódach nájdete v časti Literatúra.

4. Udržanie spojenia (Keep-Alive)
Technika používaná v sieťových protokoloch na udržanie aktívneho spojenia medzi dvoma uzlami počas ich nečinnosti. Jej cieľom je minimalizovať počet nových nadväzovaných spojení, čím sa znižuje latencia spojená s vytváraním každého spojenia. Zároveň umožňuje monitorovať stav spojenia a overovať, či sú obe strany aktívne, čo zlepšuje spoľahlivosť spojenia a umožňuje rýchlejšie reagovať v prípade výpadku jedného z účastníkov spojenia.

Implementujte v rámci komunikátora vlastný mechanizmus Keep-Alive s nasledujúcimi vlastnosťami:

použite vlastné signalizačné správy,
monitorovanie spojenia začnite hneď po jeho nadviazaní,
posielajte heartbeat správy každých 5 sekúnd, ak medzi zariadeniami neprebieha žiadna aktivita,
ak jedna zo strán spojenia nedostane odpoveď na 3 po sebe odoslané heartbeat správy, považuje spojenie za ukončené,
uzol, ktorý vyhodnotí spojenie ako ukončené/prerušené, zobrazí informáciu o ukončení spojenia v používateľskom rozhraní,
komunikátor by mal byť schopný reagovať, ak počas prenosu textu/súboru dôjde k náhlemu výpadku spojenia (napr. odpojenie sieťového kábla), vtedy overí stav druhej strany poslaním heartbeat správ a na základe výsledku vykoná jednu z nasledujúcich akcií:
ak na všetky odoslané heartbeat správy nedostane od druhej strany odpoveď, prehlási spojenie za ukončené a vypíše, že prenos textu/súboru zlyhal,
ak sa spojenie podarí obnoviť, teda aspoň na poslednú odoslanú heartbeat správu príde odpoveď od druhej strany, pokúsi sa pokračovať v prenose textu/súboru, vrátane opätovného odoslania fragmentov, ktoré neboli úspešne doručené počas výpadku spojenia.
5. Lua skript vo Wiresharku
Vytvorte Lua skript, ktorý bude analyzovať váš protokol nad UDP a zobrazí jeho obsah vo WS. Skript rozpozná váš vlastný protokol na základe portu, dekóduje jednotlivé polia protokolu a zobrazí ich hodnoty priamo vo výstupe analýzy WS. Farebne odlíšte správy, ktoré prenášajú užitočné dáta, od režijných správ. Príklad nájdete na tomto odkaze.

6. Finálna dokumentácia
Študent dokumentáciu z návrhu protokolu doplní o nasledujúce kapitoly:

zmeny vykonané počas implementácie oproti návrhu riešenia,
doplní diagramy, ak mú chýbali v kontrolnom bode,
uvedie aspoň 1 komplexnú ukážku testovacieho scenára so screenami z WS(otvorenie spojenia, posielanie bez chyby prenosu, posielanie s chybou prenosu a následnou opravou, zatvorenie spojenia),
zhodnotenie a použité zdroje.
Hodnotí sa prehľadnosť a zrozumiteľnosť odovzdanej dokumentácie ako aj kvalita pracovania celového riešenia.

7. Kvalita spracovania
Hodnotí sa celková kvalita implementácie komunikátora, čo môže zahŕňať nasledujúce aspekty:

prívetivosť používateľského rozhrania v command line(CLI)(práca s ním, prehľadnosť výpisov atď.), áno, aj v CLI je možné vytvoriť prehľadné a užívateľsky príjemné rozhranie programu,
rýchlosť prenosu,
stabilita komunikátora (frekvencia pádu komunikátora pri prezentácii),
schopnosť adaptácie komunikátora na rôzne používateľské požiadavky bez reštartu.
Akceptačné podmienky
Podmienky, ktoré je potrebné splniť pri finálnom odovzdaní zadania, aby vaše zadanie bolo akceptované a mohlo byť hodnotené. Nesplnenie aj jednej z týchto podmienok má za následok hodnotenie 0 bodmi. V prípade P2P sú uzly rovnocenné, a preto podmienky musia spĺňať oba uzly.

Program musí byť implementovaný v jednom z nasledujúcich programovacích jazykov: C, C++, C#, Python a Rust(len, ak cvičiaci odsúhlasí).

Používateľ musí vedieť nastaviť na uzle port na počúvanie.

Používateľ musí vedieť nastaviť cieľovú IP adresu a port.

Používateľ musí mať možnosť zvoliť si max. veľkosť fragmentu na uzle a meniť ju dynamicky počas behu programu pred poslaním textu/súboru (neplatí pre režijné správy).

Uzol musí vedieť zobraziť nasledujúce informácie o prijatom/odoslanom texte/súbore:

názov a absolútnu cestu k súboru na danom uzle,
veľkosť a počet fragmentov vrátane celkovej veľkosti (posledný fragment môže mať odlišnú veľkosť ako predchádzajúce fragmenty).
Simulovať chybu prenosu odoslaním minimálne 1 chybného fragmentu pri prenose textu a súboru (do dátovej časti fragmentu alebo do checksum je cielene vnesená chyba, to znamená, že prijímajúca strana deteguje chybu pri prenose).

Prijímajúca strana musí byť schopná oznámiť odosielateľovi správne aj nesprávne doručenie fragmentov. Pri nesprávnom doručení fragmentu vyžiada znovu poslať poškodené dáta.

Možnosť odoslať 2MB súbor do 60 sekúnd a uložiť ho na prijímacom uzle ako rovnaký súbor.

Možnosť nastaviť na uzle miesto, kam sa súbor uloží po prijatí.

Pomocou nasledujúcej tabuľky si môžete overiť, či pred odovzdaním zadania spĺňate všetky akceptačné požiadavky. Zadanie odovzdáte iba v prípade, ak máte 'YES' 9/9.
