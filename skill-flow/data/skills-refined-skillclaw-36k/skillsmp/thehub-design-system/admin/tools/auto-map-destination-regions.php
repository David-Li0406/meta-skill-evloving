<?php
/**
 * Auto-map Destination Regions
 *
 * Automatically assigns SCF districts to destinations based on their city.
 * Uses a mapping of Swedish cities/municipalities to SCF districts.
 *
 * @package TheHUB
 * @version 1.0
 */

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

// City to SCF District mapping
// Format: 'city_name' => 'SCF District'
$cityToDistrict = [
    // Stockholms Cykelförbund (Stockholm län)
    'Stockholm' => 'Stockholms Cykelförbund',
    'Nacka' => 'Stockholms Cykelförbund',
    'Sollentuna' => 'Stockholms Cykelförbund',
    'Täby' => 'Stockholms Cykelförbund',
    'Huddinge' => 'Stockholms Cykelförbund',
    'Södertälje' => 'Stockholms Cykelförbund',
    'Tyresö' => 'Stockholms Cykelförbund',
    'Haninge' => 'Stockholms Cykelförbund',
    'Lidingö' => 'Stockholms Cykelförbund',
    'Sundbyberg' => 'Stockholms Cykelförbund',
    'Solna' => 'Stockholms Cykelförbund',
    'Vallentuna' => 'Stockholms Cykelförbund',
    'Danderyd' => 'Stockholms Cykelförbund',
    'Sigtuna' => 'Stockholms Cykelförbund',
    'Norrtälje' => 'Stockholms Cykelförbund',
    'Nykvarn' => 'Stockholms Cykelförbund',
    'Salem' => 'Stockholms Cykelförbund',
    'Botkyrka' => 'Stockholms Cykelförbund',
    'Järfälla' => 'Stockholms Cykelförbund',
    'Upplands-Bro' => 'Stockholms Cykelförbund',
    'Upplands Väsby' => 'Stockholms Cykelförbund',
    'Ekerö' => 'Stockholms Cykelförbund',
    'Värmdö' => 'Stockholms Cykelförbund',
    'Nynäshamn' => 'Stockholms Cykelförbund',
    'Österåker' => 'Stockholms Cykelförbund',

    // Upplands Cykelförbund (Uppsala län)
    'Uppsala' => 'Upplands Cykelförbund',
    'Enköping' => 'Upplands Cykelförbund',
    'Knivsta' => 'Upplands Cykelförbund',
    'Tierp' => 'Upplands Cykelförbund',
    'Älvkarleby' => 'Upplands Cykelförbund',
    'Östhammar' => 'Upplands Cykelförbund',
    'Heby' => 'Upplands Cykelförbund',
    'Håbo' => 'Upplands Cykelförbund',

    // Södermanlands Cykelförbund (Södermanlands län)
    'Nyköping' => 'Södermanlands Cykelförbund',
    'Eskilstuna' => 'Södermanlands Cykelförbund',
    'Katrineholm' => 'Södermanlands Cykelförbund',
    'Strängnäs' => 'Södermanlands Cykelförbund',
    'Flen' => 'Södermanlands Cykelförbund',
    'Gnesta' => 'Södermanlands Cykelförbund',
    'Oxelösund' => 'Södermanlands Cykelförbund',
    'Trosa' => 'Södermanlands Cykelförbund',
    'Vingåker' => 'Södermanlands Cykelförbund',

    // Östergötlands Cykelförbund (Östergötlands län)
    'Linköping' => 'Östergötlands Cykelförbund',
    'Norrköping' => 'Östergötlands Cykelförbund',
    'Motala' => 'Östergötlands Cykelförbund',
    'Mjölby' => 'Östergötlands Cykelförbund',
    'Finspång' => 'Östergötlands Cykelförbund',
    'Vadstena' => 'Östergötlands Cykelförbund',
    'Ödeshög' => 'Östergötlands Cykelförbund',
    'Söderköping' => 'Östergötlands Cykelförbund',
    'Åtvidaberg' => 'Östergötlands Cykelförbund',
    'Valdemarsvik' => 'Östergötlands Cykelförbund',
    'Kinda' => 'Östergötlands Cykelförbund',
    'Boxholm' => 'Östergötlands Cykelförbund',
    'Ydre' => 'Östergötlands Cykelförbund',

    // Smålands Cykelförbund (Jönköpings, Kronobergs och Kalmar län)
    'Jönköping' => 'Smålands Cykelförbund',
    'Växjö' => 'Smålands Cykelförbund',
    'Kalmar' => 'Smålands Cykelförbund',
    'Västervik' => 'Smålands Cykelförbund',
    'Nässjö' => 'Smålands Cykelförbund',
    'Vetlanda' => 'Smålands Cykelförbund',
    'Eksjö' => 'Smålands Cykelförbund',
    'Tranås' => 'Smålands Cykelförbund',
    'Värnamo' => 'Smålands Cykelförbund',
    'Gislaved' => 'Smålands Cykelförbund',
    'Vaggeryd' => 'Smålands Cykelförbund',
    'Sävsjö' => 'Smålands Cykelförbund',
    'Habo' => 'Smålands Cykelförbund',
    'Mullsjö' => 'Smålands Cykelförbund',
    'Aneby' => 'Smålands Cykelförbund',
    'Alvesta' => 'Smålands Cykelförbund',
    'Ljungby' => 'Smålands Cykelförbund',
    'Älmhult' => 'Smålands Cykelförbund',
    'Markaryd' => 'Smålands Cykelförbund',
    'Tingsryd' => 'Smålands Cykelförbund',
    'Lessebo' => 'Smålands Cykelförbund',
    'Uppvidinge' => 'Smålands Cykelförbund',
    'Oskarshamn' => 'Smålands Cykelförbund',
    'Vimmerby' => 'Smålands Cykelförbund',
    'Hultsfred' => 'Smålands Cykelförbund',
    'Nybro' => 'Smålands Cykelförbund',
    'Emmaboda' => 'Smålands Cykelförbund',
    'Mönsterås' => 'Smålands Cykelförbund',
    'Högsby' => 'Smålands Cykelförbund',
    'Torsås' => 'Smålands Cykelförbund',
    'Mörbylånga' => 'Smålands Cykelförbund',
    'Borgholm' => 'Smålands Cykelförbund',
    'Öland' => 'Smålands Cykelförbund',

    // Gotland (del av Stockholms Cykelförbund)
    'Visby' => 'Stockholms Cykelförbund',

    // Hallands Cykelförbund (Hallands län)
    'Halmstad' => 'Hallands Cykelförbund',
    'Varberg' => 'Hallands Cykelförbund',
    'Kungsbacka' => 'Hallands Cykelförbund',
    'Falkenberg' => 'Hallands Cykelförbund',
    'Laholm' => 'Hallands Cykelförbund',
    'Hylte' => 'Hallands Cykelförbund',

    // Skånes Cykelförbund (Skåne län)
    'Malmö' => 'Skånes Cykelförbund',
    'Helsingborg' => 'Skånes Cykelförbund',
    'Lund' => 'Skånes Cykelförbund',
    'Kristianstad' => 'Skånes Cykelförbund',
    'Landskrona' => 'Skånes Cykelförbund',
    'Trelleborg' => 'Skånes Cykelförbund',
    'Ängelholm' => 'Skånes Cykelförbund',
    'Ystad' => 'Skånes Cykelförbund',
    'Eslöv' => 'Skånes Cykelförbund',
    'Hässleholm' => 'Skånes Cykelförbund',
    'Höganäs' => 'Skånes Cykelförbund',
    'Vellinge' => 'Skånes Cykelförbund',
    'Staffanstorp' => 'Skånes Cykelförbund',
    'Lomma' => 'Skånes Cykelförbund',
    'Burlöv' => 'Skånes Cykelförbund',
    'Svedala' => 'Skånes Cykelförbund',
    'Kävlinge' => 'Skånes Cykelförbund',
    'Bjuv' => 'Skånes Cykelförbund',
    'Svalöv' => 'Skånes Cykelförbund',
    'Klippan' => 'Skånes Cykelförbund',
    'Åstorp' => 'Skånes Cykelförbund',
    'Båstad' => 'Skånes Cykelförbund',
    'Simrishamn' => 'Skånes Cykelförbund',
    'Tomelilla' => 'Skånes Cykelförbund',
    'Sjöbo' => 'Skånes Cykelförbund',
    'Skurup' => 'Skånes Cykelförbund',
    'Hörby' => 'Skånes Cykelförbund',
    'Höör' => 'Skånes Cykelförbund',
    'Osby' => 'Skånes Cykelförbund',
    'Östra Göinge' => 'Skånes Cykelförbund',
    'Bromölla' => 'Skånes Cykelförbund',
    'Perstorp' => 'Skånes Cykelförbund',
    'Örkelljunga' => 'Skånes Cykelförbund',

    // Göteborgs Cykelförbund (Göteborg och delar av Västra Götaland)
    'Göteborg' => 'Göteborgs Cykelförbund',
    'Mölndal' => 'Göteborgs Cykelförbund',
    'Partille' => 'Göteborgs Cykelförbund',
    'Härryda' => 'Göteborgs Cykelförbund',
    'Lerum' => 'Göteborgs Cykelförbund',
    'Ale' => 'Göteborgs Cykelförbund',
    'Kungälv' => 'Göteborgs Cykelförbund',
    'Öckerö' => 'Göteborgs Cykelförbund',
    'Stenungsund' => 'Göteborgs Cykelförbund',
    'Tjörn' => 'Göteborgs Cykelförbund',

    // Bohuslän-Dals Cykelförbund (Norra Bohuslän och Dalsland)
    'Uddevalla' => 'Bohuslän-Dals Cykelförbund',
    'Trollhättan' => 'Bohuslän-Dals Cykelförbund',
    'Vänersborg' => 'Bohuslän-Dals Cykelförbund',
    'Lysekil' => 'Bohuslän-Dals Cykelförbund',
    'Munkedal' => 'Bohuslän-Dals Cykelförbund',
    'Sotenäs' => 'Bohuslän-Dals Cykelförbund',
    'Tanum' => 'Bohuslän-Dals Cykelförbund',
    'Strömstad' => 'Bohuslän-Dals Cykelförbund',
    'Orust' => 'Bohuslän-Dals Cykelförbund',
    'Lilla Edet' => 'Bohuslän-Dals Cykelförbund',
    'Mellerud' => 'Bohuslän-Dals Cykelförbund',
    'Åmål' => 'Bohuslän-Dals Cykelförbund',
    'Bengtsfors' => 'Bohuslän-Dals Cykelförbund',
    'Dals-Ed' => 'Bohuslän-Dals Cykelförbund',
    'Färgelanda' => 'Bohuslän-Dals Cykelförbund',

    // Västergötlands Cykelförbund (Skaraborg och delar av Västra Götaland)
    'Borås' => 'Västergötlands Cykelförbund',
    'Skövde' => 'Västergötlands Cykelförbund',
    'Lidköping' => 'Västergötlands Cykelförbund',
    'Mariestad' => 'Västergötlands Cykelförbund',
    'Alingsås' => 'Västergötlands Cykelförbund',
    'Ulricehamn' => 'Västergötlands Cykelförbund',
    'Mark' => 'Västergötlands Cykelförbund',
    'Tranemo' => 'Västergötlands Cykelförbund',
    'Svenljunga' => 'Västergötlands Cykelförbund',
    'Herrljunga' => 'Västergötlands Cykelförbund',
    'Vårgårda' => 'Västergötlands Cykelförbund',
    'Bollebygd' => 'Västergötlands Cykelförbund',
    'Tidaholm' => 'Västergötlands Cykelförbund',
    'Falköping' => 'Västergötlands Cykelförbund',
    'Skara' => 'Västergötlands Cykelförbund',
    'Tibro' => 'Västergötlands Cykelförbund',
    'Karlsborg' => 'Västergötlands Cykelförbund',
    'Gullspång' => 'Västergötlands Cykelförbund',
    'Götene' => 'Västergötlands Cykelförbund',
    'Vara' => 'Västergötlands Cykelförbund',
    'Essunga' => 'Västergötlands Cykelförbund',
    'Grästorp' => 'Västergötlands Cykelförbund',
    'Töreboda' => 'Västergötlands Cykelförbund',
    'Hjo' => 'Västergötlands Cykelförbund',

    // Värmlands Cykelförbund (Värmlands län)
    'Karlstad' => 'Värmlands Cykelförbund',
    'Kristinehamn' => 'Värmlands Cykelförbund',
    'Arvika' => 'Värmlands Cykelförbund',
    'Säffle' => 'Värmlands Cykelförbund',
    'Hagfors' => 'Värmlands Cykelförbund',
    'Filipstad' => 'Värmlands Cykelförbund',
    'Forshaga' => 'Värmlands Cykelförbund',
    'Grums' => 'Värmlands Cykelförbund',
    'Hammarö' => 'Värmlands Cykelförbund',
    'Kil' => 'Värmlands Cykelförbund',
    'Munkfors' => 'Värmlands Cykelförbund',
    'Storfors' => 'Värmlands Cykelförbund',
    'Sunne' => 'Värmlands Cykelförbund',
    'Torsby' => 'Värmlands Cykelförbund',
    'Eda' => 'Värmlands Cykelförbund',
    'Årjäng' => 'Värmlands Cykelförbund',

    // Örebro Läns Cykelförbund (Örebro län)
    'Örebro' => 'Örebro Läns Cykelförbund',
    'Karlskoga' => 'Örebro Läns Cykelförbund',
    'Lindesberg' => 'Örebro Läns Cykelförbund',
    'Kumla' => 'Örebro Läns Cykelförbund',
    'Hallsberg' => 'Örebro Läns Cykelförbund',
    'Askersund' => 'Örebro Läns Cykelförbund',
    'Nora' => 'Örebro Läns Cykelförbund',
    'Degerfors' => 'Örebro Läns Cykelförbund',
    'Hällefors' => 'Örebro Läns Cykelförbund',
    'Ljusnarsberg' => 'Örebro Läns Cykelförbund',
    'Laxå' => 'Örebro Läns Cykelförbund',
    'Lekeberg' => 'Örebro Läns Cykelförbund',

    // Västmanlands Cykelförbund (Västmanlands län)
    'Västerås' => 'Västmanlands Cykelförbund',
    'Köping' => 'Västmanlands Cykelförbund',
    'Sala' => 'Västmanlands Cykelförbund',
    'Fagersta' => 'Västmanlands Cykelförbund',
    'Hallstahammar' => 'Västmanlands Cykelförbund',
    'Surahammar' => 'Västmanlands Cykelförbund',
    'Arboga' => 'Västmanlands Cykelförbund',
    'Kungsör' => 'Västmanlands Cykelförbund',
    'Norberg' => 'Västmanlands Cykelförbund',
    'Skinnskatteberg' => 'Västmanlands Cykelförbund',

    // Dalarnas Cykelförbund (Dalarnas län)
    'Falun' => 'Dalarnas Cykelförbund',
    'Borlänge' => 'Dalarnas Cykelförbund',
    'Mora' => 'Dalarnas Cykelförbund',
    'Avesta' => 'Dalarnas Cykelförbund',
    'Ludvika' => 'Dalarnas Cykelförbund',
    'Hedemora' => 'Dalarnas Cykelförbund',
    'Säter' => 'Dalarnas Cykelförbund',
    'Leksand' => 'Dalarnas Cykelförbund',
    'Rättvik' => 'Dalarnas Cykelförbund',
    'Orsa' => 'Dalarnas Cykelförbund',
    'Malung' => 'Dalarnas Cykelförbund',
    'Malung-Sälen' => 'Dalarnas Cykelförbund',
    'Sälen' => 'Dalarnas Cykelförbund',
    'Vansbro' => 'Dalarnas Cykelförbund',
    'Älvdalen' => 'Dalarnas Cykelförbund',
    'Gagnef' => 'Dalarnas Cykelförbund',
    'Smedjebacken' => 'Dalarnas Cykelförbund',
    'Idre' => 'Dalarnas Cykelförbund',
    'Grönklitt' => 'Dalarnas Cykelförbund',

    // Gästriklands Cykelförbund (Gävle och södra Gävleborg)
    'Gävle' => 'Gästriklands Cykelförbund',
    'Sandviken' => 'Gästriklands Cykelförbund',
    'Hofors' => 'Gästriklands Cykelförbund',
    'Ockelbo' => 'Gästriklands Cykelförbund',
    'Älvkarleby' => 'Gästriklands Cykelförbund',

    // Hälsinglands Cykelförbund (Norra Gävleborg)
    'Hudiksvall' => 'Hälsinglands Cykelförbund',
    'Bollnäs' => 'Hälsinglands Cykelförbund',
    'Söderhamn' => 'Hälsinglands Cykelförbund',
    'Ljusdal' => 'Hälsinglands Cykelförbund',
    'Ovanåker' => 'Hälsinglands Cykelförbund',
    'Nordanstig' => 'Hälsinglands Cykelförbund',
    'Järvsö' => 'Hälsinglands Cykelförbund',
    'Kårböle' => 'Hälsinglands Cykelförbund',

    // Västernorrlands Cykelförbund (Västernorrlands län)
    'Sundsvall' => 'Västernorrlands Cykelförbund',
    'Härnösand' => 'Västernorrlands Cykelförbund',
    'Örnsköldsvik' => 'Västernorrlands Cykelförbund',
    'Sollefteå' => 'Västernorrlands Cykelförbund',
    'Kramfors' => 'Västernorrlands Cykelförbund',
    'Timrå' => 'Västernorrlands Cykelförbund',
    'Ånge' => 'Västernorrlands Cykelförbund',

    // Jämtland-Härjedalens Cykelförbund (Jämtlands län)
    'Östersund' => 'Jämtland-Härjedalens Cykelförbund',
    'Krokom' => 'Jämtland-Härjedalens Cykelförbund',
    'Åre' => 'Jämtland-Härjedalens Cykelförbund',
    'Strömsund' => 'Jämtland-Härjedalens Cykelförbund',
    'Berg' => 'Jämtland-Härjedalens Cykelförbund',
    'Bräcke' => 'Jämtland-Härjedalens Cykelförbund',
    'Ragunda' => 'Jämtland-Härjedalens Cykelförbund',
    'Härjedalen' => 'Jämtland-Härjedalens Cykelförbund',
    'Sveg' => 'Jämtland-Härjedalens Cykelförbund',
    'Funäsdalen' => 'Jämtland-Härjedalens Cykelförbund',
    'Tännäs' => 'Jämtland-Härjedalens Cykelförbund',
    'Björnrike' => 'Jämtland-Härjedalens Cykelförbund',
    'Vemdalen' => 'Jämtland-Härjedalens Cykelförbund',
    'Lofsdalen' => 'Jämtland-Härjedalens Cykelförbund',

    // Västerbottens Cykelförbund (Västerbottens län)
    'Umeå' => 'Västerbottens Cykelförbund',
    'Skellefteå' => 'Västerbottens Cykelförbund',
    'Lycksele' => 'Västerbottens Cykelförbund',
    'Vilhelmina' => 'Västerbottens Cykelförbund',
    'Storuman' => 'Västerbottens Cykelförbund',
    'Dorotea' => 'Västerbottens Cykelförbund',
    'Sorsele' => 'Västerbottens Cykelförbund',
    'Åsele' => 'Västerbottens Cykelförbund',
    'Vindeln' => 'Västerbottens Cykelförbund',
    'Robertsfors' => 'Västerbottens Cykelförbund',
    'Vännäs' => 'Västerbottens Cykelförbund',
    'Norsjö' => 'Västerbottens Cykelförbund',
    'Malå' => 'Västerbottens Cykelförbund',
    'Nordmaling' => 'Västerbottens Cykelförbund',
    'Bjurholm' => 'Västerbottens Cykelförbund',

    // Norrbottens Cykelförbund (Norrbottens län)
    'Luleå' => 'Norrbottens Cykelförbund',
    'Piteå' => 'Norrbottens Cykelförbund',
    'Boden' => 'Norrbottens Cykelförbund',
    'Kiruna' => 'Norrbottens Cykelförbund',
    'Gällivare' => 'Norrbottens Cykelförbund',
    'Kalix' => 'Norrbottens Cykelförbund',
    'Haparanda' => 'Norrbottens Cykelförbund',
    'Älvsbyn' => 'Norrbottens Cykelförbund',
    'Arvidsjaur' => 'Norrbottens Cykelförbund',
    'Arjeplog' => 'Norrbottens Cykelförbund',
    'Jokkmokk' => 'Norrbottens Cykelförbund',
    'Överkalix' => 'Norrbottens Cykelförbund',
    'Övertorneå' => 'Norrbottens Cykelförbund',
    'Pajala' => 'Norrbottens Cykelförbund',
];

