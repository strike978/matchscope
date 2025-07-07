import requests
import flet as ft

REGION_LABELS = {
    "00100": "Senegal",
    "00200": "Mali",
    "00300": "Ivory Coast & Ghana",
    "00401": "Benin & Togo",
    "00402": "Yorubaland",
    "00403": "Central West Africa",
    "00501": "Central Nigeria",
    "00502": "North-Central Nigeria",
    "00503": "Nigeria",
    "00600": "Nigerian Woodlands",
    "00700": "Cameroon",
    "00750": "Western Bantu Peoples",
    "00760": "Twa",
    "00800": "Southern Bantu Peoples",
    "00900": "Eastern Bantu Peoples",
    "01000": "Nilotic Peoples",
    "01100": "Ethiopia & Eritrea",
    "01200": "Somalia",
    "01300": "Khoisan, Aka & Mbuti Peoples",
    "01400": "Northern Africa",
    "01500": "Egypt",
    "01600": "Arabian Peninsula",
    "01700": "Levant",
    "01800": "Cyprus",
    "01900": "Anatolia & the Caucasus",
    "02000": "Iran/Persia",
    "02001": "Lower Central Asia",
    "02002": "Northern Iraq & Northern Iran",
    "02100": "Burusho",
    "02200": "Indo-Gangetic Plain",
    "02301": "Western Himalayas & the Hindu Kush",
    "02302": "Gujarat",
    "02303": "Gulf of Khambhat",
    "02401": "Southern India",
    "02402": "Southwest India",
    "02403": "The Deccan & the Gulf of Mannar",
    "02500": "Bengal",
    "02600": "Nepal & the Himalayan Foothills",
    "02700": "Tibetan Peoples",
    "02800": "Northern Asia",
    "02900": "Mongolia & Upper Central Asia",
    "03000": "Korea",
    "03100": "Japan",
    "03200": "Southern Japanese Islands",
    "03300": "Northern China",
    "03350": "Western China",
    "03400": "Southwestern China",
    "03500": "Central & Eastern China",
    "03600": "Southern China",
    "03700": "Dai",
    "03800": "Mainland Southeast Asia",
    "03850": "Maritime Southeast Asia",
    "03900": "Vietnam",
    "04000": "Northern & Central Philippines",
    "04150": "Central & Southern Philippines",
    "04151": "Luzon",
    "04152": "Western Visayas",
    "04200": "Guam",
    "04300": "Melanesia",
    "04400": "Aboriginal and/or Torres Strait Islander Peoples",
    "04500": "Tonga",
    "04600": "Samoa",
    "04700": "Hawaii",
    "04800": "New Zealand Maori",
    "04900": "Indigenous Arctic",
    "05000": "Indigenous Americas—North",
    "05100": "Indigenous Americas—Mexico ",
    "05200": "Indigenous Americas— Yucatán Peninsula ",
    "05300": "Indigenous Americas—Central",
    "05400": "Indigenous Americas—Panama & Costa Rica",
    "05500": "Indigenous Cuba",
    "05600": "Indigenous Haiti & Dominican Republic",
    "05700": "Indigenous Puerto Rico",
    "05800": "Indigenous Americas—Colombia & Venezuela",
    "05900": "Indigenous Americas—Ecuador",
    "06000": "Indigenous Americas—Bolivia & Peru",
    "06100": "Indigenous Americas—Chile",
    "06200": "Indigenous Eastern South America",
    "06300": "Ashkenazi Jews",
    "06301": "Sephardic Jews",
    "06400": "Finland",
    "06500": "Sweden",
    "06501": "Denmark",
    "06600": "Norway",
    "06601": "Iceland",
    "06700": "Baltics",
    "06800": "Central & Eastern Europe",
    "06801": "Russia",
    "06900": "The Balkans",
    "06950": "Eastern European Roma",
    "07000": "Greece & Albania",
    "07100": "Aegean Islands",
    "07200": "Malta",
    "07300": "Sardinia",
    "07400": "Southern Italy & the Eastern Mediterranean",
    "07500": "Northern Italy",
    "07600": "France",
    "07700": "Germanic Europe",
    "07701": "The Netherlands",
    "07800": "Basque",
    "07900": "Spain",
    "08000": "Portugal",
    "08100": "England & Northwestern Europe",
    "08101": "Cornwall",
    "08200": "Wales",
    "08300": "Scotland",
    "08400": "Ireland",
}

