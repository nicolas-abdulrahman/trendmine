export class User {
  id: number;
  email: string;
  name: string;
  score: number;

  constructor(id: number, email: string, name: string, score: number) {
    // Atribuímos manualmente os valores
    this.id = id;
    this.email = email;
    this.name = name;
    this.score = score;
  }

  // Transforma o JSON do servidor ou do LocalStorage em uma instância da Classe User
  static fromJSON(data: any): User {
    return new User(data.id, data.email, data.name, data.score);
  }

  // Busca o usuário logado no momento
  static current(): User | null {
    const data = localStorage.getItem("user");
    if (!data) return null;
    try {
      return User.fromJSON(JSON.parse(data));
    } catch {
      return null;
    }
  }

  // Salva os dados no storage
  persist() {
    localStorage.setItem("user", JSON.stringify(this));
  }

  // Atalho para atualizar o score
  updateScore(newScore: number) {
    this.score = newScore;
    this.persist();
  }

  // Limpa a sessão
  static logout() {
    localStorage.removeItem("user");
  }
}