// Additional known destination mappings (based on venue names)
$knownDestinations = [
    // Bike parks and specific locations
    'Järvsö Bergscykelpark' => 'Hälsinglands Cykelförbund',
    'Järvsö' => 'Hälsinglands Cykelförbund',
    'Isaberg' => 'Smålands Cykelförbund',
    'Gesundaberget' => 'Dalarnas Cykelförbund',
    'Romme Alpin' => 'Dalarnas Cykelförbund',
    'Kungsberget' => 'Gästriklands Cykelförbund',
    'Hammarbybacken' => 'Stockholms Cykelförbund',
    'Vallåsen' => 'Hallands Cykelförbund',
    'Branäs' => 'Värmlands Cykelförbund',
    'Tolvmannabacken' => 'Stockholms Cykelförbund',
    'Bocksten' => 'Hallands Cykelförbund',
    'Skatås' => 'Göteborgs Cykelförbund',
    'Partille Arena' => 'Göteborgs Cykelförbund',
    'Ekbacken' => 'Upplands Cykelförbund',
    'Ulriksdal' => 'Stockholms Cykelförbund',
    'Nacka' => 'Stockholms Cykelförbund',
    'Hellasgården' => 'Stockholms Cykelförbund',
    'Storhogna' => 'Jämtland-Härjedalens Cykelförbund',
    'Klövsjö' => 'Jämtland-Härjedalens Cykelförbund',
    'Bruksvallarna' => 'Jämtland-Härjedalens Cykelförbund',
    'Tänndalen' => 'Jämtland-Härjedalens Cykelförbund',
    'Hemavan' => 'Västerbottens Cykelförbund',
    'Tärnaby' => 'Västerbottens Cykelförbund',
    'Dundret' => 'Norrbottens Cykelförbund',
    'Riksgränsen' => 'Norrbottens Cykelförbund',
    'Kåbdalis' => 'Norrbottens Cykelförbund',
];

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';
    $updated = 0;
    $skipped = 0;

    if ($action === 'auto_map') {
        // Get all destinations without region
        $destinations = $db->getAll("SELECT id, name, city, region FROM venues WHERE (region IS NULL OR region = '')");

        foreach ($destinations as $dest) {
            $matchedDistrict = null;

            // First try to match by city
            if (!empty($dest['city'])) {
                $city = trim($dest['city']);
                foreach ($cityToDistrict as $c => $district) {
                    if (strcasecmp($city, $c) === 0 || stripos($city, $c) !== false) {
                        $matchedDistrict = $district;
                        break;
                    }
                }
            }

            // If no city match, try to match by destination name
            if (!$matchedDistrict && !empty($dest['name'])) {
                $name = trim($dest['name']);
                foreach ($knownDestinations as $knownName => $district) {
                    if (stripos($name, $knownName) !== false) {
                        $matchedDistrict = $district;
                        break;
                    }
                }

                // Also try city mapping against name
                if (!$matchedDistrict) {
                    foreach ($cityToDistrict as $c => $district) {
                        if (stripos($name, $c) !== false) {
                            $matchedDistrict = $district;
                            break;
                        }
                    }
                }
            }

            if ($matchedDistrict) {
                $db->update('venues', ['region' => $matchedDistrict], 'id = ?', [$dest['id']]);
                $updated++;
            } else {
                $skipped++;
            }
        }

        $message = "Uppdaterade $updated destinationer. $skipped kunde inte matchas automatiskt.";
        $messageType = 'success';
    }

    if ($action === 'update_single') {
        $destId = (int)($_POST['dest_id'] ?? 0);
        $region = trim($_POST['region'] ?? '');

        if ($destId > 0 && !empty($region)) {
            $db->update('venues', ['region' => $region], 'id = ?', [$destId]);
            $message = "Destination uppdaterad!";
            $messageType = 'success';
        }
    }
}

