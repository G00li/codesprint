import logging

logger = logging.getLogger("crewai_agents")

def extract_section(text, section_name):
    """Extrai uma seção específica do resultado - versão melhorada"""
    try:
        if not text or not section_name:
            return ""
            
        # Normaliza o texto e o nome da seção para comparação
        text_lower = text.lower()
        section_name_lower = section_name.lower()
        
        # Procura pelo título da seção
        section_start = text_lower.find(f"# {section_name_lower}")
        if section_start == -1:
            # Tenta encontrar sem o #
            section_start = text_lower.find(section_name_lower)
            if section_start == -1:
                return ""
        
        # Encontra o início do conteúdo (após o título)
        content_start = text.find('\n', section_start)
        if content_start == -1:
            return ""
        content_start += 1  # Pula a quebra de linha
        
        # Encontra o próximo título de seção
        next_section = text.find('#', content_start)
        if next_section == -1:
            # Se não houver próxima seção, pega todo o conteúdo até o final
            return text[content_start:].strip()
        
        # Retorna o conteúdo entre o título atual e o próximo título
        return text[content_start:next_section].strip()
    except Exception as e:
        logger.error(f"Erro ao extrair seção {section_name}: {str(e)}")
        return ""

def extract_resources(resources_text):
    """Converte recursos de texto para uma lista - versão melhorada"""
    if not resources_text:
        return []
    
    # Dividir por linhas e remover espaços
    lines = [line.strip() for line in resources_text.split('\n') if line.strip()]
    
    # Filtrar linhas que começam com - ou *
    resources = []
    for line in lines:
        if line.startswith('- ') or line.startswith('* '):
            # Remove o marcador e espaços extras
            resource = line[2:].strip()
            if resource:
                resources.append(resource)
        elif line.startswith('## '):
            # Adiciona o título da subseção como um recurso
            resources.append(line[3:].strip())
    
    return resources 