COMMUNITY_LABELS = {
    "AFAM182021_1.1.1_1.1.2_Ghost": "Early Southern U.S. African Americans",
    "AFAM182021_1.1.3_1.1.4_Ghost": "Early Louisiana Creoles & African Americans",
    "AFAM182021_1.2": "Early South Carolina African Americans",
    "AFAM182021_1.3_1.4_Ghost": "Early North Carolina African Americans",
    "AFAM182021_1.6": "Central & Southern Mississippi & Eastern Louisiana African Americans",
    "AFAM182021_1.7": "Early Delmarva Peninsula African Americans",
    "AFAM192021_1.1.1.1_1.1.1.3_Ghost": "Upland South African Americans",
    "AFAM192021_1.1.1.4": "West Tennessee African Americans",
    "AFAM192021_1.1.2": "East Texas & Oklahoma African Americans",
    "AFAM192021_1.1.4": "Northern Louisiana & Southern Arkansas African Americans",
    "AFAM192021_1.1.5": "Eastern Louisiana & Western Mississippi African Americans",
    "AFAM192021_1.10_Ghost": "Southwestern Alabama African Americans",
    "AFAM192021_1.11": "Robeson County, North Carolina, Lumbee & African Americans",
    "AFAM192021_1.12": "Central Ohio & Northern West Virginia African Americans",
    "AFAM192021_1.13": "New York & New Jersey African Americans",
    "AFAM192021_1.2.3_1.2.5_1.2.7_1.2.8_Ghost": "Georgia Coastal Plain to Central Florida African Americans",
    "AFAM192021_1.2.9_1.2.1_1.2.2_Ghost": "Early Alabama & Georgia African Americans",
    "AFAM192021_1.4.10": "Afro-Bermudians",
    "AFAM192021_1.4.1_Ghost": "Jamaica",
    "AFAM192021_1.4.2_1.4.4_1.4.5_1.4.10_Ghost": "Afro-Caribbean Peoples of the Lesser Antilles",
    "AFAM192021_1.4.3": "Haiti",
    "AFAM192021_1.4.5": "Bahamas",
    "AFAM192021_1.4.6_1.4.7_Ghost": "Afro-Caribbean Peoples of Belize, Honduras & Nicaragua",
    "AFAM192021_1.5": "Coastal Carolina African Americans",
    "AFAM192021_1.6.2_1.6.6_1.6.7_1.6.8_Ghost": "Delmarva Peninsula & Chesapeake Bay African Americans",
    "AFAM192021_1.7": "South & Central Louisiana Creole & African Americans",
    "AFAM192021_DC_Area_Ghost": "Washington, D.C. Area African Americans",
    "AFAM192021_MS_inland_Ghost": "Inland Mississippi African Americans",
    "AFAM192021_NC_Ghost": "Lower Chesapeake Bay to Northeast North Carolina African Americans",
    "AFAM192021_SC_Ghost": "South Carolina African Americans",
    "AFAM192021_VA_Ghost": "Virginia & Southern Ohio African Americans",
    "ASIA2023_1.1.1.4_1.1.1.3_Ghost": "Japan",
    "ASIA2023_1.1.3": "Okinawa",
    "ASIA2023_1.2.1": "Eastern & Southeastern China",
    "ASIA2023_1.3.1.4": "Parsis in India",
    "ASIA2023_1.3.15": "Asians in South Africa",
    "ASIA2023_1.3.16": "Sri Lanka",
    "ASIA2023_1.3.2.3": "Peninsular Malaysia",
    "ASIA2023_1.3.3.2": "Mascarene Islands",
    "ASIA2023_1.3.4": "Bengal Delta",
    "ASIA2023_1.3.5": "Goans",
    "ASIA2023_1.3.8": "Southeast India",
    "ASIA2023_1.4.2": "Thailand",
    "ASIA2023_1.4.8": "Vietnam",
    "ASIA2023_1.5": "Korea",
    "ASIA2023_1.6.1": "Indentured Indian Diaspora",
    "ASIA2023_1.6.2": "Lesser Antilles & Guyana",
    "ASIA2023_1.6.3": "South Asians in Jamaica",
    "ASIA2023_2.1.1": "Fujian & Taiwan",
    "ASIA2023_2.1.2_2.1.4_Ghost": "Central Luzon & North Central Calabarzon",
    "ASIA2023_2.1.3_2.1.6_Ghost": "Calabarzon & Manila",
    "ASIA2023_2.1.5": "Bicol",
    "ASIA2023_2.2.1_2.2.2_2.2.3_Ghost": "Northern & Central Luzon & Central Calabarzon",
    "ASIA2023_2.3": "Central & Eastern Visayas",
    "ASIA2023_2.4": "Western Visayas",
    "ASIA2023_3.3.1.1.2": "Polynesia",
    "ASIA2023_3.3.2.3": "Tonga",
    "ASIA2023_3.3.2.4": "Fiji",
    "ASIA2023_4.2": "North Indian Muslims",
    "ASIA2023_4.3_Ghost": "Khatri & Arora Punjabis",
    "ASIA2023_4.4": "Central Asia—North",
    "ASIA2023_4.6": "Gujarat",
    "ASIA2023_4.9": "Punjabi & Sindhi Hindu",
    "ASIA2023_5": "Guam",
    "ASIA2023_AdmixedIndia_Ghost": "Anglo-Indians",
    "ASIA2023_Guangdong_Ghost": "Guangdong",
    "ASIA2023_Hawaii_Ghost": "Hawaiian Islands",
    "ASIA2023_Indonesia_Ghost": "Indonesia",
    "ASIA2023_NewZealand_Ghost": "New Zealand",
    "ASIA2023_Samoa_Ghost": "Samoan Islands",
    "AUNZ2019_1.1": "New Zealand, European & British Settlers",
    "AUNZ2019_1.2": "Victoria, Australia, European & British Settlers",
    "AUNZ2019_1.4": "South Australia, European & British Settlers",
    "AUNZ2019_1.5": "Tasmania, European & British Settlers",
    "AUNZ2019_1.6": "Western Australia, European & British Settlers",
    "AUNZ2019_2.1_2.3_2.4_2.5_2.6_2.7_2.10": "New South Wales, Australia, European & British Settlers",
    "AUNZ2019_2.2": "Queensland, European & British Settlers",
    "CA2018_594.64": "Cardston, Alberta Mormon Pioneers",
    "CA2023_1.4.16": "Prince Edward Island",
    "CA2023_1.5": "New Brunswick",
    "CA2023_3": "Newfoundland & Labrador",
    "CA2023_EastOntario_Ghost": "Eastern Ontario & Southwestern Quebec",
    "CA2023_NovaScotia_Ghost": "Nova Scotia",
    "CA2023_Ontario_Ghost": "Southwestern & Central Ontario",
    "CA2023_Ottowa_Ghost": "Eastern Ontario",
    "DE_2021_1.1.1.1.4.2": "German Palatines in Lower Austria, Central Poland & Western Ukraine",
    "DE_2021_1.1.1.3.6": "Germans on the Ontario Peninsula",
    "DE_2021_1.1.1_Ghost": "Baden-Württemberg & Hesse",
    "DE_2021_1.1.2.3": "Bavaria-Bohemia Borderlands",
    "DE_2021_1.1.2_Ghost": "Franconia",
    "DE_2021_1.1.3.1": "Luxembourg",
    "DE_2021_1.2.4.1": "Northeastern Germany",
    "DE_2021_1.2.4.2": "Schleswig-Holstein",
    "DE_2021_1.3.1_1.3.3_Ghost": "Northwestern Germany",
    "DE_2021_1.3.2.1.3": "Belgium",
    "DE_2021_3.4.1.1_1.1.1.3.4_Ghost": "Switzerland",
    "DE_2021_7.1": "Catholic Black Sea Germans",
    "DE_2021_7.2_7.5_Ghost": "German Anabaptists",
    "DE_2021_7.3": "Protestant Black Sea Germans",
    "DE_2021_7.4_1.1.1.5_Ghost": "Volga Germans",
    "DE_2021_EastGermany_Ghost": "Central & Eastern Germany",
    "DE_2021_Netherlands_Ghost": "The Netherlands",
    "DE_2021_Rhineland_Ghost": "The Rhineland",
    "DE_2021_RomaniaGermans_Ghost": "Germans in Romania",
    "EEU2023_4.2.1.1": "Eastern Ukraine",
    "EEU2023_Austria_Ghost": "Austria",
    "EEU2023_Belarus_Ghost": "Eastern Lithuania & Western Belarus",
    "EEU2023_CzechBohemia_Ghost": "Central & Western Czechia",
    "EEU2023_CzechMoravia_Ghost": "Central & Eastern Czechia",
    "EEU2023_Estonia_Ghost": "Estonia",
    "EEU2023_GreaterPoland_Ghost": "West Central Poland",
    "EEU2023_HungaryEast_Ghost": "Eastern Hungary",
    "EEU2023_HungaryWest_Ghost": "Western Hungary",
    "EEU2023_Latvia_Ghost": "Latvia",
    "EEU2023_LesserPoland_Ghost": "Western Galicia",
    "EEU2023_Lithuania_Ghost": "Lithuania",
    "EEU2023_PodlachiaWarmiaMasuria_Ghost": "North Central Poland",
    "EEU2023_PolandMasovia_Ghost": "Mazovia",
    "EEU2023_PolandPomerania_Ghost": "Gdansk Pomerania",
    "EEU2023_PolandSilesia_Ghost": "South Central Poland",
    "EEU2023_Russia_Ghost": "Russia",
    "EEU2023_Slovakia_Ghost": "Slovakia",
    "EEU2023_UkraineWest_Ghost": "Western Ukraine",
    "EJ2019_2.2": "Ashkenazi Jews in Central & Eastern Europe",
    "EJ2019_3.2": "Ashkenazi Jews in Northeastern Europe",
    "FRAM2019_1.1": "Southwestern Quebec, New York & Vermont French Settlers",
    "FRAM2019_1.2": "Southeastern Quebec French Settlers",
    "FRAM2019_1.3": "Southwestern Quebec French Settlers",
    "FRAM2019_1.3.3": "Southeast Michigan & St. Louis, Missouri French Settlers",
    "FRAM2019_4.1": "Canadian Maritimes Acadians",
    "FRAM2019_4.2": "Southern Louisiana French Settlers",
    "FRAM2019_4.3": "East Central Louisiana Acadians",
    "France2021_1.1.5.2": "France",
    "GreatBritain_2021_1.1.1_1.1.3_Ghost": "East of England",
    "GreatBritain_2021_1.1.2.1_1.1.2.2_1.1.2.3_Ghost": "Greater London to Southern East Midlands ",
    "GreatBritain_2021_1.2.1_1.3.1_Ghost": "Central Southern England",
    "GreatBritain_2021_1.2.2_1.2.3_1.2.4_Ghost": "Eastern South East England",
    "GreatBritain_2021_1.3.2": "Birmingham",
    "GreatBritain_2021_1.4.1": "Devon, Dorset & Somerset",
    "GreatBritain_2021_1.4.2_1.4.3_Ghost": "Cornwall",
    "GreatBritain_2021_2.1.1": "Scotland Central Belt",
    "GreatBritain_2021_2.1.2_2.1.3_Ghost": "Northern Ireland & Southwest Scotland",
    "GreatBritain_2021_2.1.4": "Southwestern Scotland & Northern Ulster",
    "GreatBritain_2021_2.3.1_2.3.2_2.3.3_Ghost": "Scottish Highlands & the Hebrides",
    "GreatBritain_2021_2.3.4": "Southern Hebrides & Southwestern Scottish Highlands",
    "GreatBritain_2021_2.4.1_2.4.2_Ghost": "East & Central Scottish Lowlands",
    "GreatBritain_2021_2.4.3": "Northeast Scotland & Orkney & the Shetland Islands",
    "GreatBritain_2021_2.5": "North England & Scotland Border",
    "GreatBritain_2021_3.1.1_3.1.2_3.1.3_Ghost": "East Midlands, Yorkshire & North England",
    "GreatBritain_2021_3.2.2.2_1.3.3_Ghost": "Wales",
    "GreatBritain_2021_3.2.5": "Isle of Man",
    "GreatBritain_2021_3.3.1_3.3.2_3.3.3_Ghost": "The Midlands",
    "GreatBritain_NWEngland_Ghost": "North West England & Northern Wales",
    "IRL2018_1.1.1": "Donegal, Ireland",
    "IRL2018_1.1.3_1.1.2": "Connacht, Ireland",
    "IRL2018_1.2.10": "Ulster",
    "IRL2018_1.2.5_1.2.3": "Central Ireland",
    "IRL2018_1.2.6": "Leinster",
    "IRL2018_1.3": "Munster, Ireland",
    "LA182019_2.2.1": "Cuba, Canary Islands & Uruguay",
    "LA182019_2.2.2": "Northern Spain & Argentina",
    "LA182019_2.2.3": "Central & Eastern Cuba",
    "LA182019_2.2.4": "Central & Western Cuba",
    "LA182019_2.2.5": "Venezuela",
    "LA182019_2.3.1.1_2.3.1.2": "El Salvador",
    "LA182019_2.3.1.3": "Honduras & Belize",
    "LA182019_2.3.2": "Guatemala",
    "LA182019_2.3.3.1": "Nicaragua",
    "LA182019_2.3.3.2": "Costa Rica",
    "LA182019_2.3.4": "Panama",
    "LA182019_2.4.1.1_2.4.1.2_2.4.1.4_2.4.1.5": "Peru",
    "LA182019_2.4.1.3": "Bolivia",
    "LA182019_2.4.2.1": "Southern Spain",
    "LA182019_2.4.2.2": "Spain, France & Basque Country",
    "LA182019_2.4.2.4": "Northern Spain",
    "LA182019_2.4.3": "Chile",
    "LA182019_2.4.4": "Argentina & Paraguay",
    "LA182019_2.5.1_2.5.2": "Colombia",
    "LA182019_2.5.3": "Ecuador",
    "LA182019_2.7": "Dominican Republic",
    "LA192019_2.1.1.1": "Portuguese in Southern Brazil",
    "LA192019_2.1.1.2": "Portuguese in Northern Brazil",
    "LA192019_2.1.2_2.1.3_2.1.6_2.1.7": "Azores",
    "LA192019_2.1.4": "Madeira",
    "LA192019_2.1.5": "Portuguese in Hawaii & California",
    "LA192019_2.8": "Portuguese Islanders in the Eastern U.S.",
    "MENA2019_1.4.1": "South Greece",
    "MENA2019_1.4.2.1": "Albania, Northern Greece & North Macedonia",
    "MENA2019_1.4.2.2.1": "Bulgaria",
    "MENA2019_1.4.2.2.2_1.4.2.2.3": "Romania",
    "MENA2019_1.4.2.3": "Western Balkans",
    "MENA2019_1.4.3": "West Anatolia & Aegean Islands",
    "MENA2019_1.6.4": "Eastern Africa",
    "MENA2023_1.1": "Eastern Anatolia & Armenia",
    "MENA2023_1.3": "Anatolian Turks",
    "MENA2023_1.4_Ghost": "North Anatolia Pontian Greeks",
    "MENA2023_1.5": "Northern Iraq & Iran",
    "MENA2023_1.6": "Eastern Armenia & Iran",
    "MENA2023_1.7": "Georgia",
    "MENA2023_1.8": "Southern & Eastern European Roma",
    "MENA2023_2.1.5": "Central Asia—South ",
    "MENA2023_2.2.1": "Morocco & Western Algeria",
    "MENA2023_2.2.2": "Arabian Peninsula",
    "MENA2023_2.2.3": "Iraq",
    "MENA2023_2.2.4": "Algeria",
    "MENA2023_2.2.5": "Tunisia & Western Libya",
    "MENA2023_2.2.6": "Gulf of Aden",
    "MENA2023_2.3": "Sephardic Jews in the Eastern Mediterranean",
    "MENA2023_2.4": "Mizrahi Jews of Iraq & Iran",
    "MENA2023_2.5": "Sephardic Jews of North Africa",
    "MENA2023_3.1_3.2_3.4_Ghost": "Lebanon",
    "MENA2023_3.3": "Western Levant",
    "MENA2023_4.1_4.3_Ghost": "Southern Levant",
    "MENA2023_4.2": "Egypt",
    "MENA2023_Cyprus_Ghost": "Cyprus",
    "MENA2023_Iran_Ghost": "Iran",
    "Mexico_2021_1.1.1": "San Luis Potosí, Aguascalientes & Central Zacatecas",
    "Mexico_2021_1.1.2_1.1.5_Ghost": "Guanajuato",
    "Mexico_2021_1.1.3": "East Central Mexico",
    "Mexico_2021_1.1.4": "Central & Southern Mexico",
    "Mexico_2021_1.1.6": "Yucatán",
    "Mexico_2021_1.2.4": "Durango",
    "Mexico_2021_1.3.1": "Sonora & Southern Arizona",
    "Mexico_2021_1.3.2_1.3.4_Ghost": "Sinaloa",
    "Mexico_2021_1.3.3_1.7.3_Ghost": "Baja California Peninsula & the California Coast",
    "Mexico_2021_1.4": "Jalisco, Colima & Michoacán",
    "Mexico_2021_1.5": "Aguascalientes & Eastern Jalisco",
    "Mexico_2021_1.6": "Zacatecas",
    "Mexico_2021_2.1": "Eastern Mexico & Southern Texas",
    "Mexico_2021_2.2_2.3_2.4_Ghost": "Northeastern Mexico & Southern Texas",
    "Mexico_2021_2.5": "Nacogdoches, Texas to Natchitoches, Louisiana",
    "Mexico_2021_3.1": "Southern Colorado & New Mexico",
    "Mexico_2021_3.2": "New Mexico",
    "Mexico_2021_NorthMex_Ghost": "Chihuahua, West Texas & Southern New Mexico",
    "NA9_PPR_3": "Puerto Rico",
    "SCAND2018_1.1": "Central & Southern Sweden",
    "SCAND2018_1.2": "Northern Sweden",
    "SCAND2018_1.3": "Southern Sweden",
    "SCAND2018_1.4": "Central Sweden",
    "SCAND2018_3.1": "Western Norway",
    "SCAND2018_3.2": "Eastern Norway",
    "SCAND2018_3.3": "Southern & Southwestern Norway",
    "SCAND2018_3.4": "Southeastern, Central & Northern Norway",
    "SCAND2018_4.2": "Iceland",
    "SCAND2018_5.3.5": "Denmark",
    "SCAND2018_6.1": "Western Finland",
    "SCAND2018_6.3": "Ostrobothnia, Central Ostrobothnia & South Ostrobothnia, Finland",
    "SCAND2018_6.4": "Central & Southern Finland",
    "SEUR2019_1.5.1": "Slovenia & Northwest Croatia",
    "SEUR2019_1.5.2": "Western Croatia",
    "SEUR2019_1.5.3": "Croatia",
    "SEUR2019_1.5.5": "Northeast Italy",
    "SEUR2019_2.1": "Southeastern Sicily",
    "SEUR2019_2.2": "Apulia Region",
    "SEUR2019_2.3": "Central Southwest Italy",
    "SEUR2019_2.4": "North Italy",
    "SEUR2019_2.5": "Central Eastern Italy",
    "SEUR2019_2.6": "Northern Sicily",
    "SEUR2019_2.7": "Calabria",
    "SouthAfrica_top.2": "South Africa, European Settlers",
    "US_NSCW_18th_2021_2.1.1": "Southern Midwestern Settlers",
    "US_NSCW_18th_2021_2.1.2": "Early Upper South Settlers ",
    "US_NSCW_18th_2021_2.1.3": "Southern Backcountry to Oklahoma & Texas Settlers",
    "US_NSCW_18th_2021_2.1.4": "Southern Appalachia Settlers",
    "US_NSCW_18th_2021_2.2.1": "Early Alabama, Mississippi, Louisiana & East Texas Settlers",
    "US_NSCW_18th_2021_2.2.2": "Early Georgia Coastal Plain & Northern Florida Settlers",
    "US_NSCW_18th_2021_2.3.1": "West Virginia, Kentucky & Tennessee Settlers",
    "US_NSCW_18th_2021_2.3.2": "Eastern Kentucky & Western West Virginia Settlers",
    "US_NSCW_18th_2021_2.3.3": "Appalachian Settlers of Kentucky",
    "US_NSCW_18th_2021_2.3.4": "Northwestern North Carolina Settlers",
    "US_NSCW_18th_2021_Ghost_NC_Coast": "Eastern North Carolina Settlers",
    "US_NSCW_19th_2021_1.1.3": "Arkansas, Oklahoma & Texas Settlers",
    "US_NSCW_19th_2021_1.1.4": "Western Gulf States Settlers",
    "US_NSCW_19th_2021_1.4.1": "St. Louis, Missouri & Western U.S. Settlers",
    "US_NSCW_19th_2021_1.7.1": "Upper Midwest & Western U.S. Settlers",
    "US_NSCW_19th_2021_1.7.2": "Northern Utah & Southeast Idaho Settlers",
    "US_NSCW_19th_2021_1.7.4": "Southern Utah & Arizona Settlers",
    "US_NSCW_19th_2021_1.7.56": "Utah Settlers",
    "US_NSCW_19th_2021_Ghost_AL": "Alabama Settlers",
    "US_NSCW_19th_2021_Ghost_GA_FL": "Georgia & Florida Settlers",
    "US_NSCW_19th_2021_Ghost_KY": "Kentucky Settlers",
    "US_NSCW_19th_2021_Ghost_NC": "North Carolina Settlers",
    "US_NSCW_19th_2021_Ghost_SC": "South Carolina & North Carolina Border Settlers",
    "US_NSCW_19th_2021_Ghost_SouthCentral": "Northern Upland South Settlers",
    "US_NSCW_19th_2021_Ghost_TN": "Tennessee Settlers",
    "US_NSCW_19th_2021_Ghost_VA": "Virginia & Eastern Kentucky Settlers",
    "US_NSCW_19th_2021_Ghost_WV": "West Virginia Settlers",
    "US_NSC_18th_2019_1.2.1": "Delaware Valley, Chesapeake & Midwest Settlers",
    "US_NSC_18th_2019_1.2.2": "Early Pennsylvania Settlers",
    "US_NSC_18th_2019_1.2.3": "North Central Appalachia Settlers",
    "US_NSC_18th_2019_1.2.4": "Eastern Ohio River Valley & Northern Blue Ridge Mountains Settlers",
    "US_NSC_18th_2019_1.3.1": "Early Connecticut & New York Settlers",
    "US_NSC_18th_2019_1.3.2": "Early New England Settlers",
    "US_NSC_19th_2019_1.2.7": "Southern Pennsylvania, Northern Ohio, Indiana & Illinois Settlers",
    "US_NSC_19th_2019_1.4.6": "Kansas & Southern Nebraska Settlers",
    "US_NSC_19th_Ghost_CT_MA_RI": "Southern New England Settlers",
    "US_NSC_19th_Ghost_IA_NE_ND_SD": "Upper Midwest Settlers",
    "US_NSC_19th_Ghost_IN_IL": "Illinois & Indiana Settlers",
    "US_NSC_19th_Ghost_MD_DE": "Delaware & Chesapeake Bay Settlers",
    "US_NSC_19th_Ghost_ME_NH_VT": "Northern New England Settlers",
    "US_NSC_19th_Ghost_MI": "Michigan Settlers",
    "US_NSC_19th_Ghost_MN": "Southern Minnesota & Northwestern Wisconsin Settlers",
    "US_NSC_19th_Ghost_MO": "Missouri Settlers",
    "US_NSC_19th_Ghost_NJ": "New Jersey & Eastern Pennsylvania Settlers",
    "US_NSC_19th_Ghost_NY_VT_NorthPA": "Northern Mid-Atlantic Settlers",
    "US_NSC_19th_Ghost_NorthOH_IN": "Ohio, Indiana & Eastern Kentucky Settlers",
    "US_NSC_19th_Ghost_PA_NorthwestMD_EastOH_NorthWV": "Pennsylvania, Eastern Ohio, Northern West Virginia & Maryland Settlers",
    "US_NSC_19th_Ghost_WI": "Early Wisconsin Settlers",
}


