from freeroad.domain.repositories.week_repository import WeekRepository


class DeleteWeekUseCase:
    def __init__(self, repository: WeekRepository):
        self.repository = repository

    def execute(self, week_id: str) -> None:
        """
        Remove um registro de abastecimento.
        
        Args:
            week_id: ID do registro a ser removido
        """
        self.repository.delete(week_id)
