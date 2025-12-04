INSERT INTO topics (id_topic, name) VALUES
(1, 'zwierzęta'),
(2, 'zawody'),
(3, 'jedzenie'),
(4, 'technologia'),
(6, 'sport'),
(7, 'kosmos'),
(8, 'przyroda'),
(9, 'miasto')
ON CONFLICT (id_topic) DO NOTHING;


INSERT INTO exercises (id_exercise, type, level, topics) VALUES
(1, 'match_image', 1, '{1}'),
(2, 'match_image', 2, '{2,3}'),
(3, 'match_image', 2, '{3}'),
(4, 'match_image', 3, '{4}'),
(5, 'match_image', 3, '{2}'),
(6, 'match_image', 4, '{6,8}'),
(7, 'match_image', 4, '{2,1}'),
(8, 'match_image', 5, '{7,4}'),
(9, 'text_question', 3, '{2}'),
(10, 'text_question', 3, '{2,6}'),
(11, 'text_question', 3, '{8}'),
(12, 'text_question', 3, '{9}'),
(13, 'text_question', 4, '{2,8}'),
(14, 'text_question', 4, '{9}'),
(15, 'text_question', 5, '{9}'),
(16, 'text_question', 5, '{6}')
ON CONFLICT (id_exercise) DO NOTHING;


INSERT INTO exercise_match (exercise_id, text, image_urls, correct_index) VALUES
(1, 'Wesoły kotek\nTo jest kotek Mruczek. Mruczek jest mały i czarny. Ma białe łapki. Kotek bawi się kłębkiem wełny. Wełna jest czerwona. Mruczek jest bardzo wesoły\nGdzie ukrył się {child_name}?.', ARRAY['http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png'], 0),
(2, 'Piekarz\nPan Jan jest piekarzem. Wstaje bardzo wcześnie rano. Wkłada biały fartuch i dużą czapkę. Wyrabia ciasto w wielkiej misce. Potem wkłada bochenki do gorącego pieca. Upieczony chleb jest brązowy i chrupiący.', ARRAY['http://10.0.2.2:8000/static/piekarz1.png', 'http://10.0.2.2:8000/static/piekarz2.png', 'http://10.0.2.2:8000/static/piekarz3.png'], 2),
(3, 'Pyszna pizza\nTata robi obiad. Dziś będzie pizza. Ania wałkuje ciasto. Jest białe i miękkie. Tata kroi szynkę i ser. Kładą wszystko na ciasto. Teraz pizza idzie do pieca. Pachnie w całym domu. Wszyscy są już głodni.', ARRAY['http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png'], 2),
(4, 'Młody wynalazca\nTomek spędził popołudnie w garażu. Z kartonów i starych części zbudował robota. Robot ma kwadratową głowę i antenkę z drutu. Jego oczy są zrobione z dwóch zielonych nakrętek. Tomek jest dumny ze swojej pracy.', ARRAY['http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png'], 2),
(5, 'Wizyta u pani doktor\nKasia obudziła się z bólem gardła. Mama zabrała ją do przychodni.\nPani doktor była bardzo miła i miała kolorowy fartuch w motyle. Zbadała Kasię słuchawkami, które były trochę zimne. Potem zajrzała do gardła, świecąc małą latarką. Okazało się, że to tylko lekkie przeziębienie.\nKasia dostała naklejkę z dzielnym lwem za bycie grzeczną pacjentką.', ARRAY['http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png'], 0),
(6, 'Zimowe szaleństwo\nStok narciarski lśnił w słońcu. Ola w swoim jaskraworóżowym kombinezonie zapięła narty. Założyła kask i gogle, żeby chronić oczy. Ruszyła w dół, zostawiając za sobą ślad na świeżym śniegu. Mijała ośnieżone choinki, czując wiatr na twarzy.', ARRAY['http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png'], 0),
(7, 'Strażak i kot\nW sercu przytulnej angielskiej uliczki, z wesołymi, krzywymi domkami i czerwoną budką telefoniczną, rozegrała się akcja ratunkowa.\nPuszysty rudy kotek wspiął się na jesienne drzewo i nie mógł zejść! Mama z Tosią i Jasiem, mijając przystanek autobusowy, z niepokojem patrzyła w górę. Na szczęście, dzielny strażak w mig ustawił drabinę i z uśmiechem sięgnął po przestraszonego kotka.\nWszyscy odetchnęli z ulgą, a czerwony piętrowy autobus zatrąbił wesoło na cześć udanej misji ratunkowej!', ARRAY['http://10.0.2.2:8000/static/strazak_i_kot1.png', 'http://10.0.2.2:8000/static/strazak_i_kot2.png', 'http://10.0.2.2:8000/static/strazak_i_kot3.png'], 1),
(8, 'Marzenie o gwiazdach\nZosia od zawsze fascynowała się tym, co kryje nocne niebo. Zamiast bawić się lalkami, wolała przeglądać atlasy astronomiczne pełne zdjęć odległych galaktyk i mgławic.\nW dniu jej dziesiątych urodzin rodzice sprawili jej niesamowitą niespodziankę- prawdziwy teleskop. Gdy wieczorem ustawiła go na balkonie, po raz pierwszy zobaczyła kratery na Księżycu z taką dokładnością. Wyglądały jak tajemnicze blizny na srebrnej tarczy.\nW tej magicznej chwili Zosia podjęła ważną decyzję: w przyszłości zostanie astronautką, by osobiście odkrywać sekrety wszechświata i stąpać tam, gdzie nie dotarł jeszcze żaden człowiek.', ARRAY['http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png', 'http://10.0.2.2:8000/static/placeholder.png'], 2)
ON CONFLICT (exercise_id) DO NOTHING;