def parse_cookie_string(cookie_string):
    cookies = {}
    if not cookie_string:
        return cookies
    cookie_string = cookie_string.strip()
    # Accept both semicolon and newline as delimiters, robustly
    import re
    # Split on semicolon or newline, ignore empty parts
    pairs = re.split(r';|\n', cookie_string)
    for pair in pairs:
        pair = pair.strip()
        if not pair:
            continue
        if '=' in pair:
            k, v = pair.split('=', 1)
            cookies[k.strip()] = v.strip()
    return cookies


def get_common_headers():
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.8",
        "ancestry-context-ube": "eyJldmVudElkIjoiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwIiwiY29ycmVsYXRlZFNjcmVlblZpZXdlZElkIjoiY2FkNzQ3ZTQtODY2ZS00YjMxLWFiMTQtMTEzOTA5MzUzODg3IiwiY29ycmVsYXRlZFNlc3Npb25JZCI6ImQ5ZWRiOGRiLTYzMTEtNGRhMS1iNjM0LTlkMmQxYWUwMzZmZiIsInNjcmVlbk5hbWVTdGFuZGFyZCI6IiIsInNjcmVlbk5hbWUiOiIiLCJ1c2VyQ29uc2VudCI6Im5lY2Vzc2FyeXxwcmVmZXJlbmNlfHBlcmZvcm1hbmNlfGFuYWx5dGljczFzdHxhbmFseXRpY3MzcmR8YWR2ZXJ0aXNpbmcxc3R8YXR0cmlidXRpb24zcmQiLCJ2ZW5kb3JzIjoiIiwidmVuZG9yQ29uZmlndXJhdGlvbnMiOiJ7fSJ9",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE2OTA1NzAiLCJhcCI6IjMxMjUwMjkyMyIsImlkIjoiNTg2NjcwY2EzMWEwZDA2OCIsInRyIjoiYjNjMjQzZTU0YzA3OWViYTg0NzU1ODVkYTQxZTIyNjkiLCJ0aSI6MTc1MTM4NjY3MjQxNywidGsiOiIyNjExNzUwIn19",
        "priority": "u=1, i",
        "referer": "https://www.ancestry.com/",
        "sec-ch-ua": "",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "traceparent": "00-b3c243e54c079eba8475585da41e2269-586670ca31a0d068-01",
        "tracestate": "2611750@nr=0-1-1690570-312502923-586670ca31a0d068----1751386672417",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }


