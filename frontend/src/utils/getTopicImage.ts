import log from "loglevel";

// Placeholder customizado com as cores do seu tema (Roxo #6a1cf6 e Texto Branco)
const NO_IMAGE_PLACEHOLDER = (name: string) =>
  `https://placehold.co/600x800/6a1cf6/ffffff/png?text=${encodeURIComponent(name)}+%0A(Sem+Foto)`;

export async function getTopicImage(name: string): Promise<string> {
  // 1. Tentar Wikipédia
  try {
    const slug = encodeURIComponent(name.replace(/ /g, "_"));

    // NOTA: Se os seus temas forem brasileiros, mude 'en' para 'pt' na URL abaixo
    const res = await fetch(
      `https://en.wikipedia.org/api/rest_v1/page/summary/${slug}`,
    );

    if (res.ok) {
      const data = await res.json();
      if (data.thumbnail?.source) {
        return data.thumbnail.source;
      }
      log.debug(`Thumbnail não encontrada para ${name}, usando fallback.`);
    }
  } catch (error) {
    log.debug(`Erro ao buscar Wikipédia para ${name}:`, error);
  }

  // 2. Retorna o ícone/placeholder de "No Image"
  return NO_IMAGE_PLACEHOLDER(name);
}
