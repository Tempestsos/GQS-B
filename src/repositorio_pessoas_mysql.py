import os
from importlib import import_module
mysql_connector = import_module("mysql.connector")
ClientFlag = import_module("mysql.connector.constants").ClientFlag

from pessoa import Pessoa
from repositorio_pessoas import RepositorioPessoas


class RepositorioPessoasMySQL(RepositorioPessoas):
    """Grava e consulta pessoas no banco de dados."""

    def _conectar(self):
        return mysql_connector.connect(
            host="127.0.0.1",
            port=3306,
            database="cadastro_pessoas",
            user="cadastro_app",
            password=os.environ["CADASTRO_DB_PASSWORD"],
            client_flags=[ClientFlag.FOUND_ROWS],
        )

    def cadastrar(self, pessoa: Pessoa) -> None:
        with self._conectar() as conexao, conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pessoas (nome, idade, email) VALUES (%s, %s, %s)",
                (pessoa.getNome(), pessoa.getIdade(), pessoa.getEmail()),
            )
            conexao.commit()

    def buscar(self, nome: str) -> Pessoa | None:
        with self._conectar() as conexao, conexao.cursor() as cursor:
            cursor.execute(
                "SELECT nome, idade, email FROM pessoas WHERE nome = %s "
                "ORDER BY id LIMIT 1",
                (nome,),
            )
            linha = cursor.fetchone()
            return Pessoa(*linha) if linha is not None else None

    def listar(self) -> list[Pessoa]:
        with self._conectar() as conexao, conexao.cursor() as cursor:
            cursor.execute("SELECT nome, idade, email FROM pessoas ORDER BY id")
            return [Pessoa(*linha) for linha in cursor.fetchall()]

    def alterar(self, nome: str, nova_pessoa: Pessoa) -> bool:
        with self._conectar() as conexao, conexao.cursor() as cursor:
            cursor.execute(
                "UPDATE pessoas SET nome = %s, idade = %s, email = %s "
                "WHERE nome = %s ORDER BY id LIMIT 1",
                (
                    nova_pessoa.getNome(),
                    nova_pessoa.getIdade(),
                    nova_pessoa.getEmail(),
                    nome,
                ),
            )
            conexao.commit()
            return cursor.rowcount == 1