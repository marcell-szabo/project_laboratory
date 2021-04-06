import json
import re
import time
import get_dictionary_form_testing
import concurrent.futures

#{"paragraphs": "Detto fatto, prese subito l'ascia arrotata per cominciare a levargli la scorza e a digrossarlo; ma quando fu l\u00ec per lasciare andare la prima asciata, rimase col braccio sospeso in aria, perch\u00e8 sent\u00ec una vocina sottile sottile, che disse raccomandandosi:/n/\u2014 Non mi picchiar tanto forte!\u00a0\u2014/n/Figuratevi come rimase quel buon vecchio di maestro Ciliegia!/n/Gir\u00f2 gli occhi smarriti intorno alla stanza per vedere di dove mai poteva essere uscita quella vocina, e non vide nessuno! Guard\u00f2 sotto il banco, e nessuno: guard\u00f2 dentro un armadio che stava sempre chiuso, e nessuno; guard\u00f2 nel corbello dei trucioli e della segatura, e nessuno; apr\u00ec l'uscio di bottega per dare un'occhiata anche sulla strada, e nessuno. O dunque?.../n/\u2014 Ho capito; \u2014 disse allora ridendo e grattandosi la parrucca \u2014 si vede che quella vocina me la son figurata io. Rimettiamoci a lavorare.\u00a0\u2014/n/E ripresa l'ascia in mano, tir\u00f2 gi\u00f9 un solennissimo colpo sul pezzo di legno./n/\u2014 Ohi! tu m'hai fatto male! \u2014 grid\u00f2 rammaricandosi la solita vocina./n/Questa volta maestro Ciliegia rest\u00f2 di stucco, cogli occhi fuori del capo per la paura, colla bocca  spalancata e colla lingua gi\u00f9 ciondoloni fino al mento, come un mascherone da fontana./n/Appena riebbe l'uso della parola, cominci\u00f2 a dire tremando e balbettando dallo spavento:/n/\u2014 Ma di dove sar\u00e0 uscita questa vocina che ha detto ohi?... Eppure qui non c'\u00e8 anima viva. Che sia per caso questo pezzo di legno che abbia imparato a piangere e a lamentarsi come un bambino? Io non lo posso credere. Questo legno eccolo qui; \u00e8 un pezzo di legno da caminetto, come tutti gli altri, e a buttarlo sul fuoco, c'\u00e8 da far bollire una pentola di fagioli.... O dunque? Che ci sia nascosto dentro qualcuno? Se c'\u00e8 nascosto qualcuno, tanto peggio per lui. Ora l'accomodo io!\u00a0\u2014/n/E cos\u00ec dicendo, agguant\u00f2 con tutt'e due le mani quel povero pezzo di legno, e si pose a sbatacchiarlo senza carit\u00e0 contro le pareti della stanza./n/Poi si messe in ascolto, per sentire se c'era qualche vocina che si lamentasse. Aspett\u00f2 due minuti, e nulla; cinque minuti, e nulla; dieci minuti, e nulla!/n/\u2014 Ho capito \u2014 disse allora sforzandosi di ridere e arruffandosi la parrucca \u2014 si vede che quella vocina che ha detto ohi, me la son figurata io! Rimettiamoci a lavorare.\u00a0\u2014/n/E perch\u00e8 gli era entrato addosso una gran  paura, si prov\u00f2 a canterellare per farsi un po' di coraggio./n/Intanto, posata da una parte l'ascia, prese in mano la pialla, per piallare e tirare a pulimento il pezzo di legno; ma nel mentre che lo piallava in su e in gi\u00f9, sent\u00ec la solita vocina che gli disse ridendo:/n/\u2014 Smetti! tu mi fai il pizzicorino sul corpo!\u00a0\u2014/n/Questa volta il povero maestro Ciliegia cadde gi\u00f9 come fulminato. Quando riapr\u00ec gli occhi, si trov\u00f2 seduto per terra./n/Il suo viso pareva trasfigurito, e perfino la punta del naso, di paonazza come era quasi sempre, gli era diventata turchina dalla gran paura."}
def main(paragraph_json):
    paragraph = json.loads(paragraph_json)["paragraphs"]
    paragraph = re.sub(r"/n/", r"\n", paragraph)
    words = re.split(r"\s", paragraph)
    words = list(map(lambda x: re.sub(r'.*[./,:";()—!?-]+.*', "", x), words))
    words = list(filter(lambda x: re.fullmatch(r"[a-zA-Z]+", x), words))
    words = list(map(lambda x: x.lower(), words))
    dict_of_words = {}
    for i in words:
        if i in dict_of_words:
            dict_of_words[i] += 1
        else:
            dict_of_words[i] = 1
    print(list(dict_of_words.keys()))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: get_dictionary_form_testing.lambda_handler({"word": x}, None), list(dict_of_words.keys()))

if __name__ == '__main__':
    text = input()
    t = time.process_time()
    main(text)
    print(f"-------------------{time.process_time() - t}------------------------")

