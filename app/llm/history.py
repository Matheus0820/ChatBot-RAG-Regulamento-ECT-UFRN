from app.database.chat_repository import ChatRepository

class History:

    def __init__(self):
        self.chat_repository = ChatRepository()


    def createHistory(self, user_id, question):

        # Busca os históricos atuais do usuário
        history = self.chat_repository.findAllHistory(user_id)

        # Se já tiver 5 mensagens
        if len(history) >= 5:

            # O último item da lista DESC é o mais antigo
            oldest_history = history[-1]

            # id do histórico
            oldest_history_id = oldest_history[0]

            # Remove o mais antigo
            self.chat_repository.deleteHistory(oldest_history_id)

        # Cria novo histórico
        self.chat_repository.createHistory(
            user_id,
            question
        )


    def createUserHistory(self, user_id, question):

        # Cria usuário caso não exista
        self.chat_repository.createUser(user_id)

        # Cria histórico seguindo regras
        self.createHistory(
            user_id,
            question
        )
    
    def getUserHistoryById(self, user_id):
        history = self.chat_repository.findAllHistory(user_id=user_id)
        return history

        