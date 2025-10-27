# Lista abrangente de categorias e subcategorias de despesas e receitas em pt-BR
# Inclui o máximo de opções úteis para o dia a dia brasileiro

CATEGORIES = {
    "Moradia": [
        "Aluguel",
        "Condomínio",
        "Prestação do imóvel",
        "IPTU",
        "Água",
        "Luz/Energia",
        "Gás",
        "Telefone fixo",
        "Internet",
        "TV a cabo/Streaming",
        "Seguro residencial",
        "Manutenção/Reparos",
        "Móveis e decoração",
        "Eletrodomésticos",
        "Limpeza",
        "Faxina/Empregada",
        "Jardinagem",
    ],
    "Alimentação": [
        "Supermercado",
        "Hortifruti/Feira",
        "Açougue",
        "Padaria",
        "Restaurante",
        "Lanche/Fast food",
        "Delivery",
        "Bebidas",
        "Café",
        "Água mineral",
        "Gás de cozinha",
    ],
    "Transporte": [
        "Combustível",
        "Estacionamento",
        "Pedágio",
        "IPVA",
        "Licenciamento",
        "Seguro do veículo",
        "Lavagem/Estética",
        "Manutenção/Revisão",
        "Pneus",
        "Peças",
        "Oficina",
        "Financiamento do veículo",
        "Transporte público",
        "Aplicativos (Uber, 99)",
        "Táxi",
        "Bicicleta/Patinete",
    ],
    "Saúde": [
        "Plano de saúde",
        "Odontológico",
        "Medicamentos",
        "Consultas",
        "Exames",
        "Terapias/Fisioterapia",
        "Academia",
        "Suplementos",
        "Óculos/Lentes",
        "Vacinas",
        "Emergências",
    ],
    "Educação": [
        "Mensalidade escolar",
        "Faculdade/Pós",
        "Cursos/Idiomas",
        "Livros/Material didático",
        "Transporte escolar",
        "Aulas particulares",
    ],
    "Trabalho/Renda": [
        "Ferramentas e softwares",
        "Equipamentos",
        "Coworking",
        "Cursos/Certificações",
        "Transporte de trabalho",
        "Impostos sobre renda",
        "MEI/Simples",
        "Taxas de marketplace",
    ],
    "Lazer": [
        "Cinema/Teatro",
        "Shows/Eventos",
        "Bares/Noites",
        "Viagens",
        "Passeios",
        "Hobbies",
        "Jogos",
        "Esportes",
        "Clubes",
        "Parques",
        "Assinaturas de jogos",
    ],
    "Pessoais": [
        "Roupas",
        "Calçados",
        "Acessórios",
        "Beleza/Estética",
        "Salão/Barbearia",
        "Cosméticos",
        "Cuidados pessoais",
        "Joias/Relógios",
    ],
    "Casa": [
        "Utensílios domésticos",
        "Produtos de limpeza",
        "Descartáveis",
        "Manutenção de eletrodomésticos",
        "Decoração",
    ],
    "Assinaturas/Serviços": [
        "Netflix/Prime/Disney+/HBO",
        "Spotify/Apple Music/Deezer",
        "Storage em nuvem",
        "Antivírus",
        "Softwares",
        "Clube de assinatura",
        "Revistas/Jornais",
    ],
    "Impostos/Taxas": [
        "IRPF",
        "ISS/ICMS",
        "Tarifas bancárias",
        "Tarifas de cartão",
        "Juros/Multas",
        "Cartório",
    ],
    "Investimentos": [
        "Aportes Renda Fixa",
        "Aportes Ações/FIIs",
        "Previdência privada",
        "Cripto",
        "Tesouro Direto",
        "Corretagem/Taxas",
    ],
    "Dívidas/Crédito": [
        "Cartão de crédito",
        "Empréstimo pessoal",
        "Financiamento",
        "Cheque especial",
        "Renegociação",
        "Juros",
    ],
    "Animais de estimação": [
        "Ração",
        "Petiscos",
        "Brinquedos",
        "Veterinário",
        "Banho e tosa",
        "Medicamentos",
        "Acessórios",
    ],
    "Crianças": [
        "Fraldas",
        "Leite/Fórmula",
        "Roupas infantis",
        "Brinquedos",
        "Babá/Creche",
        "Mesada",
        "Material escolar",
    ],
    "Presentes/Doações": [
        "Presentes",
        "Doações",
        "Aniversários",
        "Casamentos",
        "Natal",
    ],
    "Viagens": [
        "Passagens",
        "Hospedagem",
        "Bagagem",
        "Seguro viagem",
        "Aluguel de carro",
        "Câmbio",
        "Passeios/Tours",
    ],
    "Tecnologia": [
        "Celular",
        "Computador",
        "Acessórios",
        "Periféricos",
        "Apps",
        "Games/Consoles",
    ],
    "Serviços domésticos": [
        "Encanador",
        "Eletricista",
        "Pintura",
        "Marcenaria",
        "Chaveiro",
        "Dedetização",
        "Conserto geral",
    ],
}

# Categorias de receita (para referência; podem usar as mesmas chaves acima ou genéricas)
INCOME_CATEGORIES = {
    "Salário": ["Salário", "13º", "Bônus"],
    "Freelance": ["Projeto", "Consultoria", "Aulas"],
    "Rendimentos": ["Dividendos", "Juros", "Aluguel recebido"],
    "Reembolsos": ["Trabalho", "Saúde", "Cartão"],
    "Outros": ["Presentes", "Venda de itens", "Prêmios"],
}


def get_categories():
    # Apenas chaves; o app decide o uso conforme 'tipo'
    return list(CATEGORIES.keys())


def get_subcategories(categoria: str):
    return CATEGORIES.get(categoria, [])


# ---- Novas funções para receitas e visão combinada ----
def get_income_categories():
    return list(INCOME_CATEGORIES.keys())


def get_income_subcategories(categoria: str):
    return INCOME_CATEGORIES.get(categoria, [])


def get_all_categories():
    # União de chaves de despesas e receitas, mantendo ordem aproximada: despesas depois receitas
    return list(CATEGORIES.keys()) + [c for c in INCOME_CATEGORIES.keys() if c not in CATEGORIES]


def get_any_subcategories(categoria: str):
    # Busca subcategorias em despesas; se não achar, busca em receitas
    if categoria in CATEGORIES:
        return CATEGORIES[categoria]
    if categoria in INCOME_CATEGORIES:
        return INCOME_CATEGORIES[categoria]
    return []
