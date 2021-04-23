import boto3
import re
import json
import concurrent.futures


# {"text": "///V. Pinocchio ha fame e cerca un uovo per farsi una frittata; ma sul pi\u00f9 bello, la frittata gli vola via dalla finestra.///Intanto cominci\u00f2 a farsi notte, e Pinocchio, ricordandosi che non aveva mangiato nulla, sent\u00ec un'uggiolina allo stomaco, che somigliava moltissimo all'appetito./n/Ma l'appetito dei ragazzi cammina presto, e difatti, dopo pochi minuti l'appetito divent\u00f2 fame, e la fame, dal vedere al non vedere si convert\u00ec in una fame da lupi, in una fame da tagliarsi col coltello./n/Il povero Pinocchio corse subito al focolare dove c'era una pentola che bolliva, e fece l'atto di scoperchiarla, per vedere che cosa ci fosse dentro: ma la pentola era dipinta sul muro. Immaginatevi come rest\u00f2. Il suo naso, che era gi\u00e0 lungo, gli divent\u00f2 pi\u00f9 lungo almeno quattro dita./n/Allora si d\u00e8tte a correre per la stanza e a frugare per tutte le cassette e per tutti i ripostigli  in cerca di un po' di pane, magari un po' di pan secco, un crosterello, un osso avanzato al cane, un po' di polenta muffita, una lisca di pesce, un nocciolo di ciliegia, insomma qualche cosa da masticare: ma non trov\u00f2 nulla, il gran nulla, proprio nulla./n/E intanto la fame cresceva, e cresceva sempre: e il povero Pinocchio non aveva altro sollievo che quello di sbadigliare e faceva degli sbadigli cos\u00ec lunghi, che qualche volta la bocca gli arrivava fino agli orecchi. E dopo avere sbadigliato, sputava, e sentiva che lo stomaco gli andava via./n/Allora piangendo e disperandosi, diceva:/n/\u2014 Il Grillo-parlante aveva ragione. Ho fatto male a rivoltarmi al mio babbo e a fuggire di casa.... Se il mio babbo fosse qui ora non mi troverei a morire di sbadigli! Oh! che brutta malattia che \u00e8 la fame!\u00a0\u2014/n/Quand'ecco che gli parve di vedere nel monte della spazzatura qualche cosa di tondo e di bianco, che somigliava tutto ad un uovo di gallina. Spiccare un salto e gettarvisi sopra, fu un punto solo. Era un uovo davvero./n/La gioia del burattino \u00e8 impossibile descriverla: bisogna sapersela figurare. Credendo quasi che fosse un sogno, si rigirava quest'uovo fra  le mani, e lo toccava e lo baciava e baciandolo diceva:/n/\u2014 E ora come dovr\u00f2 cuocerlo? Ne far\u00f2 una frittata?... No, \u00e8 meglio cuocerlo nel piatto!... o non sarebbe pi\u00f9 saporito se lo friggessi in padella? O se invece lo cuocessi a uso uovo a bere? No, la pi\u00f9 lesta di tutte \u00e8 di cuocerlo nel piatto o nel tegamino: ho troppa voglia di mangiarmelo!\u00a0\u2014/n/Detto fatto, pose un tegamino sopra un caldano pieno di brace accesa: messe nel tegamino, invece d'olio o di burro, un po' d'acqua: e quando l'acqua principi\u00f2 a fumare, tac!... spezz\u00f2 il guscio dell'uovo, e fece l'atto di scodellarvelo dentro./n/Ma invece della chiara e del torlo scapp\u00f2 fuori un pulcino tutto allegro e complimentoso, il quale facendo una bella riverenza disse:/n/\u2014 Mille grazie, signor Pinocchio, d'avermi risparmiata la fatica di rompere il guscio! Arrivedella, stia bene e tanti saluti a casa!\u00a0\u2014/n/Ci\u00f2 detto, distese le ali, e, infilata la finestra che era aperta, se ne vol\u00f2 via a perdita d'occhio./n/Il povero burattino rimase l\u00ec, come incantato, cogli occhi fissi, colla bocca aperta e coi gusci dell'uovo in mano. Riavutosi, peraltro, dal primo sbigottimento, cominci\u00f2 a piangere, a strillare,  a battere i piedi in terra per la disperazione, e piangendo diceva:/n/\u2014 Eppure il Grillo-parlante aveva ragione! Se non fossi scappato di casa e se il mio babbo fosse qui, ora non mi troverei a morire di fame. Eh! che brutta malattia che \u00e8 la fame!...\u00a0\u2014/n/E perch\u00e8 il corpo gli seguitava a brontolare pi\u00f9 che mai, e non sapeva come fare a chetarlo, pens\u00f2 di uscir di casa e di dare una scappata al paesello vicino, nella speranza di trovare qualche persona caritatevole, che gli facesse l'elemosina di un po' di pane.///"}
def concurrent_lambdacall(paragraph, aws_lambda):
    aws_lambda.invoke(FunctionName='split_ebook_words',
                      InvocationType='Event',
                      LogType='Tail',
                      Payload=bytes(json.dumps({"paragraph": paragraph}).encode())
                      )
    print('invoked concurrent')


def lambda_handler(event, context):
    chapter = event['text']

    # split text into paragraphs
    paragraphs = chapter.split('///')
    paragraphs = list(filter(lambda x: not re.fullmatch(r' *', x), paragraphs))

    # invoke for each paragraph
    aws_lambda = boto3.client('lambda')
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda x: concurrent_lambdacall(x, aws_lambda), paragraphs)
    except Exception as e:
        print(e)
        return {
            "statuscode": 500,
            "body": json.dumps("server error")
        }
    """
    for i in paragraphs:
        try:
            aws_lambda.invoke(FunctionName='split_ebook_words',
                             InvocationType='Event',
                             LogType='Tail',
                             Payload=bytes(json.dumps({"paragraph": i}).encode())
                )
        except Exception:
            print("Exception occured")
            return {
                "statuscode": 500,
                "body": json.dumps("server error")
            }
    """
    print(f'Executed: {paragraphs}')

    return {
        'statuscode': 200,
        'body': 'Everything is OK'
    }