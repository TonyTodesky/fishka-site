export type NavItem = { href: string; label: string };

export const primaryNav: NavItem[] = [
  { href: "/about", label: "О проекте" },
  { href: "/news", label: "Новости" },
  { href: "/archive/theory", label: "Теория" },
  { href: "/archive/history", label: "История" },
  { href: "/archive/games", label: "Игротека" },
  { href: "/archive/people", label: "Люди" },
  { href: "/contacts", label: "Контакты" },
];

export const secondaryNav: NavItem[] = [
  { href: "/membership", label: "Членство" },
  { href: "/archive/puzzles", label: "Головоломки" },
  { href: "/archive/applied", label: "Прикладное" },
  { href: "/archive/reviews", label: "Рецензии" },
  { href: "/archive/journal", label: "Журнал" },
  { href: "/archive/other", label: "Другое" },
  { href: "/map", label: "Карта сайта" },
  { href: "/en", label: "English" },
];

export const goals = [
  "Свободная зона общения для исследователей знаковых игр.",
  "Информационная поддержка членов Ассоциации Фишка.Ру.",
  "Научные методы в истории, педагогике и теории игрового мышления.",
  "Популяризация культурного интеллектуального досуга.",
  "Связи с издателями, школами, музеями и культурными институциями.",
  "Основания Общей теории игр — игроники.",
  "Престиж профессии игротехника.",
];

export const members = {
  full: [
    { name: "Гинзбург Т.И.", city: "СПб", role: "Игротехник «Школы Игратехников», организатор МузеУма" },
    { name: "Гурин Ю.В.", city: "СПб", role: "Обучающие и развивающие игры", slug: "personalii/gurin/13" },
    { name: "Кислюк Л.У.", city: "Москва", role: "Восточные шахматы: сёги, сянци", slug: "personalii/kisluk/14" },
    { name: "Михайлёв А.", city: "СПб", role: "Музей настольных игр, Питерлэнд" },
    { name: "Новиков В.И.", city: "Москва", role: "Маджонг, зам. руководителя АФР, администратор сайта", slug: "personalii/novikov/27" },
    { name: "Прелуцкий И.П.", city: "СПб", role: "Головоломки" },
    { name: "Трубицын В.А.", city: "СПб", role: "Теоретик и изобретатель, модератор сайта", slug: "personalii/trubicin/valeriytrubicin" },
    { name: "Широков Г.А.", city: "СПб", role: "Патриарх «Школы Игратехников»" },
    { name: "Нестеров В.Г.", city: "СПб", role: "Переводчик и исследователь го и сянци", slug: "personalii/nesterov/Nesterov" },
  ],
  names: [
    "Авербах Ю.Л. — гроссмейстер, историк шахмат",
    "Асташкин В.А. — основатель го-движения в СССР",
    "Боровиков А.Г. — столбовые шашки",
    "Голосуев В.М. — гроссмейстер, историк шашек",
    "Линдер И.М. — историк шахмат",
    "Нилов Г.И. — исследователь го",
    "Нудельман Д.М. — библиограф шашек",
    "Филатов Ю.П. — игротехник и изобретатель",
    "Юдасин Л.Г. — гроссмейстер, исследователь шахмат",
  ],
};

export const featuredGames = [
  { title: "Гексофен", slug: "igroteka/geksofen/35", image: "http://www.fishka.spb.ru/articles/igroteka/geksofen/35.files/image007.gif" },
  { title: "Дипломат", slug: "igroteka/diplomat/36", image: "http://www.fishka.spb.ru/articles/igroteka/diplomat/36.files/image002.gif" },
  { title: "Синхрогекс", slug: "igroteka/sinhrogex/sinhrogex", image: "http://www.fishka.spb.ru/articles/igroteka/sinhrogex/sinhrogex.jpg" },
  { title: "Суго", slug: "igroteka/sugo/sugo", image: "http://www.fishka.spb.ru/articles/igroteka/sugo/sugo.jpg" },
  { title: "Хэй-го", slug: "igroteka/heygo/312", image: "http://www.fishka.spb.ru/articles/igroteka/heygo/heygo.jpg" },
  { title: "Невские шашки", slug: "igroteka/nevskie/nevskie", image: "http://www.fishka.spb.ru/articles/igroteka/nevskie/pic7.jpg" },
];

export function articleSlug(href: string): string {
  const path = href.split("/articles/")[1] ?? href.replace(/^\/+/, "");
  return path.replace(/\.(html?|htm)$/i, "").replace(/\/+$/, "");
}

/** Prefix site paths with Astro `base` (e.g. `/new`). */
export function withBase(href = "/"): string {
  const base = (import.meta.env.BASE_URL || "/").replace(/\/$/, "");
  if (/^(https?:|mailto:|tel:)/i.test(href)) return href;
  const path = href.startsWith("/") ? href : `/${href}`;
  if (path === "/") return base || "/";
  return `${base}${path}`;
}

export function rewriteLegacyPaths(html: string): string {
  // Serve article assets from the live original site so /new can ship without
  // re-uploading the 277MB legacy mirror.
  return html.replace(/(src|href)="\/legacy\//gi, `$1="http://www.fishka.spb.ru/`);
}
