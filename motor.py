import numpy as np
import pandas as pd

class EmeklilikMotoru:
    def __init__(self, teknik_faiz=0.04):
        self.teknik_faiz = teknik_faiz # Aktüerlerin kullandığı standart faiz
        
    def hayatta_kalma_tablosu(self, baslangic_yas, bitis_yas=100):
        yaslar = np.arange(baslangic_yas, bitis_yas + 1)
        # Gompertz-Makeham yasası (Basitleştirilmiş): Yaşlandıkça ölüm riski artar
        q_x = 0.0001 * (1.1 ** yaslar) 
        
        survivors = [1.0]
        for q in q_x[:-1]:
            survivors.append(survivors[-1] * (1 - q))
            
        return pd.DataFrame({
            'Yas': yaslar,
            'Olum_Olasiligi': q_x,
            'Hayatta_Kalma_Orani': survivors
        })

# Test Edelim
motor = EmeklilikMotoru()
tablo = motor.hayatta_kalma_tablosu(30)
print(tablo.head(10)) # 30-40 yaş arası riskler