INSERT INTO exercise_question (exercise_id, text, image_url) VALUES
(9, 'Pani Kierowca\nPani Ewa prowadzi duży, zielony autobus miejski. Codziennie rano zabiera dzieci do szkoły, a dorosłych do pracy. Zatrzymuje się na przystanku przy parku. Pani Ewa zawsze wita pasażerów uśmiechem.\nDziś ma na sobie niebieski mundur i ciemne okulary, bo słońce mocno świeci. Pasażerowie bardzo ją lubią, bo jeździ bezpiecznie.', 'http://10.0.2.2:8000/static/placeholder.png'),
(10, 'Szybka wyścigówka\nPan Marek jest mechanikiem. Naprawia samochody w swoim warsztacie.\nDziś przyjechało do niego wyjątkowe auto. To czerwona wyścigówka z numerem jeden na masce. Samochód miał przebitą oponę.\nPan Marek szybko wziął klucz i nowe koło. W kilka minut auto było naprawione. Kierowca pomachał mechanikowi i ruszył z piskiem opon na tor wyścigowy.', 'http://10.0.2.2:8000/static/placeholder.png'),
(11, 'Nocna przygoda\nTo była pierwsza noc Kuby pod namiotem. Rozbili obóz na skraju lasu, tuż przy jeziorze.\nGdy słońce zaszło, zrobiło się ciemno, ale i przytulnie. Tata rozpalił małe ognisko, które dawało ciepło. Kuba siedział na pieńku i trzymał patyk z kiełbaską. W oddali pohukiwała sowa. Chłopiec czuł się jak prawdziwy podróżnik.', 'http://10.0.2.2:8000/static/placeholder.png'),
(12, 'Superbohater w domu\nKrzyś uwielbia komiksy o superbohaterach. Pewnego popołudnia postanowił sam zostać jednym z nich. Zawiązał czerwoną pelerynę z koca i założył papierową maskę. Biegał po ogrodzie, udając, że potrafi latać.\nNagle usłyszał wołanie taty. Okazało się, że tata nie mógł znaleźć swoich okularów. Super-Krzyś użył swojego „wzroku rentgenowskiego” i szybko zauważył zgubę pod gazetą na stoliku.\nTata uścisnął dłoń syna. Krzyś zrozumiał, że prawdziwy bohater to ktoś, kto pomaga innym w potrzebie.', 'http://10.0.2.2:8000/static/superbohater_w_domu.png'),
(13, 'Odkrywca dinozaurów\nNa gorącej pustyni pracował pan Adam, paleontolog. Miał kapelusz chroniący przed słońcem i torbę z narzędziami.\nOstrożnie omiatał pędzelkiem wystający z ziemi kamień. To nie był zwykły głaz, lecz skamieniała kość dinozaura! Pan Adam wstrzymał oddech z wrażenia. Właśnie odkrył fragment ogona gigantycznego jaszczura. Wiedział, że to znalezisko trafi do muzeum.', 'http://10.0.2.2:8000/static/placeholder.png'),
(14, 'Koncert fortepianowy\nSala koncertowa była wypełniona po brzegi. Ludzie siedzieli w eleganckich fotelach, czekając w ciszy.\nMała Hania weszła na scenę w swojej odświętnej, granatowej sukience. Ukłoniła się i usiadła przy wielkim, czarnym fortepianie. Kiedy jej palce dotknęły klawiszy, popłynęła piękna melodia. Hania grała utwór Chopina bez żadnego błędu. Po występie publiczność wstała i biła brawo bardzo długo.', 'http://10.0.2.2:8000/static/placeholder.png'),
(15, 'Sąsiedzka pomoc\nBył piękny poranek. Tosia w swojej żółtej sukience i Jaś w niebieskim sweterku spacerowali z ich wesołym pieskiem Reksiem. Gdy tak szli, mijając wystawę warzywniaka, zobaczyli swoją sąsiadkę, która wracała z zakupów.\nStarsza pani niosła ciężkie torby, ale nagle jedna z nich, papierowa i przeciążona, rozerwała się z głośnym szelestem! Soczyste, czerwone jabłka potoczyły się po brukowanej ulicy. Tosia i Jaś natychmiast przybiegli na pomoc, zbierając owoce. Reksio, choć chciał pomóc, ograniczył się do radosnego merdania ogonem i skakania wokół dzieci.\nSąsiadka uśmiechnęła się promiennie i podziękowała im z całego serca za ich uprzejmość. Ten drobny akt dobroci sprawił, że poranek w miasteczku stał się jeszcze piękniejszy.', 'http://10.0.2.2:8000/static/sasiedzka_pomoc.png'),
(16, 'Wielki Mecz\nTo była decydująca chwila finałowego meczu szkolnej ligi piłkarskiej. Murawa boiska lśniła od porannej rosy, a trybuny były pełne kibicujących uczniów.\nBartek, bramkarz drużyny „Orłów”, czuł na sobie ogromną odpowiedzialność. Przeciwnik ustawił piłkę na rzucie karnym. Wokół zapadła cisza. Bartek wziął głęboki oddech i skupił się na piłce. Gdy napastnik uderzył, bramkarz instynktownie rzucił się w prawy róg bramki. Złapał piłkę w locie! Rozległy się wiwaty i oklaski.\nDzięki jego koncentracji i refleksowi, „Orły” zdobyły puchar, a Bartek został bohaterem dnia.', 'http://10.0.2.2:8000/static/placeholder.png')
ON CONFLICT (exercise_id) DO NOTHING;


