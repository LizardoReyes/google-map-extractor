""" Esta script procesa archivos CSV para extraer palabras clave de preguntas frecuentes (headlines) y elimina canibalizaciones entre ellas.
    Requiere:
        - /input: directorio con archivos CSV que contienen la columna "Also Asked Headline".
        - /output: directorio donde se guardarán los resultados en formato TXT y CSV.
"""

import unicodedata

import pandas as pd

from pathlib import Path
from partials.helper_csv import read_csv_full
from typing import List, Set

STOPWORDS_ES = {"de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","no","una","su","al","lo","como","m\u00e1s","pero","sus","le","ya","o","este","s\u00ed","porque","esta","entre","cuando","muy","sin","sobre","tambi\u00e9n","me","hasta","hay","donde","quien","desde","todo","nos","durante","todos","uno","les","ni","contra","otros","ese","eso","ante","ellos","e","esto","m\u00ed","antes","algunos","qu\u00e9","unos","yo","otro","otras","otra","\u00e9l","tanto","esa","estos","mucho","quienes","nada","muchos","cual","poco","ella","estar","estas","algunas","algo","nosotros","mi","mis","t\u00fa","te","ti","tu","tus","ellas","nosotras","vosotros","vosotras","os","m\u00edo","m\u00eda","m\u00edos","m\u00edas","tuyo","tuya","tuyos","tuyas","suyo","suya","suyos","suyas","nuestro","nuestra","nuestros","nuestras","vuestro","vuestra","vuestros","vuestras","esos","esas","estoy","est\u00e1s","est\u00e1","estamos","est\u00e1is","est\u00e1n","est\u00e9","est\u00e9s","estemos","est\u00e9is","est\u00e9n","estar\u00e9","estar\u00e1s","estar\u00e1","estaremos","estar\u00e9is","estar\u00e1n","estar\u00eda","estar\u00edas","estar\u00edamos","estar\u00edais","estar\u00edan","estaba","estabas","est\u00e1bamos","estabais","estaban","estuve","estuviste","estuvo","estuvimos","estuvisteis","estuvieron","estuviera","estuvieras","estuvi\u00e9ramos","estuvierais","estuvieran","estuviese","estuvieses","estuvi\u00e9semos","estuvieseis","estuviesen","estando","estado","estada","estados","estadas","estad","he","has","ha","hemos","hab\u00e9is","han","haya","hayas","hayamos","hay\u00e1is","hayan","habr\u00e9","habr\u00e1s","habr\u00e1","habremos","habr\u00e9is","habr\u00e1n","habr\u00eda","habr\u00edas","habr\u00edamos","habr\u00edais","habr\u00edan","hab\u00eda","hab\u00edas","hab\u00edamos","hab\u00edais","hab\u00edan","hube","hubiste","hubo","hubimos","hubisteis","hubieron","hubiera","hubieras","hubi\u00e9ramos","hubierais","hubieran","hubiese","hubieses","hubi\u00e9semos","hubieseis","hubiesen","habiendo","habido","habida","habidos","habidas","soy","eres","es","somos","sois","son","sea","seas","seamos","se\u00e1is","sean","ser\u00e9","ser\u00e1s","ser\u00e1","seremos","ser\u00e9is","ser\u00e1n","ser\u00eda","ser\u00edas","ser\u00edamos","ser\u00edais","ser\u00edan","era","eras","\u00e9ramos","erais","eran","fui","fuiste","fue","fuimos","fuisteis","fueron","fuera","fueras","fu\u00e9ramos","fuerais","fueran","fuese","fueses","fu\u00e9semos","fueseis","fuesen","siendo","sido","tengo","tienes","tiene","tenemos","ten\u00e9is","tienen","tenga","tengas","tengamos","teng\u00e1is","tengan","tendr\u00e9","tendr\u00e1s","tendr\u00e1","tendremos","tendr\u00e9is","tendr\u00e1n","tendr\u00eda","tendr\u00edas","tendr\u00edamos","tendr\u00edais","tendr\u00edan","ten\u00eda","ten\u00edas","ten\u00edamos","ten\u00edais","ten\u00edan","tuve","tuviste","tuvo","tuvimos","tuvisteis","tuvieron","tuviera","tuvieras","tuvi\u00e9ramos","tuvierais","tuvieran","tuviese","tuvieses","tuvi\u00e9semos","tuvieseis","tuviesen","teniendo","tenido","tenida","tenidos","tenidas","tened",""}
STOPWORDS_EN = {"i","me","my","myself","we","us","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","whose","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","will","would","should","can","could","ought","i'm","you're","he's","she's","it's","we're","they're","i've","you've","we've","they've","i'd","you'd","he'd","she'd","we'd","they'd","i'll","you'll","he'll","she'll","we'll","they'll","isn't","aren't","wasn't","weren't","hasn't","haven't","hadn't","doesn't","don't","didn't","won't","wouldn't","shan't","shouldn't","can't","cannot","couldn't","mustn't","let's","that's","who's","what's","here's","there's","when's","where's","why's","how's","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","upon","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","say","says","said","shall",""}
STOPWORDS_FR = {"ai","au","aux","avec","ce","ces","dans","de","des","du","elle","en","et","eux","il","je","la","le","les","leur","lui","ma","mais","me","m\u00eame","mes","moi","mon","ne","nos","notre","nous","on","ou","par","pas","pour","qu","que","qui","sa","se","ses","son","sur","ta","te","tes","toi","ton","tu","un","une","vos","votre","vous","c","d","j","l","\u00e0","m","n","s","t","y","\u00e9t\u00e9","\u00e9t\u00e9e","\u00e9t\u00e9es","\u00e9t\u00e9s","\u00e9tant","\u00e9tante","\u00e9tants","\u00e9tantes","suis","es","est","sommes","\u00eates","sont","serai","seras","sera","serons","serez","seront","serais","serait","serions","seriez","seraient","\u00e9tais","\u00e9tait","\u00e9tions","\u00e9tiez","\u00e9taient","fus","fut","f\u00fbmes","f\u00fbtes","furent","sois","soit","soyons","soyez","soient","fusse","fusses","f\u00fbt","fussions","fussiez","fussent","ayant","ayante","ayantes","ayants","eu","eue","eues","eus","ai","as","avons","avez","ont","aurai","auras","aura","aurons","aurez","auront","aurais","aurait","aurions","auriez","auraient","avais","avait","avions","aviez","avaient","eut","e\u00fbmes","e\u00fbtes","eurent","aie","aies","ait","ayons","ayez","aient","eusse","eusses","e\u00fbt","eussions","eussiez","eussent",""}
STOPWORDS_PT = {"de","a","o","que","e","do","da","em","um","para","pra","com","n\u00e3o","uma","os","no","se","na","por","mais","as","dos","como","mas","ao","ele","das","\u00e0","seu","sua","ou","quando","muito","nos","j\u00e1","eu","tamb\u00e9m","s\u00f3","pelo","pela","at\u00e9","isso","ela","entre","depois","sem","mesmo","aos","seus","quem","nas","me","esse","eles","voc\u00ea","essa","num","nem","suas","meu","\u00e0s","minha","numa","pelos","elas","qual","n\u00f3s","lhe","deles","essas","esses","pelas","este","dele","tu","te","voc\u00eas","vos","lhes","meus","minhas","teu","tua","teus","tuas","nosso","nossa","nossos","nossas","dela","delas","esta","estes","estas","aquele","aquela","aqueles","aquelas","isto","aquilo","estou","est\u00e1","estamos","est\u00e3o","estive","esteve","estivemos","estiveram","estava","est\u00e1vamos","estavam","estivera","estiv\u00e9ramos","esteja","estejamos","estejam","estivesse","estiv\u00e9ssemos","estivessem","estiver","estivermos","estiverem","hei","h\u00e1","havemos","h\u00e3o","houve","houvemos","houveram","houvera","houv\u00e9ramos","haja","hajamos","hajam","houvesse","houv\u00e9ssemos","houvessem","houver","houvermos","houverem","houverei","houver\u00e1","houveremos","houver\u00e3o","houveria","houver\u00edamos","houveriam","sou","somos","s\u00e3o","era","\u00e9ramos","eram","fui","foi","fomos","foram","fora","f\u00f4ramos","seja","sejamos","sejam","fosse","f\u00f4ssemos","fossem","for","formos","forem","serei","ser\u00e1","seremos","ser\u00e3o","seria","ser\u00edamos","seriam","tenho","tem","temos","t\u00e9m","tinha","t\u00ednhamos","tinham","tive","teve","tivemos","tiveram","tivera","tiv\u00e9ramos","tenha","tenhamos","tenham","tivesse","tiv\u00e9ssemos","tivessem","tiver","tivermos","tiverem","terei","ter\u00e1","teremos","ter\u00e3o","teria","ter\u00edamos","teriam",""}
STOPWORDS_IT = {"ad","al","allo","ai","agli","all","agl","alla","alle","con","col","coi","da","dal","dallo","dai","dagli","dall","dagl","dalla","dalle","di","del","dello","dei","degli","dell","degl","della","delle","in","nel","nello","nei","negli","nell","negl","nella","nelle","su","sul","sullo","sui","sugli","sull","sugl","sulla","sulle","per","tra","contro","io","tu","lui","lei","noi","voi","loro","mio","mia","miei","mie","tuo","tua","tuoi","tue","suo","sua","suoi","sue","nostro","nostra","nostri","nostre","vostro","vostra","vostri","vostre","mi","ti","ci","vi","lo","la","li","le","gli","ne","il","un","uno","una","ma","ed","se","perch\u00e9","anche","come","dov","dove","che","chi","cui","non","pi\u00f9","quale","quanto","quanti","quanta","quante","quello","quelli","quella","quelle","questo","questi","questa","queste","si","tutto","tutti","a","c","e","i","l","o","ho","hai","ha","abbiamo","avete","hanno","abbia","abbiate","abbiano","avr\u00f2","avrai","avr\u00e0","avremo","avrete","avranno","avrei","avresti","avrebbe","avremmo","avreste","avrebbero","avevo","avevi","aveva","avevamo","avevate","avevano","ebbi","avesti","ebbe","avemmo","aveste","ebbero","avessi","avesse","avessimo","avessero","avendo","avuto","avuta","avuti","avute","sono","sei","\u00e8","siamo","siete","sia","siate","siano","sar\u00f2","sarai","sar\u00e0","saremo","sarete","saranno","sarei","saresti","sarebbe","saremmo","sareste","sarebbero","ero","eri","era","eravamo","eravate","erano","fui","fosti","fu","fummo","foste","furono","fossi","fosse","fossimo","fossero","essendo","faccio","fai","facciamo","fanno","faccia","facciate","facciano","far\u00f2","farai","far\u00e0","faremo","farete","faranno","farei","faresti","farebbe","faremmo","fareste","farebbero","facevo","facevi","faceva","facevamo","facevate","facevano","feci","facesti","fece","facemmo","faceste","fecero","facessi","facesse","facessimo","facessero","facendo","sto","stai","sta","stiamo","stanno","stia","stiate","stiano","star\u00f2","starai","star\u00e0","staremo","starete","staranno","starei","staresti","starebbe","staremmo","stareste","starebbero","stavo","stavi","stava","stavamo","stavate","stavano","stetti","stesti","stette","stemmo","steste","stettero","stessi","stesse","stessimo","stessero","stando",""}
STOPWORDS_DE = {"aber","alle","allem","allen","aller","alles","als","also","am","an","ander","andere","anderem","anderen","anderer","anderes","anderm","andern","anderr","anders","auch","auf","aus","bei","bin","bis","bist","da","damit","dann","der","den","des","dem","die","das","dass","da\u00df","derselbe","derselben","denselben","desselben","demselben","dieselbe","dieselben","dasselbe","dazu","dein","deine","deinem","deinen","deiner","deines","denn","derer","dessen","dich","dir","du","dies","diese","diesem","diesen","dieser","dieses","doch","dort","durch","ein","eine","einem","einen","einer","eines","einig","einige","einigem","einigen","einiger","einiges","einmal","er","ihn","ihm","es","etwas","euer","eure","eurem","euren","eurer","eures","f\u00fcr","gegen","gewesen","hab","habe","haben","hat","hatte","hatten","hier","hin","hinter","ich","mich","mir","ihr","ihre","ihrem","ihren","ihrer","ihres","euch","im","in","indem","ins","ist","jede","jedem","jeden","jeder","jedes","jene","jenem","jenen","jener","jenes","jetzt","kann","kein","keine","keinem","keinen","keiner","keines","k\u00f6nnen","k\u00f6nnte","machen","man","manche","manchem","manchen","mancher","manches","mein","meine","meinem","meinen","meiner","meines","mit","muss","musste","nach","nicht","nichts","noch","nun","nur","ob","oder","ohne","sehr","sein","seine","seinem","seinen","seiner","seines","selbst","sich","sie","ihnen","sind","so","solche","solchem","solchen","solcher","solches","soll","sollte","sondern","sonst","\u00fcber","um","und","uns","unse","unsem","unsen","unser","unses","unter","viel","vom","von","vor","w\u00e4hrend","war","waren","warst","was","weg","weil","weiter","welche","welchem","welchen","welcher","welches","wenn","werde","werden","wie","wieder","will","wir","wird","wirst","wo","wollen","wollte","w\u00fcrde","w\u00fcrden","zu","zum","zur","zwar","zwischen",""}
STOPWORDS_CA = {"a","abans","ac\u00ed","ah","aix\u00ed","aix\u00f2","al","als","aleshores","algun","alguna","algunes","alguns","alhora","all\u00e0","all\u00ed","all\u00f2","altra","altre","altres","amb","ambd\u00f3s","ambdues","apa","aquell","aquella","aquelles","aquells","aquest","aquesta","aquestes","aquests","aqu\u00ed","baix","cada","cadasc\u00fa","cadascuna","cadascunes","cadascuns","com","contra","d\u2019un","d\u2019una","d\u2019unes","d\u2019uns","dalt","de","del","dels","des","despr\u00e9s","dins","dintre","donat","doncs","durant","e","eh","el","els","em","en","encara","ens","entre","\u00e9rem","eren","\u00e9reu","es","\u00e9s","esta","est\u00e0","est\u00e0vem","estaven","est\u00e0veu","esteu","et","etc","ets","fins","fora","gaireb\u00e9","ha","han","has","havia","he","hem","heu","hi ","ho","i","igual","iguals","ja","l\u2019hi","la","les","li","li\u2019n","llavors","m\u2019he","ma","mal","malgrat","mateix","mateixa","mateixes","mateixos","me","mentre","m\u00e9s","meu","meus","meva","meves","molt","molta","moltes","molts","mon","mons","n\u2019he","n\u2019hi","ne","ni","no","nogensmenys","nom\u00e9s","nosaltres","nostra","nostre","nostres","o","oh","oi","on","pas","pel","pels","per","per\u00f2","perqu\u00e8","poc ","poca","pocs","poques","potser","propi","qual","quals","quan","quant ","que","qu\u00e8","quelcom","qui","quin","quina","quines","quins","s'ha","s\u2019han","sa","semblant","semblants","ses","seu ","seus","seva","seva","seves","si","sobre","sobretot","s\u00f3c","solament","sols","son ","s\u00f3n","sons ","sota","sou","t\u2019ha","t\u2019han","t\u2019he","ta","tal","tamb\u00e9","tampoc","tan","tant","tanta","tantes","teu","teus","teva","teves","ton","tons","tot","tota","totes","tots","un","una","unes","uns","us","va","vaig","vam","van","vas","veu","vosaltres","vostra","vostre","vostres",""}

