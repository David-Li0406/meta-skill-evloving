from typing import Generic, TypeVar, List, Optional, Type
import os
from supabase import create_client, Client

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """
    Classe base para repositórios Supabase.
    Gerencia a conexão e operações CRUD básicas.
    """
    def __init__(self, table_name: str):
        self.table_name = table_name
        self._client: Optional[Client] = None

    @property
    def client(self) -> Client:
        if not self._client:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if not url or not key:
                raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidos no .env")
            self._client = create_client(url, key)
        return self._client

    def get_all(self) -> List[dict]:
        """Retorna todos os registros da tabela."""
        try:
            response = self.client.table(self.table_name).select("*").execute()
            return response.data
        except Exception as e:
            print(f"Erro ao buscar dados em {self.table_name}: {e}")
            return []

    def get_by_id(self, id: str) -> Optional[dict]:
        """Retorna um registro pelo ID."""
        try:
            response = self.client.table(self.table_name).select("*").eq("id", id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Erro ao buscar ID {id} em {self.table_name}: {e}")
            return None

    def create(self, data: dict) -> Optional[dict]:
        """Cria um novo registro."""
        try:
            response = self.client.table(self.table_name).insert(data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Erro ao criar registro em {self.table_name}: {e}")
            return None

    def update(self, id: str, data: dict) -> Optional[dict]:
        """Atualiza um registro existente."""
        try:
            response = self.client.table(self.table_name).update(data).eq("id", id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Erro ao atualizar ID {id} em {self.table_name}: {e}")
            return None

    def delete(self, id: str) -> bool:
        """Deleta um registro."""
        try:
            self.client.table(self.table_name).delete().eq("id", id).execute()
            return True
        except Exception as e:
            print(f"Erro ao deletar ID {id} em {self.table_name}: {e}")
            return False
