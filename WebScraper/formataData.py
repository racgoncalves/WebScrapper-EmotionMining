from dateutil.parser import *
from datetime import *

data = parse("Wed, 21 Oct 2020 14:22:43 +0000").strftime('%d-%m-%Y')
print("data traço:",data)

# Formata data com barra
dataFormatada = parse("Wed, 21 Oct 2020 14:22:43 +0000").strftime('%d/%m/%Y')
print("data barra:",dataFormatada)

# Pega a data de hoje
hoje = date.today()
print("data hoje:", hoje)

# Soma dias da data de hoje
futuro = date.fromordinal(hoje.toordinal() + 5)
print("data futuro:",futuro)

# Transforma string em data
futuro="28-10-2020"
futuro = datetime.strptime(futuro, '%d-%m-%Y').date()
print("data str:",futuro)

# Transforma string do datapicker em data
futuro="2020-10-28"
futuro = datetime.strptime(futuro, '%Y-%m-%d').date()
print("data datapicker:",futuro)

# Looping com data de hoje e data futura
while (futuro > hoje):
    diferenca = futuro - hoje
    print ("diferença entre",futuro,"e",hoje,":",diferenca.days)
    futuro = date.fromordinal(futuro.toordinal() - 1)


