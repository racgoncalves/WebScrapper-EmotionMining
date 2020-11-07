import nltk
from copy import deepcopy
import acervoFrases

baseTreinamento = acervoFrases.getBase()

def aplicarStemmer(texto):
    stemmer = nltk.stem.RSLPStemmer()
    frasesStemming = []
    for (palavras, emocao) in texto:
        comStemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in stopwordsNLTK]
        frasesStemming.append((comStemming, emocao))
    return frasesStemming

def buscaPalavras(frases):
    todasPalavras = []
    for (palavras, emocao) in frases:
        todasPalavras.extend(palavras)
    return todasPalavras

def buscaFrequencia(palavras):
    palavras = nltk.FreqDist(palavras)
    return palavras

def buscaPalavrasUnicas(frequencia):
    freq = frequencia.keys()
    return freq

def extratorPalavras(documento):
    doc = set(documento)
    caracteristicas = {}
    for palavras in palavrasUnicasTreinamento:
        caracteristicas['%s' % palavras] = (palavras in doc)
    return caracteristicas

negativo = ['desgosto','medo','raiva','tristeza']
positivo = ['alegria','surpresa']

for i in range(len(baseTreinamento)):
    if baseTreinamento[i][1] in negativo:
        baseTreinamento[i][1] = 'negativo'
    if baseTreinamento[i][1] in positivo:
        baseTreinamento[i][1] = 'positivo'

stopwordsNLTK = nltk.corpus.stopwords.words('portuguese')
frasesStemmingTreinamento = aplicarStemmer(baseTreinamento)
palavrasTreinamento = buscaPalavras(frasesStemmingTreinamento)
frequenciaTreinamento = buscaFrequencia(palavrasTreinamento)
palavrasUnicasTreinamento = buscaPalavrasUnicas(frequenciaTreinamento)
baseCompletaTreinamento = nltk.classify.apply_features(extratorPalavras, frasesStemmingTreinamento)

# Constrói a tabela de probabilidade
classificador = nltk.NaiveBayesClassifier.train(baseCompletaTreinamento)

# Testes (não precisa remover stopwords)
teste = ['Acontece e Rádios Criativa e Cultura FM entrevistam novamente candidatos a partir de terça-feira, 03', 'Polícia Ambiental de Botucatu faz grande apreensão na Operação Pré-Piracema', 'Febre Aftosa: Campanha de vacinação tem início no dia 1º de novembro', 'Embraer divulga imagem conceitual de turboélice', 'Hoje é o último dia para realizar matrículas e rematrículas na rede estadual', 'Guarda Municipal resgata cães acorrentados e sem alimento em São Manuel', 'Apesar da chuva desta sexta-feira, 30, feriado prolongado deve ser de tempo estável em Botucatu', 'Pix começa a funcionar no dia 3 de novembro para clientes selecionados']
testeStemming = []
conjuntoTesteStemming = []
conjuntoNovoRegistro = []
conjuntoDistribuicao = []
stemmer = nltk.stem.RSLPStemmer()
for (frases) in teste:
    for (palavrasTreinamento) in frases.split():
        comStem = [p for p in palavrasTreinamento.split()]
        testeStemming.append(str(stemmer.stem(comStem[0])))
    # copia = deepcopy(testeStemming)
    conjuntoTesteStemming.append(deepcopy(testeStemming))
    testeStemming.clear()

for (registro) in conjuntoTesteStemming:
    novoRegistro = extratorPalavras(registro)
    distribuicao = classificador.prob_classify(novoRegistro)
    conjuntoNovoRegistro.append(novoRegistro)
    conjuntoDistribuicao.append(distribuicao)

contPositivo = 0
contNegativo = 0

# Imprime o resultado
for (registro) in conjuntoNovoRegistro:
    classificacao = classificador.classify(registro)
    if (classificacao == 'positivo'):
        contPositivo += 1
    else:
        contNegativo += 1

    print("Classe:", classificacao)

# Imprime a probabilidade do resultado
for distribuicao in conjuntoDistribuicao:
    for classe in distribuicao.samples():
        print("%s: %f" % (classe, distribuicao.prob(classe)))

print("Quantidade de Positivos:",contPositivo)
print("Quantidade de Negativos:",contNegativo)
print(str(contPositivo+contNegativo)+"|"+str(contPositivo)+"|"+str(contNegativo))