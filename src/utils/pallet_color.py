def pallet_color():
    pallet_color_ = {
        'cinza': '#262626',
        'cinza_escuro': '#0D0D0D',
        'alaranjado': '#F2A649',
        'branco': '#FFFFFF'
        
    }
    
    return pallet_color_

def color_barra (status_bar):
    palet_color_barra = {'inicio': '#55B3F2', 'meio': '#EDF54B', 'final': '#F22929'}
    cor = ''
    
    if status_bar['progresso'] >= 300: 
        cor = palet_color_barra['inicio']
    elif status_bar['progresso'] < 300 and status_bar['progresso'] >= 100:
        cor = palet_color_barra['meio']
    else:
        cor = palet_color_barra['final']
        
    return cor