def get_csrf_token(cookies):
    import re
    csrf_cookie = cookies.get('_dnamatches-matchlistui-x-csrf-token')
    if csrf_cookie:
        return re.split(r'%7C|\|', csrf_cookie)[0]
    return None


VERSION = "0.8-BETA"


def main(page: ft.Page):
    # Centralized delay for all per-match and per-skip waits
    MATCH_PROCESS_DELAY = 0.3
    # Helper to update custom match count label only

    def update_custom_match_count_label():
        match_type_radio.content.controls[3].label = get_match_type_label(
            "custom")
        page.update()

    page.title = f"MatchScope v{VERSION}"
    page.window_title_bar_hidden = False
    page.window_title_bar_buttons_hidden = False
    # Set app icon if supported
    try:
        page.window_icon = "icon.ico"
    except Exception:
        pass

    # Preload cookie.txt content if available
    try:
        with open("cookie.txt", "r", encoding="utf-8") as f:
            cookie_txt_content = f.read().strip()
    except Exception:
        cookie_txt_content = ""
    text_area = ft.TextField(
        multiline=True,
        min_lines=10,
        max_lines=20,
        width=800,
        label="🍪 Paste your AncestryDNA browser cookie here",
        value=cookie_txt_content,
        visible=True,
        read_only=False
    )
    # Column of Rows, each Row holds up to 5 Cards (horizontal layout, 5 per row)
    output_cards_grid = ft.Column([], width=900, spacing=10)

    # Text widget for processing status below progress bar
    processing_status_text = ft.Text(value="", size=16, selectable=False)
    # Text widget for time left notification below the progress bar
    time_left_text = ft.Text(
        value="", size=14, color="#888888", selectable=False)
    test_dropdown = ft.Dropdown(
        label="Select DNA Test", options=[], visible=False, width=400)
    # Radio buttons for match type
    # Store match counts for each type
    match_type_counts = {"all": None, "close": None, "distant": None}

    def get_match_type_label(mt):
        base = {
            "all": "All matches",
            "close": "Close matches (4th cousin or closer)",
            "distant": "Distant matches",
            "custom": "Custom centimorgan range"
        }[mt]
        count = match_type_counts.get(mt) if mt in match_type_counts else None
        # Show count for all types, including custom
        if mt == "custom":
            return f"{base} ({count if count is not None else '...'})"
        return f"{base} ({count if count is not None else '...'})"

    # Custom cM range input fields (hidden until match counts are fetched)
    custom_min_cm = ft.TextField(
        label="Min cM (min of 6 cM)",
        width=100,
        visible=False
    )
    custom_max_cm = ft.TextField(
        label="Max cM (max of 3,490 cM)",
        width=120,
        visible=False
    )

    def on_match_type_change(e):
        # Do not show/hide custom cM fields here; handled after match count fetch
        # If custom is selected, update the label with the latest count
        if match_type_radio.value == "custom":
            # Optionally, trigger a fetch for the custom count
            fetch_and_show_match_count()
        else:
            page.update()

    def on_custom_cm_change(e):
        # Only update label if custom is selected and both fields are filled with valid ints
        min_val = custom_min_cm.value.strip()
        max_val = custom_max_cm.value.strip()
        if match_type_radio.value == "custom":
            if min_val and max_val:
                try:
                    lower = int(min_val)
                    upper = int(max_val)
                    if lower <= upper:
                        # Call fetch_and_show_match_count in a new thread to avoid blocking UI
                        import threading
                        threading.Thread(
                            target=fetch_and_show_match_count).start()
                        return
                    else:
                        match_type_counts["custom"] = None
                        match_type_radio.content.controls[3].label = get_match_type_label(
                            "custom")
                        page.update()
                except Exception:
                    match_type_counts["custom"] = None
                    match_type_radio.content.controls[3].label = get_match_type_label(
                        "custom")
                    page.update()
            else:
                match_type_counts["custom"] = None
                match_type_radio.content.controls[3].label = get_match_type_label(
                    "custom")
                page.update()

    custom_min_cm.on_change = on_custom_cm_change
    custom_max_cm.on_change = on_custom_cm_change

    match_type_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="all", label=get_match_type_label("all")),
            ft.Radio(value="close", label=get_match_type_label("close")),
            ft.Radio(value="distant", label=get_match_type_label("distant")),
            ft.Radio(value="custom", label=get_match_type_label("custom")),
        ]),
        value="all",
        visible=False,
        on_change=on_match_type_change
    )
    number_input = ft.TextField(
        label="Number",
        value="50",
        width=80,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    get_matches_btn = ft.ElevatedButton("Get Matches", visible=False)
    pause_btn = ft.ElevatedButton("Pause", visible=False)
    resume_btn = ft.ElevatedButton("Resume", visible=False)
    matches_thread = None  # Track the running thread
    import threading
    pause_event = threading.Event()
    resume_event = threading.Event()
    run_id = 0  # Incremented each time Get Matches is clicked
    # Remove match_count_text, use only match_count_number
    progress_bar = ft.ProgressBar(value=0.0, width=400, visible=False)

    tests_data = {}

    # Create a single SnackBar instance and add it to the page
    snack_bar = ft.SnackBar(content=ft.Text(""), open=False)
    page.snack_bar = snack_bar
    page.overlay.append(snack_bar)

    def show_message(msg):
        snack_bar.content.value = msg
        snack_bar.open = True
        page.update()

    def clear_clicked(e):
        text_area.value = ""
        output_cards_grid.controls.clear()
        processing_status_text.value = ""
        test_dropdown.options = []
        test_dropdown.visible = False
        # removed match_count_number
        number_input.value = "50"
        number_input.visible = False
        custom_min_cm.visible = False
        custom_max_cm.visible = False
        page.update()

    def authenticate_clicked(e):
        cookie_string = text_area.value.strip()
        if not cookie_string:
            show_message("Please enter cookies.")
            return
        cookies = parse_cookie_string(cookie_string)
        headers = get_common_headers()
        url = "https://www.ancestry.com/api/navheaderdata/v1/header/data/user"
        try:
            resp = requests.get(url, headers=headers, cookies=cookies)
            if resp.status_code == 200:
                auth_json = resp.json()
                name = auth_json.get('user', {}).get('name')
                if name:
                    # Fetch tests
                    fetch_tests(headers, cookies)
                    test_dropdown.visible = True
                    text_area.visible = False
                    auth_btn.visible = False
                    clear_btn.visible = False
                    # custom_min_cm and custom_max_cm remain hidden until match count is fetched
                    show_message(f"Authenticated as {name}")
                else:
                    show_message("Authentication failed.")
            else:
                show_message("Authentication failed.")
        except Exception as ex:
            show_message(f"Error: {ex}")
        number_input.visible = False
        custom_min_cm.visible = False
        custom_max_cm.visible = False
        page.update()

    def fetch_tests(headers, cookies):
        url = 'https://www.ancestry.com/dna/insights/api/dnaSubnav/tests'
        test_headers = headers.copy()
        test_headers['accept'] = 'application/json'
        test_headers['content-type'] = 'application/json'
        test_headers.pop('referer', None)
        try:
            resp = requests.get(url, headers=test_headers, cookies=cookies)
            tests_json = resp.json()
            nonlocal tests_data
            tests_data = {(t.get('testGuid') or t.get('subjectName')): t for t in tests_json.get('dnaSamplesData', [])}
            test_dropdown.options = [ft.dropdown.Option(key=k, text=t.get(
                'subjectName') or k) for k, t in tests_data.items()]
        except Exception as ex:
            test_dropdown.options = []
            show_message(f"Failed to fetch tests: {ex}")
        page.update()

    # Communities filter group: label and checkboxes inside a Card with border
    communities_checkbox_label = ft.Row([
        ft.Icon(name=ft.Icons.GROUPS, color="#1565c0", size=26),
        ft.Text(
            "Communities Filter: Grab matches with ONLY the selected communities",
            size=16, weight=ft.FontWeight.BOLD, visible=True
        )
    ], visible=False, spacing=10)
    communities_checkbox_column = ft.Column(
        controls=[], visible=False, spacing=4)
    communities_filter_group = ft.Card(
        content=ft.Container(
            content=ft.Column([
                communities_checkbox_label,
                communities_checkbox_column
            ], spacing=8),
            padding=ft.padding.all(18),
            border=ft.border.all(2, "#1565c0"),  # strong blue border
            border_radius=14,
            # No background color, use default
            # No shadow
        ),
        visible=False
    )

    def dropdown_changed(e):
        selected = test_dropdown.value
        if not selected or selected not in tests_data:
            get_matches_btn.visible = False
            number_input.visible = False
            match_type_radio.visible = False
            custom_min_cm.visible = False
            custom_max_cm.visible = False
            communities_checkbox_label.visible = False
            communities_checkbox_column.visible = False
            communities_checkbox_column.controls = []
            page.update()
            return
        get_matches_btn.visible = True
        number_input.visible = True
        match_type_radio.visible = True
        match_options_card.visible = True
        # Hide custom cM fields until match count is fetched (handled in card)
        custom_min_cm.visible = False
        custom_max_cm.visible = False

        # Hide old communities UI, show group
        communities_checkbox_label.visible = False
        communities_checkbox_column.visible = False
        communities_filter_group.visible = True

        # Fetch and show communities for the selected test as checkboxes, with label
        def fetch_communities():
            test = tests_data[selected]
            cookie_string = text_area.value.strip()
            cookies = parse_cookie_string(cookie_string)
            headers = get_common_headers()
            headers['referer'] = f"https://www.ancestry.com/discoveryui-matches/"
            headers['content-type'] = 'application/json'
            csrf_token = get_csrf_token(cookies)
            if csrf_token:
                headers['x-csrf-token'] = csrf_token
            try:
                url = f"https://www.ancestry.com/dna/origins/secure/tests/{selected}/branches"
                resp = requests.get(url, headers=headers, cookies=cookies)
                if resp.status_code == 200:
                    data = resp.json()
                    # Only collect top-level community IDs (not nested)
                    top_level_ids = []
                    if isinstance(data, list):
                        for entry in data:
                            if 'id' in entry:
                                top_level_ids.append(entry['id'])
                    if top_level_ids:
                        # Use COMMUNITY_LABELS to get names
                        checkboxes = []
                        for cid in top_level_ids:
                            name = COMMUNITY_LABELS.get(cid, cid)
                            cb = ft.Checkbox(label=f"{name}", value=False, data={
                                             "id": cid, "name": name})
                            checkboxes.append(cb)
                        communities_checkbox_column.controls = checkboxes
                        communities_checkbox_column.visible = True
                        communities_checkbox_label.visible = True
                        communities_filter_group.visible = True
                    else:
                        communities_checkbox_column.controls = [
                            ft.Text("Communities: None")]
                        communities_checkbox_column.visible = True
                        communities_checkbox_label.visible = True
                        communities_filter_group.visible = True
                else:
                    communities_checkbox_column.controls = [
                        ft.Text("Communities: (failed to fetch)")]
                    communities_checkbox_column.visible = True
                    communities_checkbox_label.visible = True
                    communities_filter_group.visible = True
            except Exception as ex:
                communities_checkbox_column.controls = [
                    ft.Text(f"Communities: (error: {ex})")]
                communities_checkbox_column.visible = True
                communities_checkbox_label.visible = True
                communities_filter_group.visible = True
            page.update()
        # Run in a thread to avoid blocking UI
        import threading
        threading.Thread(target=fetch_communities).start()

        fetch_and_show_match_count()
        page.update()

    def fetch_and_show_match_count():
        selected = test_dropdown.value
        if not selected or selected not in tests_data:
            # removed match_count_number and match_count_label
            return
        test_guid = selected
        url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchCount/{test_guid}"
        cookie_string = text_area.value.strip()
        cookies = parse_cookie_string(cookie_string)
        headers = get_common_headers()
        headers['referer'] = f"https://www.ancestry.com/discoveryui-matches/"
        headers['content-type'] = 'application/json'
        csrf_token = get_csrf_token(cookies)
        if csrf_token:
            headers['x-csrf-token'] = csrf_token
        # Fetch all 3 match type counts in sequence, update radio labels

        def fetch_count_for_type(mt):
            if mt == "close":
                payload = {"lower": 0, "upper": 9}
                try:
                    resp = requests.post(
                        url, headers=headers, cookies=cookies, json=payload, allow_redirects=False)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data.get("count")
                except Exception:
                    pass
                return None
            elif mt == "distant":
                payload = {"lower": 10, "upper": 10}
                try:
                    resp = requests.post(
                        url, headers=headers, cookies=cookies, json=payload, allow_redirects=False)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data.get("count")
                except Exception:
                    pass
                return None
            elif mt == "custom":
                try:
                    lower = int(
                        custom_min_cm.value) if custom_min_cm.value else 6
                except Exception:
                    lower = 6
                try:
                    upper = int(
                        custom_max_cm.value) if custom_max_cm.value else 3490
                except Exception:
                    upper = 3490
                # Step 1: Get totalPages from first page
                first_url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage=1&sharedDna={lower}-{upper}"
                try:
                    resp = requests.get(
                        first_url, headers=headers, cookies=cookies)
                    if resp.status_code == 200:
                        data = resp.json()
                        total_pages = data.get("totalPages")
                        if total_pages is None:
                            return None
                        # Step 2: Get last page and count matches
                        last_url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage={total_pages}&sharedDna={lower}-{upper}"
                        try:
                            last_resp = requests.get(
                                last_url, headers=headers, cookies=cookies)
                            if last_resp.status_code == 200:
                                last_data = last_resp.json()
                                match_list = last_data.get("matchList", [])
                                if total_pages > 1:
                                    total_matches = (
                                        total_pages - 1) * 100 + len(match_list)
                                else:
                                    total_matches = len(match_list)
                                return total_matches
                        except Exception:
                            return None
                    return None
                except Exception:
                    return None
            else:
                payload = {"lower": 0, "upper": 10}
                try:
                    resp = requests.post(
                        url, headers=headers, cookies=cookies, json=payload, allow_redirects=False)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data.get("count")
                except Exception:
                    pass
                return None

        # Only fetch custom cM count if custom is currently selected and both fields are valid
        for mt in ["all", "close", "distant"]:
            match_type_counts[mt] = fetch_count_for_type(mt)
        # Only fetch custom if custom is selected and both fields are valid
        if match_type_radio.value == "custom":
            min_val = custom_min_cm.value.strip()
            max_val = custom_max_cm.value.strip()
            try:
                lower = int(min_val)
                upper = int(max_val)
                if min_val and max_val and lower <= upper:
                    # Show spinner in label while fetching
                    match_type_radio.content.controls[
                        3].label = "Custom centimorgan range (⏳)"
                    page.update()
                    match_type_counts["custom"] = fetch_count_for_type(
                        "custom")
                else:
                    match_type_counts["custom"] = None
            except Exception:
                match_type_counts["custom"] = None
        else:
            match_type_counts["custom"] = None
        # Update radio labels
        match_type_radio.content.controls[0].label = get_match_type_label(
            "all")
        match_type_radio.content.controls[1].label = get_match_type_label(
            "close")
        match_type_radio.content.controls[2].label = get_match_type_label(
            "distant")
        match_type_radio.content.controls[3].label = get_match_type_label(
            "custom")
        # Show custom cM fields now that match counts are fetched
        custom_min_cm.visible = True
        custom_max_cm.visible = True
        page.update()

    import threading
    import queue

    def get_matches_clicked(e):
        import time
        nonlocal matches_thread, run_id
        # Cancel old thread if running by incrementing run_id (thread checks this)
        run_id += 1
        this_run = run_id
        # No need for global, matches_thread is already nonlocal
        if matches_thread is not None and matches_thread.is_alive():
            # Cancel the old run by incrementing run_id (the old thread will exit on next check)
            processing_status_text.value = "Cancelling previous run..."
            page.update()
            # The old thread will see run_id has changed and exit promptly
            # Optionally, give a short delay to allow the old thread to clean up UI
            time.sleep(0.2)
        progress_bar.visible = False
        output_cards_grid.controls.clear()
        processing_status_text.value = ""
        time_left_text.value = ""
        pause_btn.visible = False  # Only show after we start fetching
        resume_btn.visible = False
        pause_event.clear()
        resume_event.set()
        page.update()

        # State for retrying failed match/page
        retry_match_state = {"pending": False,
                             "match": None, "match_args": None}

        def process_matches_thread():
            nonlocal retry_match_state
            # Clear resume_event at start of thread since we set it initially
            resume_event.clear()
            # Cancel this thread if a new run is started
            # Cancel this thread if a new run is started
            if this_run != run_id:
                # Clean up UI if this thread is being cancelled
                if threading.current_thread() == matches_thread:
                    progress_bar.visible = False
                    processing_status_text.value = "Run cancelled."
                    time_left_text.value = ""
                    pause_btn.visible = False
                    resume_btn.visible = False
                    page.update()
                return
            selected = test_dropdown.value
            if not selected or selected not in tests_data:
                if this_run == run_id:
                    show_message("Please select a valid DNA test.")
                    page.update()
                return
            test_guid = selected
            cookie_string = text_area.value.strip()
            cookies = parse_cookie_string(cookie_string)
            headers = get_common_headers()
            headers['referer'] = f"https://www.ancestry.com/discoveryui-matches/"
            headers['content-type'] = 'application/json'
            csrf_token = get_csrf_token(cookies)
            if csrf_token:
                headers['x-csrf-token'] = csrf_token
            count_url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchCount/{test_guid}"
            # Determine payload based on match type
            match_type = match_type_radio.value if hasattr(
                match_type_radio, 'value') else "all"
            if match_type == "close":
                payload = {"lower": 0, "upper": 9}
                try:
                    resp = requests.post(
                        count_url, headers=headers, cookies=cookies, json=payload, allow_redirects=False)
                    if resp.status_code == 200:
                        data = resp.json()
                        match_count = data.get("count", 0)
                        if not match_count:
                            if this_run == run_id:
                                show_message("No matches found.")
                                page.update()
                            return
                        total_pages = (match_count + 99) // 100
                    else:
                        if this_run == run_id:
                            show_message(
                                "Failed to fetch match count for matches.")
                            page.update()
                        return
                except Exception as ex:
                    if this_run == run_id:
                        show_message(f"Error fetching match count: {ex}")
                        page.update()
                    return
            elif match_type == "distant":
                payload = {"lower": 10, "upper": 10}
                try:
                    resp = requests.post(
                        count_url, headers=headers, cookies=cookies, json=payload, allow_redirects=False)
                    if resp.status_code == 200:
                        data = resp.json()
                        match_count = data.get("count", 0)
                        if not match_count:
                            if this_run == run_id:
                                show_message("No matches found.")
                                page.update()
                            return
                        total_pages = (match_count + 99) // 100
                    else:
                        if this_run == run_id:
                            show_message(
                                "Failed to fetch match count for matches.")
                            page.update()
                        return
                except Exception as ex:
                    if this_run == run_id:
                        show_message(f"Error fetching match count: {ex}")
                        page.update()
                    return
            elif match_type == "custom":
                try:
                    lower = int(
                        custom_min_cm.value) if custom_min_cm.value else 6
                except Exception:
                    lower = 6
                try:
                    upper = int(
                        custom_max_cm.value) if custom_max_cm.value else 3490
                except Exception:
                    upper = 3490
                first_url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage=1&sharedDna={lower}-{upper}"
                try:
                    resp = requests.get(
                        first_url, headers=headers, cookies=cookies)
                    if resp.status_code == 200:
                        data = resp.json()
                        total_pages = data.get("totalPages")
                        match_count = data.get("matchCount")
                        if total_pages is not None:
                            last_url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage={total_pages}&sharedDna={lower}-{upper}"
                            last_resp = requests.get(
                                last_url, headers=headers, cookies=cookies)
                            if last_resp.status_code == 200:
                                last_data = last_resp.json()
                                match_list = last_data.get("matchList", [])
                                if total_pages > 1:
                                    match_count = (
                                        total_pages - 1) * 100 + len(match_list)
                                else:
                                    match_count = len(match_list)
                                if not match_count:
                                    if this_run == run_id:
                                        show_message("No matches found.")
                                        page.update()
                                    return
                                total_pages = (match_count + 99) // 100
                            else:
                                if this_run == run_id:
                                    show_message(
                                        "Failed to fetch last page for matches.")
                                    page.update()
                                return
                        elif match_count:
                            if not match_count:
                                if this_run == run_id:
                                    show_message("No matches found.")
                                    page.update()
                                return
                            total_pages = (match_count + 99) // 100
                        else:
                            if this_run == run_id:
                                show_message("No matches found.")
                                page.update()
                            return
                    else:
                        if this_run == run_id:
                            show_message(
                                "Failed to fetch match count for matches.")
                            page.update()
                        return
                except Exception as ex:
                    if this_run == run_id:
                        show_message(f"Error fetching match count: {ex}")
                        page.update()
                    return
            else:
                payload = {"lower": 0, "upper": 10}
                try:
                    resp = requests.post(
                        count_url, headers=headers, cookies=cookies, json=payload, allow_redirects=False)
                    if resp.status_code == 200:
                        data = resp.json()
                        match_count = data.get("count", 0)
                        if not match_count:
                            if this_run == run_id:
                                show_message("No matches found.")
                                page.update()
                            return
                        total_pages = (match_count + 99) // 100
                    else:
                        if this_run == run_id:
                            show_message(
                                "Failed to fetch match count for matches.")
                            page.update()
                        return
                except Exception as ex:
                    if this_run == run_id:
                        show_message(f"Error fetching match count: {ex}")
                        page.update()
                    return
            import sys
            try:
                max_matches = int(number_input.value)
            except Exception:
                max_matches = 50
            printed = 0
            import time
            import csv
            printed = 0
            all_region_labels = set()
            matches_data = []
            import datetime
            today_str = datetime.datetime.now().strftime("%Y%m%d")
            csv_filename = f"matches_{test_guid}_{today_str}.csv"
            match_list_accum = []
            # Step 1: Fetch matches (as before, but accumulate for next step)
            # We want to keep fetching pages until we have enough matches that pass the communities filter, or run out of pages
            fetched_pages = 0
            total_fetched_pages = 0
            page_num = 1
            start_time = None
            # Show pause/resume buttons now that we're starting fetching
            if this_run == run_id:
                pause_btn.visible = True
                resume_btn.visible = False
                page.update()
            # We'll keep a set of sample_ids we've already seen to avoid duplicates if we go past needed_pages
            seen_sample_ids = set()

            # Move append_to_csv_smart definition here so it is available before use
            def append_to_csv_smart(match_data, all_region_labels, filename, is_first_match=False):
                import os
                import csv
                current_regions = sorted(all_region_labels)
                header = ["Display Name", "Sample ID",
                          "sharedCM", "Communities"] + current_regions
                communities_str = match_data.get("communities", "")
                if is_first_match or not os.path.exists(filename):
                    with open(filename, "w", newline='', encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                        row = [match_data.get("display_name", ""), match_data.get(
                            "sample_id", ""), match_data.get("sharedCM", ""), communities_str]
                        region_percents = match_data.get("regions", {})
                        for label in current_regions:
                            row.append(region_percents.get(label, ""))
                        writer.writerow(row)
                else:
                    existing_header = []
                    existing_data = []
                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            reader = csv.reader(f)
                            existing_header = next(reader, [])
                            for row in reader:
                                if row:
                                    existing_data.append(row)
                    except Exception as e:
                        print(f"Error reading existing CSV: {e}")
                        existing_header = []
                        existing_data = []
                    # Ensure Communities column exists in header and all rows
                    if existing_header:
                        if "Communities" not in existing_header:
                            # Insert Communities after sharedCM (index 3)
                            existing_header.insert(3, "Communities")
                            for i in range(len(existing_data)):
                                existing_data[i].insert(3, "")
                    existing_regions = set(existing_header[4:]) if len(
                        existing_header) > 4 else set()
                    new_regions = set(current_regions) - existing_regions
                    # If new regions, rewrite file with new columns
                    if new_regions or (existing_header[:4] != header[:4]) or (existing_header[4:] != header[4:]):
                        print(
                            f"Rewriting CSV with {len(new_regions)} new columns: {sorted(new_regions)}")
                        # Insert new region columns after Communities
                        new_header = ["Display Name", "Sample ID",
                                      "sharedCM", "Communities"] + current_regions
                        # Map old region indices (after Communities)
                        old_region_indices = {
                            region: idx+4 for idx, region in enumerate(existing_header[4:])}
                        with open(filename, "w", newline='', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow(new_header)
                            for row in existing_data:
                                new_row = row[:4]
                                for region in current_regions:
                                    idx = old_region_indices.get(region, None)
                                    if idx is not None and idx < len(row):
                                        new_row.append(row[idx])
                                    else:
                                        new_row.append("")
                                writer.writerow(new_row)
                            # Write the new match row
                            row = [match_data.get("display_name", ""), match_data.get(
                                "sample_id", ""), match_data.get("sharedCM", ""), communities_str]
                            region_percents = match_data.get("regions", {})
                            for label in current_regions:
                                row.append(region_percents.get(label, ""))
                            writer.writerow(row)
                    else:
                        # Append new row with correct communities value
                        with open(filename, "a", newline='', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            row = [match_data.get("display_name", ""), match_data.get(
                                "sample_id", ""), match_data.get("sharedCM", ""), communities_str]
                            region_percents = match_data.get("regions", {})
                            for label in current_regions:
                                row.append(region_percents.get(label, ""))
                            writer.writerow(row)

            # --- Combined fetch and process loop ---
            matches_written = 0
            page_num = 1
            seen_sample_ids = set()
            match_start_time = None
            # Always try to fetch more pages if we haven't reached max_matches, even if total_pages is reached (in case of filtering)
            # We'll keep fetching until we run out of pages (no more data returned), or reach max_matches
            while matches_written < max_matches:
                # Pause/Resume logic for page fetching
                # Check for cancellation at the start of each page
                if this_run != run_id:
                    if threading.current_thread() == matches_thread:
                        progress_bar.visible = False
                        processing_status_text.value = "Run cancelled."
                        time_left_text.value = ""
                        pause_btn.visible = False
                        resume_btn.visible = False
                        page.update()
                    return
                while pause_event.is_set():
                    resume_btn.visible = True
                    pause_btn.visible = False
                    page.update()
                    resume_event.wait()
                    resume_event.clear()  # Clear the event for next pause cycle
                # Check for cancellation after pause
                if this_run != run_id:
                    if threading.current_thread() == matches_thread:
                        progress_bar.visible = False
                        processing_status_text.value = "Run cancelled."
                        time_left_text.value = ""
                        pause_btn.visible = False
                        resume_btn.visible = False
                        page.update()
                    return
                resume_btn.visible = False
                pause_btn.visible = True
                # Progress bar for page fetching
                progress_bar.visible = True
                progress_bar.value = min(
                    1.0, matches_written / max_matches) if max_matches > 0 else 0
                processing_status_text.value = f"Fetching page {page_num} (written {matches_written}/{max_matches} matches)..."
                if page_num > 1:
                    elapsed = time.time() - start_time
                    avg_time_per_page = elapsed / (page_num - 1)
                    pages_left = total_pages - page_num + 1
                    est_time_left = int(avg_time_per_page * pages_left)
                    mins, secs = divmod(est_time_left, 60)
                    time_left_text.value = f"Estimated time left: {mins}m {secs}s"
                else:
                    start_time = time.time()
                    time_left_text.value = ""
                page.update()

                # Check if we need to retry a failed request
                if retry_match_state["pending"]:
                    if retry_match_state["match"] is not None:
                        # Retry failed match processing
                        match = retry_match_state["match"]
                        eth_url, headers, cookies = retry_match_state["match_args"]
                        # Skip to the match processing part - we'll handle this in the match loop
                        pass
                    elif retry_match_state["match_args"] is not None:
                        # Retry failed page fetch
                        url, headers, cookies = retry_match_state["match_args"]
                        retry_match_state["pending"] = False
                        retry_match_state["match"] = None
                        retry_match_state["match_args"] = None
                        # Try the failed request again
                        resp = requests.get(
                            url, headers=headers, cookies=cookies)
                        if resp.status_code == 200:
                            try:
                                matches_json = resp.json()
                                match_list = matches_json.get("matchList", [])
                                if match_list:
                                    # Process this page's matches
                                    print(
                                        f"[PAGE RETRY] Retrieved {len(match_list)} matches:")
                                    for idx, match in enumerate(match_list, 1):
                                        profile = match.get("matchProfile", {})
                                        display_name = profile.get(
                                            "displayName", "?")
                                        sample_id = match.get("sampleId", "?")
                                        print(
                                            f"  {idx}. {display_name} (Sample ID: {sample_id})")
                                    # Continue with normal processing below
                                else:
                                    break
                            except Exception:
                                processing_status_text.value = "Still no JSON response for match page. Paused. Click Resume to retry."
                                page.update()
                                retry_match_state["pending"] = True
                                retry_match_state["match"] = None
                                retry_match_state["match_args"] = (
                                    url, headers, cookies)
                                pause_event.set()
                                continue  # Go back to pause check instead of returning
                        else:
                            processing_status_text.value = f"Still failed to fetch matches for page. Paused. Click Resume to retry."
                            page.update()
                            retry_match_state["pending"] = True
                            retry_match_state["match"] = None
                            retry_match_state["match_args"] = (
                                url, headers, cookies)
                            pause_event.set()
                            continue  # Go back to pause check instead of returning
                else:
                    # Normal page fetching logic
                    # Build URL based on match type (refactored for clarity)
                    if match_type == "distant":
                        shared_dna = "distantMatches"
                    elif match_type == "close":
                        shared_dna = "closeMatches"
                    elif match_type == "custom":
                        try:
                            lower = int(
                                custom_min_cm.value) if custom_min_cm.value else 6
                        except Exception:
                            lower = 6
                        try:
                            upper = int(
                                custom_max_cm.value) if custom_max_cm.value else 3490
                        except Exception:
                            upper = 3490
                        shared_dna = f"{lower}-{upper}"
                    else:
                        shared_dna = None

                    if shared_dna:
                        url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage={page_num}&sharedDna={shared_dna}"
                    else:
                        url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage={page_num}"

                    # --- Stop if we've reached the last page (avoid infinite fetch) ---
                    if 'total_pages' in locals() and page_num > total_pages:
                        print(
                            f"[INFO] Reached last page: page_num={page_num} > total_pages={total_pages}. Stopping fetch loop.")
                        break

                    resp = requests.get(url, headers=headers, cookies=cookies)
                    if resp.status_code == 200:
                        try:
                            matches_json = resp.json()
                        except Exception:
                            processing_status_text.value = "No JSON response for match page. Paused. Click Resume to retry."
                            retry_match_state["pending"] = True
                            retry_match_state["match"] = None
                            retry_match_state["match_args"] = (
                                url, headers, cookies)
                            pause_event.set()
                            pause_btn.visible = False
                            resume_btn.visible = True
                            page.update()
                            continue  # Go back to pause check instead of returning
                    else:
                        processing_status_text.value = f"Failed to fetch matches for page {page_num}. Paused. Click Resume to retry."
                        retry_match_state["pending"] = True
                        retry_match_state["match"] = None
                        retry_match_state["match_args"] = (
                            url, headers, cookies)
                        pause_event.set()
                        pause_btn.visible = False
                        resume_btn.visible = True
                        page.update()
                        continue  # Go back to pause check instead of returning
                    match_list = matches_json.get("matchList", [])
                    if not match_list:
                        break
                    print(f"[PAGE] Retrieved {len(match_list)} matches:")
                    for idx, match in enumerate(match_list, 1):
                        profile = match.get("matchProfile", {})
                        display_name = profile.get("displayName", "?")
                        sample_id = match.get("sampleId", "?")
                        print(
                            f"  {idx}. {display_name} (Sample ID: {sample_id})")

                # Process the match_list (either from retry or normal fetch)
                custom_cm_early_exit = False
                match_error_break = False  # Flag to track if we broke due to error
                if match_type == "custom":
                    if len(match_list) == 100:
                        all_below = True
                        for match in match_list:
                            shared_cm_val = match.get("relationship", {}).get(
                                "sharedCentimorgans", None)
                            try:
                                shared_cm_val = float(shared_cm_val)
                            except Exception:
                                shared_cm_val = None
                            if shared_cm_val is not None and shared_cm_val >= lower:
                                all_below = False
                                break
                        if all_below:
                            custom_cm_early_exit = True
                match_idx = 0
                while match_idx < len(match_list):
                    retrying = False
                    if retry_match_state["pending"] and retry_match_state["match"] is not None:
                        match = retry_match_state["match"]
                        eth_url, headers, cookies = retry_match_state["match_args"]
                        retry_match_state["pending"] = False
                        retry_match_state["match"] = None
                        retry_match_state["match_args"] = None
                        retrying = True
                    else:
                        match = match_list[match_idx]

                    while pause_event.is_set():
                        resume_btn.visible = True
                        pause_btn.visible = False
                        processing_status_text.value = "Paused. Click Resume to continue."
                        page.update()
                        resume_event.wait()
                        resume_event.clear()  # Clear the event for next pause cycle
                    if this_run != run_id:
                        if threading.current_thread() == matches_thread:
                            progress_bar.visible = False
                            processing_status_text.value = "Run cancelled."
                            time_left_text.value = ""
                            pause_btn.visible = False
                            resume_btn.visible = False
                            page.update()
                        return
                    profile = match.get("matchProfile", {})
                    display_name = profile.get("displayName", "?")
                    sample_id = match.get("sampleId", "?")
                    shared_cm = match.get("relationship", {}).get(
                        "sharedCentimorgans", "")
                    if this_run != run_id:
                        if threading.current_thread() == matches_thread:
                            progress_bar.visible = False
                            processing_status_text.value = "Run cancelled."
                            time_left_text.value = ""
                            pause_btn.visible = False
                            resume_btn.visible = False
                            page.update()
                        return
                    if sample_id in seen_sample_ids:
                        if not retrying:
                            match_idx += 1
                        continue
                    seen_sample_ids.add(sample_id)
                    # Only increment match_idx if not retrying
                    if not retrying:
                        match_idx += 1
                    # ...existing code for communities filter, ethnicity, CSV, UI, etc...
                    selected_community_ids = set()
                    if communities_checkbox_column.visible:
                        for cb in communities_checkbox_column.controls:
                            if hasattr(cb, 'value') and cb.value and hasattr(cb, 'data') and cb.data and 'id' in cb.data:
                                selected_community_ids.add(cb.data['id'])

                    skip_for_communities = False
                    if selected_community_ids:
                        migrations_url = f"https://www.ancestry.com/discoveryui-matchesservice/api/compare/{test_guid}/with/{sample_id}/sharedmigrations"
                        try:
                            mig_resp = requests.get(
                                migrations_url, headers=headers, cookies=cookies)
                            if mig_resp.status_code == 200:
                                mig_json = mig_resp.json()
                                sampleB = mig_json.get("sampleB", {})
                                sampleB_communities = set(
                                    sampleB.get("communities", []))
                                if sampleB_communities != selected_community_ids:
                                    processing_status_text.value = f"Skipping ({sample_id}): communities do not match selection"
                                    page.update()
                                    time.sleep(MATCH_PROCESS_DELAY)
                                    continue
                            else:
                                processing_status_text.value = f"Skipping ({sample_id}): failed to fetch communities"
                                page.update()
                                time.sleep(MATCH_PROCESS_DELAY)
                                continue
                        except Exception as ex:
                            processing_status_text.value = f"Skipping ({sample_id}): error fetching communities"
                            page.update()
                            time.sleep(MATCH_PROCESS_DELAY)
                            continue

                    # --- Ethnicity fetch and CSV write ---
                    processing_status_text.value = f"Processing match {matches_written+1}/{max_matches}: ({sample_id})..."
                    if matches_written == 0:
                        match_start_time = time.time()
                        time_left_text.value = ""
                    elif match_start_time is not None:
                        elapsed = time.time() - match_start_time
                        avg_time_per_match = elapsed / matches_written
                        matches_left = max_matches - matches_written
                        est_time_left = int(avg_time_per_match * matches_left)
                        mins, secs = divmod(est_time_left, 60)
                        time_left_text.value = f"Estimated time left: {mins}m {secs}s"
                    progress_bar.value = (matches_written+1)/max_matches
                    progress_bar.visible = True
                    page.update()

                    # Fetch communities for this match ONCE
                    communities_url = f"https://www.ancestry.com/discoveryui-matchesservice/api/compare/{test_guid}/with/{sample_id}/sharedmigrations"
                    communities_list = []
                    try:
                        comm_resp = requests.get(
                            communities_url, headers=headers, cookies=cookies)
                        if comm_resp.status_code == 200:
                            comm_json = comm_resp.json()
                            sampleB = comm_json.get("sampleB", {})
                            comm_ids = sampleB.get("communities", [])
                            for cid in comm_ids:
                                name = COMMUNITY_LABELS.get(cid, cid)
                                communities_list.append(name)
                    except Exception as e:
                        print(
                            f"Error fetching communities for {sample_id}: {e}")
                    communities_str = "; ".join(communities_list)

                    # Ethnicity fetch
                    eth_url = f'https://www.ancestry.com/discoveryui-matchesservice/api/compare/{test_guid}/with/{sample_id}/ethnicity'
                    region_dict = {}
                    region_line = ""
                    while True:
                        try:
                            eth_resp = requests.get(
                                eth_url, headers=headers, cookies=cookies)
                            print(
                                f"[MATCH {matches_written+1}/{max_matches}] [COMPARE] Response for {sample_id}: {eth_resp.status_code}")
                            try:
                                resp_json = eth_resp.json()
                            except Exception:
                                processing_status_text.value = f"No JSON response for match {sample_id}. Paused. Click Resume to retry."
                                retry_match_state["pending"] = True
                                retry_match_state["match"] = match
                                retry_match_state["match_args"] = (
                                    eth_url, headers, cookies)
                                pause_event.set()
                                pause_btn.visible = False
                                resume_btn.visible = True
                                page.update()
                                # Wait for resume, then retry this match (do not continue outer loop)
                                while pause_event.is_set():
                                    resume_btn.visible = True
                                    pause_btn.visible = False
                                    processing_status_text.value = "Paused. Click Resume to continue."
                                    page.update()
                                    resume_event.wait()
                                    resume_event.clear()
                                continue
                            if isinstance(resp_json, dict) and "comparisons" in resp_json:
                                region_list = []
                                for comp in resp_json["comparisons"]:
                                    if "rightList" in comp:
                                        for entry in comp["rightList"]:
                                            rid = entry.get("resourceId")
                                            pct = entry.get("percent")
                                            label = REGION_LABELS.get(
                                                str(rid), str(rid))
                                            print(
                                                f"[MATCH {matches_written+1}/{max_matches}] [COMPARE][rightList] resourceId: {rid} ({label}), percent: {pct}")
                                            if label and pct is not None:
                                                region_list.append(
                                                    (label, pct))
                                for label, pct in region_list:
                                    if label not in region_dict or pct > region_dict[label]:
                                        region_dict[label] = pct
                                all_region_labels.update(region_dict.keys())
                                if region_dict:
                                    region_line = ", ".join(f"{lbl}: {pct}%" for lbl, pct in sorted(
                                        region_dict.items(), key=lambda x: -x[1]))
                                else:
                                    region_line = "No ethnicity data"
                            break  # Success, break out of retry loop
                        except Exception as e:
                            processing_status_text.value = f"Error fetching match {sample_id}. Paused. Click Resume to retry."
                            retry_match_state["pending"] = True
                            retry_match_state["match"] = match
                            retry_match_state["match_args"] = (
                                eth_url, headers, cookies)
                            pause_event.set()
                            pause_btn.visible = False
                            resume_btn.visible = True
                            page.update()
                            # Wait for resume, then retry this match (do not continue outer loop)
                            while pause_event.is_set():
                                resume_btn.visible = True
                                pause_btn.visible = False
                                processing_status_text.value = "Paused. Click Resume to continue."
                                page.update()
                                resume_event.wait()
                                resume_event.clear()
                            continue

                    # Output: Communities above bar chart for regions
                    output_cards_grid.controls.clear()
                    if communities_list:
                        numbered_list = "\n".join([
                            f"{i+1}. {name}" for i, name in enumerate(communities_list)
                        ])
                        output_cards_grid.controls.append(
                            ft.Text(
                                f"Communities:\n{numbered_list}", size=18, weight=ft.FontWeight.BOLD, color="#1976d2")
                        )
                    else:
                        output_cards_grid.controls.append(
                            ft.Text("Communities: None", size=18,
                                    weight=ft.FontWeight.BOLD, color="#888888")
                        )
                    # Bar chart for regions (sorted by percent descending)
                    if region_dict:
                        sorted_regions = sorted(
                            region_dict.items(), key=lambda x: -x[1])
                        bars = []
                        max_label_len = max(
                            (len(lbl) for lbl, _ in sorted_regions), default=10)
                        bar_max_width = 500  # px, for 100%
                        for idx, (lbl, pct) in enumerate(sorted_regions, 1):
                            bar_width = int(bar_max_width * (pct / 100.0))
                            bars.append(
                                ft.Row([
                                    ft.Text(lbl, size=16, width=180,
                                            overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Container(
                                        content=ft.Container(
                                            bgcolor="#1976d2",
                                            border_radius=6,
                                            width=bar_width,
                                            height=28,
                                            alignment=ft.alignment.center_left,
                                            padding=ft.padding.only(left=8),
                                            content=ft.Text(
                                                f"{pct}%", size=15, color="#FFFFFF", weight=ft.FontWeight.BOLD)
                                        ),
                                        bgcolor="#e3e3e3",
                                        border_radius=6,
                                        width=bar_max_width,
                                        height=28,
                                        alignment=ft.alignment.center_left,
                                        margin=ft.margin.only(bottom=6)
                                    )
                                ], alignment="start", spacing=12)
                            )
                        output_cards_grid.controls.extend(bars)
                    else:
                        output_cards_grid.controls.append(
                            ft.Row([
                                ft.Text("No ethnicity data", size=16)
                            ], alignment="start")
                        )
                    page.update()

                    # Save match data (including communities_str)
                    match_data = {
                        "display_name": display_name,
                        "sample_id": sample_id,
                        "sharedCM": shared_cm,
                        "regions": region_dict.copy(),
                        "communities": communities_str
                    }
                    matches_data.append(match_data)
                    try:
                        append_to_csv_smart(
                            match_data, all_region_labels, csv_filename, is_first_match=(matches_written == 0))
                        print(
                            f"[MATCH {matches_written+1}/{max_matches}] Saved to CSV: {csv_filename}")
                    except Exception as e:
                        print(
                            f"[MATCH {matches_written+1}/{max_matches}] Error saving to CSV: {e}")
                    matches_written += 1
                    if matches_written >= max_matches:
                        break
                    time.sleep(MATCH_PROCESS_DELAY)
                if matches_written >= max_matches:
                    break
                if custom_cm_early_exit:
                    break
                # No need for match_error_break logic; handled by continue above
                page_num += 1
                if matches_written < max_matches:
                    time.sleep(MATCH_PROCESS_DELAY)
            # After all pages fetched, clear the processing label for match processing
            processing_status_text.value = ""
            page.update()
            # Step 2: For each match, fetch ethnicity and save to CSV

            def append_to_csv_smart(match_data, all_region_labels, filename, is_first_match=False):
                current_regions = sorted(all_region_labels)
                header = ["Display Name", "Sample ID",
                          "sharedCM"] + current_regions
                import os
                if is_first_match or not os.path.exists(filename):
                    with open(filename, "w", newline='', encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                        row = [match_data.get("display_name", ""), match_data.get(
                            "sample_id", ""), match_data.get("sharedCM", "")]
                        region_percents = match_data.get("regions", {})
                        for label in current_regions:
                            row.append(region_percents.get(label, ""))
                        writer.writerow(row)
                else:
                    existing_header = []
                    existing_data = []
                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            reader = csv.reader(f)
                            existing_header = next(reader, [])
                            for row in reader:
                                if row:
                                    existing_data.append(row)
                    except Exception as e:
                        print(f"Error reading existing CSV: {e}")
                        existing_header = []
                        existing_data = []
                    existing_regions = set(existing_header[3:]) if len(
                        existing_header) > 3 else set()
                    new_regions = set(current_regions) - existing_regions
                    if new_regions:
                        print(
                            f"Rewriting CSV with {len(new_regions)} new columns: {sorted(new_regions)}")
                        with open(filename, "w", newline='', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow(header)
                            for row in existing_data:
                                if len(row) >= 3:
                                    new_row = row[:3]
                                    old_regions = existing_header[3:] if len(
                                        existing_header) > 3 else []
                                    old_region_data = row[3:] if len(
                                        row) > 3 else []
                                    old_data_map = {}
                                    for i, region in enumerate(old_regions):
                                        if i < len(old_region_data):
                                            old_data_map[region] = old_region_data[i]
                                    for region in current_regions:
                                        new_row.append(
                                            old_data_map.get(region, ""))
                                    writer.writerow(new_row)
                            row = [match_data.get("display_name", ""), match_data.get(
                                "sample_id", ""), match_data.get("sharedCM", "")]
                            region_percents = match_data.get("regions", {})
                            for label in current_regions:
                                row.append(region_percents.get(label, ""))
                            writer.writerow(row)
                    else:
                        with open(filename, "a", newline='', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            row = [match_data.get("display_name", ""), match_data.get(
                                "sample_id", ""), match_data.get("sharedCM", "")]
                            region_percents = match_data.get("regions", {})
                            for label in current_regions:
                                row.append(region_percents.get(label, ""))
                            writer.writerow(row)

            if this_run == run_id:
                progress_bar.value = 1.0
                pause_btn.visible = False
                resume_btn.visible = False
                processing_status_text.value = "Processing done."
                time_left_text.value = ""
                show_message(
                    f"Done. {len(matches_data)} matches processed. Saved to {csv_filename}.")
                page.update()
        # Start the thread and track it
        matches_thread = threading.Thread(target=process_matches_thread)
        matches_thread.start()

    clear_btn = ft.ElevatedButton("Clear", on_click=clear_clicked)
    auth_btn = ft.ElevatedButton("Authenticate", on_click=authenticate_clicked)
    test_dropdown.on_change = dropdown_changed
    get_matches_btn.on_click = get_matches_clicked

    def pause_clicked(e):
        import time
        pause_event.set()
        resume_event.clear()  # Clear resume event when pausing
        pause_btn.visible = False
        resume_btn.visible = True
        processing_status_text.value = "Paused. Click Resume to continue."
        page.update()
        # Force UI update and allow the processing thread to hit the pause check quickly
        time.sleep(0.05)

    def resume_clicked(e):
        if pause_event.is_set():
            pause_event.clear()
            resume_event.set()  # Signal the waiting thread to continue
            resume_btn.visible = False
            pause_btn.visible = True
            processing_status_text.value = "Resuming..."
            page.update()

    pause_btn.on_click = pause_clicked
    resume_btn.on_click = resume_clicked
    # (REMOVED BAD nonlocal STATEMENT)
    # Remove any code that sets pause/resume button visibility or status at startup
    pause_btn.visible = False
    resume_btn.visible = False
    processing_status_text.value = ""
    page.update()
    # Only show Pause button when processing is started (handled in get_matches_clicked)
    # Remove match count label and number from UI
    match_options_title = ft.Row([
        ft.Icon(name=ft.Icons.TUNE, color="#1565c0", size=26),
        ft.Text(
            "Match Options",
            size=16,
            weight=ft.FontWeight.BOLD,
            visible=True
        )
    ], spacing=10)
    match_options_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                match_options_title,
                match_type_radio,
                ft.Row([
                    custom_min_cm,
                    custom_max_cm
                ], alignment="start", spacing=10)
            ], spacing=8),
            padding=ft.padding.all(18),
            border=ft.border.all(2, "#1565c0"),  # strong blue border
            border_radius=14,
        ),
        visible=False
    )

    main_column = ft.Column([
        text_area,
        ft.Row([auth_btn, clear_btn]),
        test_dropdown,
        communities_filter_group,
        match_options_card,
        ft.Row([
            number_input,
            get_matches_btn
        ], alignment="start", spacing=10),
        progress_bar,
        time_left_text,
        processing_status_text,
        ft.Row([pause_btn, resume_btn], alignment="start", spacing=10),
        output_cards_grid
    ], scroll="auto", expand=True)
    page.add(ft.Container(content=main_column, expand=True))


ft.app(target=main)
