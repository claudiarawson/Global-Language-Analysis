# Country code to name mapping
country_dict = {
    20: "Andorra", 32: "Argentina", 36: "Australia", 50: "Bangladesh", 51: "Armenia",
    68: "Bolivia", 76: "Brazil", 104: "Myanmar", 124: "Canada", 152: "Chile",
    156: "China", 158: "Taiwan", 170: "Colombia", 196: "Cyprus", 203: "Czechia",
    218: "Ecuador", 231: "Ethiopia", 276: "Germany", 300: "Greece", 320: "Guatemala",
    344: "Hong Kong SAR", 356: "India", 360: "Indonesia", 364: "Iran", 368: "Iraq",
    392: "Japan", 398: "Kazakhstan", 400: "Jordan", 404: "Kenya", 410: "South Korea",
    417: "Kyrgyzstan", 422: "Lebanon", 434: "Libya", 446: "Macau SAR", 458: "Malaysia",
    462: "Maldives", 484: "Mexico", 496: "Mongolia", 504: "Morocco", 528: "Netherlands",
    554: "New Zealand", 558: "Nicaragua", 566: "Nigeria", 586: "Pakistan", 604: "Peru",
    608: "Philippines", 630: "Puerto Rico", 642: "Romania", 643: "Russia", 688: "Serbia",
    702: "Singapore", 703: "Slovakia", 704: "Vietnam", 716: "Zimbabwe", 762: "Tajikistan",
    764: "Thailand", 788: "Tunisia", 792: "Turkey", 804: "Ukraine", 818: "Egypt",
    826: "Great Britain", 840: "United States", 858: "Uruguay", 860: "Uzbekistan",
    862: "Venezuela", 909: "Northern Ireland"
}

# Language code to name mapping
language_dict = {
    30: "Afar",
    40: "Afrikaans",
    100: "Albanian",
    140: "Amharic",
    170: "Arabic",
    200: "Armenian; Hayeren",
    230: "Assyrian Neo-Aramaic",
    245: "Auslan",
    250: "Avar; Avaric",
    290: "Aymara",
    310: "Azerbaijani; Azeri",
    350: "Balinese",
    370: "Balochi",
    410: "Banjar",
    460: "Batak",
    490: "Bengali; Bangla",
    500: "Berber; Amazigh; Tamaziɣt",
    520: "Betawi",
    550: "Bikol; Bicolano",
    610: "Romblomanon",
    630: "Blaan",
    680: "Brahui",
    710: "Buginese/Bugis",
    720: "Bulgarian",
    740: "Burmese",
    790: "Cantonese",
    810: "Catalan; Valencian",
    820: "Cebuano; Bisaya; Binisaya",
    850: "Chavacano; Chabacano",
    860: "Chechen",
    890: "Karanga; Korekore",
    910: "Ndau; chiNdau",
    950: "Chitoko",
    1030: "Croatian",
    1040: "Czech",
    1100: "Danish",
    1240: "English",
    1260: "Esan",
    1270: "Spanish; Castilian",
    1290: "Estonian",
    1360: "Filipino; Pilipino",
    1400: "French",
    1490: "Garifuna",
    1530: "German",
    1540: "Gilaki",
    1580: "Greek, Modern",
    1600: "Guarani",
    1610: "Gujarati",
    1670: "Hakka Chinese",
    1695: "Hassaniyya, Klem El Bithan",
    1700: "Hausa",
    1730: "Hiligaynon; Ilonggo",
    1740: "Hindi",
    1770: "Hungarian",
    1850: "Igbo",
    1880: "Ilocano; Ilokano; Iloko",
    1890: "Indonesian",
    1930: "Pamiri languages",
    1980: "Isoko",
    1990: "Italian",
    2000: "Itneg",
    2020: "Japanese",
    2030: "Javanese",
    2100: "Kalanga",
    2103: "Kalenjin",
    2120: "Kamayo",
    2126: "Kamba",
    2170: "Kapampangan",
    2180: "Kaqchikel",
    2210: "Kashmiri",
    2220: "Sgaw Karen; Sgaw Kayin; Karen",
    2230: "Kazakh",
    2270: "Central Khmer",
    2280: "Kikuyu; Gikuyu",
    2310: "Kirghiz; Kyrgyz",
    2316: "Kisii",
    2390: "Korean",
    2420: "Kurdish; Yezidi",
    2480: "Lampung",
    2500: "Lao",
    2530: "Mayan languages",
    2560: "Lezgian; Lezgi; Lezgin",
    2657: "Luhya",
    2670: "Lurish; Luri; Bakhtiari",
    2720: "Luo, Lwo; Lwoian",
    2740: "Madurese",
    2760: "Maguindanao",
    2790: "Makassarese",
    2810: "Malay; Malaysian",
    2820: "Malayalam",
    2840: "Maltese",
    2870: "Standard Chinese; Mandarin; Putonghua; Guoyu",
    2920: "Maori",
    2930: "Maranao",
    2940: "Marathi",
    2969: "Maasai",
    2981: "Meru",
    2987: "Mijikenda",
    3020: "Mon",
    3030: "Mongolian",
    3100: "Muong",
    3200: "North Ndebele",
    3234: "Northern Thai; Lanna",
    3390: "Oromo",
    3420: "Palembang",
    3490: "Persian; Farsi; Dari",
    3510: "Nigerian Pidgin",
    3520: "Polish",
    3530: "Portuguese",
    3540: "Punjabi, Panjabi",
    3550: "Pashto, Pushto",
    3570: "Quechua",
    3580: "Romanian, Moldavian, Moldovan",
    3600: "Romansh",
    3610: "Romani; Romany",
    3630: "Russian",
    3670: "Sama-Bajaw",
    3720: "Saraiki",
    3780: "Serbian",
    3810: "Shan",
    3830: "Shona; chiShona",
    3840: "Sidamo; Sidaama; Sidaamu Afoo",
    3860: "Sindhi",
    3870: "Sinhala, Sinhalese",
    3890: "Slovak",
    3920: "Somali",
    3992: "Southern Thai; Dambro; Pak Thai",
    4040: "Sundanese",
    4060: "Surigaonon",
    4075: "Swahili",
    4110: "Swedish",
    4130: "Tagalog",
    4150: "Hokkien; Minnan",
    4160: "Tajik",
    4190: "Tamil",
    4200: "Tatar",
    4210: "Tausug",
    4220: "Telugu",
    4230: "Thai; Central Thai",
    4260: "Tigrinya",
    4280: "Tiv",
    4295: "Tonga",
    4310: "Toraja-Saʼdan",
    4360: "Tunisian Arabic; Tunisian",
    4365: "Turkana",
    4370: "Turkish",
    4380: "Turkmen",
    4400: "Uighur; Uyghur",
    4410: "Ukrainian",
    4420: "Urdu",
    4430: "Urhobo",
    4450: "Uzbek",
    4460: "Venda; Tshivenda",
    4470: "Vietnamese",
    4520: "Waray",
    4580: "Yakan",
    4610: "Yiddish",
    4620: "Yoruba",
    9000: "Other",
    9040: "Other European",
    9060: "Other Chinese dialects",
    9900: "Other local; aboriginal; tribal, community"
}