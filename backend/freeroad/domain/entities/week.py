from datetime import datetime
from typing import Optional

class Week:
    def __init__(
        self,
        id: str,
        user_id: str,
        title: str,
        kmAtual: str,
        kmFinal: str,
        custo: str,
        eficiencia: str,
        litrosAbastecidos: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.kmAtual = kmAtual
        self.kmFinal = kmFinal
        self.custo = custo
        self.eficiencia = eficiencia
        self.litrosAbastecidos = litrosAbastecidos
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