INSERT INTO questions (id_question, exercise_id, question, answers, correct_index) VALUES
(1, 9, 'Co robi Pani Ewa, gdy słońce mocno świeci?', ARRAY['Zakłada czapkę', 'Zakłada ciemne okulary', 'Zamyka okno'], 1),
(2, 10, 'Co było zepsute w wyścigówce?', ARRAY['Silnik', 'Drzwi', 'Opona'], 2),
(3, 11, 'Gdzie Kuba z tatą rozstawili namiot?', ARRAY['Pod domem w ogródku', 'W pobliżu lasu i jeziora', 'W środku samego lasu'], 1),
(4, 12, 'Co znalazł Krzyś?', ARRAY['Klucze', 'Okulary', 'Telefon'], 1),
(5, 13, 'Co odkrył pan Adam?', ARRAY['Skarb piratów', 'Kość dinozaura', 'Złotą monetę'], 1),
(6, 14, 'Na jakim instrumencie grała Hania?', ARRAY['Na skrzypcach', 'Na gitarze', 'Na fortepianie'], 2),
(7, 15, 'Jakie uczucie wyrażała sąsiadka po pomocy?', ARRAY['Niezadowolenie, że jabłka są teraz brudne', 'Zakłopotanie i zawstydzenie', 'Wdzięczność i ulgę'], 2),
(8, 16, 'Kiedy odbywał się mecz?', ARRAY['Rano', 'Po południu', 'Wieczorem'], 0)
ON CONFLICT (id_question) DO NOTHING;