// Get destinations without region
$unmappedDestinations = $db->getAll("
    SELECT v.id, v.name, v.city,
           COUNT(DISTINCT e.id) as event_count
    FROM venues v
    LEFT JOIN events e ON e.venue_id = v.id
    WHERE (v.region IS NULL OR v.region = '')
    GROUP BY v.id
    ORDER BY event_count DESC, v.name
");

// Page config
$page_title = 'Koppla destinationer till regioner';
$breadcrumbs = [
    ['label' => 'Destinations', 'url' => '/admin/destinations.php'],
    ['label' => 'Auto-map regioner']
];
include __DIR__ . '/../components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert--<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'info' ?>"></i>
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Auto-map Action -->
<div class="card mb-lg">
    <div class="card-header">
        <h2>
            <i data-lucide="wand-2"></i>
            Automatisk regionkoppling
        </h2>
    </div>
    <div class="card-body">
        <p class="text-secondary mb-md">
            Kopplar automatiskt destinationer till SCF-distrikt baserat på stad eller platsnamn.
            <?= count($unmappedDestinations) ?> destinationer saknar region.
        </p>
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="auto_map">
            <button type="submit" class="btn btn--primary" <?= empty($unmappedDestinations) ? 'disabled' : '' ?>>
                <i data-lucide="zap"></i>
                Kör automatisk mappning (<?= count($unmappedDestinations) ?>)
            </button>
        </form>
    </div>
</div>

<!-- Unmapped Destinations -->
<?php if (!empty($unmappedDestinations)): ?>
<div class="card">
    <div class="card-header">
        <h2>
            <i data-lucide="map-pin"></i>
            Destinationer utan region (<?= count($unmappedDestinations) ?>)
        </h2>
    </div>
    <div class="card-body" style="padding: 0;">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Destination</th>
                        <th>Stad</th>
                        <th>Events</th>
                        <th>Välj region</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $scfDistricts = [
                        'Bohuslän-Dals Cykelförbund',
                        'Dalarnas Cykelförbund',
                        'Gästriklands Cykelförbund',
                        'Göteborgs Cykelförbund',
                        'Hallands Cykelförbund',
                        'Hälsinglands Cykelförbund',
                        'Jämtland-Härjedalens Cykelförbund',
                        'Norrbottens Cykelförbund',
                        'Skånes Cykelförbund',
                        'Smålands Cykelförbund',
                        'Stockholms Cykelförbund',
                        'Södermanlands Cykelförbund',
                        'Upplands Cykelförbund',
                        'Värmlands Cykelförbund',
                        'Västerbottens Cykelförbund',
                        'Västergötlands Cykelförbund',
                        'Västernorrlands Cykelförbund',
                        'Västmanlands Cykelförbund',
                        'Örebro Läns Cykelförbund',
                        'Östergötlands Cykelförbund'
                    ];
                    foreach ($unmappedDestinations as $dest):
                    ?>
                    <tr>
                        <td><strong><?= htmlspecialchars($dest['name']) ?></strong></td>
                        <td class="text-secondary"><?= htmlspecialchars($dest['city'] ?? '-') ?></td>
                        <td>
                            <?php if ($dest['event_count'] > 0): ?>
                            <span class="badge badge--accent"><?= $dest['event_count'] ?></span>
                            <?php else: ?>
                            <span class="badge badge--secondary">0</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <form method="POST" class="flex gap-xs items-center">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="update_single">
                                <input type="hidden" name="dest_id" value="<?= $dest['id'] ?>">
                                <select name="region" class="input" style="width: 220px; font-size: var(--text-sm);">
                                    <option value="">-- Välj --</option>
                                    <?php foreach ($scfDistricts as $district): ?>
                                    <option value="<?= htmlspecialchars($district) ?>"><?= htmlspecialchars($district) ?></option>
                                    <?php endforeach; ?>
                                </select>
                                <button type="submit" class="btn btn--secondary btn--sm">
                                    <i data-lucide="check"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php else: ?>
<div class="card">
    <div class="card-body text-center py-xl">
        <i data-lucide="check-circle" class="text-success" style="width: 48px; height: 48px;"></i>
        <h3 class="mt-md">Alla destinationer har regioner!</h3>
        <p class="text-secondary">Det finns inga destinationer som saknar regionkoppling.</p>
        <a href="/admin/destinations.php" class="btn btn--secondary mt-md">
            <i data-lucide="arrow-left"></i>
            Tillbaka till destinationer
        </a>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