def remove_accents(text: str) -> str:
    text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')


def normalizar_texto(texto: str) -> str:
    texto = texto.replace("?", "").replace("¿", "").strip().lower()
    return remove_accents(texto)


def filtrar_canibalizaciones(frases: List[str], stopwords: Set[str] = STOPWORDS_ES) -> List[str]:
    """
    Elimina frases que son canibalizadas entre sí (mismas palabras, distinto orden),
    ignorando palabras vacías y tildes.
    """
    frases_filtradas = []
    representaciones = set()

    for frase in frases:
        palabras = remove_accents(frase.lower()).split()
        palabras_significativas = sorted([p for p in palabras if p not in stopwords])
        clave = ' '.join(palabras_significativas)
        if clave and clave not in representaciones:
            representaciones.add(clave)
            frases_filtradas.append(frase)

    return frases_filtradas


def extract_asked_headlines(input_dir: Path, output_dir: Path, txt_filename: str = "asked_headlines.txt",
                            csv_filename: str = "asked_headlines.csv", stopwords: Set[str] = STOPWORDS_ES) -> None:

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_csvs = list(input_dir.glob("*.csv"))
    if not all_csvs:
        print("⚠️ No se encontraron archivos CSV en", input_dir)
        return

    headlines_raw = []

    for csv_file in all_csvs:
        print(f"📄 Leyendo {csv_file.name}")
        df = read_csv_full(csv_file)
        if "Also Asked Headline" in df.columns:
            clean_lines = (
                df["Also Asked Headline"]
                .dropna()
                .astype(str)
                .apply(normalizar_texto)
                .tolist()
            )
            headlines_raw.extend(clean_lines)
        else:
            print(f"⚠️ Columna 'Also Asked Headline' no encontrada en {csv_file.name}")

    # Quitar duplicados normales
    headlines = list(set(headlines_raw))
    # Aplicar filtro de canibalizaciones
    headlines = filtrar_canibalizaciones(headlines)

    # Guardar como .txt
    txt_path = output_dir / txt_filename
    with open(txt_path, "w", encoding="utf-8") as f:
        for line in sorted(headlines):
            f.write(line + "\n")
    print(f"✅ Archivo TXT guardado en: {txt_path}")

    # Guardar como .csv (sin cabecera ni índice)
    csv_path = output_dir / csv_filename
    pd.DataFrame(sorted(headlines)).to_csv(csv_path, index=False, header=False, encoding="utf-8")
    print(f"✅ Archivo CSV guardado en: {csv_path}")

def main():
    # Definir rutas de entrada y salida
    input_dir = Path("input")
    output_dir = Path("output")

    # Combinar CSVs en el directorio de entrada
    extract_asked_headlines(input_dir=input_dir, output_dir=output_dir, stopwords=STOPWORDS_ES)


if __name__ == "__main__":
    main()